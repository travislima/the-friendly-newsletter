# The Friendly — build notes for Claude

The Friendly is a free weekly email newsletter about events, food, and things to do in
Port Elizabeth (Gqeberha), South Africa. Sent Thursdays 8am via MailerLite (HTML is
pasted in manually). This repo is also the public website (GitHub Pages,
thefriendly.co.za) — the issue HTML files double as the web archive.

**Past issues are a documented archive. Never edit a published `issue-NNN.html`.**
All improvements go into the next issue.

## Building a new issue

Start from the most recent `issue-NNN.html` and follow its structure:
preheader → header → color stripe → intro → Editor's Pick card → This Weekend
(day labels + event cards) → Also Happening quick list → Worth Checking Out →
outro → footer.

**New in every issue from #016 onward** (these close the growth loop — do not drop them):

1. **View-in-browser line** — add to the intro block, directly under the WhatsApp line,
   same styling as that line:

   ```html
   <p style="margin: 6px 0 0; font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.5; color: #999999;">Reading on the web? <a href="{$url}" style="color: #FF6B35; text-decoration: none; font-weight: 500;">View this issue in your browser</a>.</p>
   ```

2. **Forwarded-subscriber line** — add to the outro block, after the "Forward it to a
   friend" paragraph:

   ```html
   <p style="margin: 0 0 6px; font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 14px; color: #777777; line-height: 1.65;">Was this forwarded to you? <a href="https://thefriendly.co.za" style="color: #FF6B35; text-decoration: none; font-weight: 600;">Subscribe free at thefriendly.co.za</a></p>
   ```

3. **Sponsor line** — add to the dark footer block, above the "You're getting this
   because" paragraph:

   ```html
   <p style="margin: 20px 0 0; font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 10px; color: rgba(255,251,240,0.5); line-height: 1.6;">Want your business in front of PE's most plugged-in crowd? <a href="mailto:hello@thefriendly.co.za" style="color: rgba(255,251,240,0.7); text-decoration: underline;">Reply or email us</a>.</p>
   ```

`{$url}` (view in browser) and `{$unsubscribe}` are MailerLite merge tags — keep them
verbatim in the sent HTML.

## WhatsApp and Slack versions

Written to `whatsapp/issue-NNN.md` and `slack/issue-NNN.md`. **Every version from #016
onward ends with this footer** (the WhatsApp version is the most-forwarded artifact we
produce — it must carry a subscribe path):

```
—
Get this every Thursday by email: thefriendly.co.za
```

## Publishing a new issue (web archive)

1. Commit `issue-NNN.html`.
2. Update `latest/index.html` — the redirect URL appears in **two places**
   (meta refresh + canonical) plus the fallback link in the body.
3. Add the new issue to the top of the Past Issues list in `index.html`.

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

## Pre-send checklist

- [ ] Issue number and date in header, `<title>`, and preheader all match — and the
      date really is a Thursday (`date -d YYYY-MM-DD +%A`).
- [ ] All comment headers match their content (no leftovers from the previous issue).
- [ ] All links https; every event card has a working URL.
- [ ] `{$unsubscribe}` and `{$url}` present. Growth lines 1–3 above present.
- [ ] File under 85KB (`wc -c issue-NNN.html`) — Gmail clips at ~102KB after
      MailerLite adds tracking.
- [ ] Record the subject line as a comment at the top of the file:
      `<!-- Subject: ... -->` (we correlate these with open rates).
- [ ] After sending: publish steps above (latest/ redirect + index.html list).
