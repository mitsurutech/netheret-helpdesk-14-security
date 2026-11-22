# Netheret-Helpdesk, Schritt 14: Sicherheit und Recht

[English](README.md) | [Français](README.fr.md) | [Español](README.es.md) | [日本語](README.ja.md) | [Deutsch](README.de.md)

Ein Beispiel für den Unterricht. In sechzehn Schritten bauen wir eine Helpdesk-Webanwendung für Netheret, ein erfundenes Unternehmen, das die IT kleiner Firmen betreut. Dieser Schritt fügt Schutz vor Cross-Site Request Forgery (CSRF), sicherere Cookies und Sicherheits-Header sowie einen Datenschutzhinweis nach UK GDPR hinzu.

## Was dieser Schritt hinzufügt

- `helpdesk/security.py`:
  - ein von Hand geschriebenes CSRF-Token: ein Zufallswert, der in der Sitzung liegt und
    in einem versteckten Feld jedes POST-Formulars steht; `check_csrf` läuft vor jeder
    Anfrage und antwortet auf einen POST ohne das richtige Token mit „400 Bad Request“;
  - Sicherheits-Header auf jeder Antwort: eine Content Security Policy, die nur
    unsere eigenen Skripte und Styles erlaubt, keine Einbettung in Frames, kein Erraten des Typs.
- Das Sitzungscookie ist `HttpOnly` und `SameSite=Lax`, und `Secure`, wenn Sie
  auf einem Server mit HTTPS `SESSION_COOKIE_SECURE=1` setzen.
- `/privacy`: ein Datenschutzhinweis in einfachen Worten, von jeder Seite aus verlinkt.
- Eine Seite in einfachen Worten für „400 Bad Request“.

## Die Sicherheit bis hierher, in einer Liste

| Risiko | Was die Anwendung tut | Wo |
|------|-------------------|-------|
| Gestohlene Passwörter | Nur gesalzene Hashes werden gespeichert | `models.py` (`set_password`) |
| Erraten, wer ein Konto hat | Eine einzige Meldung für jede fehlgeschlagene Anmeldung | `auth.py` |
| Session Fixation | `session.clear()` bei der Anmeldung | `auth.py` |
| Manipuliertes Sitzungscookie | Signiert mit einem geheimen Schlüssel aus der Umgebung | `__init__.py` |
| Daten anderer Firmen sehen | Jede Abfrage eines Kunden ist auf seine Firma beschränkt | `customer.py`, `tickets.py` |
| Dinge tun, die die eigene Rolle nicht darf | `@role_required` und Prüfungen in jeder Aktion | `auth.py`, `jobs.py`, `tickets.py` |
| Cross-Site-Scripting (XSS) | Jinja maskiert alles; kein `|safe`; CSP | Vorlagen, `security.py` |
| SQL-Injection | SQLAlchemy-Abfragen mit Parametern, nie zusammengesetzte Zeichenketten | überall |
| Cross-Site Request Forgery | Von Hand geschriebenes CSRF-Token in jedem POST-Formular | `security.py` |
| Clickjacking | `X-Frame-Options` und `frame-ancestors` | `security.py` |

Die berührten Gesetze: UK GDPR und der Data Protection Act 2018 (personenbezogene Daten,
der Datenschutzhinweis, nur das Nötige aufbewahren), der Computer Misuse Act 1990
(warum Zugriffskontrolle wichtig ist) und der Equality Act 2010 (warum Barrierefreiheit nicht
optional ist).

## Starten

```
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py
flask --app helpdesk run --debug
```

Melden Sie sich mit einem beliebigen Demo-Konto an (Demo-Passwort `password123`). Sehen Sie sich den Seitenquelltext
eines beliebigen Formulars an, um das versteckte Feld `csrf_token` zu sehen. Um die Prüfung
in Aktion zu sehen, öffnen Sie die Entwicklerwerkzeuge Ihres Browsers, löschen Sie das versteckte Feld aus einem Formular
und senden Sie es ab: Sie erhalten die Seite „That did not work“.

## Worauf Sie achten sollten

- `secrets.token_hex` erzeugt das Token: Das Modul `secrets` ist für Werte gedacht, die
  schwer zu erraten sein müssen, anders als `random`.
- `secrets.compare_digest` vergleicht die Tokens auf sichere Weise.
- `app.before_request` und `app.after_request` führen Code rund um jede Anfrage aus,
  ohne jede Seite zu ändern.

## Diesen Schritt lernen

Dies ist Schritt 14 von 16 aus **Task 2. Developing the solution**, einer kostenlosen Reihe von Lektionen zu T Level Digital Software Development auf Englisch, die den Helpdesk von Netheret in agilen Sprints mit Python und Flask baut. Lesen Sie die Lektion zu diesem Schritt:
[Sicherheit und das Recht](https://mitsurutech.co.uk/resources/t-level/dsd-t2-14-security).

- Vorheriger Schritt: [Schritt 13, Einstellungen zur Barrierefreiheit](https://github.com/mitsurutech/netheret-helpdesk-13-accessibility)
- Nächster Schritt: [Schritt 15, Testen von Hand und das Testprotokoll](https://github.com/mitsurutech/netheret-helpdesk-15-test-log)
- [Alle kostenlosen Lektionen zu T Level Digital](https://mitsurutech.co.uk/resources/t-level)
- [Diese Lektionen mit Ihrer Klasse auf MitsuruTech unterrichten](https://mitsurutech.co.uk/de/learning), [die Preise ansehen](https://mitsurutech.co.uk/de/pricing) oder
  [ein kostenloses Jahr für Ihre Schule beginnen](https://mitsurutech.co.uk/de/signup)

## Über dieses Beispiel

Geschrieben von [Mitsuru Technologies](https://mitsurutech.co.uk/de) (MitsuruTech) als Unterrichtsbeispiel für T Level Digital
Software Development. Die Aufgabenstellung Netheret IT Support Solutions stammt aus dem Muster-Prüfungsmaterial von Pearson; dieser Code
und seine Erläuterungen sind unsere eigenen und werden weder von Pearson noch vom Department for Education veröffentlicht, unterstützt oder genehmigt.
„T Level“ ist eine eingetragene Marke des Department for Education.
