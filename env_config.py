import os


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'
    ##### Flask-Mail configurations #####
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'hold@hold.com'
    MAIL_PASSWORD = "hold"
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    #### MONGO DB configurations #####
    MONGO_SERVER = "10.38.225.212"
    MONGO_PORT = "27017"
    MONGO_DBNAME_1 = "hcsdb"
    MONGO_DBNAME_2 = "cbtdb"
    MONGO_URI = ("mongodb://{0}:{1}".format(MONGO_SERVER, MONGO_PORT))
    #### JWT configurations #####
    JWT_SECRET_KEY = "my-super-secret-key"
    JWT_BLACKLIST_ENABLED = False
    # JWT_BLACKLIST_TOKEN_CHECKS = ("access", "refresh")
    #### FLASK CORS configurations #####
    CORS_HEADERS = 'Content-Type'


class DevelopementConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):

    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False