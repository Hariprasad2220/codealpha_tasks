# Qynera

**Spark conversations, not just posts.**

A mini social media web app built with **Django** (backend) and **HTML/CSS/JavaScript**
(frontend) — submitted for CodeAlpha Internship, Task 2 (Social Media Platform).

Qynera lets people build a profile, post updates, react to what others share, and follow
the accounts they care about — the core loop behind every social platform, distilled into
a clean, hackable Django project.

## Features
- User registration & login (Django auth)
- User profiles with bio + avatar
- Create posts (text + optional image)
- Comment on posts
- Like / unlike posts (AJAX, no page reload)
- Follow / unfollow users (AJAX, no page reload)
- Feed of all posts, individual profile pages, post detail + comments page
- Admin panel to inspect all data

## Tech stack
- Frontend: HTML, CSS, JavaScript (vanilla, `fetch` API)
- Backend: Django (Python)
- Database: SQLite (default, zero config — swap for Postgres/MySQL if you want)

---

## 1. Setup on Ubuntu

Open a terminal and run:

```bash
# Check Python is installed (Ubuntu ships with Python 3)
python3 --version

# Install pip and venv tools if you don't have them
sudo apt update
sudo apt install python3-pip python3-venv -y
```

Unzip/copy the project, then `cd` into it:

```bash
cd ~/Downloads          # wherever you extracted the project
cd socialapp
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Your prompt should now start with `(venv)`.

Install dependencies:

```bash
pip install -r requirements.txt
```

## 2. Set up the database

```bash
python manage.py makemigrations
python manage.py migrate
```

Create an admin account (used to log into `/admin/` and inspect data):

```bash
python manage.py createsuperuser
```
Follow the prompts (username, email, password).

## 3. Run the server

```bash
python manage.py runserver
```

Open your browser at:
```
http://127.0.0.1:8000/
```

You'll be redirected to login — click **Register** to create your first account.
Open a second browser (or an incognito window) and register a second account so you
can test following, liking, and commenting between two users.

Admin panel: `http://127.0.0.1:8000/admin/` (log in with the superuser you created).

## 4. Project structure

```
socialapp/
├── manage.py
├── requirements.txt
├── socialapp/            # project settings & URL root
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
└── social/                # the app itself
    ├── models.py          # Profile, Post, Comment, Like, Follow
    ├── views.py            # feed, profile, post detail, like/follow toggles, auth
    ├── forms.py
    ├── urls.py
    ├── admin.py
    ├── signals.py          # auto-creates a Profile whenever a User is created
    ├── templates/
    │   ├── social/         # feed.html, profile.html, post_detail.html, base.html...
    │   └── registration/   # login.html, register.html
    └── static/social/
        ├── css/style.css
        └── js/script.js    # AJAX like/follow logic
```

## 5. Database models (what's being stored)

- **Profile** — extends the built-in `User` with `bio` and `avatar`, one-to-one.
- **Post** — `author`, `content`, optional `image`, `created_at`.
- **Comment** — `post`, `author`, `content`, `created_at`.
- **Like** — `post` + `user` (unique together, so you can't double-like).
- **Follow** — `follower` + `following` (unique together).

## 6. How the AJAX like/follow works
`social/static/social/js/script.js` attaches click handlers to `.like-btn` and
`.follow-btn` elements. On click it `fetch()`s the corresponding Django URL with the
CSRF token, the view toggles the `Like`/`Follow` row in the database, and returns JSON
(`{liked: true/false, like_count: N}` or `{following: true/false, follower_count: N}`)
which JS uses to update the button and counters instantly — no page reload.

## 7. Common issues

- **`ModuleNotFoundError: No module named 'django'`** → you forgot to activate the
  virtualenv (`source venv/bin/activate`) or run `pip install -r requirements.txt`.
- **Images not showing** → make sure `Pillow` installed correctly (`pip show Pillow`);
  it's required for `ImageField`.
- **Port already in use** → run `python manage.py runserver 8001` to use a different port.
- **Static/CSS not loading** → hard-refresh the browser (Ctrl+Shift+R); make sure
  `DEBUG = True` in `settings.py` while developing (it already is by default).

## 8. Suggested submission notes for CodeAlpha
Mention in your submission:
- **Project name:** Qynera — a mini social media platform
- Frontend: HTML/CSS/JS (server-rendered templates + `fetch`-based AJAX for likes/follows)
- Backend: Django
- Database: SQLite, storing users, posts, comments, and followers as required by the task
- All three required features implemented: user profiles, posts & comments, like/follow system
- Branding touch: gradient identity color, "spark" terminology throughout (posting =
  sparking a conversation) to make the submission feel like a designed product rather
  than a bare CRUD app
