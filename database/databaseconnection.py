import os
import libsql_experimental as libsql

class DatabaseConnection:
    def __init__(self, database = None):
      self.url = os.getenv("TURSO_DATABASE_URL")
      self.auth_token = os.getenv("TURSO_AUTH_TOKEN")
      self.database = os.getenv("TURSO_DATABASE_NAME") if database == None else database

    def connect(self):
      try:
          if not all([self.url, self.auth_token, self.database]):
            raise ValueError("Database connection parameters are missing")
          
          return libsql.connect(self.database, sync_url=self.url, auth_token=self.auth_token)
      except Exception as e:
        print(f"Error connecting to database: {e}")
        return None