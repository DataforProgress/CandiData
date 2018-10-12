import sqlite3
import collections
import os

class CandiData:

    def __init__(self, db_file="./db/candidata_db.db"):

        self.db_file = db_file
        self.connection = sqlite3.connect(self.db_file)
        self.crsr = self.connection.cursor()

    def get_db_version(self):
        """ returns the max value of the versionHistory table
        """

        sql_stmt = "SELECT MAX(version) FROM VersionHistory;"
        
        try:
            self.crsr.execute(sql_stmt)
            ret = self.crsr.fetchall()
            db_version = ret[0][0]

        except:
            db_version = None

        return db_version

    def initialize_db(self, schema_file="./db/schema/candidata_schema.sql"):
        """ loads schema file into self.db_file
        """

        try:
            sql_file = open(schema_file, 'r',)
            sql_script = sql_file.read()
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
        """ adds a congressional election to the elections table
            NOTE: input date as DD-MM-YYYY
            TODO: make it parse dates elegantly
        """

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
                           "\', " + str(ii) + ", \'" + election_type + "\', \'" + date \
                           + "\' );"

                self.crsr.execute(sql_stmt)

        self.crsr.execute("COMMIT;")

    def get_congressional_elections( self, state='ALL', district='ALL', date='ALL'):

        if( 'ALL' == state ):
            if( 'ALL' == date ):
                sql_stmt = "SELECT * FROM elections;"
            else:
                sql_stmt = "SELECT * FROM elections WHERE electionDate=\'" + date + "\';"

        else:
            if( 'ALL' == district and 'ALL' == date ):
                sql_stmt = "SELECT * FROM elections WHERE state=\'" + state  + "\';"

            elif( 'ALL' == district ):
                sql_stmt = "SELECT * FROM elections WHERE state=\'" + state  + \
                "\' AND electionDate=\'" + date + "\';"

            elif( 'ALL' == date ):
                sql_stmt = "SELECT * FROM elections WHERE state=\'" + state  + \
                "\' AND district=\'" + str(district) + "\';"

            else:
                sql_stmt = "SELECT * FROM elections WHERE state=\'" + state  + \
                "\' AND district=\'" + str(district) + "\' AND electionDate=\'" + date + "\';"

        self.crsr.execute(sql_stmt)
        ret = self.crsr.fetchall()

        return ret

    def add_candidate( self, name, partyAffiliation='INDEPENDENT', dateOfBirth='None'):

        sql_stmt = 'SELECT candidateID, name, dateOfBirth, partyAffiliation FROM candidates ' \
                   ' WHERE name=\'' + name + '\' AND active=\'TRUE\';'

        self.crsr.execute(sql_stmt)
        ret = self.crsr.fetchall()

        duplicates = []

        for row in ret:
            if( name == row[1] ):
                duplicates.append(row)

        ch = 'n'

        if( [] != duplicates ):
            print("If this candidate is already in the db, enter the candidate ID number. Else, enter 'n' for a new entry.")
            for row in duplicates:
                print(str(row[0]) + "    " + row[1] + "   " + row[2] + "     " + row[3])

            ch = input(">>> ")

        if( 'n' == ch ):
            sql_stmt = 'INSERT INTO candidates(name, dateOfBirth, partyAffiliation)' \
                       ' VALUES(\'' + name + '\', \'' + dateOfBirth + '\', \'' + partyAffiliation + '\');'

            self.crsr.execute('BEGIN TRANSACTION;')
            self.crsr.execute(sql_stmt)
            self.crsr.execute('COMMIT;')

        else:
            print("Use update_candidate_info() to add a date of birth or party affiliation.")

    def update_candidate_info( self, name, partyAffiliation='None', dateOfBirth='None', newName='None'):

        sql_stmt = 'SELECT candidateID, name, dateOfBirth, partyAffiliation FROM candidates ' \
                   ' WHERE name=\'' + name + '\' AND active=\'TRUE\';'

        self.crsr.execute(sql_stmt)
        ret = self.crsr.fetchall()

        duplicates = []

        for row in ret:
            if( name == row[1] ):
                duplicates.append(row)

        ch = 'n'

        if( [] != duplicates ):
            print("Enter candidate ID of candidate to update or 'n' for a new candidate.")
            for row in duplicates:
                print(str(row[0]) + "    " + row[1] + "   " + row[2] + "     " + row[3])

            ch = input(">>> ")

        if( 'n' == ch ):
            print("Use add_candidate() to add a new candidate.")

        else:
            self.crsr.execute("BEGIN TRANSACTION;")

            try:
                candidId = int(ch, 10)

                if( 'None' != partyAffiliation ):
                    sql_stmt = "UPDATE candidates SET partyAffiliation=\'" + partyAffiliation + "\' " \
                               + "WHERE candidateID=" + str(candidId) + ";"

                    self.crsr.execute(sql_stmt)

                if( 'None' != dateOfBirth ):
                    sql_stmt = "UPDATE candidates SET dateOfBirth=\'" + dateOfBirth + "\' " \
                               + "WHERE candidateID=" + str(candidId) + ";"

                    self.crsr.execute(sql_stmt)

                if( 'None' != newName ):
                    sql_stmt = "UPDATE candidates SET name=\'" + newName + "\' " \
                               + "WHERE candidateID=" + str(candidId) + ";"

                    self.crsr.execute(sql_stmt)

            except:
                print( ch + " is not a number.")

            self.crsr.execute("COMMIT;")

    def purge_candidate( self, name ):

        sql_stmt = 'SELECT candidateID, name, dateOfBirth, partyAffiliation FROM candidates ' \
                   ' WHERE name=\'' + name + '\' and active=\'TRUE\';'

        self.crsr.execute(sql_stmt)
        ret = self.crsr.fetchall()

        duplicates = []

        for row in ret:
            if( name == row[1] ):
                duplicates.append(row)

        ch = 'n'

        if( [] != duplicates ):
            print("Enter candidate ID of candidate to purge or 'n' for no.")
            for row in duplicates:
                print(str(row[0]) + "    " + row[1] + "   " + row[2] + "     " + row[3])

            ch = input(">>> ")

        try:
            candidId = int(ch, 10)

            sql_stmt = "UPDATE candidates SET active='FALSE' WHERE candidateID=" + str(candidId) + ";"

            self.crsr.execute('BEGIN TRANSACTION;')
            self.crsr.execute(sql_stmt);
            self.crsr.execute('COMMIT;')

        except:
            print("No candidate purged.")

    def list_candidates( self ):

        sql_stmt = "SELECT candidateID, name, dateOfBirth, partyAffiliation FROM candidates WHERE active='TRUE';"

        self.crsr.execute(sql_stmt)
        ret = self.crsr.fetchall()

        for row in ret:
            print(str(row[0]) + "    " + row[1] + "   " + row[2] + "     " + row[3])

    def add_candidate_alias( self, name, alias ):

        sql_stmt = 'SELECT candidateID, name, dateOfBirth, partyAffiliation FROM candidates ' \
                   ' WHERE name=\'' + name + '\' and active=\'TRUE\';'

        self.crsr.execute(sql_stmt)
        ret = self.crsr.fetchall()

        duplicates = []

        for row in ret:
            if( name == row[1] ):
                duplicates.append(row)

        ch = 'n'

        if( [] != duplicates ):
            print("Enter candidate ID 'n' for none.")
            for row in duplicates:
                print(str(row[0]) + "    " + row[1] + "   " + row[2] + "     " + row[3])

            ch = input(">>> ")

        try:
            candidId = int(ch, 10)

            sql_stmt = 'INSERT INTO candidateAliases(candidateID, primaryName, alias) ' \
                       'VALUES( ' + str(candidId) + ', \'' + name + '\', ' + '\'' + alias + '\' );'

            self.crsr.execute(sql_stmt)

        except:
            print('No alias added.')

    def add_candidate_to_election( self, name, state, district, date ):

        sql_stmt = 'SELECT candidateID, name, dateOfBirth, partyAffiliation FROM candidates ' \
                   ' WHERE name=\'' + name + '\' and active=\'TRUE\';'

        self.crsr.execute(sql_stmt)
        ret = self.crsr.fetchall()

        duplicates = []

        for row in ret:
            if( name == row[1] ):
                duplicates.append(row)

        ch = 'n'

        if( [] != duplicates ):
            print("Enter candidate ID of candidate to add or 'n' for none.")
            for row in duplicates:
                print(str(row[0]) + "    " + row[1] + "   " + row[2] + "     " + row[3])

            ch = input(">>> ")

            try:
                candidId = int(ch, 10)

                rowFound = False

                for row in duplicates:
                    if( candidId == row[0] ):
                        rowFound = True
                        partyAffiliation = row[3]

                if( True == rowFound ):
                    sql_stmt = "SELECT electionID electionType FROM elections WHERE " \
                               "state='" + state + "' AND district= " + \
                               str(district) + " AND electionDate=\'" + date + "\';"


                    self.crsr.execute(sql_stmt)
                    ret2 = self.crsr.fetchall()

                    print("Enter election ID of election or 'n' for none.")
                    for row in ret2:
                        print( str(row[0]) + "   " + state + "  " + district + " " + date )

                    electionFound = False

                    ch = input(">>> ")

                    for row in ret2:
                        if( int(ch, 10) == row[0] ):
                            electionId = row[0]
                            electionFound = True

                    if( True == electionFound ):
                        sql_stmt = "INSERT INTO electionCandidates( electionID, candidateID, candidateName, partyAffiliation ) " \
                                   "VALUES( " + electionId + ", " + candidateId + ", \'" + candidateName + ", \'" + partyAffiliation + "\');"

                        self.crsr.execute('BEGIN TRANSACTION;');
                        self.crsr.execute(sql_stmt);
                        self.crsr.execute('COMMIT;');

            except:
                print("Candidate not added to election.")


    def add_candidate_contact_info( candidateId, name, contactType, contactInfo ):
        #TODO: get more clever about using just the name and providing a prompt

        sql_stmt = "SELECT * FROM candidates WHERE candidateID=" + candidateId + ";"

        self.crsr.execute(sql_stmt)
        ret = self.crsr.fetchall()

        if( name == ret[0][1] ):

            sql_stmt = "INSERT INTO candidateContactInfo( candidateID, candidateName, contactType) " \
                    "VALUES( " + candidateId + ", \'" + name + "\', \'" + contactType + \
                    "\', \'" + contactInfo + "\' );"

            self.crsr.execute("BEGIN TRANSACTION;")
            self.crsr.execute(sql_stmt)
            self.crsr.execute(sql_stmt)

        else:
            print("No contact info added.")

    def get_candidate_contact_info( candidateId ):

        sql_stmt = "SELECT * FROM candidateContactInfo WHERE candidateID=" + candidateId + ";"

        self.crsr.execute(sql_stmt)
        ret = self.crsr.fetchall()

        return ret

