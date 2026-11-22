# Centre d'assistance Netheret, étape 14 : sécurité et droit

[English](README.md) | [Français](README.fr.md) | [Español](README.es.md) | [日本語](README.ja.md) | [Deutsch](README.de.md)

Un exemple pour enseigner. En seize étapes, nous construisons une application web de centre d'assistance pour Netheret, une entreprise imaginaire qui s'occupe de l'informatique de petites entreprises. Cette étape ajoute une protection contre la falsification de requête intersite (CSRF), des cookies plus sûrs et des en-têtes de sécurité, ainsi qu'un avis de confidentialité pour le UK GDPR.

## Ce que cette étape ajoute

- `helpdesk/security.py` :
  - un jeton CSRF écrit à la main : une valeur aléatoire gardée dans la session et
    placée dans un champ caché de chaque formulaire POST ; `check_csrf` s'exécute avant chaque
    requête et répond « 400 Bad Request » à un POST sans le bon jeton ;
  - des en-têtes de sécurité sur chaque réponse : une Content Security Policy qui n'autorise
    que nos propres scripts et styles, pas d'affichage dans un cadre, pas de devinette du type.
- Le cookie de session est `HttpOnly` et `SameSite=Lax`, et `Secure` quand vous
  définissez `SESSION_COOKIE_SECURE=1` sur un serveur en HTTPS.
- `/privacy` : un avis de confidentialité en mots simples, lié depuis chaque page.
- Une page en mots simples pour « 400 Bad Request ».

## La sécurité jusqu'ici, en une liste

| Risque | Ce que fait l'application | Où |
|------|-------------------|-------|
| Mots de passe volés | Seuls des hachages salés sont enregistrés | `models.py` (`set_password`) |
| Deviner qui a un compte | Un seul message pour toute connexion échouée | `auth.py` |
| Fixation de session | `session.clear()` à la connexion | `auth.py` |
| Cookie de session falsifié | Signé avec une clé secrète tirée de l'environnement | `__init__.py` |
| Voir les données d'autres entreprises | Chaque requête d'un client est limitée à son entreprise | `customer.py`, `tickets.py` |
| Faire ce que votre rôle ne permet pas | `@role_required` et des vérifications dans chaque action | `auth.py`, `jobs.py`, `tickets.py` |
| Cross-site scripting (XSS) | Jinja échappe tout ; pas de `|safe` ; CSP | gabarits, `security.py` |
| Injection SQL | Requêtes SQLAlchemy avec paramètres, jamais de chaînes assemblées | partout |
| Falsification de requête intersite | Jeton CSRF écrit à la main sur chaque formulaire POST | `security.py` |
| Clickjacking | `X-Frame-Options` et `frame-ancestors` | `security.py` |

Les lois concernées : le UK GDPR et le Data Protection Act 2018 (les données personnelles,
l'avis de confidentialité, ne garder que le nécessaire), le Computer Misuse Act 1990
(pourquoi le contrôle d'accès compte) et l'Equality Act 2010 (pourquoi l'accessibilité n'est
pas facultative).

## Lancer l'application

```
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py
flask --app helpdesk run --debug
```

Connectez-vous avec n'importe quel compte de démonstration (mot de passe de démonstration `password123`). Affichez le code
source de n'importe quel formulaire pour voir le champ caché `csrf_token`. Pour voir la vérification
fonctionner, ouvrez les outils de développement de votre navigateur, supprimez le champ caché d'un formulaire
et envoyez-le : vous obtenez la page « That did not work ».

## À regarder

- `secrets.token_hex` fabrique le jeton : le module `secrets` est fait pour les valeurs qui
  doivent être difficiles à deviner, contrairement à `random`.
- `secrets.compare_digest` compare les jetons de façon sûre.
- `app.before_request` et `app.after_request` exécutent du code autour de chaque requête
  sans modifier chaque page.

## Apprendre cette étape

Voici l'étape 14 sur 16 de **Task 2. Developing the solution**, une série gratuite de leçons de T Level Digital Software Development, en anglais, qui construit le centre d'assistance Netheret en sprints agiles avec Python et Flask. Lisez la leçon de cette étape :
[La sécurité et la loi](https://mitsurutech.co.uk/resources/t-level/dsd-t2-14-security).

- Étape précédente : [étape 13, les réglages d'accessibilité](https://github.com/mitsurutech/netheret-helpdesk-13-accessibility)
- Étape suivante : [étape 15, tester à la main et le journal de tests](https://github.com/mitsurutech/netheret-helpdesk-15-test-log)
- [Toutes les leçons gratuites de T Level Digital](https://mitsurutech.co.uk/resources/t-level)
- [Enseigner ces leçons à votre classe sur MitsuruTech](https://mitsurutech.co.uk/fr/learning), [voir les tarifs](https://mitsurutech.co.uk/fr/pricing) ou
  [commencer une année gratuite pour votre établissement](https://mitsurutech.co.uk/fr/signup)

## À propos

Écrit par [Mitsuru Technologies](https://mitsurutech.co.uk/fr) (MitsuruTech) comme exemple pédagogique pour le T Level Digital
Software Development. Le cahier des charges Netheret IT Support Solutions provient du matériel d'évaluation type de Pearson ; ce code
et ses notes sont les nôtres, et ne sont ni publiés, ni soutenus, ni approuvés par Pearson ou le Department for Education.
« T Level » est une marque déposée du Department for Education.
