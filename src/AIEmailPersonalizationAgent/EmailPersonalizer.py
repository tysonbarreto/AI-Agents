from crewai import Agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass, field
import os
import yaml
from typing import Union
from box import ConfigBox
from AIEmailPersonalizationAgent.utils import read_yaml_file


load_dotenv(find_dotenv())

@dataclass
class EmailPersonalizerAgent:

    def __post_init__(self):
        if os.environ.get('GROQ_API_KEY') is None:
            raise ValueError("GROQ_API_KEY not found, please add it to environment variables.")
        else:
            self.llm = ChatGroq(
                groq_api_key=os.getenv('GROQ_API_KEY')
            )
  
    def personalize_email_agent(self, config_file_path:os.path):
        """
        Please add your agents role, goal and backstory to your config file under crewai_agent and specify your agents_name:email_personalizer as a header in the yaml file. 
        pass the same path to load agents configuration to this object
        """
        config_file = read_yaml_file(config_file_path)
        return Agent(
            role=config_file.crew_email_agent.email_personalizer_agent.role,
            goal=config_file.crew_email_agent.email_personalizer_agent.goal,
            backstory=config_file.crew_email_agent.email_personalizer_agent.backstory,
            name=config_file.crew_email_agent.email_personalizer_agent,
            llm=self.llm,
            max_iter=2
        )
    
    def ghost_writer_agent(self,config_file_path:os.path):
        """
        Please add your agents role, goal and backstory to your config file under crewai_agent and specify your agents_name:gost_writer as a header in the yaml file. 
        pass the same path to load agents configuration to this object
        """
        config_file = read_yaml_file(config_file_path)
        return Agent(
            role=config_file.crew_email_agent.ghost_writer.role,
            goal=config_file.crew_email_agent.ghost_writer.goal,
            backstory=config_file.crew_email_agent.ghost_writer.backstory,
            name=config_file.crew_email_agent.ghost_writer,
            llm=self.llm,
            max_iter=2
        )

if __name__ == "__main__":
    __all__=["EmailPersonalizerAgent","read_yaml_file"]