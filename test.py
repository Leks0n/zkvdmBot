from urllib.parse import urlparse
from config import DATABASE_URL

u = urlparse(DATABASE_URL)

print(u)