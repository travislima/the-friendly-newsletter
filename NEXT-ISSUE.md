# Prep brief: next issue, Thursday 8 October 2026

Covers **Friday 9 to Sunday 11 October**, plus Thursday 8 evening.

**Issue number is unconfirmed.** The repo ends at #026 (24 September) and holds no
#027. If an issue went out on Thursday 1 October and was never committed, this is
**#028**; if that week was skipped, this is **#027**. `CLAUDE.md` records a
renumbering mistake made from exactly this gap, so the number comes from MailerLite,
not from the archive. Confirm before scaffolding.

Written by a public-web research pass with no browser and no logged-in sessions:
nmbt.co.za (tourism board) and Quicket's Gqeberha listing. Instagram and the
Facebook group event tabs returned login shells. See "Still needs a browser".

## Found on the public web

Quicket publishes times in UTC in its structured data; everything below is already
converted to SAST (+2). Quicket's listing JSON shows every price as `0.0`, which
means *not populated*, not free: check the event page before printing a price.

### Thursday 8 October

- **Something Good: Music Bingo.** 6:30PM SAST. Something Good Roadhouse, 25 Marine
  Drive, Summerstrand. Price not shown.
  `CLAUDE.md`: Music Bingo took **0 clicks** last time. Skip, or tail at most.
  https://www.quicket.co.za/events/400260-something-good-music-bingo-8-october/

### Friday 9 October

- **Fittest in PE 2026.** From 7AM SAST. Lions Bay CrossFit, 208 Willow Road.
  CrossFit competition; whether spectators are welcome is not stated. Participation
  sport, narrow. Tail at most.
  https://www.quicket.co.za/events/384362-fittest-in-pe-2026/
- **Sacred Heart Catholic Church Golf Day.** Tourism board listing, details not
  fetched. A golf day is a fundraiser for players; not a reader event.
  https://www.nmbt.co.za/events/sacred_heart_catholic_church_golf_day.html

### Saturday 10 October

- **Joseph & the Amazing Technicolor Dreamcoat, closing day.** Impact Community
  Theatre. The Savoy Theatre, 100 Diaz Road, Perridgevale. Shows at **2PM and 7PM**.
  **R130 to R200**, Webtickets. Group bookings: Rose Cowpar, 072 906 1977.
  Run is 30 Sept to 10 Oct, so Saturday is the last chance. Theatre is fine in the
  quick list per the playbook; it does not carry a card.
  Tickets: https://www.webtickets.co.za/v2/event.aspx?itemid=1600831085
  Source: https://www.nmbt.co.za/events/joseph__the_amazing_technicolor_dreamcoat.html
- **Conservation Breakfast with Anne Laing.** 8:30AM SAST. St John's Anglican
  Church, 40 8th Avenue, Walmer. Talk plus breakfast; price not shown. Niche, but it
  has food attached and a Walmer address. Quick-list candidate.
  https://www.quicket.co.za/events/368704-conservation-breakfast-with-anne-laing/

### Sunday 11 October

- Nothing found on the public web. **This is the gap, not the weekend.** Sunday is
  market day and markets post on Instagram, which this pass could not read.

## Gaps against the playbook

`CLAUDE.md`'s winning mix (#023, 37 clicks): **four markets, one food spotlight,
one novel experience, one weak-category card.** This pass found:

| Category | Found | Needed |
|---|---|---|
| Markets | **0** | 2 to 4 |
| Restaurant hosting an event | **0** | 1 |
| Where to Eat | **0** | 1 |
| Novel experience / festival | **0** | 1 |
| Motorsport | 0 | 1 if on |
| Weak-category items | 5 | 0 to 1 |

Every category that produces clicks is missing, and every item found is in a
category that does not. That is the signature of a pass without Instagram, not of a
quiet weekend: in #025 and #026 Instagram supplied the markets that Facebook and the
public web had no trace of. **Do not build from this list alone.**

## Still needs a browser

Per `SOURCING.md`, run the three logged-in passes before building. These are the
whole issue:

- [ ] **Pass 1, Instagram.** `@thefriendlype` home feed, scroll 3 to 4 times, then
      directly: `@filthys_pe`, `@crosswaysvillagemarket`, `@whatsgoodinthehood_pe`
      (the Fairview night market, first Fridays), `@flavorsofgqeberha` (Where to
      Eat). Read the posters, not the captions.
- [ ] **Pass 2, Facebook group event tabs.** Local is lekker first
      (`/groups/3240642369348876/events`), then TFCPE, then Summerstrand
      Connection. Use the console one-liner in `SOURCING.md`.
- [ ] **Pass 3, Facebook Discover, date-filtered.** Set the range by hand; the
      "This week" preset drops Sunday:
      ```
      https://www.facebook.com/events/?date_filter_option=CUSTOM_DATE&discover_tab=LOCAL
        &start_date=2026-10-07T22%3A00%3A00.000Z   # Thu 8 Oct 00:00 SAST
        &end_date=2026-10-11T22%3A00%3A00.000Z     # Sun 11 Oct 23:59 SAST
      ```
- [ ] **Markets to check by name:** the Re-Seconds (rotates Walmer Town Hall and
      Londt Park), the Collective Market, the Antique Collective (first Sundays,
      Walmer Park: 4 Oct was the first Sunday, so probably not this week), the UP
      Market at Buffelsfontein, Crossways.
- [ ] **Aldo Scribante** for anything racing.
- [ ] **Marktfees** (26 to 29 Nov, Old Tramways): `UPCOMING.md` says early October is
      the right week for its first Save The Date, and it is on neither the tourism
      board nor Quicket. Needs the organiser's page.
- [ ] **Where to Eat** from Travis. Not inventable.

## Save The Date candidates found this pass

All from Quicket's Gqeberha listing. Prices unverified. Parked in `UPCOMING.md`.

- **CONect Geek Convention**, Sat 7 Nov, Fairview Sports Centre, 60 Willow Road.
  A convention is category 1 stacked on 2 and broadly appealing. The strongest
  Save The Date here if Marktfees stays unverified.
- **NMBPride festival 2026**, Sat 14 Nov, Fairview Sports Centre.
- **Mythopia, aerial arts**, Fri 13 and Sat 14 Nov, Centrestage@Baywest.
- **Barry Hilton, Audience Unplugged**, Sat 31 Oct, The Capital Boardwalk. Comedy:
  quick-list category, not a Save The Date card.
- **Hey Hey Divorcé**, 16 to 18 Oct, Savoy Theatre (and 18 Oct at Centrestage).
  Theatre. Next week's quick list, not this week's.

## Subject line

Opens are solved: five consecutive fresh constructions in the mid-to-high fifties.
Spend no time here beyond the constraint: a promise, a shape the list has not seen,
true for everyone, no "sorted", no checkmark. Write it last, once the mix is known.
