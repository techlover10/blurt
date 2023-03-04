
-- basic schema for the questions i guess


CREATE TABLE clues(
			 clueid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, -- rizo mentioned synonyms maybe?
			 tier INTEGER,
			 word TEXT,
			 def TEXT
);

CREATE TABLE synonyms(
			 synonym TEXT,
			 referent INTEGER,
			 FOREIGN KEY(referent) REFERENCES clues(clueid)
);						 						
