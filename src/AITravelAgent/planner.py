
from AITravelAgent.agents import AITravelAgent

def travel_planner(city: str, interests: str):
    # Initialize state
    state = {
        "messages": [],
        "city": "",
        "interests": [],
        "itinerary": "",
    }

    # Process the city and interests inputs
    state = AITravelAgent.input_city(city, state)
    state = AITravelAgent.input_interests(interests, state)

    # Generate the itinerary
    itinerary = AITravelAgent().create_itinerary(state)

    return itinerary

if __name__=="__main__":
    __all__=["travel_planner"]