class Config:
    SECRET_KEY = 'this-is-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///info.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwt-secret-key'