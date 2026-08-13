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
5. Sections with no content this week (e.g. Worth Checking Out, Save The Date) can
   be removed whole — from their section-divider row through their last card.
   Check `UPCOMING.md` before dropping Save The Date: it is the parking lot for
   future-dated events, and the section quietly vanished from #020 because the
   block was missing from `template.html` entirely.
6. **Where To Eat is the Worth Checking Out block, relabelled.** Same markup; the
   eyebrow becomes "Friendly Eats" and the `<h2>` becomes "Where To Eat". Use the
   `NEW` badge span on the `<h3>` for a recent opening. Food is the highest
   repeat-click category we run, so this section earns its place every week.
7. The **Friendly Highlight** is an optional bordered card that sits inside the
   relevant day, marked `OPTIONAL` in `template.html`. It is the slot partners buy
   (`STRATEGY.md`); label paid placements "Friendly Highlight &middot; Sponsored".
8. Do NOT touch the `EMAIL-ONLY` / `WEB-ONLY` / `WEB-META` markers — the publish
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

## Website analytics

GoatCounter, at `https://thefriendly.goatcounter.com`. Cookieless, stores no IP
address, honours Do Not Track, so **no consent banner is needed**. Free while the
site stays non-commercial; GoatCounter asks commercial sites to take the $15/month
plan, which is worth revisiting the day a sponsor is signed.

The snippet lives in `template.html` inside a `WEB-ONLY` block right after
`<!-- WEB-META -->`, so `publish.py` activates it on every new issue automatically.
Every existing page got it in a one-off sweep. **Nothing to do per issue.**

`latest/index.html` is deliberately *not* tracked: its meta-refresh fires before an
async script can report, so the count would be wrong rather than merely absent.
Traffic through `/latest` still shows up as a pageview on the issue it redirects
to, with the referrer intact, which is the number that actually matters.

What to read:
- **`/thank-you` pageviews ÷ `/` pageviews = the signup conversion rate.** The
  MailerLite form redirects there, so this needs no event tracking at all.
- **Referrers on `issue-NNN.html`** answer the open question in `STRATEGY.md`:
  do the WhatsApp cards actually send anyone to the site?
- Click tracking on outbound links is *not* set up. MailerLite already measures
  clicks where they happen, in the email.

`privacy/index.html` describes all of this. If the analytics setup ever changes,
that page changes with it.

## WhatsApp and Slack versions

Written to `whatsapp/issue-NNN.md` and `slack/issue-NNN.md`. **Every version ends
with this footer** (the WhatsApp version is the most-forwarded artifact we produce —
it must carry a subscribe path):

```
—
Get this every Thursday by email: thefriendly.co.za
```

## Social cards (WhatsApp gallery + Instagram carousel)

Every issue also ships a set of image cards. WhatsApp is our biggest
forwarding channel and pasted markdown reads badly there, so the cards carry
the issue as a swipeable gallery.

```
card-source/
  shoot.mjs                  the renderer, takes an issue number
  issue-NNN-cards.html       one source per issue, drives both formats
whatsapp-cards/issue-NNN/    card-1.png ... card-6.png  (1080x1080)
instagram-cards/issue-NNN/   card-1.png ... card-6.png  (1080x1350)
```

**Build steps (after the issue is finalised):**
1. `cp card-source/issue-PREV-cards.html card-source/issue-NNN-cards.html`
   and swap in this week's content. The set is: **1** cover · **2** Editor's
   Pick · **3** Friendly Highlight · **4** the weekend line-up · **5** Where
   to Eat · **6** follow closer. Pull the copy straight from the finished
   `issue-NNN.html` so the wording matches.
2. `node card-source/shoot.mjs NNN`. It renders both formats into the right
   folders. One HTML drives both sizes via a `fmt-square` / `fmt-portrait`
   body class, so never fork the template per size.
3. Eyeball each PNG (fonts loaded, no clipped text) before sending.

**Card design rules (same guardrails as the email):**
- Cream `#FFFBF0` bg, four-colour gradient stripe on top, Archivo Black logo
  with the orange dot, `#C24A20` for orange text, `#1a1a1a` dark footer.
- **Keep the palette fixed every week.** The cards' job is to be recognisable
  as The Friendly the moment they land in someone else's group chat, and
  recognition is built by repetition. The gradient stripe already supplies
  the colour variety. Do not rotate accent colours per issue.
