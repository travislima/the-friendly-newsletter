# The Friendly — growth and money

Business strategy. `CLAUDE.md` covers how to *build* an issue; this covers whether
the thing is working and what to do next. Written August 2026, after #019.

---

## Where we actually are

**443 subscribers · 53.4% open · 9.2% click · 17.3% CTOR · 1 unsubscribe · 0 spam.**

Against 2026 industry figures, that is a strong product:

| Metric | The Friendly | Media/publishing average |
|---|---|---|
| Open | 53.4% | 43.5% (MailerLite global) |
| Click | 9.2% | 4.1% |
| CTOR | 17.3% | 12.9% |

And unusually, **our open rate is honest.** Apple Mail is 0.39% of the list, so we
carry almost none of the Mail Privacy Protection inflation that pads everyone
else's numbers. When we say 53%, it is 53%.

## The actual problem: growth has stalled

| Month | Signups |
|---|---|
| March 2026 (launch) | 323 |
| April | 51 |
| May | 42 |
| June | **8** |
| July | 19 |

The launch burst was personal network. Since then we add roughly **30 a month, 7 a
week**. At that rate 1,000 subscribers is **19 months** away.

**Diagnosis: the product is strong, the audience is small, and distribution is the
bottleneck.** Twenty issues produced, almost no deliberate distribution. Do not
mistake this for a quality problem. People who read it, love it. Not enough people
read it.

## Why this matters more than pricing

Local newsletters that monetise well run roughly $2-5 per subscriber per year:

| | 443 subs | 1,000 | 2,500 |
|---|---|---|---|
| at $3/sub/yr | R1,994/mo | R4,500/mo | R11,250/mo |

At 1,000 subscribers, competently monetised, this clears **R4,500/month** without a
hard sell. At 443 we are scrapping for R2,000 and it feels like scrapping, because
it is. **Growth is worth roughly ten times more attention than sales right now.**

---

## The growth engine

**It grows when other people post about it in their WhatsApp groups.** That is the
whole mechanism. Everything below serves it.

### 1. Post the cards every week, without fail
The single biggest unfulfilled action. WhatsApp gallery and Instagram carousel are
already generated as part of the build (see `CLAUDE.md`). Producing them and not
posting them is the current failure mode.

### 2. Ask specific people, personally
We have ~100 readers who have clicked 3+ times. They are asked nothing. A named
person asking a named person converts nothing like a "forward this" line in a
footer.

Send 20 individual WhatsApp messages, not a broadcast:

> Hey, you have been reading The Friendly since the start and I really appreciate
> it. Massive favour: would you mind dropping this week's cards into [their group]?
> No pressure at all if it is awkward.

If 6 of 20 say yes and each group has 50 people, that is 300 impressions from
trusted senders, for an hour of work.

### 3. Landing page is fixed, so links now convert
Issue pages carry a subscribe bar above the fold and a conversion block at the
bottom (both `WEB-ONLY`, see `CLAUDE.md`). Send traffic to
`thefriendly.co.za/latest` and it auto-follows every new issue, so old forwards
never die.

### Not yet: referral programmes
Rewards-for-signups needs volume to work, costs real money per subscriber, and
attracts incentive-chasers who damage the engagement rate we sell on. Revisit at
2,000-3,000, and only with sponsor-funded prizes.

---

## Money

### The cost curve
- **$25/month** MailerLite today
- **$39/month** the moment we cross 500 subscribers, a 56% step
- Roughly **R12-17 per subscriber per year** to serve

Every subscriber costs money and earns nothing until something is sold. Growth is
currently a liability, which is why list hygiene matters as much as acquisition.

### Rate card
Built from actual #019 click data, triangulated three ways (CPM, cost-per-click
against local Facebook rates, and share of expected advertiser return). All three
land in the same band.

| Tier | Price | What it is |
|---|---|---|
| Quick List mention | R250 | One row in Also Happening |
| Friendly Highlight | R500 | Bordered card in the email with its own CTA |
| Highlight + Social | R950 | Above, plus a card in the WhatsApp and Instagram galleries |
| Month Partner | R2,800 | 4 issues, plus a "Presented by" line in the header |

**One Highlight + Social at R950/month makes the newsletter cost-neutral forever**,
even after the $39 step. That is the first goal. Not "$150 a month" — *one business*.

