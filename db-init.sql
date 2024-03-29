BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "weather_data" (
	"ID"	INTEGER UNIQUE,
	"Name"	TEXT NOT NULL UNIQUE,
	"Value"	REAL,
	"Min"	INTEGER,
	"Max"	INTEGER,
	"Low"	INTEGER,
	"High"	INTEGER,
	"Optimium"	INTEGER,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "indoor_data" (
	"ID"	INTEGER UNIQUE,
	"Name"	TEXT NOT NULL UNIQUE,
	"Value"	REAL,
	"Min"	INTEGER,
	"Max"	INTEGER,
	"Low"	INTEGER,
	"High"	INTEGER,
	"Optimium"	INTEGER,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "countdowns" (
	"ID"	INTEGER UNIQUE,
	"Name"	TEXT NOT NULL UNIQUE,
	"Date"	TEXT NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "pisystem_data" (
	"ID"	INTEGER UNIQUE,
	"Name"	TEXT NOT NULL UNIQUE,
	"Value"	REAL,
	"Min"	INTEGER,
	"Max"	INTEGER,
	"Low"	INTEGER,
	"High"	INTEGER,
	"Optimium"	INTEGER,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
COMMIT;
