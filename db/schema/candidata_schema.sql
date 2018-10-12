BEGIN TRANSACTION;

CREATE TABLE versionHistory(
    version INTEGER
);

CREATE TABLE candidates(
    candidateID INTEGER PRIMARY KEY, --TODO: make this autoincrement
    name VARCHAR(64),
    dateOfBirth VARCHAR(16),
    partyAffiliation VARCHAR(64),
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE candidateAliases(
    candidateID INTEGER,
    primaryName VARCHAR(64),
    alias VARCHAR(64),
    UNIQUE( candidateID, primaryName, alias )
    --FOREIGN KEY candidateID REFERENCES candidates( candidateID )
);

CREATE TABLE states(
    name VARCHAR(64),
    abbreviated VARCHAR(4),
    congressionalDistricts INTEGER
);

INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Alabama",         "AL", 7     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Alaska",          "AK", 1     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Arizona",         "AZ", 8     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Arkansas",        "AR", 4     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("California",      "CA", 53    );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Colorado",        "CO", 7     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Connecticut",     "CT", 5     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Florida",         "FL", 25    );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Georgia",         "GA", 13    );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Hawaii",          "HI", 2     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Idaho",           "ID", 1     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Illinois",        "IL", 19    );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Indiana",         "IN", 9     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Iowa",            "IA", 5     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Kansas",          "KS", 4     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Kentucky",        "KY", 6     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Louisiana",       "LA", 7     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Maine",           "ME", 2     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Maryland",        "MD", 8     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Massachussetts",  "MA", 10    );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Michigan",        "MI", 15    );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Minnesota",       "MN", 8     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Mississippi",     "MS", 4     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Missouri",        "MO", 9     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Montana",         "MT", 1     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Nebraska",        "NE", 3     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Nevada",          "NV", 3     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("New Hampshire",   "NH", 2     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("New Jersey",      "NJ", 13    );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("New Mexico",      "NM", 3     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("New York",        "NY", 29    );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("North Carolina",  "NC", 13    );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("North Dakota",    "ND", 1     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Ohio",            "OH", 18    );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Oklahoma",        "OK", 5     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Oregon",          "OR", 5     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Pennsylvania",    "PA", 19    );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Rhode Island",    "RI", 2     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("South Carolina",  "SC", 6     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("South Dakota",    "SD", 1     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Tennessee",       "TN", 9     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Texas",           "TX", 32    );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Utah",            "UT", 3     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Vermont",         "VT", 1     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Virginia",        "VA", 11    );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Washington",      "WA", 9     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("West Virginia",   "WV", 3     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Wisconsin",       "WI", 8     );
INSERT INTO states(name, abbreviated, congressionalDistricts) VALUES("Wyoming",         "WY", 1     );

CREATE TABLE elections(
    electionID INTEGER PRIMARY KEY,
    state VARCHAR(4), -- abbreviated state code
    district INTEGER,
    electionType VARCHAR(16), -- "PRIMARY", "GENERAL", "SPECIAL"
    electionDate VARCHAR(16),
    --FOREIGN KEY state REFERENCES states( abbreviated )
    UNIQUE ( state, district, electionDate )
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
    active BOOLEAN DEFAULT TRUE,
    contactPlatform VARCHAR(64),
    contactInfo VARCHAR(256)
    --FOREIGN KEY candidateID REFERENCES candidates( candidateID ),
    --FOREIGN KEY candidateName REFERENCES candidateAliases( alias )
);

COMMIT;
