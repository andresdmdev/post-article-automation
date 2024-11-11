import datetime, random, logging as log, json, os
import libsql_experimental as libsql
from crewai.flow.flow import Flow, start, listen
from pydantic import BaseModel
from utils.utils import get_topic_sets
from crews.content_generation_crew.main import main as execute_content_generation_crew

class ContentGenerator(BaseModel):
    topic: str = "Adquicision de clientes para una fintech"
    year: int = datetime.datetime.now().year
    month: int = datetime.datetime.now().month
    day: int = datetime.datetime.now().day
    result_content: str = ""

class ContentGenerationFlow(Flow[ContentGenerator]):

    @start()
    def generate_topic(self, input: str = ""):
        topic = input if len(input) > 0 else self.state.topic

        log.info(f"Generating content for topic: {topic}")

        topic_sets = get_topic_sets()

        topic = random.choice(topic_sets)

        log.info(f"Generated topic: {topic}")

        self.state.topic = topic
      
    @listen(generate_topic)
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

        # Save content in database
        try:
            """ Save content in database | Data in content_generation_result.json"""
            file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'crews', 'data_generated', 'content_generation_result.json'))

            with open(file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
                url = os.getenv("TURSO_DATABASE_URL")
                auth_token = os.getenv("TURSO_AUTH_TOKEN")

                conn = libsql.connect("postautomation.db", sync_url=url, auth_token=auth_token)

                topic = str(data.get('topic', 'Default')).replace("--", " ").replace("'", "''")
                content = str(data.get('result_content', 'Prueba')).replace("--", " ").replace("'", "''")
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        topic VARCHAR(255) NOT NULL,
                        content TEXT NOT NULL,
                        createdDate TIMESTAMP NOT NULL,
                        createdBy VARCHAR(100),
                        updatedDate TIMESTAMP,
                        updatedBy VARCHAR(100) NULL,
                        deletedDate TIMESTAMP NULL,
                        deletedBy VARCHAR(100) NULL
                    );
                """)
                conn.execute(f"INSERT INTO posts (topic, content, createdDate, createdBy, updatedDate, updatedBy, deletedDate, deletedBy) VALUES ('{topic}', '{content}', '{str(datetime.datetime.now())}', 'test', null, null, null, null);")
                conn.commit()
                conn.sync()

                print(conn.execute("select * from posts").fetchall())


        except Exception as e:
            log.error(f"Error saving content in database: {e}")
        
        finally:
            log.info("Finished attempting to save content in database")

def execute_content_generation_flow() -> str:
    flow = ContentGenerationFlow()
    flow.kickoff()
    retult = flow.state.result_content

    return retult