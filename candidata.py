import sqlite3
import collections
import os

class CandiData:

    def __init__(self, db_file="./db/candidata_db.db"):

        self.db_file = db_file
        self.connection = sqlite3.connect(self.db_file)
        self.crsr = self.connection.cursor()

    def get_db_version(self):

        sql_stmt = "SELECT MAX(version) FROM VersionHistory;"
        
        try:
            self.crsr.execute(sql_stmt)
            ret = self.crsr.fetchall()
            db_version = ret[0][0]

        except:
            db_version = None

        return db_version

    def initialize_db(self, schema_file="./db/schema/candidata_schema.sql"):

        try:
            sql_file = open(schema_file, 'r',)
            sql_script = sql_file.read()
            print('read file. closing it.')
            sql_file.close()

        except:
            print("could not open file", schema_file)
            return

        try:
            #sql_stmt = ' '.join(sql_file.read().splitlines())
            self.crsr.executescript(sql_script)

        except:
            print("could not execute sql statement:\n", sql_script)
            return

        try:
            print("adding version history")
            self.crsr.execute('BEGIN TRANSACTION;')
            sql_stmt2 = 'INSERT INTO versionHistory(version) VALUES(0);'
            self.crsr.execute(sql_stmt2)
            self.crsr.execute('COMMIT;')

        except:
            print("could not execute sql statement:\n", sql_stmt2)
            return


    def update_db(self, update_path="./db/update_db"):

        version = self.get_db_version()

        if(None == version):
            print("no version found. initializing db.")
            self.initialize_db()
            
        #TODO:  Create a scheme for adding new tables to the db with sql script
        #       files in the ./db/update_db folder.

def execute_script_from_file(filename):
    fd = open(filename, 'r')

