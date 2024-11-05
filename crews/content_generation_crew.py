import sys, os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.utils import get_openai_api_key, get_serper_api_key

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

  @task
  def researcher_task(self) -> Task:
    return Task(
      config=self.tasks_config['researcher_task'],
      output_file='./report.md'
    )

  @crew
  def content_generation_crew(self) -> Crew:
    """ Crew for generating content using AI models """
    return Crew(
      agents=self.agents,
      tasks=self.tasks,
      process=Process.sequential,
      verbose=True
    )
  

def execute_content_generation_crew(input: dict[str, str]) -> str:
  openai_api_key = get_openai_api_key()
  os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'
  os.environ["SERPER_API_KEY"] = get_serper_api_key()
  crew = ContentGenerationCrew()
  return crew.content_generation_crew().kickoff(inputs=input)