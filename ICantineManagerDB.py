# DB init and definitions
import sqlite3

class InfoStudentsDB:

    __DB_LOCATION = '../easy_facial_recognition-master/ICantineDB/infostudents.db'
    

    def __init__(self, db_location=None):
        """Initialize InfoStudents database"""
        if db_location is not None:
            self.__db_connection = sqlite3.connect(db_location)
        else:
            self.__db_connection = sqlite3.connect(self.__DB_LOCATION)
        self.__db_cursor = self.__db_connection.cursor()

    def InfoStudentsClose(self):
        """Close InfoStudents database"""
        self.__db_connection.close()

    def InfoStudentsCreateTable(self):
        """Create InfoStudents Table"""
        self.__db_cursor.execute("""CREATE TABLE IF NOT EXISTS InfoStudents(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        FirstName text,
                        LastName text,
                        Class text,
                        PhotoFile text,
                        EntryCount integer
                        )""")
    
    def InfoStudentsAdd(self, new_data):
        """Insert a new row into InfoStudents Database"""
        self.__db_cursor.execute('INSERT INTO InfoStudents(FirstName, LastName, Class, PhotoFile, EntryCount) VALUES(?, ?, ?, ?, ?)', new_data)

    def InfoStudentsModifyPhotoFile(self, PhotoFile, id):
        """Modify a row into InfoStudents Database"""
        self.__db_cursor.execute("UPDATE InfoStudents SET `PhotoFile` = ? WHERE `ID` = ? ", (PhotoFile, id,))

    def InfoStudentsQueryAll(self):
        self.__db_cursor.execute("SELECT * FROM InfoStudents")
        self.select = self.__db_cursor.fetchall()
        return self.select

    def InfoStudentsQueryAllDesc(self):
        self.__db_cursor.execute("SELECT * FROM InfoStudents order by id desc")
        self.select = self.__db_cursor.fetchall()
        return self.select

    def InfoStudentsQueryAllAsc(self):
        self.__db_cursor.execute("SELECT * FROM InfoStudents order by LastName asc")
        self.select = self.__db_cursor.fetchall()
        return self.select

    def InfoStudentsSearchByFirstName(self, firstname):
            self.select = self.__db_cursor.execute("SELECT*FROM InfoStudents where `FirstName` = (?) " , (firstname,))
            return self.select

    def InfoStudentsSearchByLastName(self, lastname):
            select = self.__db_cursor.execute("SELECT*FROM InfoStudents where `LastName` = (?) " , (lastname,))
            return select

    def InfoStudentsSearchByClass(self, Class):
            select = self.__db_cursor.execute("SELECT*FROM InfoStudents where `Class` = (?) " , (Class,))
            return select

    def InfoStudentsCommit(self):
        """Commit changes into InfoStudents Database"""
        self.__db_connection.commit()

    def InfoStudentsDeleteRecordID(self, id):
        self.__db_cursor.execute('DELETE from InfoStudents where ID = ?', (id,))

    def InfoStudentsDeleteNULL(self):
        self.__db_cursor.execute("""DELETE from InfoStudents where FirstName IS NULL OR trim(FirstName) = ''""")    

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.__db_cursor.close()
        if isinstance(exc_value, Exception):
            self.__db_connection.rollback()
        else:
            self.__db_connection.commit()
        self.__db_connection.close()

