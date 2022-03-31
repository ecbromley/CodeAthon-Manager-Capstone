import os
import json

with open('/etc/codeathon_config.json') as config_file:
    config = json.load(config_file)
class Config:
    SECRET_KEY = config.get('CODEATHON_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config.get('CODEATHON_SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = config.get('CODEATHON_MAIL_SERVER')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get('CODEATHON_EMAIL_USER')
    MAIL_PASSWORD = config.get('CODEATHON_EMAIL_PASS')
