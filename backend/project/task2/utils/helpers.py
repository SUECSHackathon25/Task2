
from os import getenv

def evalute_env_bool(key: str, default: str = 'False') -> bool:
    return getenv(key=key, default=default).lower() in ('true', '1', 't')