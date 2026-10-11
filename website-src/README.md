# Bear Lake Montessori Academy — site source

`../website/` is the finished static site (deploy that folder as-is). This folder holds the page sources it is built from.

- `pages/*.html` — one file per page. Each starts with a `<!--meta {...} -->` JSON block (title, description, share image, optional pre-footer CTA text), followed by the page body.
- `build.py` — wraps every page in the shared head, header, navigation, CTA and footer, expands the design macros, and writes `../website/*.html`, `sitemap.xml` and `robots.txt`.
- Shared styles and scripts live directly in `../website/assets/site.css` and `site.js`.

Rebuild after editing a page:

```bash
python build.py
```

Macros available inside pages: `{{wave:top|bottom:#fill[:#bg]}}`, `{{deco:star|dot|squiggle|ring|#color|css position|drift}}`, `{{u:word}}` (scribble underline), `{{ud:word}}` (animated underline), `{{tail}}` (speech-bubble tail), and `{{PHONE}}`, `{{TEL}}`, `{{EMAIL}}`, `{{INSTAGRAM}}`.

Forms open the visitor's email app addressed to the school (no server needed). To collect submissions on a server instead, point the `form[data-enquiry]` elements at a form endpoint and remove the handler in `site.js`.
