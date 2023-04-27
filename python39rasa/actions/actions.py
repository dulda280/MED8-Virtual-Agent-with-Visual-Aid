import random
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

import firebase_admin
from firebase_admin import firestore
from firebase_admin import db
from datetime import datetime

import pandas as pd
import csv
from spellchecker import SpellChecker

class fetchData(Action):

    def name(self) -> Text:
        return "fetchData"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        df = pd.read_csv("TestData.csv")
        data = next(tracker.get_latest_entity_values("data"), None)

        if not data:
            msg = "i didn't understand what you said"
            dispatcher.utter_message(text=msg)
            return []

        df = df[data]

        msg = f"the {data} from yesterday is {df.iloc[-1]}"
        dispatcher.utter_message(text=msg)
        return []

class saveToFB(Action):

    def name(self) -> Text:
        return "saveToFB"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        data = next(tracker.get_latest_entity_values("data"), None)
        input = next(tracker.get_latest_entity_values("input"), None)
        userId = tracker.sender_id

        cred_obj = firebase_admin.credentials.Certificate("resq-rasachatbot-firebase-adminsdk-uxb51-131fdcdccc.json")
        default_app = firebase_admin.initialize_app(cred_obj)
        db = firestore.client()

        doc_ref = db.collection(u'measurement_test').document(str(userId))
        collection = db.collection(u'measurement_test')
        docs = collection.stream()

        spell = SpellChecker()

        text = list(str(data).split(" "))
        # find those words that may be misspelled
        misspelled = spell.unknown(text)

        for index, word in enumerate(text):
            if word in misspelled:
                text[index] = spell.correction(word)

        newtext = ' '.join(text)

        if data == "blodtryk":
            inputList = input.split("/", 2)

            for doc in docs:
                if doc.id == str(userId):
                    sysList = doc.to_dict()["sysbp"]
                    sysList.append(int(inputList[0]))

                    diaList = doc.to_dict()["diabp"]
                    diaList.append(int(inputList[1]))

                    indexList = doc.to_dict()["index"]
                    indexList.append(len(indexList))
                    doc_ref.set({
                        u'diabp': diaList,
                        u'sysbp': sysList,
                        u'weight': doc.to_dict()["weight"],
                        u'index': indexList,
                        u'UID': str(userId)
                    })

        elif data == "vægt":
            for doc in docs:
                if doc.id == str(userId):
                    weightList = doc.to_dict()["weight"]
                    weightList.append(int(input))
                    doc_ref.set({
                        u'diabp': doc.to_dict()["diabp"],
                        u'sysbp': doc.to_dict()["sysbp"],
                        u'weight': weightList,
                        u'index': doc.to_dict()["index"],
                        u'UID': str(userId)
                    })

        else:
            msg = f"Undskyld. Men jeg tror at du kom til at stave forkert. Kan du gentage?"
            firebase_admin.delete_app(default_app)

            dispatcher.utter_message(text=msg)
            return []

        firebase_admin.delete_app(default_app)

        komplimentere = ["Super godt! ", "Fantastisk! ", "Godt klaret! ", "Super duper! "]
        randomindex = random.randint(0, 3)
        msg = f'{komplimentere[randomindex]} Tak for at fortælle mig om {data}. Du skrev {input}.'
        dispatcher.utter_message(text=msg)

        if datetime.today().strftime('%A') == datetime.today().strftime('%A'):
            #"Wednesday":
            return [SlotSet("send_PROM", True)]
        else:
            return [SlotSet("send_PROM", False)]

class EndMeasurements(Action):

    def name(self) -> Text:
        return "EndMeasurements"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        msg = f"Det var det for i dag. Vi snakkes ved i morgen!"
        dispatcher.utter_message(text=msg)
        return []

class saveData(Action):

    def name(self) -> Text:
        return "saveData"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data = next(tracker.get_latest_entity_values("data"), None)
        input = next(tracker.get_latest_entity_values("input"), None)

        df = pd.read_csv("TestData.csv")
        dflen = len(df.index)

        today = datetime.date.today().strftime('%Y-%m-%d')

        if df["day"].iloc[-1] != today:
            df.loc[dflen] = [dflen, today, None, None, None]
            df[data].iloc[-1] = input
        else:
            df[data].iloc[-1] = input

        missingData = []
        for i, value in enumerate(df.iloc[-1]):
            if pd.isna(value):
                missingData.append(df.columns[i])

        msg = f"thank you for telling me about your {data}. Your input was {input}. "
        if len(missingData) > 0:
            msg += "I'm however missing"
            for Data in missingData:
                msg += ", " + Data
        else:
            msg += "I got all the data that i need"

        dispatcher.utter_message(text=msg)
        df.to_csv("TestData.csv", index=False)
        return []

