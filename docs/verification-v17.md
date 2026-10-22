# v1.7 verification · 2026-10-22

## Scope and integrity

- Same repository, same three hosting domains, previous version retained at `archive/20261022-v1.6-before-v1.7` (`0e43526`).
- 81 static pages pass local file, internal fragment and duplicate-ID validation; 66 book records and the three creed text digests remain checked.
- Five new groups: Pentateuch5, OT history12, poetry/wisdom5, prophets17, epistles21. Their60 books have180 progression panels and22 new cross-book comparison cases. Remaining6 books retain their existing guides.
- Group chapter totals derive from existing metadata. No new word counts, dates or event counts have been invented. “52 life units” remains a selection of teaching units, not an exhaustive historical reconstruction.

## Browser observations

- All five new group URLs opened on Vercel, reporting correct numbers of books, progression panels and case cards; all use `content-visibility:auto` on long book cards.
- Group directory includes9 topics. Numbered group and book/case child links are present. Epistle search for 腓利门书 shows1/21; a book TOC jump restores all21 and lands on Romans. Recall answer opens successfully.
- Responsive: Pentateuch/history/wisdom320,768,1440; prophets/epistles/directory320,390,1440: no document overflow or fixed-control overlap. Wide tables scroll locally.
- Seven note styles are available. Violet marking, changing to green, filtering by style and green marker reload persistence checked. Notes are stored locally and the disposable test record removed. Text editing saves on input rather than relying on blur.

## Performance boundaries

- Ordinary scrolling stays browser-native. Distant anchors jump directly; near anchors use native smooth scrolling. No wheel interception or full-page animation loop.
- Long comparison cards defer offscreen rendering; small entrance effects run once and respect reduced motion. Mobile fixed toolbars avoid backdrop-blur compositing.
- Existing life/king players retain explicit play/pause and background/offscreen pause. No claim of a measured universal frame-rate or latency gain.
- Existing creed wording and historical cautions preserved; no print/PDF controls introduced.
