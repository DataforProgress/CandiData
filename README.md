# CandiData
A databasing tool that organizes data about candidates for Congress (and eventually other offices) into a searchable format.

# API Functions

## \_\_init\_\_( self, db\_file="./db/candidata\_db.db")

## get\_db\_version(self)

## initialize\_db(self, schema\_file="./db/schema/candidata\_schema.sql")

## update\_db(self, update\_path="./db/update\_db")

## get\_districts\_by\_state(self, state)

## add\_congressional\_election(self, date, state='ALL', district='ALL', election\_type='GENERAL')

## get\_congressional\_elections( self, state='ALL', district='ALL', date='ALL')

## add\_candidate( self, name, partyAffiliation='INDEPENDENT', dateOfBirth='None')

## update\_candidate\_info( self, name, partyAffiliation='None', dateOfBirth='None', newName='None')

## purge\_candidate( self, name )

## add\_candidate\_alias( self, name, alias )

## add\_candidate\_to\_election( self, name, state, district, date )

## add\_candidate\_contact\_info( candidateId, name, contactType, contactInfo )

## get\_candidate\_contact\_info( candidateId )
