# موقع أطباء الخير — رسالة مدينة نصر

Static site built with [Astro](https://astro.build). Mobile-first, Arabic RTL.

```bash
npm install
npm run images   # re-crop curated photos from ../data/media into src/assets/photos
npm run dev      # local preview
npm run build    # output in dist/
```

- `scripts/prepare_images.py` — the curated photo list: which Facebook photo, the frame ratio and focal point. Photos keep the team's overlay as published.
- `src/components/Photo.astro` — every photo goes through here: AVIF/WebP in several widths, lazy below the fold, caption (place, month) under it.
- `src/layouts/Section.astro` — template for the section pages (convoys, clinics, courses, events, team).
- Design rules: `src/styles/global.css` header comment; brief in `../.superdesign/design-system.md`.
