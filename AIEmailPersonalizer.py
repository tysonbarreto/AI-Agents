from AIEmailPersonalizationAgent.EmailPersonalizer import EmailPersonalizerAgent
from AIEmailPersonalizationAgent.EmailTaskPersonalizer import EmailTaskPersonalizerAgent
from AIEmailPersonalizationAgent.utils import read_yaml_file
import csv
from crewai import Crew
import time


config_file = read_yaml_file('config.yml')

'''
All your email_template to the config.yml file under sub_heading: email_template
'''


#################### AGENTS ####################
email_template = config_file.crew_email_agent.email_template

agents = EmailPersonalizerAgent()

email_personalizer = agents.personalize_email_agent('config.yml')
ghost_writer = agents.ghost_writer_agent('config.yml')


#################### TASKS ####################

tasks = EmailTaskPersonalizerAgent()

personalize_email_tasks = []
ghost_write_email_tasks = []

csv_file_path= 'data/clients_small.csv'

with open(file=csv_file_path, mode='r', newline="") as file:
    csv_reader = csv.DictReader(file)
#first_name,last_name,email,bio,last_conversation
    for row in csv_reader:
        recipient = {
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'bio': row['bio'],
            'last_conversation': row['last_conversation']
        }

        personalize_email_task = tasks.personalize_email(config_path='config.yml', agent=email_personalizer, recipient=recipient, email_template=email_template)
        ghost_write_email_task = tasks.ghost_write_email(config_path='config.yml', agent=ghost_writer, recipient=recipient, draft_email=personalize_email_task)

        personalize_email_tasks.append(personalize_email_task)
        ghost_write_email_tasks.append(ghost_write_email_task)


#################### CREW ####################

crew = Crew(agents=[email_personalizer, ghost_writer],tasks=[*personalize_email_tasks, *ghost_write_email_tasks],verbose=True,max_rpm=25)


#################### KICKOFF ####################


start_time = time.time()

results=crew.kickoff()

end_time = time.time()

elapsed_time = end_time - start_time

print(f"Execution time: {elapsed_time} seconds")
print(f"Crew Useage: {crew.usage_metric}")
print(f"Calculated useage_metric: {crew.calculated_usage_metric}")



