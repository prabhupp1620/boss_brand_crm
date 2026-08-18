# Boss Brand CRM — Admin Panel

Flask admin panel for the Boss Brand B2B website. Authentication, user management
and a dashboard shell, backed by the local MySQL `boss_brand` database.

## Run it

```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

./venv/bin/python -m flask --app run.py seed   # creates tables + bootstrap admin
./venv/bin/python run.py                       # http://127.0.0.1:5000
```

**Test login** (from `.env`, shown on the login page until real onboarding exists):

| Email | Password |
| --- | --- |
| `admin@bossbrand.ai` | `Admin@123` |

## Layout

```
run.py                     app entry point
app/
  __init__.py              application factory
  config.py                env-driven config (reads .env)
  extensions.py            db, login manager, csrf, migrate
  models.py                User model -> `users` table
  forms.py                 WTForms (login, user, profile, password)
  cli.py                   `flask init-db`, `flask seed`
  blueprints/
    auth.py                /login, /logout
    dashboard.py           /
    users.py               /users  (list, create, edit, enable/disable, delete)
    profile.py             /profile (details + password change)
  templates/               Jinja templates (layout.html is the admin shell)
  static/css/app.css       design system — tokens, components, dark mode
  static/js/app.js         theme toggle, mobile nav, flash, confirms
```

## Database

Connection comes from `.env` (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`)
and is assembled into a `mysql+pymysql://` URI in `app/config.py`.

`users` table:

| Column | Type | Notes |
| --- | --- | --- |
| id | int PK | auto increment |
| name | varchar(120) | |
| email | varchar(190) | unique, indexed |
| password_hash | varchar(255) | werkzeug PBKDF2 hash |
| phone | varchar(30) | nullable |
| role | varchar(30) | `admin` \| `manager` \| `staff` |
| is_active | bool | inactive users cannot sign in |
| last_login_at | datetime | stamped on each successful login |
| created_at / updated_at | datetime | |

Schema changes after this point should go through Flask-Migrate:

```bash
./venv/bin/python -m flask --app run.py db init      # once
./venv/bin/python -m flask --app run.py db migrate -m "add leads"
./venv/bin/python -m flask --app run.py db upgrade
```

## Notes

- CSRF protection is on for every POST (Flask-WTF).
- Passwords are hashed; the plaintext test password only lives in `.env`.
- Sidebar entries marked *Soon* (Leads, Companies, Orders, Enquiries, Settings)
  are placeholders — add a blueprint + model per module and drop the `is-soon` class.
- Before deploying: set a real `SECRET_KEY`, remove the credentials hint block in
  `templates/auth/login.html`, and run behind gunicorn/uwsgi instead of `run.py`.
