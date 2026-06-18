from mongoengine import connect
import os
from dotenv import load_dotenv

load_dotenv()

host = os.environ.get('DATABASE_URL')

connect(
    db="anonymous_messenger",
    host=host
)
