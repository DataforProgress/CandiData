BEGIN TRANSACTION;


CREATE TABLE versionHistory(
    version INTEGER
);

CREATE TABLE candidates(
    candidateID INTEGER PRIMARY KEY,
    name VARCHAR(64),
    partyAffiliation VARCHAR(64)
);

CREATE TABLE candidateAliases(
    candidateID INTEGER,
    primaryName VARCHAR(64),
    alias VARCHAR(64)
    --FOREIGN KEY candidateID REFERENCES candidates( candidateID )
);

CREATE TABLE states(
    name VARCHAR(64),
    abbreviated VARCHAR(4),
    congressionalDistricts INTEGER
);

CREATE TABLE elections(
    electionID INTEGER PRIMARY KEY,
    state VARCHAR(4), -- abbreviated state code
    district INTEGER,
    electionType VARCHAR(16), -- "PRIMARY", "GENERAL", "SPECIAL"
    electionDate VARCHAR(16)
    --FOREIGN KEY state REFERENCES states( abbreviated )
    --PRIMARY KEY ( state, district, electionDate )
);

CREATE TABLE electionCandidates(
    electionID INTEGER,
    caondidateID INTEGER,
    candidateName VARCHAR(64),
    partyAffiliation VARCHAR(64)
    --FOREIGN KEY electionID REFERENCES elections( electionID ),
    --FOREIGN KEY candidateID REFERENCES candidates( candidateID ),
    --FOREIGN KEY candidateName REFERENCES candidateAliases( alias )
);

CREATE TABLE candidateContactInfo(
    candidateID INTEGER,
    candidateName VARCHAR(64),
    contactType VARCHAR(64),
    active BOOLEAN,
    contactPlatform VARCHAR(64),
    contactInfo VARCHAR(256)
    --FOREIGN KEY candidateID REFERENCES candidates( candidateID ),
    --FOREIGN KEY candidateName REFERENCES candidateAliases( alias )
);

COMMIT;
