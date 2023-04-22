
import psycopg2

class DatabaseConnection:

    def __init__(self):
        self.d_connection()
        self.createtable()


    def d_connection(self):
        hostname = 'localhost'
        db = 'bmail'
        username = 'postgres'  
        pwd = 'apeed'
        port_id = 5432
        self.connection= psycopg2.connect(host=hostname, database=db, user=username, password=pwd, port=port_id)
        self.cursor=self.connection.cursor()

    def createtable(self):
        self.createusr_table = """CREATE TABLE IF NOT EXISTS user_data( fullname varchar(100), email varchar(100) PRIMARY KEY, phone varchar(50), gender varchar(20), bday text, ageaccount text,status varchar(20), password TEXT)"""
        self.createmsg_table = """CREATE TABLE IF NOT EXISTS messages(  time TEXT, sendername varchar(100),senderid varchar(100), receivername varchar(100),receiverid varchar(100), subject TEXT, message TEXT)"""
        self.cursor.execute(self.createusr_table)
        self.cursor.execute(self.createmsg_table)
        self.connection.commit()

    def __del__(self):
        """if connection is found without usage then this will anyhow close that connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()

        except BaseException as msg:
            pass


    def search(self, query, values):
        """ search the values from database"""
        self.cursor.execute(query, values)
        data = self.cursor.fetchall()
        self.connection.commit()
        return data

    def insert(self, query, values):
        """ insert values from frontend to database"""
        self.cursor.execute(query, values)
        self.connection.commit()

    def select(self, query):
        """:returns data """
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.connection.commit()
        return data

    def update(self, query, values):
        """updates the values from frontend"""
        self.cursor.execute(query, values)
        self.connection.commit()

    def delete(self, query, values):
        """ deletes the data from database"""
        self.cursor.execute(query, values)
        self.connection.commit()


DatabaseConnection()
                






