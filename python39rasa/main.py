import random
import firebase_admin
import json
import language_tool_python

from firebase_admin import firestore
from datetime import datetime

documentID = random.randint(10000000, 99999999)
UID = 31907214
    #random.randint(10000000, 99999999)

cred_obj = firebase_admin.credentials.Certificate("resq-rasachatbot-firebase-adminsdk-uxb51-131fdcdccc.json")
default_app = firebase_admin.initialize_app(cred_obj)
db = firestore.client()

doc_ref = db.collection(u'measurement_test').document(str(documentID))
collection = db.collection(u'measurement_test')
docs = collection.stream()

print(docs)
'''doc_ref.set({
    u'diabp': [0],
    u'sysbp': [0],
    u'weight': [0],
    u'index': [0],
    u'UID': str(UID)
})'''

firebase_admin.delete_app(default_app)