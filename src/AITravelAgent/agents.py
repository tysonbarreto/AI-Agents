import os
from typing import TypedDict, Annotated, List

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

from AITravelAgent.state import PlannerState

from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass, field


load_dotenv(find_dotenv())

@dataclass
class AITravelAgent:

    temperate:float=field(default=0.5)
    groq_model:str=field(default="llama-3.3-70b-versatile")

    def __post_init__(self):
        self.llm = ChatGroq(
            temperature=self.temperate,
            groq_api_key = os.getenv('GROQ_API_KEY'),
            model_name=self.groq_model
        )
    
    @property
    def prompt(self):
        itinerary_prompt=ChatPromptTemplate.from_messages([
                                            ("system"," Your are a helpful travel assistant. Create a day trip itinerary for {city} based on user's interests: {interests}. Provide a breif bulleted itinerary."),
                                            ("human", "Create an itinerary for my day trip.")])
        return itinerary_prompt
    
    @staticmethod
    def input_city(city:str,state:PlannerState)-> PlannerState:
        #print("Please enter the city you want to visit for your day trip: ")
        #user_message = input("Your input: ")
        return {
            **state,
            "city":city,
            "messages":state["messages"] + [HumanMessage(content=city)]
        }
    @staticmethod
    def input_interests(interests:str,state:PlannerState)-> PlannerState:
        #print(f"Please enter your interets for your day trip to: {state['city']} (comma-separated):")
        #user_message = input("Your input: ")
        return {
            **state,
            "interests":[interest.strip() for interest in interests.split(",")],
            "messages":state["messages"] + [HumanMessage(content=interests)]
        }
    

    def create_itinerary(self,state:PlannerState)-> PlannerState:
        #print(f"Creating itenerary for {state['city']} based on interests: {", ".join(state['interests'])}")
        response = self.llm.invoke(self.prompt.format_messages(city=state['city'], interests= ", ".join(state['interests'])))
        #print("\nFinal Itinerary: ")
        #print(response.content)
        state= {
            **state,
            "messages":state["messages"] + [AIMessage(content=response.content)],
            "itinerary": response.content
        }
        return response.content
    

if __name__=="__main__":
    __all__ = ["AITravelAgent"]

