# personal-dashboard

- `index.html` &mdash; the published dashboard (skeleton; under construction).
- `contents/docs/dashboard.html` &mdash; spec viewer that fetches and renders `contents/docs/plans/dashboard.yaml`. Must be served over HTTP (e.g. `python -m http.server` from `数字项目 Digital Projects/`); will not work via `file://` in Chrome.
- `contents/docs/plans/dashboard.yaml` &mdash; the spec data driving the viewer above.
