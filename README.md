# Flask on Docker

[![Build (development)](https://github.com/christopher-kim14/flask-on-docker/actions/workflows/build.yml/badge.svg)](https://github.com/christopher-kim14/flask-on-docker/actions/workflows/build.yml)

## Overview

This repo runs a small Flask web application as a set of Docker containers, using a stack modeled on the one Instagram is built on. In development, Docker Compose starts the Flask development server alongside a PostgreSQL database. In production, the app is served by Gunicorn, a production-grade WSGI server, behind an Nginx reverse proxy that also serves static files and user-uploaded media directly, without passing those requests through Python. The app itself exposes a JSON health-check endpoint, a page for uploading images, and routes for viewing static and uploaded files, and the entire stack can be started on any machine with Docker using a single command.

![Demo: opening the site, uploading an image, and viewing it](demo.gif)

## Build instructions

You need [Docker](https://docs.docker.com/get-docker/) with the Compose plugin (`docker compose`). Start by cloning the repo:

```bash
git clone https://github.com/christopher-kim14/flask-on-docker.git
cd flask-on-docker
```

### Development

Development uses Flask's built-in server with live code reloading, and creates the database tables automatically on startup.

```bash
docker compose up -d --build
```

The app is then available at <http://localhost:5002>. To add a sample user to the database, run:

```bash
docker compose exec web python manage.py seed_db
```

To stop the services and delete the development database:

```bash
docker compose down -v
```

### Production

Production database credentials are kept out of the repo, so you need to create them first. In the project root, create a file named `.env.prod.db` containing:

```
POSTGRES_USER=hello_flask
POSTGRES_PASSWORD=change_me
POSTGRES_DB=hello_flask_prod
```

Replace `change_me` with a password of your own. Then build and start the services, and create the database tables:

```bash
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec web python manage.py create_db
```

The app is then available through Nginx at <http://localhost:1337>. To stop the services:

```bash
docker compose -f docker-compose.prod.yml down
```

Add `-v` to that command to also delete the production database and uploaded files.

### Using the app

| URL | What it does |
| --- | --- |
| `/` | Returns `{"hello": "world"}` to confirm the app is running |
| `/upload` | Form for uploading a file (the page reloads after a successful upload) |
| `/media/<filename>` | Displays an uploaded file, e.g. `/media/cat.jpg` |

Replace `localhost:5002` or `localhost:1337` with whichever environment you're running. Uploaded filenames are sanitized, so spaces become underscores (`my photo.jpg` becomes `my_photo.jpg`).

If Docker is running on a remote server, forward the ports over SSH so your local browser can reach them:

```bash
ssh -L 5002:localhost:5002 -L 1337:localhost:1337 user@your-server
```
