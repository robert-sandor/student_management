# Define the application directory
import os

# Statement for enabling the development environment
DEBUG = True

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example

USERNAME = 'rmoctqhqiwmhtt'
PASSWORD = 'rEpdEgINldp49c7FAAjFp1sGxI'
SERVER   = 'ec2-54-217-202-109.eu-west-1.compute.amazonaws.com'
DATABASE = 'dccjnekvon43ce'
SQLALCHEMY_DATABASE_URI = 'postgresql://' + USERNAME + ':' + PASSWORD + '@' + SERVER + '/' + DATABASE
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
