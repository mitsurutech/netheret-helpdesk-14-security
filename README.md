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

## Learn this step

This is step 14 of 16 of **Task 2. Developing the solution**, a free series of T Level Digital Software Development
lessons that builds the Netheret help desk in agile sprints with Python and Flask. Read the lesson for this step:
[Security and the law](https://mitsurutech.co.uk/resources/t-level/dsd-t2-14-security).

- Previous step: [step 13, accessibility settings](https://github.com/mitsurutech/netheret-helpdesk-13-accessibility)
- Next step: [step 15, testing by hand and the test log](https://github.com/mitsurutech/netheret-helpdesk-15-test-log)
- [Every free T Level Digital lesson](https://mitsurutech.co.uk/resources/t-level)
- [Teach these lessons to your class on MitsuruTech](https://mitsurutech.co.uk/learning), [see the pricing](https://mitsurutech.co.uk/pricing) or
  [start a free year for your college](https://mitsurutech.co.uk/signup)

## About

Written by [Mitsuru Technologies](https://mitsurutech.co.uk) (MitsuruTech) as a teaching example for T Level Digital
Software Development. The Netheret IT Support Solutions brief is from Pearson's sample assessment material; this code
and its notes are our own, and are not published, endorsed or approved by Pearson or the Department for Education.
'T Level' is a registered trade mark of the Department for Education.

