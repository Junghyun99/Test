import sqlite3

class BaseDB:
    def __init__(self, logger, db_path):
        self.db_path = db_path
        self.conn = None
        self.logger = logger    

    def _create_table(self):        
        raise NotImplementedError("This method must be implemented by subclasses.")

    def execute_write_query(self, query, data=None):
        self.logger.log_info("exe query %s data %s", query, data)
        bWrite = False 
        error = None
        for i in range(10):
            try:
                with sqlite3.connect(self.db_path) as conn:
                    self.conn = conn
                    cursor = self.conn.cursor()
                    if data:
                        cursor.execute(query, data)
                    else:
                        cursor.execute(query)
                    self.conn.commit()
                    bWrite = True
                    break           
            except sqlite3.Error as e:
                self.logger.log_error("DB Write Error: %s", e)
                error = e
        if error:
            raise error 

    def execute_read_query(self, query, data=None):
        self.logger.log_info("exe query %s data %s", query, data)
        bRead = False 
        error = None
        for i in range(10):
            try:
                with sqlite3.connect(self.db_path) as conn:
                    self.conn = conn
                    cursor = self.conn.cursor()
                    if data:
                        cursor.execute(query, data)
                    else:
                        cursor.execute(query)
                    return cursor.fetchall()
            except sqlite3.Error as e:
                self.logger.log_error("DB Read Error: %s", e)
                error = e
        if error:
            raise error

    def insert_data(self, query, data):       
        self.execute_write_query(query, data)

    def read_data(self, query, data=None):
        return self.execute_read_query(query, data)

    def delete_data(self, query, data):       
        self.execute_write_query(query, data)

    def update_data(self, query, data):        
        self.execute_write_query(query, data)

    def close(self):     
        if self.conn:
            self.conn.close()
            self.conn = None



