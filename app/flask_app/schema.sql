DROP TABLE IF EXISTS secret;

CREATE TABLE secret
(
    hashText TEXT PRIMARY KEY,
    secretMessage TEXT NOT NULL,
    retrievalCount INT NOT NULL,
    expiration INT NOT NULL
);

