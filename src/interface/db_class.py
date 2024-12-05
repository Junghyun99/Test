import sqlite3

from src.service.logging.logger_manager import logger_manager

system_logger = logger_manager.get_logger('SYSTEM')

class BaseDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def _create_table(self):        
        raise NotImplementedError("This method must be implemented by subclasses.")

    def execute_query(self, query, data=None):
        system_logger.log_debug("exe query %s data %s", query, data)
        try:
            with self.conn.cursor() as cursor:
                if data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)

                # Automatically commit for write queries
                if query.strip().lower().startswith(("insert", "update", "delete")):
                    self.conn.commit()
                
                return cursor.fetchall() if query.lower().startswith("select") else None
        except sqlite3.Error as e:
            system_logger.log_error("DB error : %s", e)
            raise e

    def insert_data(self, query, data):       
        self.execute_query(query, data)

    def read_data(self, query, data=None):
        return self.execute_query(query, data)

    def delete_data(self, query, data):       
        self.execute_query(query, data)

    def update_data(self, query, data):        
        self.execute_query(query, data)

    def close(self):     
        if self.conn:
            self.conn.close()
            self.conn = None

