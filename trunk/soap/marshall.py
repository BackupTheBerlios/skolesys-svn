import pickle
import base64

def pdump(obj):
    return pickle.dumps(obj)

def pload(obj):
    return pickle.loads(obj)
