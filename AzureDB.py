from os import name
from typing import Text
import pypyodbc
import azurecred


class AzureDB:

    dsn='DRIVER='+azurecred.AZDBDRIVER+';SERVER='+azurecred.AZDBSERVER+';PORT=1433;DATABASE='+azurecred.AZDBNAME+';UID='+azurecred.AZDBUSER+';PWD='+ azurecred.AZDBPW
    def __init__(self):
        self.conn = pypyodbc.connect(self.dsn)
        self.cursor = self.conn.cursor()

    def finalize(self):
        if self.conn:
            self.conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finalize()

    def __enter__(self):
        return self

    def azureGetData(self):
        try:
            self.cursor.execute("SELECT id,name,text,DateTime FROM data ORDER BY id")
            data = self.cursor.fetchall()
            return data
        except pypyodbc.DatabaseError as exception:
            print('Failed to execute query')
            print(exception)
            exit (1)
            
#zakomentowana funkcja dodająca do bazy
    def azureAddData(self, name1, text1):
        # self.cursor.execute("DROP table data;")
        self.cursor.execute(f"INSERT into data (name, text) values ( '{name1}' , '{text1}')")
        self.conn.commit()