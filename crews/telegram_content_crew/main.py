import sys, os
from crewai import Agent, Task, Crew, Process
from crewai.project import agent, task, crew, CrewBase
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.utils import load_openai_api_config, load_serper_api_config
from models.generate_content import Telegram_Content

@CrewBase
class ContentGenerationCrew():
  """ Crew for generating telegram content usign AI models """

  @agent
  def writer(self) -> Agent:
    return Agent(
      config=self.agents_config['writer'],
      verbose=True,
      tools=[SerperDevTool(), ScrapeWebsiteTool()]
    )
  
  @agent
  def editor(self) -> Agent:
    return Agent(
      config=self.agents_config['editor'],
      verbose=True,
      tools=[SerperDevTool(), ScrapeWebsiteTool()]
    )
  
  @task
  def writer_task(self) -> Task:
    return Task(
      config=self.tasks_config['writer_task']
    )
  
  @task
  def editor_task(self) -> Task:
    return Task(
      config=self.tasks_config['editor_task'],
      context=[self.writer_task()],
      output_json=Telegram_Content,
      output_file=f"{os.path.join('post-article-automation', 'crews', 'data_generated', 'telegram_content_result.json')}"
    )
  
  @crew
  def telegram_content_crew(self) -> Crew:
    return Crew(
      agents=self.agents,
      tasks=self.tasks,
      process=Process.sequential,
      verbose=True
    )

def main(input: dict[str, str]) -> object:
  load_openai_api_config()
  load_serper_api_config()
  crew = ContentGenerationCrew()
  return crew.telegram_content_crew().kickoff(inputs=input)
