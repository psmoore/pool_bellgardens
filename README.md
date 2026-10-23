# Dreamers Aquatics Center (Bell Gardens) — unofficial preview

A mock-up of [the City of Bell Gardens Aquatics Center page](https://www.bellgardens.org/our-city/about-bell-gardens/aquatic-center).
The fall schedule, which is published as one brochure image, becomes a live page: what's in the water right now, this week by
program, and a lane-by-lane calendar. The page works in English and Spanish (`?lang=es`). Schedule from the city's Fall 2026
brochure, entered in [Pool Relay](https://www.poolrelay.com).

Not operated by or affiliated with the City of Bell Gardens.

- `build.py`: generates `index.html`; every string is written in both languages, and `I18N` translates session titles.
- `finder.js`: the live "right now" card (`#today`) and the week table (`#week`), following `window.LANG`.
- Pool Relay view: `tCWlfEHlMkThb1CBUvtswc` (Dreamers Aquatics Center, lane by lane).

No schedule is typed into the page. Hours, closures and every program's days and times are `data-live` elements that
`finder.js` fills from the live Pool Relay view, so a change to the calendar changes the page. Only ages, prices and
descriptions are written in `build.py`.
