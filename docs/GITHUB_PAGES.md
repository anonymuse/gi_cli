# GitHub Pages setup for the Factory Fit Profiler webapp

This repository includes a browser-only GitHub Pages version of the Factory Fit Profiler demo under [`docs/webapp/`](./webapp/). The Pages entry point is [`docs/index.html`](./index.html), which redirects visitors to the webapp so the site works when GitHub Pages publishes the `docs/` folder.

The webapp is intentionally static. It does not need a backend, package installation, build step, database, or live DevOps credentials. All profile analysis runs in the browser against pasted markdown, uploaded markdown, bundled sample data, or the mocked Jenkins build catalog.

## What gets published

When GitHub Pages is configured to publish from `docs/`, the public site contains:

- `/` — a small redirect page that sends users to `/webapp/`.
- `/webapp/` — the company profile demo.
- `/webapp/cicd-maturity.html` — the CI/CD maturity demo backed by `jenkins-build-catalog.json`.
- `/webapp/sample-company.md` — reusable markdown input for the profile demo.
- `/webapp/jenkins-build-catalog.json` — synthetic Jenkins records for the maturity demo.

## Enable GitHub Pages from the `docs/` folder

Use this option when you want GitHub to serve the checked-in static files directly.

1. Push this repository to GitHub.
2. Open the repository in GitHub.
3. Go to **Settings → Pages**.
4. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
5. Select the branch you want to publish, typically `main`.
6. Select the `/docs` folder.
7. Click **Save**.
8. Wait for GitHub Pages to finish the deployment.
9. Open the published URL shown on the Pages settings screen.

For a user or organization site, the URL is usually:

```text
https://<owner>.github.io/
```

For a project site, the URL is usually:

```text
https://<owner>.github.io/<repository>/
```

The root URL redirects to the webapp. You can also open the webapp directly at:

```text
https://<owner>.github.io/<repository>/webapp/
```

## Local preview before publishing

From the repository root, run a static file server:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/docs/
```

You can also open the webapp directly:

```text
http://localhost:8000/docs/webapp/
```

## Updating the Pages demo

Use this workflow when changing the static app:

1. Edit files in `docs/webapp/`.
2. Preview with `python -m http.server 8000` from the repository root.
3. Test the company profile page at `http://localhost:8000/docs/webapp/`.
4. Test the CI/CD maturity page at `http://localhost:8000/docs/webapp/cicd-maturity.html`.
5. Commit and push the changes.
6. Wait for GitHub Pages to redeploy.

## Troubleshooting

- If the root Pages URL shows a directory listing or a blank page, confirm `docs/index.html` exists on the published branch and that Pages is using the `/docs` folder.
- If CSS or JavaScript does not load, confirm the site is opened from the Pages URL or served with a local HTTP server rather than opened as a `file://` URL.
- If the CI/CD maturity page cannot load mocked Jenkins data, confirm `docs/webapp/jenkins-build-catalog.json` is present and the browser is serving the page over HTTP.
- If Pages runs Jekyll unexpectedly, keep `docs/.nojekyll` in place so GitHub serves the static files as-is.
