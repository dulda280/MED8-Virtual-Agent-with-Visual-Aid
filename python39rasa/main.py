import random
import firebase_admin
import json

from firebase_admin import db


data = "blood_pressure"
input = 256

cred_obj = firebase_admin.credentials.Certificate("resq-rasachatbot-firebase-adminsdk-uxb51-8aa0ff5053.json")
default_app = firebase_admin.initialize_app(cred_obj, {
    "databaseURL": "https://resq-rasachatbot-default-rtdb.europe-west1.firebasedatabase.app/"
})

randNum = 75146875

'''
#To create a new table
ref = db.reference("/")
ref.set({
    "table name": "measurement Table"
})
ref = db.reference("/measurement Table")
ref.set({
    randNum:{
        "blood pressure": [0],
        "weight": [0]
    }
})

#When a new user is created
ref = db.reference("/measurement Table")

dict = ref.get()
print(dict)
dict[randNum] = {
    "blood pressure": [0],
    "weight": [0]
}
ref.set(dict)
'''

#when a user updates the measurements
ref = db.reference("/measurement Table/" + str(randNum))

dict = ref.get()
print(dict)

for key, value in dict.items():
    value.append(154)

ref.set(dict)