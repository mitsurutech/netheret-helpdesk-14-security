# Netheret help desk, step 14: security and law

A teaching example. Over sixteen steps we build a help desk web app for
Netheret, a made-up company that supports the IT of small businesses. This
step adds protection against cross-site request forgery (CSRF), safer
cookies and security headers, and a privacy notice for UK GDPR.

## What this step adds

- `helpdesk/security.py`:
  - a CSRF token written by hand: a random value kept in the session and
    put in a hidden field in every POST form; `check_csrf` runs before every
    request and answers "400 Bad Request" to a POST without the right token;
  - security headers on every response: a Content Security Policy that only
    allows our own scripts and styles, no framing, no type guessing.
- The session cookie is `HttpOnly` and `SameSite=Lax`, and `Secure` when you
  set `SESSION_COOKIE_SECURE=1` on a server with HTTPS.
- `/privacy`: a privacy notice in plain words, linked from every page.
- A plain-words page for "400 Bad Request".

## Security so far, in one list

| Risk | What the app does | Where |
|------|-------------------|-------|
| Stolen passwords | Only salted hashes are stored | `models.py` (`set_password`) |
| Guessing who has an account | One message for any failed sign in | `auth.py` |
| Session fixation | `session.clear()` when signing in | `auth.py` |
| Tampered session cookie | Signed with a secret key from the environment | `__init__.py` |
| Seeing other companies' data | Every customer query is limited to their company | `customer.py`, `tickets.py` |
| Doing things your role should not | `@role_required` and checks in each action | `auth.py`, `jobs.py`, `tickets.py` |
| Cross-site scripting (XSS) | Jinja escapes everything; no `|safe`; CSP | templates, `security.py` |
| SQL injection | SQLAlchemy queries with parameters, never string building | everywhere |
| Cross-site request forgery | Hand-written CSRF token on every POST form | `security.py` |
| Clickjacking | `X-Frame-Options` and `frame-ancestors` | `security.py` |

The law this touches: UK GDPR and the Data Protection Act 2018 (personal data,
the privacy notice, keeping only what is needed), the Computer Misuse Act 1990
(why access control matters) and the Equality Act 2010 (why accessibility is
not optional).

## Run it

```
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py
flask --app helpdesk run --debug
```

Sign in with any demo account (demo password `password123`). View the page
source of any form to see the hidden `csrf_token` field. To see the check
work, open your browser's developer tools, delete the hidden field from a form
and submit it: you get the "That did not work" page.

## What to look at

- `secrets.token_hex` makes the token: the `secrets` module is for values that
  must be hard to guess, unlike `random`.
- `secrets.compare_digest` compares the tokens safely.
- `app.before_request` and `app.after_request` run code around every request
  without changing each page.

<!-- links -->
