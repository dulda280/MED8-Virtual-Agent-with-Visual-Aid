from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from firebase_admin import db

import pandas as pd
import datetime
import math
import firebase_admin
import csv

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

class saveBPToFB(Action):

    def name(self) -> Text:
        return "saveBPToFB"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        input = next(tracker.get_latest_entity_values("input"), None)
        #userId = tracker.sender_id
        userId = 24658147

        cred_obj = firebase_admin.credentials.Certificate("resq-rasachatbot-firebase-adminsdk-uxb51-8aa0ff5053.json")
        default_app = firebase_admin.initialize_app(cred_obj, {
            "databaseURL": "https://resq-rasachatbot-default-rtdb.europe-west1.firebasedatabase.app/"
        })

        # when a user updates the measurements
        ref = db.reference("/measurement Table/" + str(userId))

        dict = ref.get()

        inputList = input.split("/", 2)

        dict["sysbp"].append(int(inputList[0]))
        dict["diabp"].append(int(inputList[1]))


        ref.set(dict)
        firebase_admin.delete_app(default_app)

        msg = f"thank you for telling me about your blood pressure. Your input was {input}. "
        dispatcher.utter_message(text=msg)
        return []


class saveWToFB(Action):

    def name(self) -> Text:
        return "saveWToFB"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        input = next(tracker.get_latest_entity_values("input"), None)
        userId = 24658147

        cred_obj = firebase_admin.credentials.Certificate("resq-rasachatbot-firebase-adminsdk-uxb51-8aa0ff5053.json")
        default_app = firebase_admin.initialize_app(cred_obj, {
            "databaseURL": "https://resq-rasachatbot-default-rtdb.europe-west1.firebasedatabase.app/"
        })

        # when a user updates the measurements
        ref = db.reference("/measurement Table/" + str(userId))

        dict = ref.get()
        print(dict)

        dict["weight"].append(int(input))

        ref.set(dict)
        firebase_admin.delete_app(default_app)

        msg = f"thank you for telling me about your weight. Your input was {input}. "
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
        msg = f"Thank you for your answers"
        dispatcher.utter_message(text=msg)
        return []