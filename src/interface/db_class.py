import sqlite3

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
            print(f"Database error: {e}")
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

