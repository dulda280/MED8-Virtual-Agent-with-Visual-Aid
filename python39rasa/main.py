import random
import firebase_admin
import json
import language_tool_python

from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate("resq-rasachatbot-firebase-adminsdk-uxb51-8aa0ff5053.json")
default_app = firebase_admin.initialize_app(cred_obj, {
    "databaseURL": "https://resq-rasachatbot-default-rtdb.europe-west1.firebasedatabase.app/"
})

UID = 54976352

# when a user updates the measurements
ref = db.reference("/measurement Table")

dict = ref.get()

newEntry = {
  'diabp': [0],
  'sysbp': [0],
  'weight': [0]
}

dict[str(UID)] = newEntry

ref.set(dict)
firebase_admin.delete_app(default_app)
print(dict)