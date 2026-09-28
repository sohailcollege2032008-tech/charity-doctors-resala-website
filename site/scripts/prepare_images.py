"""Curate + crop + clean source photos from ../data/media into src/assets/photos.

Each entry: out-name -> (fb id, aspect w/h, focal x, focal y, trim-top, trim-bottom).
trim-* can cut into the Facebook overlay; all are 0 so photos keep it as published
before cropping to the target frame around the focal point.
Astro then emits responsive AVIF/WebP from these masters.
"""
import glob, json, os
from PIL import Image, ImageEnhance, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '..', 'data', 'media')
OUT = os.path.join(ROOT, 'src', 'assets', 'photos')

FB = (0.0, 0.0)        # keep the team's overlay (logo stamp + navy fade) as published
CAM = (0.0, 0.0)       # camera originals (Beyond Medicine) have no overlay

PHOTOS = {
    # hero + pillars
    'hero-eye-exam':        ('122102690979041269', 4/5, .36, .55, *FB),
    'vest-volunteer':       ('122127122799041269', 4/5, .62, .55, *FB),
    # convoys
    'convoy-desk':          ('122113367427041269', 3/2, .55, .55, *FB),
    'convoy-child-bp':      ('122125899537041269', 4/3, .45, .55, *FB),
    'convoy-elder':         ('122125899405041269', 4/3, .55, .55, *FB),
    'convoy-history':       ('122127123051041269', 1/1, .50, .55, *FB),
    'convoy-talk':          ('122127122925041269', 1/1, .50, .55, *FB),
    'convoy-women':         ('122127123003041269', 1/1, .50, .55, *FB),
    'convoy-ghaith-1':      ('122127674553041269', 4/3, .50, .45, .0, .0),
    'convoy-ghaith-2':      ('122127674511041269', 4/3, .50, .45, .0, .0),
    'convoy-ghaith-3':      ('122127674469041269', 4/3, .50, .45, .0, .0),
    'convoy-t3-team':       ('122134577889041269', 3/2, .50, .50, .0, .0),
    'convoy-growing-team':  ('122134925607041269', 3/2, .50, .50, .0, .0),
    # clinics
    'clinic-child-eye':     ('122102690937041269', 4/5, .62, .55, *FB),
    'clinic-bp':            ('122113749351041269', 1/1, .45, .55, *FB),
    'clinic-sugar':         ('122113749327041269', 1/1, .45, .55, *FB),
    'clinic-bp-2':          ('122103170385041269', 1/1, .50, .55, *FB),
    'clinic-sugar-2':       ('122103170415041269', 1/1, .50, .55, *FB),
    'clinic-team':          ('122135783085041269', 3/2, .50, .45, .0, .0),
    # courses
    'course-cpr':           ('122101524177041269', 4/5, .45, .55, *FB),
    'course-cpr-2':         ('122101524135041269', 1/1, .50, .55, *FB),
    'course-iv':            ('122101807827041269', 1/1, .50, .55, *FB),
    'course-suture':        ('122102162781041269', 4/5, .55, .55, *FB),
    'course-suture-2':      ('122102162685041269', 1/1, .50, .55, *FB),
    'course-instructor':    ('122130182091041269', 4/3, .50, .55, *FB),
    'course-icc-group':     ('122136182793041269', 3/2, .50, .55, .0, .0),
    'course-suture-group':  ('122129898123041269', 3/2, .50, .55, *FB),
    # events
    'bm-speaker-crowd':     ('122137377741041269', 4/5, .40, .55, *CAM),
    'bm-hall':              ('122137146423041269', 3/2, .50, .50, *CAM),
    'bm-crowd':             ('122137146765041269', 3/2, .50, .55, *CAM),
    'bm-balloons':          ('122137294269041269', 4/5, .50, .50, *CAM),
    'bm-rania':             ('122137293621041269', 3/2, .50, .50, *CAM),
    'bm-greeting':          ('122137378479041269', 3/2, .50, .50, *CAM),
    'bm-volunteers':        ('122137146363041269', 4/5, .50, .50, *CAM),
    'grays-hospital':       ('122126170959041269', 4/3, .50, .45, .0, .0),
    'ramadan-dusk':         ('122121131583041269', 3/2, .50, .55, .0, .0),
    'ramadan-lentils':      ('122121042495041269', 4/5, .50, .55, .0, .0),
    'ramadan-packing':      ('122121042363041269', 4/3, .50, .55, .0, .0),
    'annual-celebration':   ('122118058755041269', 3/2, .50, .55, .0, .0),
    # team
    'team-vehicle':         ('122131744509041269', 3/2, .45, .55, .0, .0),
    'team-thanks':          ('122109886485041269', 3/2, .50, .55, .0, .0),
}

def frame(im, aspect, fx, fy, tt, tb):
    w, h = im.size
    im = im.crop((0, int(h * tt), w, int(h * (1 - tb))))
    w, h = im.size
    if w / h > aspect:            # too wide -> cut width
        cw, ch = int(h * aspect), h
    else:                         # too tall -> cut height
        cw, ch = w, int(w / aspect)
    x = min(max(int(fx * w - cw / 2), 0), w - cw)
    y = min(max(int(fy * h - ch / 2), 0), h - ch)
    return im.crop((x, y, x + cw, y + ch))

def grade(im):
    # gentle, uniform finish: recover contrast lost to FB recompression
    im = ImageOps.autocontrast(im, cutoff=0.4)
    im = ImageEnhance.Color(im).enhance(1.04)
    return im

def main():
    os.makedirs(OUT, exist_ok=True)
    meta = {}
    for name, (fid, aspect, fx, fy, tt, tb) in PHOTOS.items():
        src = glob.glob(os.path.join(SRC, '*', f'*__{fid}.jpg'))[0]
        im = grade(frame(Image.open(src).convert('RGB'), aspect, fx, fy, tt, tb))
        im.thumbnail((2000, 2000), Image.LANCZOS)
        im.save(os.path.join(OUT, f'{name}.jpg'), quality=90, optimize=True, progressive=True)
        meta[name] = {'id': fid, 'w': im.width, 'h': im.height}
    json.dump(meta, open(os.path.join(OUT, '_index.json'), 'w'), indent=1)
    print(len(meta), 'photos ->', OUT)

if __name__ == '__main__':
    main()
