import logging as log, datetime
from database.databaseconnection import DatabaseConnection 

class PostDatabaseRepository():
  def _clean_data(self, data: str) -> str:
    return str(data).replace("--", " ").replace("'", "''")

  def save_content(self, data: dict):
    log.info("PostDatabaseRepository | save_content | Start")
    try:
      db = DatabaseConnection()
      db_connection = db.connect()

      if db_connection is None:
          log.error("PostDatabaseRepository | save_content | Database connection failed")
          return

      cursor = db_connection.cursor()

      for key, value in data.items():
        data[key] = self._clean_data(value)

      topic = data.get('topic', 'Content not found').upper()
      content = data.get('result_content', 'Content not found')
      twitterContent = data.get('twitterContent', '')
      notionContent = data.get('notionContent', '')
      whatsappContent = data.get('whatsappContent', '')
      created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      created_by = "system-admin"

      query = """
          INSERT INTO posts (topic, content, twitterContent, notionContent, whatsappContent, createdDate, createdBy)
          VALUES (?, ?, ?, ?, ?, ?, ?)
      """
      cursor.execute(query, (topic, content, twitterContent, notionContent, whatsappContent, created_at, created_by,))

      db_connection.commit()
      db_connection.sync()
      cursor.close()

      log.info("PostDatabaseRepository | save_content | Content saved in database")
    except Exception as e:
      log.error(f"PostDatabaseRepository | save_content | Error saving content in database: {e}")
    finally:
      log.info("PostDatabaseRepository | save_content | Finish")

    return 
    
  def update_content(self, id: int, data: dict):
    log.info("PostDatabaseRepository | update_content | Start")

    try:
      db = DatabaseConnection()
      db_connection = db.connect()

      if db_connection is None:
          log.error("PostDatabaseRepository | update_content | Database connection failed")
          return

      cursor = db_connection.cursor()

      params = ()
      query_parameters = ""
      
      for key, value in data.items():
        data[key] = self._clean_data(value)
        params = params + (data.get(key, ""),)
        query_parameters += f"{key} = ?, "

      updatedDate =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      updatedBy = "system-admin"
      
      params = params + (updatedDate, updatedBy, id, )

      query = f"""
          UPDATE posts 
          SET {query_parameters} updatedDate = ?, updatedBy = ?
          WHERE ID = ?
      """
      
      cursor.execute(query, params)

      db_connection.commit()
      db_connection.sync()
      cursor.close()

      log.info("PostDatabaseRepository | update_content | Content saved in database")
    except Exception as e:
      log.error(f"PostDatabaseRepository | update_content | Error saving content in database: {e}")
    finally:
      log.info("PostDatabaseRepository | update_content | Finish")

    return
  
  def was_topic_proccessed(self, topic: str) -> bool:
    log.info("PostDatabaseRepository | wasContentProccessed | Start")
    was_processed = False
    try:
      db = DatabaseConnection()
      db_connection = db.connect()

      if db_connection is None:
          log.error("PostDatabaseRepository | wasContentProccessed | Database connection failed")
          return

      cursor = db_connection.cursor()

      formated_topic = '%' + self._clean_data(topic).upper() + '%'

      query = """
          SELECT COUNT(*) FROM posts WHERE topic like ? and deletedBy IS NULL and deletedDate IS NULL ORDER BY ID DESC LIMIT 1
      """
      
      result = cursor.execute(query, (formated_topic,)).fetchall()
      print(result)

      if result:
        count, = result[0]

        if count > 0:
          was_processed = True

      db_connection.commit()
      db_connection.sync()
      cursor.close()

      log.info("PostDatabaseRepository | wasContentProccessed | Content saved in database")
    except Exception as e:
      log.error(f"PostDatabaseRepository | wasContentProccessed | Error saving content in database: {e}")
    finally:
      log.info("PostDatabaseRepository | wasContentProccessed | Finish")

    return was_processed