class BaseDB:
    
    def _create_table(self):
        raise NotImplementedError("This method must be implemented by subclasses.")

    def insert_data(self, query, data):
        cursor = self.conn.cursor()
        cursor.execute(query, data)
        self.conn.commit()  # 명시적 commit
 
    def read_data(self, query, data=None):
        cursor = self.conn.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        return cursor.fetchall()

    def delete_data(self, query, data):
        cursor = self.conn.cursor()
        cursor.execute(query, data)
        self.conn.commit()  # 명시적 commit

    def update_data(self, query, data):
        cursor = self.conn.cursor()
        cursor.execute(query, data)
        self.conn.commit()  # 명시적 commit

    def close(self):
        self.conn.close()