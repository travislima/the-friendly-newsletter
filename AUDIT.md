# The Friendly — Full Project Audit

**Date:** 3 July 2026 · **Scope:** all 15 issues, landing page, welcome email, thank-you page, privacy page, WhatsApp/Slack versions, publishing setup.

This audit covers code quality, email-client compatibility, security/privacy, design, tone of voice, and marketing/growth. Per the editorial policy of this repo, **past issues are treated as a documented archive** — every fix below is framed as a forward change (template, site pages, process), not a rewrite of history. The only exceptions called out are things that are *actively broken for readers today* on the live website.

---

## Executive summary

**The verdict: this is a genuinely well-built operation for a solo newsletter.** The email template is professional-grade hybrid HTML (MSO ghost tables, gradient fallbacks, proper preheaders, text-only for deliverability), the voice is the strongest asset in the project, and the multi-channel repurposing (email → WhatsApp → Slack) is smart distribution most operators never do.

The three biggest problems, in order:

1. **The growth loop is broken.** Every issue says "Forward it to a friend" — but there is no "Was this forwarded to you? Subscribe here" link anywhere in any issue, no view-in-browser link, and the WhatsApp version (the most forwardable artifact you produce) contains zero links back to thefriendly.co.za. You're asking for forwards and catching none of the people who receive them.
2. **The welcome email is a second-class citizen.** It has none of the Outlook defenses the main template has (no ghost table → renders full-width broken in Outlook desktop; both gradients invisible), no preheader, an unclosed `<p>` tag, and it hard-codes "Read Issue #015" which goes stale every week.
3. **Every issue is a hand-edited fork of the previous file.** ~80% of each event card is repeated boilerplate; inline styles are >50% of every file by bytes. This is the root cause of nearly every defect found (stale comments, drifted colors, dead CSS, section-order flips). A canonical `template.html` + per-issue content would collapse each issue from ~35KB of hand-maintained HTML to ~3KB of actual content.

Nothing found rises to a genuine security vulnerability — it's a static site with no backend, no secrets in the repo, and all links are https. The security section below is hygiene and privacy-policy accuracy, not fire.

---

## 1. What's working well (keep all of this)

