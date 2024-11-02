class BaseDB:
    
    def _create_table(self):
        pass

    def create_data(self, query, data):
        cursor = self.conn.cursor()
        cursor.execute(query, data)
        self.conn.commit()  # 명시적 commit
 
    def read_data(self, query, data):
        cursor = self.conn.cursor()
        cursor.execute(query, data)
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