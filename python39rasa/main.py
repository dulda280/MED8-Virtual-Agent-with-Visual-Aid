from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class exampleAction(Action):
    def name(self) -> Text:
        return "exampleAction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Text, Any]:
        dispatcher.utter_message(text="Hello world!")
        return []

