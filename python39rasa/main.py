import random
import firebase_admin
import json
import language_tool_python

from firebase_admin import firestore
from datetime import datetime

UID = 87643197

cred_obj = firebase_admin.credentials.Certificate("resq-rasachatbot-firebase-adminsdk-uxb51-131fdcdccc.json")
default_app = firebase_admin.initialize_app(cred_obj)
db = firestore.client()

doc_ref = db.collection('measurement_test').document(str(UID))
doc = doc_ref.get()
msg = ""
if doc.exists:
    msg = "Hej. Har du nogle målinger til mig i dag?"
    #return [SlotSet("init_setup", False)]

else:
    doc_ref = db.collection(u'measurement_test').document(str(UID))
    doc_ref.set({
        u'diabp': [0],
        u'sysbp': [0],
        u'weight': [0],
        u'index': [0],
        u'UID': str(UID),
        u'PROMbool': 0
    })
    msg = f"Hej og velkommen til. Jeg er Vera, din personlige assistent. \n" \
          f"Jeg vil hjælpe dig med dagligt at holde øje med dit blodtryk og din vægt. En gang imellem har jeg også et kort spørgeskema til dig, som kan hjælpe sundhedspersonale med at få indsigt i dit mentale helbred. \n" \
          f"Først vil jeg gerne vide om der er en ting du gør hver dag, som er en del af en rutine eller lignende, hvor du har tid til også at veje dig og måle dit blodtryk. Det kunne fx være inden du går i seng eller efter du har børstet tænder."
    #return [SlotSet("init_setup", True)]

firebase_admin.delete_app(default_app)
print(msg)