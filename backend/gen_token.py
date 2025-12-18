from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "local_dev_secret"
ALGORITHM = "HS256"

access_token_expires = timedelta(minutes=100000)
expire = datetime.utcnow() + access_token_expires
to_encode = {"sub": "1", "exp": expire}
encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
print(encoded_jwt)
