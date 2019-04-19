import os

from dotenv import load_dotenv

load_dotenv()
DOMAIN_NAME = os.getenv('MAIL_GUN_DOMAIN_NAME')
PASSWORD = os.getenv('MAIL_GUN_DOMAIN_PASSWORD')
