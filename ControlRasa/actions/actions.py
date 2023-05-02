# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import random
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

class resetSlots(Action):

    def name(self) -> Text:
        return "resetSlots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return []

class EndMeasurements(Action):

    def name(self) -> Text:
        return "EndMeasurements"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        msg = f"Det var det for i dag. Vi snakkes ved i morgen!"
        dispatcher.utter_message(text=msg)
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

        return [SlotSet("question1", None), SlotSet("question2", None), SlotSet("question3", None),
                SlotSet("question4", None), SlotSet("question5", None), SlotSet("question6", None),
                SlotSet("question7", None), SlotSet("question8", None), SlotSet("question9", None)]


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
    "overhovedet ikke", "nogle dage", "mere end halvdelen af dagene", "næsten hver dag"
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