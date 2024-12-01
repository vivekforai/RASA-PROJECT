import pandas as pd
import matplotlib.pyplot as plt
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List

# Load CSV data
try:
    data = pd.read_csv("D:/IDC_rasa/data/project_data.csv")  # Updated path
    print("CSV loaded successfully!")  # Debugging statement
except FileNotFoundError:
    print("CSV file not found. Please check the file path.")
    data = None

class ActionQueryTasks(Action):
    def name(self) -> Text:
        return "action_query_tasks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if data is None:
            dispatcher.utter_message(text="I couldn't access the task data. Please check the CSV file path.")
            return []

        milestone = tracker.get_slot("milestone")
        status = tracker.get_slot("status")
        
        filtered_data = data
        if milestone:
            filtered_data = filtered_data[filtered_data["Milestones"] == milestone]
        if status:
            filtered_data = filtered_data[filtered_data["Status"].str.lower() == status.lower()]
        
        task_count = len(filtered_data)
        dispatcher.utter_message(text=f"There are {task_count} tasks matching your criteria.")
        return []

class ActionGenerateVisualization(Action):
    def name(self) -> Text:
        return "action_generate_visualization"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if data is None:
            dispatcher.utter_message(text="I couldn't access the task data. Please check the CSV file path.")
            return []

        chart_type = tracker.get_slot("chart_type")
        milestone = tracker.get_slot("milestone")

        filtered_data = data
        if milestone:
            filtered_data = filtered_data[filtered_data["Milestones"] == milestone]

        if chart_type == "bar":
            filtered_data["Status"].value_counts().plot(kind="bar", title="Task Status Distribution")
        elif chart_type == "pie":
            filtered_data["Status"].value_counts().plot(kind="pie", autopct='%1.1f%%', title="Task Status Distribution")
        else:
            dispatcher.utter_message(text=f"Unsupported chart type: {chart_type}. Please choose bar or pie.")
            return []

        plt.savefig("chart.png")
        plt.close()
        dispatcher.utter_message(image="chart.png")
        return []
