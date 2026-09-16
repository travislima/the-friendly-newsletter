# Sourcing an issue

How to find the week's events without anyone sending screenshots. Written after the
first end-to-end run (#025, 17 September 2026), which used Claude driving Travis's
own logged-in Chrome via the Claude in Chrome extension.

> **This supersedes the pessimism in `AUDIT.md` §8.** That section ruled out
> *headless scraping against facebook.com*, and it was right to. Driving the
> browser you are already signed into, reading pages you can already see, is a
> different activity and it works. What `AUDIT.md` got right is the conclusion:
> aim to shrink the manual step, not to delete the human.

---

## Run these three passes, in this order

The order matters. Instagram is first because it is the only source that reliably
carries **times and prices**, and it is the only place the recurring markets post.

### Pass 1: Instagram (best source)

Sign-in: the `@thefriendlype` account. It already follows the right local
businesses, which is the whole asset. Treat the following list as the curated
firehose it is.

1. `https://www.instagram.com/` and read the home feed. Scroll 3 or 4 times, no
   more. It degrades into "Suggested for you" past that point and stops being local.
2. Poster images carry the detail the caption omits. **Screenshot and read the
   poster**, do not trust the caption alone.
3. Then hit the recurring organisers directly by handle. Known good:
   - `@filthys_pe` — Filthys Market, Walmer
   - `@crosswaysvillagemarket` — Crossways Village Market
   - `@flavorsofgqeberha` — food creator, useful for the Where To Eat slot

**What it produced in #025:** Filthys Market (Sunday, full times and address) and
the Crossways Heritage Day market (date, times, free entry, directions). Facebook
had neither.

### Pass 2: Facebook group *event tabs*

Not the group feeds. The feeds are a wormhole and the signal-to-noise is bad.
Go straight to `/<group>/events` and click "See more group events".

- `https://www.facebook.com/groups/3240642369348876/events` — PE "Local is lekker"
  (18.8K members, **the best of the three**)
- `https://www.facebook.com/groups/TFCPE/events` — The Friendly City of PE (59.8K)
- `https://www.facebook.com/groups/1769233483301584/events` — Summerstrand Connection

Grab the event IDs in one go with the browser console rather than clicking through:

```js
[...document.querySelectorAll('a[href*="/events/"]')]
  .map(a => a.href.split('?')[0] + ' :: ' + a.innerText.trim().replace(/\n/g,' | '))
  .filter(s => s.length > 30).join('\n')
```

### Pass 3: Facebook Discover, date-filtered

Thin, but it catches things the groups miss. The date filter is URL-drivable, which
beats clicking the dropdown. SAST is UTC+2, so subtract 2 hours from local midnight:

```
https://www.facebook.com/events/?date_filter_option=CUSTOM_DATE&discover_tab=LOCAL
  &start_date=2026-09-16T22%3A00%3A00.000Z   # Thu 17 Sept 00:00 SAST
  &end_date=2026-09-20T22%3A00%3A00.000Z     # Sun 20 Sept 23:59 SAST
```

⚠️ The built-in "This week" preset **ends at Saturday midnight and silently drops
Sunday**, which is the day the markets run. Always set the range yourself.

Expect roughly 9 results and expect some to be in the wrong country. Filter by eye.

### Pass 4 (when an event is ticketed): Quicket

Quicket is the source of truth for **price and venue**, and it has a public API if
this is ever scripted properly. Any Facebook event with a "Tickets" link is worth
following through. In #025 it supplied the fayre's full pricing, which Facebook
did not show at all.

---

## Rules learned the hard way

**Never print a venue or time that only one source gives you.** The #025 Editor's
Pick had the fayre at *Hellenic Hall, Parsons Hill* on Quicket and at *Norm-Hudlin
Trails, Kragga Kamma Rd* on Facebook. Quicket won on three grounds: it is the
ticketing platform, its structured date matched, and the event's own "Greek or
medieval dress" rule fits a *Hellenic* hall.

**Travis confirmed Hellenic Hall: the fayre moved indoors, most likely for weather.**
That is the general shape of these conflicts. An outdoor event moves to an indoor
venue late, the ticketing platform is updated because it has to be, and the Facebook
location field is left behind. **When an outdoor and an indoor venue disagree, the
indoor one is usually the newer truth.** Flag every conflict to Travis rather than
silently picking, but lead with the ticketing platform.

**Duplicate Facebook listings are common and they disagree.** "Roots, Rides &
Rhythm" returned three near-identical events across two different venues. It was
pulled from #025 for that reason. When listings conflict and none is clearly
authoritative, drop the event. A gap is cheaper than a wrong address.

**Facebook event headers localise to the viewer's timezone.** This is already rule
9 in `CLAUDE.md`. The poster artwork is authored in SAST and does not move. Poster
wins.

**Event description bodies go stale.** The fayre's Quicket copy still said
"Saturday, 15 August 2026" while the structured date field said 19 September. Trust
the structured field, not the prose.

**Do not invent the Where To Eat slot.** It is the highest repeat-click category we
run, which is exactly why a fabricated recommendation is the most expensive kind.
If no new opening can be verified, use a real restaurant and write only what is
verifiable about it.

---

## What is worth automating next

Ranked by payoff over effort:

1. **Quicket's public API.** Genuinely scriptable, no login, gives price and venue.
   A weekly script could draft the ticketed half of the candidate list unattended.
2. **A capture inbox** (still the best idea in `AUDIT.md` §8). Anything Travis sees
   during the week gets forwarded to one running list. Kills the collecting half.
3. **The three browser passes above**, as a repeatable prompt. This is what ran for
   #025 and it took one session with no screenshots.

**The realistic target is a Wednesday candidate list for Travis to approve, not an
unattended issue.** The #025 venue conflict is the argument: a human had to decide
which of two sources to believe, and getting it wrong puts readers at the wrong
address on a Saturday morning.
