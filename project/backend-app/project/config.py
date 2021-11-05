import os

class Config(object):

    SQLALCHEMY_DATABASE_URI='postgresql://{}:{}@{}:5432/{}'.format(
        os.getenv("POSTGRES_USER"),
        os.getenv("POSTGRES_PASSWORD"),
        os.getenv("DB_SERVICE"),
        os.getenv("POSTGRES_DB")
    )
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 100
    RABBITMQ_URI = os.getenv("RABBITMQ_URI")
    NATS_URI = os.getenv("NATS_URI")