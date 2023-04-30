
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
        self.createusr_table = """CREATE TABLE IF NOT EXISTS users (
                                id SERIAL PRIMARY KEY,
                                name VARCHAR(100),
                                email VARCHAR(100) UNIQUE,
                                phone VARCHAR(20),
                                gender VARCHAR(10),
                                bday VARCHAR(15),
                                createdon VARCHAR(15),
                                isdeleted  BOOLEAN DEFAULT false,
                                picture TEXT,
                                password TEXT NOT NULL
                            )"""

        self.createmsg_table = """CREATE TABLE IF NOT EXISTS messages (
                                id SERIAL PRIMARY KEY,
                                time VARCHAR(30),
                                sender INTEGER REFERENCES users(id),
                                receiver INTEGER REFERENCES users(id),
                                isdelbyrecv BOOLEAN DEFAULT false,
                                isdelbysndr BOOLEAN DEFAULT false,
                                isstarbyrecv BOOLEAN DEFAULT false,
                                isstarbysndr BOOLEAN DEFAULT false,
                                subject TEXT,
                                message TEXT
                            )"""

        self.createstar_table = """CREATE TABLE IF NOT EXISTS starred (
                                id SERIAL PRIMARY KEY,
                                starredby INTEGER REFERENCES users(id),
                                label VARCHAR(20),
                                messageid INTEGER REFERENCES messages(id)
                            )"""

        self.cursor.execute(self.createusr_table)
        self.cursor.execute(self.createmsg_table)
        self.cursor.execute(self.createstar_table)
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

    # def update(self, query, values):
    #     """updates the values from frontend"""
    #     self.cursor.execute(query, values)
    #     self.connection.commit()

    def update(self, query, values):
        """Updates the values in the database"""
        self.cursor.execute(query, values)
        rows_affected = self.cursor.rowcount
        self.connection.commit()
        return rows_affected

    def delete(self, query, values):
        """ deletes the data from database"""
        self.cursor.execute(query, values)
        self.connection.commit()

DatabaseConnection()
                






