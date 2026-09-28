# Content data — أطباء الخير · رسالة مدينة نصر

Source: facebook.com/atebaaelkheirnasrcity (scraped 2026-09-27 via Apify `facebook-posts-scraper` + `facebook-photos-scraper`).

- `posts.json` — 119 posts (Sep 2025 → Sep 2026): text, date, likes/shares/comments, media ids. Use for copy, timeline, and stats.
- `media/<category>/<sub>__<fbid>.jpg` — 268 unique full-res images (18 perceptual duplicates removed).
- `catalog.json` — one row per image: `category`, `kind` (photo|design), `sub` (specific activity), `quality` 1–5 (5 = hero-worthy), `people`, `note`, size, date, caption, links.
- `previews/<category>.jpg` — contact sheet per category for quick review.

| category | count | what |
|---|---|---|
| events | 77 | Beyond Medicine conference (55), Ramadan bags, Gray's Moments hospital visit, annual celebration, iftar, Family Day |
| convoys | 43 | Medical convoys: Ghaith, VitFam, spring allergy, T3 Care, Growing Healthy, exploratory… |
| awareness | 36 | Health-awareness infographics (diabetes, heatstroke, painkillers, cold shot, botulism…) |
| courses | 23 | Suturing, IV cannulation, BLS/CPR, ICC hands-on training |
| announcements | 21 | Promo flyers, agendas, registration calls, greetings |
| honors | 20 | Volunteer recognition: Hero El-Kheir plaques, best-volunteer cards, certificates |
| clinics | 17 | Internal-medicine & ophthalmology clinic, BP/sugar screening |
| leaders | 16 | Activity heads & supervisors (clinic heads, Gomaat El-Kheir / Gray's Moments role cards) |
| speakers | 7 | Guest doctors — "Meet Our Speaker" cards (Beyond Medicine) |
| team | 7 | Team group photos |
| other | 1 | Blank video thumbnail (ignore) |

Classification: 3 parallel vision agents labeled every image using captions + OCR; results were then spot-checked by random sheet sampling and corrected (speakers split from leaders, a few team/sub fixes).

## People (`people.json`, `people/`)
- `leadership` — 12 activity heads & supervisors merged across their role cards (clinic structure 15/5/2026, Gray's Moments, جمعة الخير): Arabic/English name, `tier` (heads | supervisors), roles, clean portrait cropped from the card (`people/<fbid>.png`), and source cards.
- `speakers` — 7 Beyond Medicine guest doctors with bio text from their "Meet Our Speaker" posts and card image.
