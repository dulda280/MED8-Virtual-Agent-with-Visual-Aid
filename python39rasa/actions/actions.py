from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import pandas as pd
import datetime
import math

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
        msg = f"this is the test for prom 1"
        dispatcher.utter_message(text=msg)
        return []

class initiate_promtwo(Action):

    def name(self) -> Text:
        return "initiate_promtwo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        msg = f"this is the test for prom 2"
        dispatcher.utter_message(text=msg)
        return []