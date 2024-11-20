import logging as log, json, os
from crewai.flow.flow import Flow, start, listen, and_
from database.databaserepository import PostDatabaseRepository
from models.generate_content import Social_Network_Content
from crews.twitter_content_crew.main import main as execute_twitter_content_crew

post_repository = PostDatabaseRepository()

class social_network_content_flow(Flow[Social_Network_Content]):
  @start()
  def get_content(self):
    log.info("Saving content in database | Start")

    try:
      file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'crews', 'data_generated', 'content_generation_result.json'))

      with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        if not data:
          log.error("Error loading content from file")
          return
        
        self.topic = data.get('topic', 'Content not found')
        self.result_content = data.get('result_content', 'Content not found')


    except Exception as e:
      log.error(f"Error saving content in database: {e}")
      return
    
    finally:
      log.info("Finished attempting to save content in database")

  @listen(get_content)
  def get_twitter_content(self):
    log.info("Getting Twitter content")

    execute_twitter_content_crew({ "topic": self.topic, "result_content": self.result_content })

    try:
      file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'crews', 'data_generated', 'twitter_content_result.json'))

      with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        if not data:
          log.error("Error loading content from file")
          return
        
        self.twitter_content = data.get('twitter_content', 'Content not found')


    except Exception as e:
      log.error(f"Error saving content in database: {e}")
      return
    
    finally:
      log.info("Finished attempting to save content in database")

  @listen(get_content)
  def get_notion_content(self):
    log.info("Getting notion content")

    self.notion_content = f"notion content for {self.topic}"

  @listen(get_content)
  def get_whatsapp_content(self):
    log.info("Getting whatsapp content")

    self.whatsapp_content = f"whatsapp content for {self.topic}"

  @listen(and_(get_twitter_content, get_notion_content, get_whatsapp_content))
  def save_social_media_content(self):
    log.info("Saving Social Media content")

    content = {
      "twitterContent": self.twitter_content,
      "notionContent": self.notion_content,
      "whatsappContent": self.whatsapp_content
    }

    post_repository.update_content(self.topic, content)

def execute_social_network_content_flow():
  flow = social_network_content_flow()
  flow.kickoff()