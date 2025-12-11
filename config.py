class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///prod.db"
    SECRET_KEY = "48942044def27ab59c4887336346eeec"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"