from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from src.AINewsletterAgent.tools.search_tools import SearchTools
from src.AINewsletterAgent.utils import save_markdown
from pydantic.dataclasses import dataclass, Field
from typing import Any
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@CrewBase
class AINewsLetterAgents:


    @agent
    def editor_agent(self)->Agent:
        return Agent(
            config=self.agents_config['editor_agent'],
            #llm=llm,
            allow_delegation=True,
            verbose=True,
            max_iter=15
        )

    @agent
    def news_fetcher_agent(self)->Agent:
        return Agent(
            config=self.agents_config['news_fetcher_agent'],
            #llm=llm,
            tools=[SearchTools.search_internet],
            verbose=True,
            allow_delegation=True,
        )

    @agent
    def news_analyzer_agent(self)->Agent:
        return Agent(
            config=self.agents_config['news_analyzer_agent'],
            #llm=llm,
            tools=[SearchTools.search_internet],
            verbose=True,
            allow_delegation=True,
        )
    @agent
    def newsletter_compiler_agent(self)->Agent:
        return Agent(
            config=self.agents_config['newsletter_compiler_agent'],
            #llm=llm,
            verbose=True,
        )

    @task
    def fetch_news_task(self)->Task:
        return Task(
            config=self.tasks_config['fetch_news_task'],
            agent=self.news_fetcher_agent(),
            async_execution=True
        )

    @task
    def analyze_news_task(self)->Task:
        return Task(
            config=self.tasks_config['analyze_news_task'],
            agent=self.news_analyzer_agent(),
            context=[self.fetch_news_task()],
            #async_execution=True
        )

    @task
    def compile_newsletter_task(self)->Task:
        return Task(
            config=self.tasks_config['compile_newsletter_task'],
            agent=self.newsletter_compiler_agent(),
            context=[self.analyze_news_task()],
            callback=save_markdown
        )
    
    @crew
    def crew(self)->Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
           manager_llm=ChatOpenAI(temperature=0, model="gpt-4o-mini"),
            verbose=True,
            max_rpm=2
        )