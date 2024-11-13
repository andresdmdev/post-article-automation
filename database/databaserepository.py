import logging as log, datetime
from database.databaseconnection import DatabaseConnection 

class PostDatabaseRepository():
  def _clean_data(data: str) -> str:
    return str(data).replace("--", " ").replace("'", "''")

  def save_content_in_db(self, data: dict):
    log.info("PostDatabaseRepository | save_content_in_db | Start")
    try:
      db = DatabaseConnection()
      db_connection = db.connect()

      if db_connection is None:
          log.error("PostDatabaseRepository | save_content_in_db | Database connection failed")
          return

      cursor = db_connection.cursor()

      for key, value in data.items():
        data[key] = PostDatabaseRepository._clean_data(value)

      topic = data.get('topic', 'Content not found')
      content = data.get('result_content', 'Content not found')
      twitterContent = data.get('twitterContent', None)
      notionContent = data.get('notionContent', None)
      whatsappContent = data.get('whatsappContent', None)
      created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      created_by = "system-admin"

      query = """
          INSERT INTO posts (topic, content, twitterContent, notionContent, whatsappContent, createdDate, createdBy)
          VALUES (?, ?, ?, ?, ?, ?, ?)
      """
      params = (f"{topic}", f"{content}", f"{twitterContent}", f"{notionContent}", f"{whatsappContent}", f"{created_at}", f"{created_by}")
      cursor.execute(query, params)

      db_connection.commit()
      db_connection.sync()
      cursor.close()

      log.info("PostDatabaseRepository | save_content_in_db | Content saved in database")
    except Exception as e:
      log.error(f"PostDatabaseRepository | save_content_in_db | Error saving content in database: {e}")
    finally:
      log.info("PostDatabaseRepository | save_content_in_db | Finish")

    return 
    
  def update_content_in_db(self, id: int, data: dict):
    log.info("PostDatabaseRepository | update_content_in_db | Start")

    try:
      db = DatabaseConnection()
      db_connection = db.connect()

      if db_connection is None:
          log.error("PostDatabaseRepository | update_content_in_db | Database connection failed")
          return

      cursor = db_connection.cursor()

      ## Search content by id
      query_search = """
        SELECT * FROM posts WHERE ID = :id LIMIT 1
      """
      search_params = {'id': id}
      cursor.execute(query_search, search_params)

      ## Get values
      params = {}

      for key, value in data.items():
        data[key] = PostDatabaseRepository._clean_data(value)
        params[key] = data.get(key, None)

      params['id'] = id
      params['updatedBy'] = "system-admin"
      params['updatedDate'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

      query = """
          UPDATE posts 
          SET twitterContent = :twitterContent, notionContent = :notionContent, whatsappContent = :whatsappContent, updatedDate = :updatedDate, updatedBy = :updatedBy
          WHERE ID = :id
      """
      
      cursor.execute(query, params)

      db_connection.commit()
      db_connection.sync()
      cursor.close()

      log.info("PostDatabaseRepository | update_content_in_db | Content saved in database")
    except Exception as e:
      log.error(f"PostDatabaseRepository | update_content_in_db | Error saving content in database: {e}")
    finally:
      log.info("PostDatabaseRepository | update_content_in_db | Finish")

    return 
    