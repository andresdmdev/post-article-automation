import datetime
from pydantic import BaseModel

class Generate_Content(BaseModel):
    topic: str = ""
    year: int = datetime.datetime.now().year
    month: int = datetime.datetime.now().month
    day: int = datetime.datetime.now().day
    result_content: str = ""

class Social_Network_Content(BaseModel):
  topic: str = ""
  result_content: str = ""
  twitter_content: str = ""
  is_twitter_content_saved: bool = False
  notion_content: str = ""
  is_notion_content_saved: bool = False
  whatsapp_content: str = ""
  is_whatsapp_content_saved: bool = False
  discord_content: str = ""
  is_discord_content_saved: bool = False

class Twitter_Content(BaseModel):
  topic: str = ""
  twitter_content: str = ""

class Notion_Content(BaseModel):
  topic: str = ""
  notion_content: str = ""

class Linkedin_Content(BaseModel):
  topic: str = ""
  linkedin_content: str = ""

class Telegram_Content(BaseModel):
  topic: str = ""
  telegram_content: str = ""