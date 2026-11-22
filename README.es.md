# Servicio de asistencia de Netheret, paso 14: seguridad y ley

[English](README.md) | [Français](README.fr.md) | [Español](README.es.md) | [日本語](README.ja.md) | [Deutsch](README.de.md)

Un ejemplo para enseñar. En dieciséis pasos construimos una aplicación web de servicio de asistencia para Netheret, una empresa inventada que da soporte informático a pequeñas empresas. Este paso añade protección contra la falsificación de peticiones entre sitios (CSRF), cookies más seguras y cabeceras de seguridad, y un aviso de privacidad para el UK GDPR.

## Qué añade este paso

- `helpdesk/security.py`:
  - un token CSRF escrito a mano: un valor aleatorio guardado en la sesión y
    puesto en un campo oculto de cada formulario POST; `check_csrf` se ejecuta antes de cada
    petición y responde "400 Bad Request" a un POST sin el token correcto;
  - cabeceras de seguridad en cada respuesta: una Content Security Policy que solo
    permite nuestros propios scripts y estilos, nada de marcos y nada de adivinar el tipo.
- La cookie de sesión es `HttpOnly` y `SameSite=Lax`, y `Secure` cuando
  pones `SESSION_COOKIE_SECURE=1` en un servidor con HTTPS.
- `/privacy`: un aviso de privacidad con palabras sencillas, enlazado desde todas las páginas.
- Una página con palabras sencillas para "400 Bad Request".

## La seguridad hasta ahora, en una lista

| Riesgo | Qué hace la aplicación | Dónde |
|------|-------------------|-------|
| Contraseñas robadas | Solo se guardan hashes con sal | `models.py` (`set_password`) |
| Adivinar quién tiene cuenta | Un solo mensaje para cualquier inicio de sesión fallido | `auth.py` |
| Fijación de sesión | `session.clear()` al iniciar sesión | `auth.py` |
| Cookie de sesión manipulada | Firmada con una clave secreta del entorno | `__init__.py` |
| Ver datos de otras empresas | Cada consulta de un cliente se limita a su empresa | `customer.py`, `tickets.py` |
| Hacer lo que tu rol no permite | `@role_required` y comprobaciones en cada acción | `auth.py`, `jobs.py`, `tickets.py` |
| Cross-site scripting (XSS) | Jinja escapa todo; sin `|safe`; CSP | plantillas, `security.py` |
| Inyección SQL | Consultas de SQLAlchemy con parámetros, nunca juntando cadenas | en todas partes |
| Falsificación de peticiones entre sitios | Token CSRF escrito a mano en cada formulario POST | `security.py` |
| Clickjacking | `X-Frame-Options` y `frame-ancestors` | `security.py` |

Las leyes que entran en juego: el UK GDPR y la Data Protection Act 2018 (datos personales,
el aviso de privacidad, guardar solo lo necesario), la Computer Misuse Act 1990
(por qué importa el control de acceso) y la Equality Act 2010 (por qué la accesibilidad no es
opcional).

## Ejecútalo

```
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py
flask --app helpdesk run --debug
```

Inicia sesión con cualquier cuenta de demostración (contraseña de demostración `password123`). Mira el código
fuente de cualquier formulario para ver el campo oculto `csrf_token`. Para ver la comprobación
en acción, abre las herramientas para desarrolladores del navegador, borra el campo oculto de un formulario
y envíalo: te sale la página "That did not work".

## En qué fijarse

- `secrets.token_hex` crea el token: el módulo `secrets` sirve para valores que
  tienen que ser difíciles de adivinar, a diferencia de `random`.
- `secrets.compare_digest` compara los tokens de forma segura.
- `app.before_request` y `app.after_request` ejecutan código alrededor de cada petición
  sin cambiar cada página.

## Aprende este paso

Este es el paso 14 de 16 de **Task 2. Developing the solution**, una serie gratuita de lecciones de T Level Digital Software Development, en inglés, que construye el servicio de asistencia de Netheret en sprints ágiles con Python y Flask. Lee la lección de este paso:
[La seguridad y la ley](https://mitsurutech.co.uk/resources/t-level/dsd-t2-14-security).

- Paso anterior: [paso 13, ajustes de accesibilidad](https://github.com/mitsurutech/netheret-helpdesk-13-accessibility)
- Paso siguiente: [paso 15, probar a mano y el registro de pruebas](https://github.com/mitsurutech/netheret-helpdesk-15-test-log)
- [Todas las lecciones gratuitas de T Level Digital](https://mitsurutech.co.uk/resources/t-level)
- [Enseña estas lecciones a tu clase en MitsuruTech](https://mitsurutech.co.uk/es/learning), [mira los precios](https://mitsurutech.co.uk/es/pricing) o
  [empieza un año gratis para tu centro](https://mitsurutech.co.uk/es/signup)

## Acerca de

Escrito por [Mitsuru Technologies](https://mitsurutech.co.uk/es) (MitsuruTech) como ejemplo para enseñar T Level Digital
Software Development. El encargo de Netheret IT Support Solutions procede del material de evaluación de muestra de Pearson; este código
y sus notas son nuestros, y no los publica, respalda ni aprueba Pearson ni el Department for Education.
"T Level" es una marca registrada del Department for Education.
