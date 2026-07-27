# The Friendly — build notes for Claude

The Friendly is a free weekly email newsletter about events, food, and things to do in
Port Elizabeth (Gqeberha), South Africa. Sent Thursdays 8am via MailerLite (HTML is
pasted in manually). This repo is also the public website (GitHub Pages,
thefriendly.co.za) — the issue HTML files double as the web archive.

**Past issues are a documented archive. Never edit a published `issue-NNN.html`.**
All improvements go into `template.html`, which every new issue starts from.

## Building a new issue

> ⛔ **NEVER clone the previous issue** (`cp issue-0NN.html issue-0NN+1.html`).
> **ALWAYS start from `template.html`.** Cloning issue-to-issue silently
> propagates styling drift (wrong text colors, `<p>` headings, unwrapped emoji)
> from whatever crept into an earlier issue. `template.html` is the one
> known-compliant source. Step 1 is not optional.

1. `cp template.html issue-NNN.html`
2. Fill every `[BRACKETED]` slot. Repeatable blocks (day label, event card,
   quick-list row) are marked `BEGIN REPEATABLE` / `END REPEATABLE` — duplicate them
   as needed, keeping the markup byte-identical apart from content.
3. The last event card under each day label drops its
   `border-bottom: 1px dashed #e5e5e0`.
4. Delete the instruction banner comment at the top of the file, and update the
   `<!-- Subject: ... -->` comment with the real subject line.
5. Sections with no content this week (e.g. Worth Checking Out) can be removed
   whole — from their section-divider row through their last card.
6. Do NOT touch the `EMAIL-ONLY` / `WEB-ONLY` / `WEB-META` markers — the publish
   script depends on them.

`{$url}` (view in browser) and `{$unsubscribe}` are MailerLite merge tags — keep them
verbatim in the sent HTML. MailerLite converts them at send time.

### Template rules that are easy to break — don't

- **Orange CTA buttons use dark text** (`#1a1a1a` on `#FF6B35`) — accessibility.
  The Editor's Pick button is dark with cream text.
- Vibe lines, eyebrows, and inline links on cream use `#C24A20` (accessible
  orange), never `#FF6B35` for text.
- Meta text is `#6B6B6B`. No rgba() text colors anywhere — dark-mode clients
  invert alpha colors into invisibility.
- Emoji are wrapped in `<span aria-hidden="true">` — keep that on new emoji.
- Section titles are `<h2>`, event names `<h3>` — don't demote them to `<p>`.

## Sending + publishing workflow

1. Build `issue-NNN.html` (above). Run the pre-send checklist (below).
2. **Paste the HTML into MailerLite and send/schedule.** Record the subject line
   in the `<!-- Subject: ... -->` comment.
3. **Then** run `python3 scripts/publish.py issue-NNN.html`. This converts the
   file to the web version in place (strips MailerLite merge-tag links, adds a
   subscribe line, injects OG/meta tags), points `latest/` at it, rotates the
   Recent Issues teasers on `index.html` (newest 3), and prepends the issue to
   `archive/index.html`. The teaser shown on both pages is the preheader — one
   more reason to write it well. Order matters: publish AFTER pasting, because
   the web version no longer contains `{$unsubscribe}`.
4. Review `git diff`, commit, push.

## WhatsApp and Slack versions

Written to `whatsapp/issue-NNN.md` and `slack/issue-NNN.md`. **Every version ends
with this footer** (the WhatsApp version is the most-forwarded artifact we produce —
it must carry a subscribe path):

```
—
Get this every Thursday by email: thefriendly.co.za
```

## Editorial rules (short version)

- Voice: warm, local, first-person-plural. Opens "Hey PE 👋", pivots "Let's get into
  it.", closes "That's your weekend sorted. 🧡 … See you next Thursday."
- "PE" in the friendly register; "Gqeberha, South Africa" in the formal footer;
  official event names exactly as organisers style them.
