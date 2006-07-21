import pickle
import base64

def pdump(obj):
    return base64.b64encode(pickle.dumps(obj))

def pload(obj):
    return pickle.loads(base64.b64decode(obj))
