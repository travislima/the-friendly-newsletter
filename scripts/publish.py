#!/usr/bin/env python3
"""Publish an issue to the web archive.

Usage:  python3 scripts/publish.py issue-NNN.html

Run this AFTER pasting the issue into MailerLite (it converts the file
from the email version to the web version, in place), then commit.

What it does:
  1. Pre-flight checks on the email version (merge tags present, subject
     line recorded, size under the Gmail-clipping budget, date sanity).
  2. Strips EMAIL-ONLY blocks (MailerLite merge-tag links that 404 on
     the web) and activates WEB-ONLY blocks.
  3. Injects meta description, canonical, and Open Graph tags into the
     issue page (replacing the WEB-META marker).
  4. Points latest/index.html at the new issue.
  5. Adds the issue to the top of the Past Issues list in index.html.
"""

import datetime
import html as htmllib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://thefriendly.co.za"
SIZE_BUDGET = 85 * 1024  # Gmail clips at ~102KB after MailerLite adds tracking

MONTHS = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June",
     "July", "August", "September", "October", "November", "December"])}


def fail(msg):
    print(f"ERROR: {msg}")
    sys.exit(1)


def warn(msg):
    print(f"WARNING: {msg}")


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"issue-\d{3}\.html", Path(sys.argv[1]).name):
        fail("usage: python3 scripts/publish.py issue-NNN.html")

    issue_path = ROOT / Path(sys.argv[1]).name
    if not issue_path.exists():
        fail(f"{issue_path} not found")
    src = issue_path.read_text(encoding="utf-8")
    issue_no = issue_path.stem.split("-")[1]

    # ---- 1. Pre-flight checks (on the email version) --------------------
    if "{$unsubscribe}" not in src:
        if "<!-- EMAIL-ONLY-START -->" not in src:
            fail("no {$unsubscribe} and no EMAIL-ONLY markers — is this already published?")
        warn("{$unsubscribe} missing from the email version")
    if "{$url}" not in src:
        warn("{$url} (view in browser) missing")
    if not re.search(r"<!--\s*Subject:", src):
        warn("no `<!-- Subject: ... -->` comment at the top — record it for open-rate tracking")
    if re.search(r"\[[A-Z][A-Z /'’.\-]{2,}\]", src):
        fail("unfilled [PLACEHOLDER] slots remain in the file")
    if len(src.encode()) > SIZE_BUDGET:
        warn(f"file is {len(src.encode())//1024}KB — over the {SIZE_BUDGET//1024}KB budget, Gmail may clip")

    # Downstream files must be ready BEFORE we write anything. Steps 3-4 modify
    # files on disk, so a failure discovered at step 5 leaves the issue converted
    # and latest/ moved but the homepage and archive untouched — a half-publish
    # that can only be undone with `git checkout`. Check the contracts up front.
    index_path = ROOT / "index.html"
    archive_path = ROOT / "archive" / "index.html"
    latest_path = ROOT / "latest" / "index.html"
    for p in (index_path, archive_path, latest_path):
        if not p.exists():
            fail(f"{p.relative_to(ROOT)} not found")
    if not re.search(r"<!-- RECENT-ISSUES -->\n(.*?)<!-- /RECENT-ISSUES -->",
                     index_path.read_text(encoding="utf-8"), re.DOTALL):
        fail("index.html is missing the <!-- RECENT-ISSUES --> / <!-- /RECENT-ISSUES --> "
             "markers — publish.py needs them to rotate the homepage teasers")
    if "<!-- ARCHIVE-LIST -->" not in archive_path.read_text(encoding="utf-8"):
        fail("archive/index.html is missing the <!-- ARCHIVE-LIST --> marker")
    if not re.search(r"issue-\d{3}\.html", latest_path.read_text(encoding="utf-8")):
        fail("latest/index.html has no issue-NNN.html link to point at the new issue")

    m = re.search(r"Issue #(\d+)\s*&middot;\s*(\w+)\s+(\d+)\s+(\w+)\s+(\d{4})", src)
    if not m:
        fail("couldn't find the 'Issue #NNN · Weekday D Month YYYY' header line")
    if int(m.group(1)) != int(issue_no):
        fail(f"header says issue #{m.group(1)} but the file is issue-{issue_no}.html")
    claimed_day, day, month, year = m.group(2), int(m.group(3)), m.group(4), int(m.group(5))
    if month not in MONTHS:
        fail(f"unrecognised month {month!r} in header date")
    date = datetime.date(year, MONTHS[month], day)
    if date.strftime("%A") != claimed_day:
        warn(f"header claims {claimed_day} but {date} is a {date.strftime('%A')}")

    # ---- 2. EMAIL-ONLY / WEB-ONLY swap ----------------------------------
    out, n_stripped = re.subn(
        r"[ \t]*<!-- EMAIL-ONLY-START -->.*?<!-- EMAIL-ONLY-END -->\n?",
        "", src, flags=re.DOTALL)
    if n_stripped == 0:
        warn("no EMAIL-ONLY blocks found (template.html has two: view-in-browser + unsubscribe)")
    out = re.sub(r"<!-- WEB-ONLY\n(.*?)\n[ \t]*-->", r"\1", out, flags=re.DOTALL)

    # ---- 3. Web meta tags -----------------------------------------------
    pre = re.search(
        r'aria-hidden="true">\s*(.*?)&nbsp;&zwnj;', out, flags=re.DOTALL)
    if pre:
        teaser = htmllib.unescape(re.sub(r"\s+", " ", pre.group(1)).strip())
    else:
        # Silent fallback here is how #016-#018 shipped generic teasers: issues
        # cloned from a previous issue lost aria-hidden="true" on the preheader.
        warn("couldn't read the preheader — is aria-hidden=\"true\" missing from it? "
             "Falling back to a generic teaser on the homepage and archive")
        teaser = "Events, food, and things to do in Port Elizabeth this weekend."
    description = htmllib.escape(teaser, quote=True)
    url = f"{SITE}/issue-{issue_no}.html"
    title = f"The Friendly · Issue #{issue_no} · {day} {month} {year}"
    meta = f"""<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="The Friendly">
<meta property="og:locale" content="en_ZA">
<meta property="og:image" content="{SITE}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">"""
    if "<!-- WEB-META -->" in out:
        out = out.replace("<!-- WEB-META -->", meta, 1)
    else:
        warn("no WEB-META marker — skipping meta-tag injection")

    issue_path.write_text(out, encoding="utf-8")
    print(f"issue-{issue_no}.html converted to web version")

    # ---- 4. latest/ redirect --------------------------------------------
    txt, n = re.subn(r"issue-\d{3}\.html", f"issue-{issue_no}.html", latest_path.read_text(encoding="utf-8"))
    latest_path.write_text(txt, encoding="utf-8")
    print(f"latest/index.html now points at issue-{issue_no}.html ({n} URLs)")

    # ---- 5. Homepage recent list + archive page --------------------------
    short_date = f"{day} {month[:3]}"
    teaser_html = htmllib.escape(teaser, quote=False)

    def issue_li(kind):
        return (f'        <li class="{kind}-issue"><a href="/issue-{issue_no}.html" '
                f'class="{kind}-issue-link"><span class="{kind}-issue-num">#{issue_no} '
                f'&middot; {short_date}</span><span class="{kind}-issue-teaser">'
                f'{teaser_html}</span></a></li>')

    idx = index_path.read_text(encoding="utf-8")
    block = re.search(r"<!-- RECENT-ISSUES -->\n(.*?)<!-- /RECENT-ISSUES -->", idx, re.DOTALL)
    if not block:
        fail("couldn't find the RECENT-ISSUES markers in index.html")
    items = [l for l in block.group(1).splitlines() if '<li class="recent-issue">' in l]
    if f"/issue-{issue_no}.html" in block.group(1):
        print("index.html already lists this issue — skipping")
    else:
        items = ([issue_li("recent")] + items)[:3]  # newest first, keep 3
        idx = idx.replace(block.group(0),
                          "<!-- RECENT-ISSUES -->\n" + "\n".join(items)
                          + "\n<!-- /RECENT-ISSUES -->")
        index_path.write_text(idx, encoding="utf-8")
        print(f"index.html: #{issue_no} added to Recent Issues (keeping {len(items)})")

    arc = archive_path.read_text(encoding="utf-8")
    if f"/issue-{issue_no}.html" in arc:
        print("archive/index.html already lists this issue — skipping")
    else:
        marker = "<!-- ARCHIVE-LIST -->"
        if marker not in arc:
            fail("couldn't find the ARCHIVE-LIST marker in archive/index.html")
        arc = arc.replace(marker, marker + "\n" + issue_li("archive"), 1)
        archive_path.write_text(arc, encoding="utf-8")
        print(f"archive/index.html: #{issue_no} added to All Issues")

    print("\nDone. Review with `git diff`, then commit and push.")


if __name__ == "__main__":
    main()
