# Frame & Field — Django blog

A full-featured blog about cinema, sport and culture: articles, categories, tags,
comments, authors, authentication, DRF API, tests and Cloudflare Turnstile protection.

## Run locally

```bash
python -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/python manage.py migrate
venv/bin/python manage.py seed_demo
venv/bin/python manage.py runserver
```

Open http://127.0.0.1:8000/ . Admin panel: http://127.0.0.1:8000/admin/ .
API root: http://127.0.0.1:8000/api/ .

Demo users (password `demo12345`): `aisha`, `mia`, `omar`, `leo`.
Create a superuser with `venv/bin/python manage.py createsuperuser` if needed.

## Tests

```bash
venv/bin/python -m pytest -q
```

## Human verification

All user forms use the `dj-turnstile` package (Cloudflare Turnstile). Out of the box
`TURNSTILE_TESTING=True` uses Cloudflare's public dummy keys, so every challenge passes.
For production, set real keys in the environment:

```bash
export TURNSTILE_SITEKEY="your-site-key"
export TURNSTILE_SECRET="your-secret-key"
```
