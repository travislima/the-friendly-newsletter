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

## Social cards (WhatsApp gallery + Instagram carousel)

Every issue also ships a set of image cards — WhatsApp is our biggest
forwarding/growth channel and pasted markdown reads badly there, so the cards
carry the issue as a swipeable gallery. Source of truth is
`whatsapp-cards/issue-NNN-cards.html` (one template) rendered by
`whatsapp-cards/shoot.mjs`.

**Build steps (after the issue is finalised):**
1. `cp whatsapp-cards/issue-PREV-cards.html whatsapp-cards/issue-NNN-cards.html`
   and swap in this week's content. The card set is: **1** cover · **2**
   Editor's Pick · **3** a Friendly Highlight / second feature · **4** the
   weekend line-up (What's On) · **5** Where to Eat · **6** follow closer.
   Pull card copy straight from the finished `issue-NNN.html` so wording matches.
2. Point `shoot.mjs` at the new file (the `file`/`out` issue number) and run
   `node whatsapp-cards/shoot.mjs`. It writes both formats:
   `issue-NNN-wa-N.png` (1080×1080, WhatsApp) and `issue-NNN-ig-N.png`
   (1080×1350, Instagram 4:5). One HTML renders both via a `fmt-square` /
   `fmt-portrait` body class — don't fork the template per size.
3. Eyeball each PNG (fonts loaded, no clipped text) before sending.

**Card design rules (same guardrails as the email):**
- Cream `#FFFBF0` bg, four-colour gradient stripe on top, Archivo Black logo
  with the orange dot, `#C24A20` for orange text, `#1a1a1a` dark footer.
- **No link is tappable on an image.** Cards print `thefriendly.co.za` as a
  visual CTA only; the real link goes in the WhatsApp caption / Instagram
  link-in-bio. Card footers say where to tap ("Full details + links",
  "Book via the link").
- Note on Node: Playwright lives at `/opt/node22/lib/node_modules` — `shoot.mjs`
  imports it by absolute path (ESM ignores `NODE_PATH`), and Chromium is at
  `/opt/pw-browsers/chromium`.

**Captions to ship with them:**
- *WhatsApp* (paste with the album — the domain auto-links): lead line, 3–5
  emoji event bullets weirdest-first, then `Full issue + links → thefriendly.co.za`.
- *Instagram* (link isn't tappable — set link-in-bio to `thefriendly.co.za`):
  same bullets + a hashtag block (`#GqeberhaEvents #PortElizabeth #ThingsToDoPE`
  …). End on the free-every-Thursday line.

Rendered PNGs are disposable (regenerate any time); commit the `-cards.html`
template + `shoot.mjs` so next week starts from the last known-good source.

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
- **No em dashes.** Not in the newsletter, not on the site, not in captions or
  card copy. Use a colon for a reveal, a comma for an aside, a full stop to
  split the sentence, and `&middot;` as a separator in titles and meta lines.
  En dashes stay for ranges (`9AM&ndash;12PM`, `2&ndash;4 sentences`).
  Published `issue-NNN.html` files are an archive and keep whatever they shipped
  with, so the archive teasers quoting them may still contain em dashes.

## The welcome email

`welcome-email.html` is a MailerLite automation, not something `publish.py`
touches. Editing the file changes nothing until it is pasted into MailerLite.

It has **exactly one ask: reply with a favourite place to eat in PE.** Do not add
a second competing call to action; a single CTA is worth several times the clicks
of a page full of them. The reasoning is specific to this list:

- A reply is the strongest signal Gmail accepts that a sender is wanted, and
  ~71% of readers are on Gmail. It lifts inbox placement for *every* later issue,
  which nothing else in the email does.
- The answers feed the weekly Where to Eat slot, the highest repeat-click
  category we run.

Everything else is deliberately quiet: the latest-issue link and the WhatsApp
group sit below a divider in small grey text. WhatsApp is covered properly on the
thank-you page instead, and the evidence for demoting it here is #019, where the
group link took 1 click from 189 opens. "Add us to your contacts" and "forward to
a friend" were cut: near-zero compliance, and nobody forwards a newsletter they
have not read yet.

> **Growth, pricing and sponsorship live in `STRATEGY.md`.** This file is how to
> build and ship an issue. That one is whether the business is working.

## Event selection — what actually gets clicked (data-backed)

Analysis of click data across issues #013–#019 (MailerLite link activity). The
event TYPE drives clicks far more than where it sits in the layout.

**Click ranking by event type (highest → lowest):**
1. **Novel experiences / festivals** — the biggest winners by far. Whale Festival
   (18 clicks), SAAF Museum after-hours (15), Winter Solstice Polar Plunge (7),
   Mardi Gras (7). "Only-in-PE", experiential, broadly appealing.
2. **Markets** — the reliable workhorse. Pull 3–8 clicks *every* issue, even when
   buried in the "Also Happening" quick-list (Collective Market 8, 67 Blankets 7
   *from the tail*). Always include 2–3.
3. **Food / new-restaurant spotlights** — overperform massively, and they pull the
   highest *repeat* rate of anything we run: Crave donuts drew 9 clicks from 5
   people (1.8×) — readers go back a second time. ZZAN 10 clicks (2nd in its
   issue) from "Worth Checking Out". **Feature one every week.**
4. **Cars / motorsport** — solid. A rally took 9 (top of its issue), a club
   circuit round took 8, Vespa's 80th got 3. An earlier note here claimed club
   fixtures underperform, based on reading that round at 2 clicks a day after
   send. It finished at 8. Do not judge motorsport early.
5. **Live music / ticketed gigs** — near-universally 0–1 clicks (Spoegwolf 1,
   Music Bingo 0). Exception: wine+culture "experiences" (Jazz & Wine 6).
   Comedy and theatre are fine in the quick-list (Lag in Afrikaans 2).
6. **Tribute shows — cut them.** Not weak, *dead*: Queen 0, Boks & ABBA 0,
   Adele 0. Six straight issues at zero. They cost a slot and earn nothing.
7. **Kids-specific / participation sport** — narrow (2 or fewer). A Women's
   Month fun run took 1.

**Rules that follow:**
- **Editor's Pick = the most novel, broadly-appealing EXPERIENCE — and it works
  best in an unexpected venue.** The strongest result on record is #019's SAAF
  Museum Market Day: **14 of 29 clickers (48%)**, 2.8× the runner-up. It stacked
  category 1 on category 2 — a *market* inside an *Air Force museum*. When the
  Pick was niche it lost to ordinary markets (#016 Grease Party 5th; #017 mohair
  hero 4; #014 Little Gravity 2, beaten by a demoted Polar Plunge at 7).
- The Editor's Pick slot does **not** create clicks — the right event does.
- **Never hand the Pick to a paid niche workshop, even a friend's.** #019's
  watercolour workshop placed 4th on 3 clicks, behind a plain bohemian market.
  Use the **Friendly Highlight** card instead: it gives partners real visibility
  and a booking link without spending the hero slot.
- Don't trim the "Also Happening" tail; markets there still pull well.
- Total clicks track with how many markets + experiences + food + cars an issue
  packs in. That's the lever — not send-time or button count.

**Benchmarks (#019, the reference issue):** 444 recipients · **53.4% open** ·
**9.2% click** · **17.3% CTOR** · 1 bounce · 0 spam · 1 unsubscribe (0.2%).

**Measure on the Monday after, not the day of.** #019 read 42.6% open / 11.9%
CTOR at 8 hours, 51.6% / 14.4% at 24 hours, and 53.4% / 17.3% once the weekend
had passed. Clicks alone grew from 33 to 41 *after* the 24-hour mark, because
this is weekend-planning content: people reopen the email on Friday and Saturday
to decide what to actually do. Every early read understates the issue, and it
understates events happening later in the weekend most of all.
The mix that produced it: 1 novel experience + 3 markets + 1 food + 1 motorsport.

Watch CTOR, not opens — it measures content quality independently of the subject
line. But read it *late*: it climbed 11.9% → 13.5% → 15.3% through the day, then
settled to 14.4% as late openers arrived without clicking. **Judge against the
settled figure, never the mid-day peak** — clicks finish hours before opens do.

**How that sits against industry (2026):** MailerLite's global average open rate
is 43.5%; media/publishing averages 4.1% click and 12.9% CTOR. #019 beat all
three: opens by 8 points, CTOR by 1.5, and the click rate by ~80%. Caveat worth keeping: a 444-person list that opted
in recently will always outperform benchmarks drawn from far larger lists. Treat
these as a floor to hold, not a trophy — and expect the percentages to drift down
as the list grows, which is normal and not a quality problem.

**Per-issue results (MailerLite, actual):**

| Issue | Sent | Recip | Open | Click | CTOR | Unsub | Bounces |
|---|---|---|---|---|---|---|---|
| #016 | 9 Jul  | 434 | **54.2%** (235) | 5.99% (26) | 11.1% | 2 | 8 |
| #017 | 16 Jul | 439 | 43.3% (190) | 4.33% (19) | 10.0% | 0 | 2 |
| #018 | 23 Jul | 438 | 42.9% (188) | 4.11% (18) | 9.6% | 2 | 2 |
| #019 | 30 Jul | 444 | 51.6% (229) | **7.43%** (33) | **14.4%** | 1 | **0** |

**What this actually says.** #019 is the best issue on record on the two
metrics we control. Clicks hit **7.4%** and CTOR **14.4%**, against previous bests
of 5.99% and 11.1%, and CTOR broke clean out of the tight 9.6-11.1% band the
three issues before it sat in. That is a content result: the event mix, not the
layout. Opens finished at 51.6%, within 2.6 points of #016's 54.2%, so the only
metric #016 still wins is the one most exposed to subject-line luck.

**Read the numbers late.** See the benchmark note above: wait until the Monday
after the weekend. Judging earlier has now produced three wrong calls in a row,
including a playbook rule about motorsport that the final data contradicted.

**Who actually reads it (from the #016 and #019 campaign exports):**

| | #016 | #019 |
|---|---|---|
| Gmail Image Proxy | 66.3% | **71.0%** |
| Webmail overall | 87% | **89.1%** |
| Apple Mail | 1.2% | **0.47%** |
| Outlook | 0.4% | 0.93% |

Two things follow, and both are unusual:

- **Optimise for Gmail, nothing else.** ~71% of readers are on Gmail and 89% on
  webmail. This is why the 85KB budget matters (Gmail clips at ~102KB) and why
  the Promotions tab is the real deliverability battle. The MSO/Outlook
  conditionals in `template.html` serve under 1% of readers — harmless to keep,
  but never trade Gmail rendering for Outlook.
- **Our open rate is trustworthy, unlike most.** Industry open rates are inflated
  by Apple's Mail Privacy Protection, which pre-fetches images and logs opens
  nobody made. Apple Mail is **0.47%** of this list. Gmail's proxy loads images
  when the message is actually displayed. So treat our open numbers as close to
  real — a genuine advantage when comparing against inflated benchmarks.

**Deliverability is improving:** #016 had 1 hard + 7 soft bounces and 2
unsubscribes; #019 had **zero bounces** and 1 unsubscribe (0.23%). List hygiene
is healthy — nothing to fix.

**Send time is not the variable. Stop blaming it.** All four exports:

| Sent (UTC) | Issue | Open |
|---|---|---|
| 07:08:42 | #017 | 43.3% |
| 07:10:41 | #016 | **54.2%** |
| 07:11:37 | #019 | 45.5% |
| 07:32:06 | #018 | 42.9% |

Three sends inside a **three-minute window** span **10.9 points**, and the
*earliest* send placed third. Keep sending ~07:10 UTC (09:10 SAST) for habit,
but never explain a soft issue with timing — the variance is in the subject
line and the event mix.

**Subject lines, ranked by the open rate they produced:**

| Issue | Subject line | Open | What it does |
|---|---|---|---|
| #016 | `Weekend plans: sorted. ✅` | **54.2%** | promises the reader an outcome |
| #019 | `A market inside the Air Force Museum 🛩️` | 45.5% | one specific curiosity hook |
| #017 | `PE Weekend: Goats, ABBA & More!` | 43.3% | lists contents, "& More!" filler |
| #018 | `PE's epic weekend awaits` | 42.9% | generic hype, says nothing |

**Sell the outcome, not the contents.** The winner is the only one that makes a
promise about the reader's life rather than describing what's inside. Length
isn't the lever — #016 and #018 are both ~24 characters and 11 points apart.
Hype words ("epic", "awaits") and content lists both underperform. Never put a
dead category in the subject line (#017 led with ABBA, a tribute act).

**Subject and preheader should do different jobs.** #016 split them properly:
subject made the promise ("sorted"), preheader supplied the proof (Grease Party,
rally racing, coastal walks). #019 used specifics in both, so the preheader
added nothing the subject hadn't already promised. Promise in the subject,
evidence in the preheader.

**Next test:** #020 should run an outcome-promise subject in the #016 mould with
a specifics-led preheader, and see whether opens climb back toward 54%. Timing
is ruled out, so the subject line is the only open-rate lever left.

Caveat: one issue per style, and #016 also followed a skipped week. Treat this
as the best available direction, not a proven law.

**Record the subject line every week.** #016–#018 had no `<!-- Subject: -->`
comment and had to be recovered by hand — the best open rate on record was
nearly undiagnosable. Fill that comment in every single time.

**An earlier claim here was wrong: skipping a week does not explain the dips.**
#016 came *after* a skipped week and posted the best open rate of the four; the
decline then happened across #017 and #018, which were sent on consecutive
weeks. Don't use "we skipped" to explain a soft issue — look at the event mix
first. Consistency is still worth keeping for habit and list health, but the
open-rate evidence for it isn't there.

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
