# Pet API Guide — MkDocs Documentation Portal

This is a documentation portal built with [MkDocs](https://www.mkdocs.org/) and the [Material theme](https://squidfunk.github.io/mkdocs-material/), converted from the original print-style `PetAPI.html` reference document into a navigable, searchable web docs site.

## Running locally

1. Install dependencies:
   ```bash
   pip install mkdocs-material
   ```

2. Serve the site with live-reload:
   ```bash
   mkdocs serve
   ```
   Then open http://127.0.0.1:8000

3. Build a static site (output goes to `site/`):
   ```bash
   mkdocs build
   ```

## Deploying

- **GitHub Pages:** `mkdocs gh-deploy`
- **Netlify / Vercel:** point the build command to `mkdocs build` and publish the `site/` directory
- **Self-hosted:** copy the contents of `site/` to any static file host

## Project structure

```
docs/
├── index.md                       # Home page
├── getting-started/
│   ├── overview.md
│   ├── authentication.md
│   └── request-response.md
├── endpoints/
│   ├── add-pet.md                 # POST /pet
│   ├── update-pet.md              # PUT /pet
│   ├── find-by-status.md          # GET /pet/findByStatus
│   ├── find-by-tags.md            # GET /pet/findByTags
│   ├── find-by-id.md              # GET /pet/{petId}
│   ├── update-by-form.md          # POST /pet/{petId}
│   └── delete-pet.md              # DELETE /pet/{petId}
├── reference/
│   ├── summary.md                 # Endpoint summary table
│   ├── data-model.md              # Pet schema
│   └── status-codes.md            # HTTP status reference
└── stylesheets/
    └── extra.css                  # Custom method-badge styling

mkdocs.yml                         # Site config & navigation
```

## Customizing

- **Navigation** lives in the `nav:` section of `mkdocs.yml` — reorder, rename, or add pages there.
- **Colors/branding** are in `docs/stylesheets/extra.css` (currently matches the original navy `#003580` theme).
- **Theme features** (search, dark mode toggle, code copy buttons) are already enabled in `mkdocs.yml` under `theme.features`.
