import logging as log, json, os
from crewai.flow.flow import Flow, start, listen, and_
from database.databaserepository import PostDatabaseRepository
from models.generate_content import Social_Network_Content
from crews.twitter_content_crew.main import main as execute_twitter_content_crew
from crews.notion_content_crew.main import main as execute_notion_content_crew
from crews.linkedin_content_crew.main import main as execute_linkedin_content_crew
from crews.telegram_content_crew.main import main as execute_telegram_content_crew
from services.telegram_services.telegram_services import TelegramServices

post_repository = PostDatabaseRepository()
telegram_service = TelegramServices()

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
    log.info("Getting Notion content")

    execute_notion_content_crew({ "topic": self.topic, "result_content": self.result_content })

    try:
      file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'crews', 'data_generated', 'notion_content_result.json'))

      with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        if not data:
          log.error("Error loading content from file")
          return
        
        self.notion_content = data.get('notion_content', 'Content not found')

    except Exception as e:
      log.error(f"Error saving content in database: {e}")
      return
    
    finally:
      log.info("Finished attempting to save content in database")

  @listen(get_content)
  def get_linkedin_content(self):
    log.info("Getting Linkedin content")

    execute_linkedin_content_crew({ "topic": self.topic, "result_content": self.result_content })

    try:
      file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'crews', 'data_generated', 'linkedin_content_result.json'))

      with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        if not data:
          log.error("Error loading content from file")
          return
        
        self.linkedin_content = data.get('linkedin_content', 'Content not found')

    except Exception as e:
      log.error(f"Error saving content in database: {e}")
      return
    
    finally:
      log.info("Finished attempting to save content in database")

  ## TODO - publish content on social media

  @listen(get_content)
  def get_telegram_content(self):
    log.info("Getting Telgram content")

    execute_telegram_content_crew({ "topic": self.topic, "result_content": self.result_content, "linkedinLink": "https://google.com", "notionLink": "https://google.com", "tweetLink": "https://google.com" }) ## TODO - Add links

    try:
      file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'crews', 'data_generated', 'telegram_content_result.json'))

      with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        if not data:
          log.error("Error loading content from file")
          return
        
        self.telegram_content = data.get('telegram_content', 'Content not found')

      telegram_service.send_message(self.telegram_content)

    except Exception as e:
      log.error(f"Error saving content in database: {e}")
      return
    
    finally:
      log.info("Finished attempting to save content in database")

  @listen(and_(get_telegram_content)) ## get_twitter_content, get_notion_content, get_telegram_content
  def save_social_media_content(self):
    log.info("Saving Social Media content")

    content = {
      ## "twitterContent": self.twitter_content,
      ## "notionContent": self.notion_content,
      ## "linkedinContent": self.linkedin_content
      "telegramContent": self.telegram_content
    }

    post_repository.update_content(self.topic, content)

def execute_social_network_content_flow():
  flow = social_network_content_flow()
  flow.kickoff()