from datetime import datetime
import uuid

def new_uuid():
    return str(uuid.uuid4())

def now():
    return datetime.utcnow().isoformat()