- Every event: emoji · name · time · venue · price ("R250pp"), then one "vibe" line.
- CTA buttons: playful but clear. Never reuse a label within 4 issues. Never bare
  "Details". Keep a ticketed signal for paid events ("Grab tickets →",
  "Reserve your seat →"). If the pun needs a re-read, it's too clever.
- Preheader: concrete items, lead with the weirdest one. Don't reuse the intro
  sentence, and vary the closing tail (not "Your PE weekend sorted." every week).
- Phone bookings: link as `https://wa.me/27XXXXXXXXX` (drop the leading 0) when the
  organiser uses WhatsApp, else `tel:`.

## Event selection — what actually gets clicked (data-backed)

Analysis of click data across issues #013–#018 (MailerLite link activity). The
event TYPE drives clicks far more than where it sits in the layout.

**Click ranking by event type (highest → lowest):**
1. **Novel experiences / festivals** — the biggest winners by far. Whale Festival
   (18 clicks), SAAF Museum after-hours (15), Winter Solstice Polar Plunge (7),
   Mardi Gras (7). "Only-in-PE", experiential, broadly appealing.
2. **Markets** — the reliable workhorse. Pull 3–8 clicks *every* issue, even when
   buried in the "Also Happening" quick-list (Collective Market 8, 67 Blankets 7
   *from the tail*). Always include 2–3.
3. **Food / new-restaurant spotlights** — overperform massively. ZZAN (10 clicks,
   2nd in its issue) from "Worth Checking Out". Under-used — feature one most weeks.
4. **Cars / motorsport** — strong. Rally (9, top of its issue), Vespa (3).
5. **Live music / ticketed gigs / tributes** — the WORST category. Near-universally
   0–1 clicks (Spoegwolf 1, Queen 0, Boks & ABBA 0, Music Bingo 0). Exception:
   wine+culture "experiences" (Jazz & Wine 6). Demote gigs to the quick-list.
6. **Kids-specific** — low (2 or fewer). Narrow audience.

**Rules that follow:**
- **Editor's Pick = always the most novel, broadly-appealing EXPERIENCE.** Never a
  ticketed gig, never a permanent venue/kids park. When the Pick was niche it got
  beaten by regular markets (e.g. #016 Grease Party came 5th; #014 Little Gravity
  got 2 and lost to a demoted Polar Plunge at 7).
- The Editor's Pick slot does **not** create clicks — the right event does.
- Don't trim the "Also Happening" tail; markets there still pull well.
- Total clicks track with how many markets + experiences + food + cars an issue
  packs in. That's the lever — not send-time or button count.

## Pre-send checklist

- [ ] No unfilled `[SLOTS]` (`grep -o '\[[A-Z][A-Z ]*\]' issue-NNN.html`).
- [ ] Issue number and date in header, `<title>`, and preheader all match — and the
      date really is a Thursday (`date -d YYYY-MM-DD +%A`).
- [ ] All comment headers match their content (no leftovers from the template or a
      previous issue).
- [ ] All links https; every event card has a working URL.
- [ ] **No styling drift** — all three commands below return nothing:
      `grep -o 'color: #888888' issue-NNN.html` (meta must be `#6B6B6B`),
      `grep -oE 'color: #FF6B35; (font-style|text-decoration|">)' issue-NNN.html`
      (vibe/link/eyebrow text must be `#C24A20`; `#FF6B35` is background-only),
      `grep -o 'font-size: 11px; font-weight: 600; color: #FFFBF0' issue-NNN.html`
      (orange CTA text must be dark `#1a1a1a`). Any hit means the issue drifted
      from `template.html` — see the build-section warning.
- [ ] `{$unsubscribe}` and `{$url}` present.
- [ ] File under 85KB (`wc -c issue-NNN.html`) — Gmail clips at ~102KB after
      MailerLite adds tracking.
- [ ] Subject line recorded in the `<!-- Subject: ... -->` comment.
- [ ] After sending: `python3 scripts/publish.py issue-NNN.html`, then commit.

(The publish script re-checks most of this and refuses to publish a file with
unfilled slots or a missing header date.)