- **No link is tappable on an image.** Cards print `thefriendly.co.za` as a
  visual CTA only; the real link goes in the WhatsApp caption or the
  Instagram link-in-bio. Card footers say where to tap.
- Note on Node: Playwright lives at `/opt/node22/lib/node_modules`, and
  `shoot.mjs` imports it by absolute path because ESM ignores `NODE_PATH`.
  Chromium is at `/opt/pw-browsers/chromium`.

**Captions to ship with them:**
- *WhatsApp* (paste with the album; the domain auto-links): lead line, 3 to 5
  emoji event bullets weirdest-first, then
  `Full issue + links → thefriendly.co.za/latest`.
- *Instagram* (the link is not tappable, so set link-in-bio to
  `thefriendly.co.za`): same bullets plus a hashtag block
  (`#GqeberhaEvents #PortElizabeth #ThingsToDoPE`). End on the
  free-every-Thursday line.

Rendered PNGs are committed so past sets stay downloadable, but they are
disposable: rerun `shoot.mjs` any time to regenerate them.

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

Analysis of click data across issues #013–#020 (MailerLite link activity). The
event TYPE drives clicks far more than where it sits in the layout.

**#020's full ranking**, for reference below: Pasta Evening @ Savages 10 &middot;
Pretty In Pink Ladies 5km 6 &middot; Food &amp; Craft Night Market 6 &middot;
Laser Tag (Editor's Pick) 6 &middot; A Mezza (Where to Eat) 5.

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
   #020 settles it: food took **45% of all clicks** (15 of 33). A restaurant
   *event* topped the issue outright (Savages pasta evening, 10) and A Mezza
   repeated the pattern exactly, 8 clicks from 5 people (1.6×). Three separate
   issues now show food producing return visits nothing else produces.
   **A restaurant hosting an event is the single strongest slot we have** — it
   stacks category 3 on category 1 and beat the Editor's Pick by 67%.
4. **Cars / motorsport** — solid. A rally took 9 (top of its issue), a club
   circuit round took 8, Vespa's 80th got 3. An earlier note here claimed club
   fixtures underperform, based on reading that round at 2 clicks a day after
   send. It finished at 8. Do not judge motorsport early.
5. **Live music / ticketed gigs** — near-universally 0–1 clicks (Spoegwolf 1,
   Music Bingo 0). Exception: wine+culture "experiences" (Jazz & Wine 6).
   Comedy and theatre are fine in the quick-list (Lag in Afrikaans 2).
6. **Tribute shows — cut them.** Not weak, *dead*: Queen 0, Boks & ABBA 0,
   Adele 0. Six straight issues at zero. They cost a slot and earn nothing.
7. **Kids-specific / participation sport** — usually narrow (2 or fewer). A Women's
   Month fun run took 1. **But #020's Pretty In Pink Ladies 5km took 6**, tied for
   second in its issue. The rule needs qualifying: an *established local charity
   fixture with its own following* is a different animal from a generic fun run.
   Ask whether the event already has a name in PE. If it does, it can carry a slot.

**Rules that follow:**
- **Editor's Pick = the most novel, broadly-appealing EXPERIENCE — and it works
  best in an unexpected venue.** The strongest result on record is #019's SAAF
  Museum Market Day: **14 of 29 clickers (48%)**, 2.8× the runner-up. It stacked
  category 1 on category 2 — a *market* inside an *Air Force museum*. When the
  Pick was niche it lost to ordinary markets (#016 Grease Party 5th; #017 mohair
  hero 4; #014 Little Gravity 2, beaten by a demoted Polar Plunge at 7).
- **The unexpected venue is not the magic. Broad appeal is.** #020's Pick was laser
  tag at the Algoa Flying Club: an experience, in a genuinely unexpected venue, and
  it still placed 4th on 6 clicks behind a Thursday pasta night. It was narrow
  (participatory, R180pp, aimed young), and narrow beats novel every time. Read the
  #019 result correctly: the SAAF market won because a *market* is broadly
  appealing, and the museum made it novel on top. Venue is the garnish.
- The Editor's Pick slot does **not** create clicks — the right event does.
- **Weeknight events are fair game.** #020's winner was a *Thursday* pasta evening,
  included against the weekend-only habit because the venue is well known locally.
  It beat everything. A popular venue doing something specific outranks the day of
  the week.
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
| #020 | 6 Aug  | 424 | 41.0% (174) | 8.25% (35) | **20.11%** | **0** | **0** |

(#016&ndash;#019 rows are 24-hour readings. #020 is the settled Monday figure, which
is why it is not comparable to #019's row: #019 settled at 53.4% / 9.2% / 17.3%.)

**What this actually says.** #020 posted the **best CTOR on record, 20.11%**, nearly
3 points above #019's settled 17.3%, with the second-best click rate and a clean
sheet: zero unsubscribes, zero spam complaints, zero hard bounces. It also posted
the **worst open rate on record, 41.0%**, two points below #018.

That combination is the whole story of the issue: **far fewer people opened it, and
those who did engaged harder than any audience we have ever had.** Whatever went
wrong happened at the "decide to open" step, not in the content.

**The cause is unresolved, and two explanations fit equally well.** Both predict a
low open rate *and* a record CTOR, because both filter for the most loyal readers:

1. **The subject line.** `Three days off. Sorted. ✅` was a near-repeat of #016's
   winner in construction, wording and emoji. Formats decay even when lines do
   not, "sorted" already closes every issue, and "three days off" is untrue for
   anyone working the public holiday.
2. **Deliverability, from the sunset send.** A campaign to people defined by never
   opening posts a dreadful engagement rate, and Gmail is 70%+ of this list.

The email-client split was proposed as the tiebreaker and **it failed**: #020's
export carries a **33.9% "Unknown"** bucket absent from earlier exports, and the
reading-environment percentages imply most of it is webmail, i.e. probably
unfingerprinted Gmail. So the apparent Gmail fall from 71% to 48.6% is likely a
reporting artefact, not readers disappearing. Do not cite it as evidence.

The one real signal: **zero spam complaints and zero hard bounces**, which is not
what a damaged sender reputation usually looks like. That leans toward the subject
line.

**#021 settles it.** Run a genuinely fresh subject line. Opens recovering toward
50% means the subject line was the cause. Opens sitting near 41% behind a good
line means deliverability, which mends over a few issues on its own.

**Read the numbers late.** See the benchmark note above: wait until the Monday
after the weekend. Judging earlier has now produced three wrong calls in a row,
including a playbook rule about motorsport that the final data contradicted.
#020 confirmed it again: Friday read 36.8% / 18.6%, Monday read 41.0% / 20.1%.

**Who actually reads it (from the #016, #019 and #020 campaign exports):**

| | #016 | #019 | #020 |
|---|---|---|---|
| Gmail Image Proxy | 66.3% | **71.0%** | 48.6% † |
| Unknown | — | — | **33.9%** † |
| Webmail overall | 87% | **89.1%** | 83.4% |
| Apple Mail | 1.2% | **0.47%** | 1.13% |
| Outlook | 0.4% | 0.93% | 1.13% |

† **Do not read #020's Gmail figure as a real fall.** A 33.9% "Unknown" bucket
appears in that export and not in the earlier ones. Identified webmail only reaches
about 60% of openers, so most of Unknown has to be webmail too, which at this list's
composition means unfingerprinted Gmail. Gmail is almost certainly still ~70-80%.
Treat client-mix comparisons across exports as unreliable unless the Unknown bucket
is small in both.

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
| #020 | `Three days off. Sorted. ✅` | **41.0%** | re-ran #016's format a second time |

**Do not re-run a winning subject line as a template.** This is the #020 lesson and
it cost 13 points against #016. Take the *principle* (promise an outcome), never
the wording. `Sorted` plus `✅` was fresh once; by its second outing the list had
already seen it, and "That's your weekend sorted" closes every single issue, so the
word was worn out before it reached the subject line. A repeated format also stops
reading as a promise and starts reading as a template, which is exactly what
"generic" feels like from the inbox.

**Check the promise is true for everyone.** "Three days off" only applied to readers
who got the public holiday. Retail, hospitality, healthcare and the self-employed
did not. #016's "Weekend plans" applies to the whole list. A promise that excludes
part of the audience is worse than a vaguer one that includes all of it.

(The #020 figure is confounded: see the per-issue results above. The subject line is
the leading explanation but not a proven one.)

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

**Next test (#021):** an outcome promise in a **construction the list has not seen
before**. No "sorted", no ✅, and a promise that holds for someone working the
weekend. This doubles as the tiebreaker on #020's open-rate collapse, so it matters
that the line is genuinely good: a weak one leaves the question open for another
week.

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