class initiate_promone(Action):

    def name(self) -> Text:
        return "initiate_promone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        msg = f"Are you ready for prom 1?"
        dispatcher.utter_message(text=msg)
        return []

class promoneqone(Action):
    def name(self) -> Text:
        return "promoneqone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        questionList = [["question number", "question text", "answer"],
                    [1, "question 1", ""],
                    [2, "question 2", ""]]

        with open('tempfile.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(questionList)
        msg = f"this is the first question for prom 1"
        dispatcher.utter_message(text=msg)
        return []

class promoneqtwo(Action):
    def name(self) -> Text:
        return "promoneqtwo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        answer = next(tracker.get_latest_entity_values("answer"), None)

        msg = f"this is the second question for prom 1"
        dispatcher.utter_message(text=msg)
        return []

class initiate_promtwo(Action):

    def name(self) -> Text:
        return "initiate_promtwo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        msg = f"Are you ready for prom 2?"
        dispatcher.utter_message(text=msg)
        return []

class promtwoqone(Action):
    def name(self) -> Text:
        return "promtwoqone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        msg = f"this is the first question for prom 2"
        dispatcher.utter_message(text=msg)
        return []

class promtwoqtwo(Action):
    def name(self) -> Text:
        return "promtwoqtwo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        msg = f"this is the second question for prom 2"
        dispatcher.utter_message(text=msg)
        return []

class prom_end(Action):
    def name(self) -> Text:
        return "prom_end"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        msg = f"Mange tak for dine svar"
        dispatcher.utter_message(text=msg)
        return []

class utterUID(Action):
    def name(self) -> Text:
        return "utterUID"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        UID = tracker.sender_id
        msg = f"The UID is: " + str(UID)
        dispatcher.utter_message(text=msg)
        return []

class measurementSetup(Action):
    def name(self) -> Text:
        return "measurementSetup"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        UID = tracker.sender_id

        cred_obj = firebase_admin.credentials.Certificate("resq-rasachatbot-firebase-adminsdk-uxb51-131fdcdccc.json")
        default_app = firebase_admin.initialize_app(cred_obj)
        db = firestore.client()

        doc_ref = db.collection(u'measurement_test').document(str(UID))
        doc_ref.set({
            u'diabp': [0],
            u'sysbp': [0],
            u'weight': [0],
            u'index': [0],
            u'UID': str(UID)
        })

        firebase_admin.delete_app(default_app)

        msg = f"Hej og velkommen til. Jeg er Vera, din personlige assistent. \n"\
            f"Jeg vil hjælpe dig med dagligt at holde øje med dit blodtryk og din vægt. En gang imellem har jeg også et kort spørgeskema til dig, som kan hjælpe sundhedspersonale med at få indsigt i dit mentale helbred. \n"\
            f"Først vil jeg gerne vide om der er en ting du gør hver dag, som er en del af en rutine eller lignende, hvor du har tid til også at veje dig og måle dit blodtryk. Det kunne fx være inden du går i seng eller efter du har børstet tænder."
        dispatcher.utter_message(text=msg)

        return []

class saveContext(Action):
    def name(self) -> Text:
        return "saveContext"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = tracker.latest_message.get('text')
        UID = tracker.sender_id

        cred_obj = firebase_admin.credentials.Certificate("resq-rasachatbot-firebase-adminsdk-uxb51-131fdcdccc.json")
        default_app = firebase_admin.initialize_app(cred_obj)
        db = firestore.client()

        doc_ref = db.collection(u'notification_table').document(str(UID))
        doc_ref.set({
            u'text': message,
            u'UID': str(UID)
        })

        firebase_admin.delete_app(default_app)

        msg = f"Fantastisk! Hvad er klokken typisk når du gør det?"
        dispatcher.utter_message(text=msg)
        return []

class contextTime(Action):
    def name(self) -> Text:
        return "contextTime"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = tracker.latest_message.get('text')
        UID = tracker.sender_id

        cred_obj = firebase_admin.credentials.Certificate("resq-rasachatbot-firebase-adminsdk-uxb51-131fdcdccc.json")
        default_app = firebase_admin.initialize_app(cred_obj)
        db = firestore.client()

        collection = db.collection(u'notification_table')
        docs = collection.stream()
        for doc in docs:
            if doc.id == str(UID):
                doc_ref = db.collection(u'notification_table').document(str(UID))
                doc_ref.set({
                    u'text': doc.to_dict()["text"],
                    u'time': message,
                    u'uid': str(UID)
                })

        firebase_admin.delete_app(default_app)
        msg = f"Mange tak, det er alt for nu. Du vil modtage en notifikation ved dette tidspunkt, der skal huske dig på at måle blodtryk og vægt. \n" \
              f"Du kan bare skrive dine målinger her i chatten (fx “min vægt er 74” eller “min vægt i dag 83 kg (undlad 83kg) eller “mit blodtryk er 126/68”). \n" \
              f"Skriv venligst dine målinger i to seperate beskeder."

        dispatcher.utter_message(text=msg)
        return []
class reminderSetup(Action):

    def name(self) -> Text:
        return "reminderSetup"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        msg = f"Thank you for setting up the reminders!"
        dispatcher.utter_message(text=msg)
        return []

class initPROM(Action):
    def name(self) -> Text:
        return "initPROM"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        msg = f"Jeg har et kort spørgeskema omkring dit helbred til dig i dag. Vil du gerne udfylde den nu?"
        dispatcher.utter_message(text=msg)
        return []

ALLOWED_ANSWERS = [
    "overhovedet ikke", "nogle dage", "mere en halvdelen af dagene", "næsten hver dag"
]

class ValidateSimplePROMForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_PROM_form"

    def validate_question1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""

        if slot_value.lower() not in ALLOWED_ANSWERS:
            dispatcher.utter_message(text=f"Undskyld. Men dette er ikke et gyldigt svar")
            return {"question1": None}
        #dispatcher.utter_message(text=f"Mange tak. Her er næste spørgsmål")
        return {"question1": slot_value}

    def validate_question2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""

        if slot_value.lower() not in ALLOWED_ANSWERS:
            dispatcher.utter_message(text=f"Undskyld. Men dette er ikke et gyldigt svar")
            return {"question2": None}
        #dispatcher.utter_message(text=f"Mange tak. Her er næste spørgsmål")
        return {"question2": slot_value}

    def validate_question3(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""

        if slot_value.lower() not in ALLOWED_ANSWERS:
            dispatcher.utter_message(text=f"Undskyld. Men dette er ikke et gyldigt svar")
            return {"question3": None}
        #dispatcher.utter_message(text=f"Mange tak. Her er næste spørgsmål")
        return {"question3": slot_value}

    def validate_question4(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""

        if slot_value.lower() not in ALLOWED_ANSWERS:
            dispatcher.utter_message(text=f"Undskyld. Men dette er ikke et gyldigt svar")
            return {"question4": None}
        #dispatcher.utter_message(text=f"Mange tak. Her er næste spørgsmål")
        return {"question4": slot_value}

    def validate_question5(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""

        if slot_value.lower() not in ALLOWED_ANSWERS:
            dispatcher.utter_message(text=f"Undskyld. Men dette er ikke et gyldigt svar")
            return {"question5": None}
        #dispatcher.utter_message(text=f"Mange tak. Her er næste spørgsmål")
        return {"question5": slot_value}

    def validate_question6(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""

        if slot_value.lower() not in ALLOWED_ANSWERS:
            dispatcher.utter_message(text=f"Undskyld. Men dette er ikke et gyldigt svar")
            return {"question6": None}
        #dispatcher.utter_message(text=f"Mange tak. Her er næste spørgsmål")
        return {"question6": slot_value}

    def validate_question7(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""

        if slot_value.lower() not in ALLOWED_ANSWERS:
            dispatcher.utter_message(text=f"Undskyld. Men dette er ikke et gyldigt svar")
            return {"question7": None}
        #dispatcher.utter_message(text=f"Mange tak. Her er næste spørgsmål")
        return {"question7": slot_value}

    def validate_question8(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""

        if slot_value.lower() not in ALLOWED_ANSWERS:
            dispatcher.utter_message(text=f"Undskyld. Men dette er ikke et gyldigt svar")
            return {"question8": None}
        #dispatcher.utter_message(text=f"Mange tak. Her er næste spørgsmål")
        return {"question8": slot_value}

    def validate_question9(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""

        if slot_value.lower() not in ALLOWED_ANSWERS:
            dispatcher.utter_message(text=f"Undskyld. Men dette er ikke et gyldigt svar")
            return {"question9": None}
        #dispatcher.utter_message(text=f"Mange tak. Her er næste spørgsmål")
        return {"question9": slot_value}