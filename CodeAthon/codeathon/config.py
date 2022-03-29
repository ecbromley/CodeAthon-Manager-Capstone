import os

class Config:
    SECRET_KEY = os.environ.get('CODEATHON_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('CODEATHON_EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('CODEATHON_EMAIL_PASS')
