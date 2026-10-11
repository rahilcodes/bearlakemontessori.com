# Bear Lake Montessori Academy Website

Official website for Bear Lake Montessori Academy ([bearlakemontessori.com](https://bearlakemontessori.com)).

## Project Structure

- `website/` — Finished static website files (`index.html`, pages, CSS, JS, images, sitemap, robots.txt) ready for deployment.
- `website-src/` — Source pages and generator scripts.
  - `pages/` — Individual page content templates with JSON front-matter.
  - `build.py` — Python build script that compiles pages into the complete static site in `website/`.
- `Bear Lake Montessori Redesign/` — Redesign mockups, design assets, and page templates.

## Development & Building

To rebuild the static site after updating page content:

```bash
cd website-src
python build.py
```

To run a local preview server:

```bash
python -m http.server 8765 --directory website
```
