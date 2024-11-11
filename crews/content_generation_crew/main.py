import sys, os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crews.models.generate_content import Generate_Content
from utils.utils import load_openai_api_config, load_serper_api_config

@CrewBase
class ContentGenerationCrew():
  """Crew for generating content using AI models"""

  @agent
  def researcher(self) -> Agent:
    return Agent(
      config=self.agents_config['researcher'],
      verbose=True,
      tools=[SerperDevTool(), ScrapeWebsiteTool()]
    )
  
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
  def researcher_task(self) -> Task:
    return Task(
      config=self.tasks_config['researcher_task'],
    )

  @task
  def writer_task(self) -> Task:
    return Task(
      config=self.tasks_config['writer_task'],
      context=[self.researcher_task()]
    )
  
  @task
  def editor_task(self) -> Task:
    return Task(
      config=self.tasks_config['editor_task'],
      context=[self.researcher_task(), self.writer_task()],
      output_json=Generate_Content,
      output_file=f"{os.path.join('post-article-automation', 'crews', 'data_generated', 'content_generation_result.json')}"
    )

  @crew
  def content_generation_crew(self) -> Crew:
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
  return crew.content_generation_crew().kickoff(inputs=input)