import random, logging as log, json, os
from crewai.flow.flow import Flow, start, listen, router
from utils.utils import get_topic_sets
from crews.content_generation_crew.main import main as execute_content_generation_crew
from database.databaserepository import PostDatabaseRepository
from models.generate_content import Generate_Content

post_repository = PostDatabaseRepository()

class content_generation_flow(Flow[Generate_Content]):
    @start()
    def generate_topic(self, input: str = ""):

        topic = input

        if not input:
            topic_sets = get_topic_sets()
            topic = random.choice(topic_sets)

        log.info(f"Generating content for topic: {topic}")
        
        self.state.topic = topic

    @router(generate_topic)
    def check_if_topic_was_proccessed(self):
        if post_repository.was_topic_proccessed(self.state.topic):
            return "topic_already_proccessed"
        else:
            return "generate_content"

    @listen("topic_already_proccessed")
    def topic_already_proccessed(self):
        log.info(f"Topic already proccessed | Topic: {self.state.topic}")
        return
    
    @listen("generate_content")
    def generate_content(self):
        log.info("Generating content")

        inputs = {
            "topic": self.state.topic,
            "year": self.state.year,
            "month": self.state.month,
            "day": self.state.day
        }

        result = execute_content_generation_crew(inputs)

        log.info("Content generated")

        self.state.result_content = result.raw

    @listen(generate_content)
    def save_content_in_db(self):
        log.info("Saving content in database | Start")

        try:
            file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'crews', 'data_generated', 'content_generation_result.json'))

            with open(file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
                post_repository.save_content(data)


        except Exception as e:
            log.error(f"Error saving content in database: {e}")
        
        finally:
            log.info("Finished attempting to save content in database")

def execute_content_generation_flow() -> str:
    flow = content_generation_flow()
    flow.kickoff()
    retult = flow.state.result_content

    return retult