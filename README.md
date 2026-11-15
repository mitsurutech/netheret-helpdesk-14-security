# Netheret help desk, step 13: accessibility

A teaching example. Over sixteen steps we build a help desk web app for
Netheret, a made-up company that supports the IT of small businesses. This
step adds per-user accessibility settings, larger text and high contrast,
and friendlier error pages.

## What this step adds

- `helpdesk/settings.py` and `templates/settings.html`: a Settings page where
  each person chooses a text size (normal, large, larger) and high contrast.
  The choices are saved in the `text_size` and `high_contrast` columns of
  their `User` row, so they follow them to any computer.
- `base.html` turns the settings into classes on `<html>`, for example
  `class="text-larger high-contrast"`.
- `style.css`:
  - `html.text-large` and `html.text-larger` raise the root font size, and
    because every size is in `rem` the whole page grows;
  - `html.high-contrast` changes the colour variables to white and yellow on
    black, and fixes the few places that needed more than that;
  - the bar charts read their colour from `--chart-bar`, so they change too.
- Messages after an action have `role="status"`, so screen readers read them.
- Plain-words pages for "403 Forbidden" and "404 Not found", with a way back.

Already there from earlier steps: the skip link, landmarks, a visible focus
ring, a label for every field, error summaries linked to their fields, and
tables with captions and headers.

## Run it

```
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py
flask --app helpdesk run --debug
```

Sign in with any demo account (demo password `password123`), open Settings,
choose "Larger" and high contrast, then visit Reports or Jobs. Try using the
whole app with only the keyboard.

## What to look at

- How changing a few CSS variables recolours the whole site.
- `fieldset` and `legend` around the radio buttons: a screen reader says
  "Text size" before reading each choice.
- Colour is never the only clue: badges carry words, cancelled jobs are
  struck through and today's column says "(today)".

<!-- links -->
