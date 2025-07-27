import os

REDMINE_URL = os.getenv('REDMINE_URL')
REDMINE_KEY = os.getenv('REDMINE_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
CHROMA_HOST = os.getenv('CHROMA_HOST')

os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY