# The Friendly

A free weekly email newsletter about events, food and things to do in Port
Elizabeth (Gqeberha), South Africa. Sent every Thursday at 8am SAST via
MailerLite. This repo is also the public website, [thefriendly.co.za](https://thefriendly.co.za),
served by GitHub Pages from `claude/friendly-newsletter-project`.

The issue HTML files do double duty: they are pasted into MailerLite to send,
then converted in place into the web archive.

---

## Thursday, in six steps

```bash
cp template.html issue-NNN.html      # 1. never clone last week's issue
                                     # 2. fill every [BRACKETED] slot
                                     # 3. run the pre-send checklist in CLAUDE.md
                                     # 4. paste into MailerLite and send
python3 scripts/publish.py issue-NNN.html   # 5. converts to web, updates the site
git add -A && git commit && git push        # 6.
```

**Order matters.** `publish.py` strips the MailerLite merge tags, so run it
*after* pasting into MailerLite, never before. If you run it too early,
`git checkout HEAD~1 -- issue-NNN.html` restores the email version.

Then, after sending: build the social cards (below), post the WhatsApp gallery
Thursday late afternoon, and **read the numbers on Monday, not Thursday.**

---

## What lives where

| Path | What it is |
|---|---|
| `template.html` | **The one canonical source for a new issue.** Every improvement goes here. |
| `issue-NNN.html` | Sent issues, doubling as the web archive. Never edit a published one. |
| `scripts/publish.py` | Converts a sent issue to its web version and updates the site. |
| `index.html` `archive/` `latest/` `privacy/` `thank-you/` `404.html` | The website. |
| `welcome-email.html` | MailerLite automation, sent on signup. Editing it here changes nothing until pasted into MailerLite. |
| `sunset-email.html` | One-off re-engagement send for subscribers who never open. |
| `card-source/` | `shoot.mjs` plus one HTML per issue, driving both social formats. |
| `whatsapp-cards/issue-NNN/` | 1080x1080 PNGs for the WhatsApp gallery. |
| `instagram-cards/issue-NNN/` | 1080x1350 PNGs for the Instagram carousel. |
| `whatsapp/` `slack/` | Plain-text versions of older issues. |
| `subscribe-card.html` | Shareable signup card with a QR code. |
| `*-old.html` | The pre-redesign pages, kept so a revert is a rename. |

---

## The three docs

- **`CLAUDE.md`** is how to build and ship an issue: the template rules, the
  pre-send checklist, the editorial voice, and the data-backed playbook for
  which events actually get clicked.
- **`STRATEGY.md`** is whether the business is working: growth, the rate card,
  who to sell to, list hygiene, and the 90-day plan.
- **`BRAND.md`** is fonts, colours and the logo, for making visuals elsewhere.

`AUDIT.md` is an older one-off review, kept for reference.

---

## Building the social cards

```bash
cp card-source/issue-PREV-cards.html card-source/issue-NNN-cards.html
# swap in this week's content, pulled from the finished issue-NNN.html
node card-source/shoot.mjs NNN
```

One HTML renders both sizes via a `fmt-square` / `fmt-portrait` body class, so
never fork the template per format. Six cards: cover, Editor's Pick, Friendly
Highlight, the weekend line-up, Where to Eat, follow closer.

**No link on an image is tappable.** Cards print the domain as a visual cue
only; the real link goes in the WhatsApp caption or the Instagram link-in-bio.

---

## Rules that are easy to break

1. **Start every issue from `template.html`.** Cloning last week's issue
   silently carries styling drift forward. This has bitten us before.
2. **Never edit a published `issue-NNN.html`.** It is an archive.
3. **Orange buttons take dark text** (`#1a1a1a` on `#FF6B35`). Cream on orange
   fails contrast.
4. **No em dashes** anywhere: not the newsletter, not the site, not captions.
   Colon for a reveal, comma for an aside, full stop to split, `&middot;` as a
   separator. En dashes stay for ranges.
5. **Record the subject line** in the `<!-- Subject: ... -->` comment, exactly
   as sent. Issues #016 to #018 did not, and the best open rate on record was
   nearly impossible to diagnose.
6. **Keep the card palette fixed.** Recognition in someone else's group chat is
   the whole point, and that comes from repetition.
7. **Judge an issue on the Monday after.** Weekend-planning content has a long
   tail; readers reopen it on Friday and Saturday. Reading it early has produced
   three wrong calls, including one rule that the final data contradicted.

---

## Where it stands

As of issue #020, August 2026:

| | |
|---|---|
| Subscribers | ~443 |
| Open rate | 53.4% |
| Click rate | 9.2% |
| CTOR | 17.3% |
| Bounces / spam complaints | 0 |

For context, media and publishing averages are roughly 4.1% click and 12.9%
CTOR. Apple Mail is under 1% of this list, so unlike most senders the open rate
is not inflated by Mail Privacy Protection: 53% means 53%.

The bottleneck is distribution, not quality. See `STRATEGY.md`.

---

## Notes on this environment

- Playwright lives at `/opt/node22/lib/node_modules`. `shoot.mjs` imports it by
  absolute path because ESM ignores `NODE_PATH`. Chromium is at
  `/opt/pw-browsers/chromium`.
- `publish.py` needs no dependencies beyond the standard library.
- One branch only: `claude/friendly-newsletter-project`. It is the Pages source.
