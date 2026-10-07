import os


basedir = os.path.abspath(os.path.dirname(__file__))


def get_database_url():
    # Development sets DATABASE_URL directly in .env.dev.
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    # Production builds it from the values in .env.prod.db,
    # so the password never appears in a committed file.
    user = os.getenv("POSTGRES_USER")
    if user:
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("SQL_HOST", "db")
        port = os.getenv("SQL_PORT", "5432")
        name = os.getenv("POSTGRES_DB")
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"

    return "sqlite://"


class Config(object):
    SQLALCHEMY_DATABASE_URI = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static"
    MEDIA_FOLDER = f"{os.getenv('APP_FOLDER')}/project/media"
