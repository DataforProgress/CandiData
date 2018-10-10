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

    def get_districts_by_state(self, state):
        sql_stmt = "SELECT congressionalDistricts FROM states WHERE abbreviated=\"" + state + "\";"
        self.crsr.execute(sql_stmt)
        ret = self.crsr.fetchall()

        return ret[0][0]

    def add_congressional_election(self, date, state='ALL', district='ALL', election_type='GENERAL'):

        # build sql statement
        if( 'ALL' == state ):
            sql_stmt = "SELECT abbreviated, congressionalDistricts FROM states;"

        else:
            if ( 2 == len(state) ):
                sql_stmt = "SELECT abbreviated, congressionalDistricts FROM" \
                            + " states WHERE abbreviated=\'" + state + "\';"

            else:
                sql_stmt = "SELECT abbreviated, congressionalDistricts FROM" \
                            + " states WHERE name=\'" + state + "\';"

        #execute statement
        self.crsr.execute(sql_stmt)
        ret = self.crsr.fetchall()

        #add elections
        self.crsr.execute("BEGIN TRANSACTION;")
        for item in ret:
            state = item[0]
            num_districts = item[1]

            for ii in range( 1, num_districts + 1 ):
                sql_stmt = "INSERT INTO elections(state, district, " \
                           "electionType, electionDate) VALUES(\'" + state + \
                           "\', " + str(ii) + ", \'" + election_type + "\', " + date \
                           + " );"

                self.crsr.execute(sql_stmt)

        self.crsr.execute("COMMIT;")

