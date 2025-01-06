from dataclasses import dataclass, field
from crewai import Agent, Task
from box import ConfigBox
import os

from AIEmailPersonalizationAgent.utils import read_yaml_file

@dataclass
class EmailTaskPersonalizerAgent:

    def personalize_email(self, config_path:os.path, agent:Agent, recipient:dict, email_template:str):
        config_file = read_yaml_file(config_path)
        return Task(
            description= config_file.crew_email_agent.email_personalizer_task.personalize_email,
            agent = agent, 
            expected_output= f"Personalized email draft.",
            async_execution=True,
            verbose=True
        )
    

    def ghost_write_email(self, config_path:os.path, agent:Agent, draft_email:Task, recipient:dict):
        config_file = read_yaml_file(config_path)
        return Task(
            description= config_file.crew_email_agent.email_personalizer_task.ghost_write_email,
            agent = agent, 
            context=[draft_email],
            expected_output= f"A revised email draft in ghost writer's specified tone and style.",
            output_file=f"artifact/generated_emails/{recipient['first_name']}_{recipient['last_name']}.txt",
            verbose=True
        )


if __name__=="__main__":
    __all__=["EmailTaskPersonalizerAgent"]