import pandas as pd
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionTaskCount(Action):
    def name(self) -> Text:
        return "action_task_count"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Load the CSV file
            data = pd.read_csv("data/project_data.csv")
            task_count = len(data)

            # Send a response back to the user
            dispatcher.utter_message(text=f"There are {task_count} tasks in total.")
            return [SlotSet("task_count", task_count)]
        except Exception as e:
            dispatcher.utter_message(text="Unable to retrieve task count.")
            print(f"Error in ActionTaskCount: {e}")
            return []


class ActionMilestoneTasks(Action):
    def name(self) -> Text:
        return "action_milestone_tasks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the milestone slot value
        milestone = tracker.get_slot("milestone")
        if not milestone:
            dispatcher.utter_message(text="Please specify the milestone.")
            return []

        try:
            # Load the CSV file
            data = pd.read_csv("data/project_data.csv")

            # Filter tasks based on the specified milestone
            milestone_tasks = data[data['Milestones'].str.strip().str.lower() == milestone.strip().lower()]
            task_count = len(milestone_tasks)

            # Send a response back to the user
            dispatcher.utter_message(text=f"Milestone {milestone} has {task_count} tasks.")
            return [
                SlotSet("task_count", task_count),
                SlotSet("milestone", milestone)
            ]
        except Exception as e:
            # Handle any errors
            dispatcher.utter_message(text="Unable to retrieve milestone tasks.")
            print(f"Error in ActionMilestoneTasks: {e}")
            return []


class ActionGenerateChart(Action):
    def name(self) -> Text:
        return "action_generate_chart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Load the CSV file
            data = pd.read_csv("data/project_data.csv")

            # Example logic to generate a chart (e.g., task status distribution)
            chart_data = data['Status'].value_counts()
            chart = chart_data.plot(kind='pie', autopct='%1.1f%%')

            # Save the chart
            output_path = "data/output_chart.png"
            chart.figure.savefig(output_path)

            # Send a response back to the user
            dispatcher.utter_message(text=f"Chart generated successfully! Check the image at: {output_path}")
            return []
        except Exception as e:
            dispatcher.utter_message(text="Unable to generate chart.")
            print(f"Error in ActionGenerateChart: {e}")
            return []