### What never goes on sale
- **The Editor's Pick.** It produced 48% of clickers in #019. The moment it is
  purchasable it stops working.
- **Where to Eat.** Highest repeat-click category precisely because it reads as a
  genuine recommendation. Sell the Highlight card instead.
- Label everything paid as "Friendly Highlight · Sponsored".
- Only take money from businesses we would have featured anyway. That discipline
  is the product.

### Who to approach

**Tier A, sell confidently** (the data says these convert): restaurants, cafés,
bakeries, food trucks · breweries and tasting rooms · market organisers ·
experience operators (tours, boat trips, surf lessons) · unusual venues hosting
one-offs.

**Tier B, set expectations**: beginner-friendly workshops · motorsport · retail
*with an event attached*.

**Tier C, turn away**: live music venues and gig promoters · tribute acts ·
kids-only activities · any B2B or service business. Readers are in weekend-planning
mode; there is no conversion path and taking their money burns the relationship.

**New vs established is the wrong question.** The filter is whether there is
something new to say: a new opening, new menu, new season, an anniversary, a
one-off. "We exist and we are nice" does not convert.

### Warm leads, in order
1. **Businesses already featured.** We have their click data. "Five readers clicked
   through to you last week, unpaid" is a receipt, not a pitch.
2. **Business addresses on our own list.** 47 of them, 23 opening most issues.
   These people already read it weekly and work somewhere with a budget.
3. **Inbound leads who went quiet.**
4. **Cold local businesses.** Only after a case study exists.

### The pricing test
Ask **five** businesses at **R500/month**, not one. One rejection is noise.

- 3+ yes → underpriced, raise it
- 1-2 yes → normal outbound, and a case study
- 0 yes → genuine information. Park it until 1,000 subscribers.

A cheap paid ask beats a free trial: free tests *delivery*, paid tests *demand*,
and demand is the open question. A sponsor also creates an obligation to post the
cards every week, which is worth more than the R500.

---

## List hygiene

Chronic non-openers cost money, drag inbox placement, and suppress the number we
sell on. **Prune before crossing 500**, because it delays the price step and
improves the rate card at the same time.

Rule: zero opens across **15+ issues** is dead. Fewer sends than that is too new to
judge. Send a sunset email first (`sunset-email.html`), keep anyone who **opened or
clicked**, remove the rest.

Two exceptions, both learned the hard way:
- **Shared inboxes** (`info@`, `admin@`) often never register an open even when
  read. Leave them.
- **Local business addresses** are sponsorship prospects. Never delete a prospect
  to save R1.40 a month.

---

## 90-day plan

### Phase 1, now to November: fix distribution
**Target 750 subscribers. Sell nothing except the five-business price test.**

1. WhatsApp cards and Instagram carousel, every week, no exceptions
2. 20 personal share-asks to the most engaged readers
3. Five sponsorship emails at R500/month, for the signal
4. Prune the dead

**Gate: if not at 600 by November, the problem is distribution, not the newsletter.
Change channels, not content.**

### Phase 2, months 4-9: monetise properly
1,000 subscribers, R2,500-4,500/month from two or three month-long partnerships.
By then the maths is obviously favourable, which is what fixes the reluctance to
charge. Not a pep talk.

### Phase 3, months 9-18: decide what this is
At 2,500 subscribers it is R7,500-11,000/month and a real decision: scale, sell, or
let it pay for itself and stay small. All three are fine. Do not decide now.

---

## Honest risks

- **Single point of failure.** Twenty issues solo is the achievement and the
  fragility.
- **Small market.** PE caps the ceiling. Fine for a R10k/month business, not more.
- **No moat.** Anyone could copy the format. The defence is being first and being
  trusted, and both compound only while we keep shipping.

## The thing to remember when it feels not worth charging for

Founder underpricing is close to universal, but reassurance is the wrong answer
because the doubt is half right. Two different questions:

- *"Is The Friendly any good?"* Not supported by data. Top-decile engagement.
- *"Is R750 a fair ask at 443 subscribers?"* Supported by data. That flinch is
  correct arithmetic.

**The product is strong; the audience is small.** Those need different fixes, and
conflating them makes a scale problem feel like a confidence problem.
