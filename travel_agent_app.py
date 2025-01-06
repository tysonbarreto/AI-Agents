from AITravelAgent.planner import travel_planner
import gradio as gr
import sys

def app():
    interface = gr.Interface(
        fn=travel_planner,
        theme='Yntec/HaleyCH_Theme_Orange_Green',
        inputs=[
            gr.Textbox(label="Enter the city for your day trip"),
            gr.Textbox(label="Enter your interests (comma-separated)"),
        ],
        outputs=gr.Textbox(label='Generated Itinerary'),
        title="Day Travel Itinerary Planner",
        description="Enter a city and your interests to generate a personalized day trip itinerary."
    )
    interface.launch(share=True)

if __name__=="__main__":
    app()



