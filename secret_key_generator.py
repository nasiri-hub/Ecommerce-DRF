from django.utils.crypto import get_random_string
from pprint import pprint
import secrets

pprint(get_random_string(length=100))
# Choose one of these.
print(secrets.token_urlsafe(100))
