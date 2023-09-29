from os import system
import sqlite3
import json

class SQLiteDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.conn.close()   

    def createTable(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                              "id" TEXT PRIMARY KEY,
                              "name" TEXT,
                              "itemname" TEXT,
                              "ext" TEXT,
                              contact TEXT,
                              "location" TEXT,
                              "date" DATE,
                              "status" INTEGER,
                              "type" TEXT
                              )''')
        self.conn.commit()
        self.conn.close()    

    def insertData(self, itemId, name, itemName, ext, contact, location, date, statusType):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        itemStatus = 0

        try:
            query = "INSERT INTO data (id, name, itemname, ext, contact, location, date, status, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            values = (itemId, name, itemName, ext, contact, location, date, itemStatus, statusType)
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print("Insert Exception:", e)
            return {"message":"error uploading data to db"}
        finally:
            self.conn.close()
            return {"message":"connection closed sucessfully"}
      

    def markFound(self, id):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute("UPDATE data SET status = 1 WHERE id = ?", (id,))
        self.conn.commit()
        self.conn.close()  
        return {"message": "Item Marked Found Successfully"}

    def fetchAll(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM data")
        data = self.cursor.fetchall()

        columns = ["id", "name", "itemName", "ext", "contact", "location", "date", "status","statusType"]
        json_data = [dict(zip(columns, row)) for row in data]
        self.conn.close()  
        return json.dumps(json_data)

    def deleteItem(self, itemId):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM data WHERE id = ?", (itemId,))
        self.conn.commit()
        self.conn.close()
        return {"message": "Item Deleted Successfully"}
          

    def revertItem(self, itemId):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute("UPDATE data set status=0 WHERE id = ?", (itemId,))
        self.conn.commit()
        self.conn.close()
        return {"message": "Item Reverted Successfully"}
