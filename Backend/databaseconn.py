import psycopg2

class DatabaseConnection:

    def __init__(self):
        self.d_connection()
        self.createtable()

    def d_connection(self):
        hostname = 'localhost'
        db = 'bmailtest'
        username = 'postgres'  
        pwd = 'apeed'
        port_id = 5432
        self.connection= psycopg2.connect(host=hostname, database=db, user=username, password=pwd, port=port_id)
        self.cursor=self.connection.cursor()

    def createtable(self):
        self.createusr_table = """CREATE TABLE IF NOT EXISTS users (
                                user_id SERIAL PRIMARY KEY,
                                name VARCHAR(100),
                                email VARCHAR(100) UNIQUE,
                                isdeleted  BOOLEAN DEFAULT false,
                                password TEXT NOT NULL
                            )"""
        
        self.createusr_infotable = """CREATE TABLE IF NOT EXISTS users_info (
                                user_id INTEGER REFERENCES users(user_id),
                                phone VARCHAR(20),
                                gender VARCHAR(10),
                                bday VARCHAR(15),
                                createdon VARCHAR(15),
                                picture TEXT DEFAULT 'userimages\default.png'
                            )"""

        self.createemail_table = """CREATE TABLE IF NOT EXISTS emails (
                                email_id SERIAL PRIMARY KEY,
                                time VARCHAR(30),
                                sender INTEGER REFERENCES users(user_id),
                                receiver INTEGER REFERENCES users(user_id),
                                key INTEGER,
                                subject TEXT,
                                message TEXT
                            )"""
        
        self.createemail_statustable = """CREATE TABLE IF NOT EXISTS email_status (
                                email_id INTEGER REFERENCES emails(email_id),
                                isdelbyrecv BOOLEAN DEFAULT false,
                                isdelbysndr BOOLEAN DEFAULT false,
                                isstarbyrecv BOOLEAN DEFAULT false,
                                isstarbysndr BOOLEAN DEFAULT false
                            )"""

        self.createstar_table = """CREATE TABLE IF NOT EXISTS starred (
                                starred_id SERIAL PRIMARY KEY,
                                starredby INTEGER REFERENCES users(user_id),
                                label VARCHAR(20),
                                email_id INTEGER REFERENCES emails(email_id)
                            )"""

        self.cursor.execute(self.createusr_table)
        self.cursor.execute(self.createusr_infotable)
        self.cursor.execute(self.createemail_table)
        self.cursor.execute(self.createemail_statustable)
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

    def insert_return(self, query, values):
        """ insert values from frontend to database"""
        self.cursor.execute(query, values)
        data = self.cursor.fetchone()[0]
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