- **Voice.** Warm, local, funny without trying too hard, and measurably improving. The issue-010 pivot (Editor's Pick + bespoke CTAs + honest opinions like "we went a few weeks back and loved it") turned the product from "event listing with a smile" into "a mate who curates." The unsubscribe copy — "Not your vibe? No hard feelings." — is best-in-class.
- **Email craft.** `role="presentation"` on every table, correct MSO ghost-table wrapper, gradient stripes with solid-color Outlook fallbacks, zwnj-padded preheaders unique to every issue, `{$unsubscribe}` never missing, zero images (fast + deliverability-friendly), correct hybrid fluid/fixed width handling.
- **Structure.** Editor's Pick → day-labelled What's On → Also Happening → Worth Checking Out → outro is scannable and disciplined: every event carries time · venue · price.
- **The "vibe" line.** "6km along the coast. Easy pace. Shoes optional." This one-line format is the soul of the product.
- **PE vs Gqeberha handling** is a coherent editorial policy, not drift: "PE" for the affectionate register, "Gqeberha, South Africa" in the formal footer, official names as organisers style them. Correct call.
- **Failure handling on-brand:** "Blame the whales." / "See you next Thursday. For real this time."
- **Charity/community events consistently featured** — brand equity money can't buy in a city this size.
- **Landing page fundamentals:** "One email. Every Thursday. Everything worth doing in Port Elizabeth this weekend." is a complete value prop in ten words; "no politics, no crime, no doom" is the sharpest differentiator on the page; SEO/OG/schema markup is unusually thorough.

---

## 2. Broken today on the live site (fix first)

| # | Issue | Where |
|---|-------|-------|
| B1 | **Thank-you page "Read the latest issue" links `/issue-006.html`** — nine issues stale. Point it (and the welcome email's button) at an evergreen URL — see the `/latest` recommendation in §7. | `thank-you/index.html:231` |
| B2 | **`{$unsubscribe}` published literally on every archived issue page** — the footer "Unsubscribe here" link 404s on the web (`/%7B$unsubscribe%7D`). Correct tag for MailerLite sends; broken on GitHub Pages. Needs a publish step that swaps the footer for the web copy (§7). | all 15 `issue-*.html` |
| B3 | **`favicon.ico` and `apple-touch-icon.png` are referenced by every page but don't exist in the repo** → 404s, no home-screen icon on iOS. | `index.html:31,33` etc. |
| B4 | **Homepage archive date for #002 is wrong**: says "20 Mar" (a Friday); the issue itself says Thursday 19 March, which is correct. | `index.html:393` |
| B5 | **Hotlinked third-party image in issue-003** (Utrecht photo from a Belgian travel blog's WordPress) — copyright exposure + will silently break on the archive if they enable hotlink protection. The one place a fix to an archived issue is justified: self-host the image or remove it. | `issue-003.html:98` |
| B6 | **Privacy policy says "We don't use cookies, analytics, or any tracking scripts on thefriendly.co.za"** — but the homepage loads MailerLite Universal JS, a third-party script that can set cookies. Soften the wording ("no analytics or ad tracking; our signup form is powered by MailerLite, which may set a functional cookie") to keep the policy accurate. | `privacy/index.html:192` vs `index.html:413-420` |

Historical note (archive, no action needed unless you care): issues 001 and 003 are headed "Thursday 13 March" / "Thursday 27 March" — both dates were Fridays in 2026.

---

## 3. Email-client compatibility

### High severity

- **welcome-email.html has no Outlook support at all.** No MSO ghost table and only `max-width: 520px` (Outlook ignores max-width → renders full viewport width); both linear-gradients (top bar, card divider) have no MSO fallback → invisible in Outlook desktop; missing `xmlns:v/o`, `OfficeDocumentSettings`, and `mso-table-lspace/rspace` resets. The main newsletter template does all of this correctly — copy its patterns over. Also: no preheader (the highest-open-rate email you send previews as "THE FRIENDLY. Welcome to the crew ●…"), missing `x-apple-disable-message-reformatting` / `format-detection` metas, and an **unclosed `<p>` at line 59** (a table opens inside an open paragraph — stricter parsers reflow unpredictably).
- **Dark mode.** `color-scheme: light only` is respected by Apple Mail/iOS — but **Gmail apps and Outlook ignore it** and apply their own inversion. At risk: the cream `#FFFBF0` body, the `#1a1a1a` footer and day-label chips (classic Gmail dark-on-dark bug), and every low-alpha `rgba()` text color (header "THE", issue date, footer text), which can land near the background and disappear after inversion math. Minimum viable defense in the template:
  1. Replace low-alpha rgba text with solid hex equivalents (e.g. `rgba(26,26,26,0.3)` on cream ≈ `#CFCBC1`; `rgba(255,251,240,0.5)` on `#1a1a1a` ≈ `#8D8B84`).
  2. Add a `@media (prefers-color-scheme: dark)` block plus `[data-ogsc]`/`[data-ogsb]` duplicates re-asserting footer/chip/button colors.
  3. Pin the footer background with the `background-image: linear-gradient(#1a1a1a,#1a1a1a)` trick for Gmail.

### Medium severity

- **CTA buttons aren't bulletproof for Outlook.** Padding lives on the `<a>` (`display:inline-block; padding: 6px 12px`); Outlook's Word engine ignores anchor padding, so buttons collapse to tight text on a color chip. Fix: move padding to the `<td>` (keep `display:inline-block` on the `<a>` for everyone else); optionally `mso-padding-alt`.
- **Spacer/divider rows** (`height: 3px` tds) can render ~15px+ tall in Outlook. Add `mso-line-height-rule: exactly` with matching `font-size`/`line-height` values.
- **Logo dot** (`border-radius:50%` inline-block span with `position:relative`) degrades to an orange smear in Outlook. Serve Outlook a styled period via `[if mso]` and wrap the CSS dot in `[if !mso]` — the welcome email's literal orange "." is actually the more robust technique.
- **Web fonts:** `@import` is the *right* choice here (a `<link>` to a font stylesheet is a known trigger for Outlook's "everything becomes Times New Roman" bug; Gmail strips both and your fallbacks — Arial Black / system sans / Georgia — are well chosen). One belt-and-braces improvement: wrap the `@import` in its own `<!--[if !mso]><!--><style>…</style><!--<![endif]-->` block so Outlook can never see it.

### Low severity

- **Gmail 102KB clipping: currently safe.** Largest issue ever is 48KB; MailerLite's tracking rewrites add ~3–6KB. Treat ~85KB raw as your ceiling and check `wc -c` if you ever double the event count — clipping hides the footer *and your unsubscribe link*, which is a deliverability risk.
- Newer emoji (e.g. 🥾 U+1F97E) show as ☐ on older Windows/Android. Cosmetic.
- Confirm MailerLite's auto-generated **plain-text alternative** is enabled and readable — the emoji-bullet layout produces noisy text, and a clean text part helps spam scoring on a link-dense email.
- Verify MailerLite appends a **physical/postal address** in the footer (CAN-SPAM/POPIA-adjacent hygiene and a spam-filter heuristic).
- Verify **domain authentication** (SPF/DKIM/DMARC for thefriendly.co.za) is set up in MailerLite — can't be checked from the repo; it's the single biggest deliverability lever if not already done.

---

## 4. Code quality & template consistency

**Verified clean:** tag balance across all 15 issues (zero unclosed/mismatched tags — the only defect is in welcome-email.html), all MSO conditional pairs correctly matched, no `href="#"`, no placeholders, no http:// links, titles all match filenames.

**Findings (all fixed by moving to one canonical template, §7):**

- **Boilerplate cost:** inline `style=""` attributes are 51–54% of every file by bytes; the 85-byte Outfit font stack repeats 38–85× per file; ~80% of every event card is repeated chrome around ~350 bytes of actual content.
- **Drift:** Editor's Pick label suffix varies randomly (`★ Editor's Pick · Friday` / no suffix / `· Saturday`); the "Worth Checking Out" section has had three different renderings; featured-card colors fork between `#777`/`#444` and `#888888`/`#444444`; section order flipped in 012; "Save the Date" was demoted from card to rows in 010 but its CSS still ships in every file since.
- **Dead CSS:** `.save-date-card` (unused since 010), `.mobile-padding-event` (byte-identical duplicate of `.mobile-padding`), orphan `food-card` classes in 002–007.
- **Copy-paste artifacts:** issue-014's Editor's Pick comment still says "Winter Solstice Polar Plunge" but contains Little Gravity Kids Park (`issue-014.html:98`); issue-003's intro claims "It's a long weekend" for a weekend with no SA public holiday (content drafted for the following week).

---

## 5. Accessibility

- **Good:** `lang="en"`, `role="presentation"` everywhere, meaningful alt on the one image, properly hidden preheaders. Consider `lang="en-ZA"`.
- **Contrast failures at body size on cream `#FFFBF0`** (template-forward fixes; WCAG AA needs 4.5:1):
  - Event "vibe" line `#FF6B35` @13px italic — **2.7:1**. This is every event description. Darkening to ~`#D14E1A` keeps the brand orange feel and roughly doubles contrast.
  - Event meta `#888888` @13px — 3.4:1 → use `#6B6B6B`.
  - WhatsApp intro line `#999999` — 2.8:1.
  - Orange CTA buttons: `#FFFBF0` on `#FF6B35` — 2.7:1 (the dark buttons are fine).
  - Issue date line `rgba(26,26,26,0.35)` — 2.2:1.
- **No heading structure:** section titles ("This Weekend", "Also Happening") are styled `<p>`s. Make them `<h2>` with identical inline styles — free screen-reader navigation.
- **Decorative emoji announced by screen readers** ("wine glass", "party popper Friday"). Wrap in `<span aria-hidden="true">`.
- Historical: issues 001–004 had a near-invisible unsubscribe (1.6–2.2:1 at 10px) — fixed from 005 onward. Good instinct; keep the current values.

---

## 6. Copy, tone & marketing

### Tone (working — protect it)
The honest-recommendation register that arrived with issue 010 ("Honest take: we went a few weeks back and loved it… go early — it fills up fast") is the trust engine. Never let it read like ad copy — especially once sponsors arrive.

### Tone (tighten)
- **Retire the "Yes, X" tic** to ~quarterly ("Yes, a hoedown / a church ruin / knitting counts" — 4× in five issues; you already self-corrected after 006).
- **Stop duplicating the preheader in the intro** (002, 005, 006 are near-verbatim). Preheader teases; intro adds a joke, opinion, or context.
- **Vary the preheader tail:** 9 of 15 end "Your PE weekend sorted." — in an inbox list that tail is wasted; your three best preheaders are exactly the ones that broke formula ("PE, you're spoilt." / "School holidays start here.").
- Slang lands best when it's Gqeberha's, not Instagram's: "lekker/bakkie/roosterkoek" > "hold my coffee / glow up / if you know, you know."

### CTA buttons
- Best of the run: "Shh, just show up →". Worst: venue names as labels ("Barn & Barrel →") and bare "Details" in the quick list (a regression to worse-than-001 inside the playful era).
- "Ice one for the road →" is the ceiling of pun-obscurity — at that point clarity loses.
- Rules worth adopting: no label reused within 4 issues ("Bring the camera →" ran three straight weeks); keep a **ticketed-vs-free signal** (the old "Grab tickets" vs "More info" distinction was functional — "Reserve your seat →" preserves it, "Take your seat →" doesn't).
- Phone-number bookings should be tappable `wa.me/27…` (or `tel:`) links — this audience books via WhatsApp.

### Growth mechanics — the ranked gap list
1. **Add "Was this forwarded to you? Subscribe at thefriendly.co.za" to the issue template.** The forward ask exists in every issue; the catch for forwarded readers exists nowhere. Highest-leverage single line in this audit.
2. **Add "View this issue online" (MailerLite `{$url}`) + link the homepage** from the email body. Currently the only site links in an issue are `/privacy`.
3. **Put a subscribe line at the end of the WhatsApp/Slack versions** ("Full version + subscribe: thefriendly.co.za"). The WhatsApp file is your most forwardable artifact and carries zero acquisition surface.
4. **Social proof:** "Join N+ PE locals" on the landing page near the form (and later in the email footer). Zero social proof exists anywhere today.
5. **Make the sponsor pathway visible:** one recurring footer line in issues ("Want your business in front of PE's most plugged-in crowd? Reply to this email.") and a short `/advertise` page. Local business owners already read this — today the only pitch is one clause buried in the landing-page tip section.
6. Instagram is never promoted inside issues (only welcome email + landing page). One occasional plug.
7. Add UTM parameters (`?utm_source=newsletter` etc.) so you can attribute traffic between email/WhatsApp/Slack/Instagram in future analytics.
8. Manual referral milestone ("forward to 3 friends, get a shout-out") fits the brand better than referral software.

### Landing page conversion
- Add "Read last week's issue →" directly under the signup form — the archive is below the fold and framed as an archive, not risk-reduction.
- Cap the past-issues list at the latest 5 + "All issues →" (15 rows of visual noise and growing).
- Split the tip section's two audiences (tipsters vs advertisers) into separate lines.
- Unify meta description ("worth knowing about") with OG description ("worth doing").

### Welcome email content
Founder story, expectation-setting, contacts ask, and reply prompt are all present and good. Add: a preheader, the WhatsApp group invite (peak-enthusiasm moment, yet the group is only promoted in later issues), a forward ask, and an evergreen latest-issue link instead of the hardcoded issue-015. The "I" voice (vs the newsletter's "we") is a strength — keep it deliberate.

### Cadence
The archive shows the wobble (#013 → #014 skipped a week and shipped on a Friday) against an "Every Thursday at 8am" promise made in three places. The apologies were charming, but build one **evergreen backup issue** ("Best of PE this winter") so the streak survives a bad week.

---

## 7. The structural recommendation: one template, thin issues

Root cause of nearly everything in §4: each issue is a hand-edited fork of the previous file. Recommended forward workflow (no change to the archive):

1. **`template.html`** — one canonical file carrying all fixes from §3/§5 (dark-mode defense, bulletproof buttons, h2 headings, contrast-safe colors, forwarded-subscriber line, view-in-browser). Clearly marked slots: preheader, issue number/date, intro, editor's pick, repeating day-label + event-card blocks, also-happening rows, worth-checking-out, outro line, footer.
2. **`CLAUDE.md`** — the build playbook, so every future Claude session produces identical output: the slot list, editorial rules (CTA rules from §6, preheader rules, PE/Gqeberha policy, "Yes, X" quota), the pre-send checklist (weekday matches date, `wc -c` under 85KB, all links https, comment headers match content), and the publish steps below.
3. **A tiny publish step** for the web archive: when committing `issue-NNN.html`, replace the `{$unsubscribe}` footer with web-appropriate copy, add per-issue `<title>`/meta description/OG tags (the archive pages could rank for "things to do in Port Elizabeth this weekend" — right now they have zero SEO metadata), and update the homepage list. This can be a 30-line script or simply part of the documented Claude workflow.
4. **An evergreen `/latest` redirect** (e.g. a tiny `latest/index.html` with a meta-refresh, updated each week by the same publish step) so the welcome email and thank-you page never go stale again.
5. Add the missing site files: `favicon.ico`, `apple-touch-icon.png`, `404.html`, `robots.txt` + `sitemap.xml`.

---

## 8. Phase 2: automating Facebook event collection

Honest assessment of the options, because this is the tedious part of your week:

- **What doesn't work:** Facebook's Graph API events endpoints have been locked down since 2018 — you can only read events for Pages you admin, after app review. Scraping Facebook (headless browser against facebook.com) violates their ToS, is brittle behind login walls, and risks the personal account you use for the newsletter. Not recommended.
- **What actually works — shrink the manual step instead of eliminating it:**
  1. **A capture inbox.** An iOS/Android "share to" shortcut (or just WhatsApp-message-yourself) that appends every event link you encounter during the week to one running list — a GitHub issue, a `next-issue.md` file, or a note. The tedium isn't finding events (you see them while scrolling anyway); it's collecting and transcribing. This kills the collecting half for near-zero effort.
  2. **Claude does the transcribing.** Your existing workflow — "feed it a link and Claude builds the newsletter" — already covers the second half. With `CLAUDE.md` + `template.html` from §7, "build issue 016 from next-issue.md" becomes a one-line prompt with consistent output.
  3. **Add structured sources for the ticketed layer:** Quicket (big in SA, has a public API), Webtickets, Computicket, plus venue Google Calendars / ICS feeds where they exist. These can be genuinely automated (a weekly script that drafts the "candidates list" for you) and would surface events you *don't* see on Facebook. Facebook stays what it's best at: the community/market/free events you curate by eye.
- **Net:** aim for "10 minutes of forwarding links to yourself during the week + one build prompt on Wednesday," not "zero-touch scraping."

---

## 9. Priority roadmap

**P1 — this week (broken things + the growth loop)**
1. Fix thank-you page stale link; create `/latest` and point welcome email + thank-you at it (B1).
2. Add to the issue template: forwarded-subscriber line, view-in-browser link, sponsor footer line.
3. Add subscribe footer to WhatsApp/Slack versions.
4. Fix welcome email: MSO ghost table + gradient fallbacks, preheader, close the `<p>`, missing metas, WhatsApp invite, evergreen link.
5. Add `favicon.ico` / `apple-touch-icon.png`; fix homepage #002 date; adjust privacy-policy tracking sentence (B3, B4, B6).

**P2 — this month (template + conversion)**
6. Build canonical `template.html` with dark-mode defense, bulletproof buttons, contrast fixes, `<h2>` headings, aria-hidden emoji.
7. Write `CLAUDE.md` build playbook + publish step (web-safe unsubscribe swap, per-issue OG/meta tags, homepage list update).
8. Landing page: subscriber count near the form, sample-issue link under the form, cap archive list at 5.
9. Self-host or remove the issue-003 hotlinked image (B5).
10. Verify in MailerLite: SPF/DKIM/DMARC, plain-text part, postal address in footer.

**P3 — nice to have**
11. `/advertise` page + rate card; UTMs on all links; wa.me phone links; manual referral milestones; evergreen backup issue; `404.html`/`robots.txt`/`sitemap.xml`; Quicket/venue-calendar candidate script (phase 2, §8).
