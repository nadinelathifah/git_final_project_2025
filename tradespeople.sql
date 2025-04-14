CREATE DATABASE homeheroes2;
USE homeheroes2;

SHOW TABLES;

SELECT * FROM clients;

CREATE TABLE clients (
clientID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
firstname VARCHAR(100),
lastname VARCHAR(100),
date_of_birth date,
email VARCHAR(100) UNIQUE NOT NULL,
password VARCHAR(255) NOT NULL,
registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);


SELECT * FROM tasks;

CREATE TABLE tasks (
taskID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
task_name VARCHAR(200),
description VARCHAR(200)
);


SELECT * FROM location;

CREATE TABLE location (
townID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
town VARCHAR(150),
council VARCHAR(200),
country VARCHAR(150)
);


SELECT * FROM tradespeople;

CREATE TABLE tradespeople (
workerID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
firstname VARCHAR(100),
lastname VARCHAR(100),
date_of_birth date,
taskID BIGINT,
townID BIGINT,
email VARCHAR(100) UNIQUE NOT NULL,
password VARCHAR(255) NOT NULL,
registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
FOREIGN KEY (taskID) references tasks(taskID),
FOREIGN KEY (townID) REFERENCES location(townID)
);


SELECT * FROM tradesperson_profile;

CREATE TABLE tradesperson_profile (
tp_profileID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
workerID BIGINT,
phone_number VARCHAR(20),
hourly_rate decimal(10,2),
bio TEXT,
FOREIGN KEY (workerID) REFERENCES tradespeople(workerID),
UNIQUE(workerID)
);


SELECT * FROM job_status;

CREATE TABLE job_status (
statusID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
status VARCHAR(50) NOT NULL
);


SELECT * FROM job_booking;

CREATE TABLE job_booking (
bookingID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
clientID BIGINT,
workerID BIGINT,
taskID BIGINT,
booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
service_start_date DATE,
service_end_date DATE,
townID BIGINT,
task_description TEXT,
statusID BIGINT DEFAULT 1,
FOREIGN KEY (townID) REFERENCES location(townID),
FOREIGN KEY (taskID) REFERENCES tasks(taskID),
FOREIGN KEY (clientID) REFERENCES clients(clientID),
FOREIGN KEY (workerID) REFERENCES tradespeople(workerID),
FOREIGN KEY (statusID) REFERENCES job_status(statusID)
);


SELECT * FROM reviews;

CREATE TABLE reviews (
reviewID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
clientID BIGINT,
tp_profileID BIGINT,
rating INT CHECK (rating BETWEEN 1 AND 5),
comment TEXT,
review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
FOREIGN KEY (clientID) REFERENCES clients(clientID),
FOREIGN KEY (tp_profileID) REFERENCES tradesperson_profile(tp_profileID)
);


INSERT INTO location(town, council, country)
VALUES('Livingston', 'West Lothian', 'Scotland'),
('Bathgate', 'West Lothian', 'Scotland'),
('Broxburn', 'West Lothian', 'Scotland'),
('Linlithgow', 'West Lothian', 'Scotland'),
('Armadale', 'West Lothian', 'Scotland'),
('Whitburn', 'West Lothian', 'Scotland'),
('East Calder', 'West Lothian', 'Scotland'),
('West Calder', 'West Lothian', 'Scotland'),
('Blackburn', 'West Lothian', 'Scotland'),
('Polbeth', 'West Lothian', 'Scotland'),
('Kirknewton', 'West Lothian', 'Scotland'),
('Uphall', 'West Lothian', 'Scotland'),
('Winchburgh', 'West Lothian', 'Scotland'),
('Dechmont', 'West Lothian', 'Scotland'),
('Seafield', 'West Lothian', 'Scotland');

INSERT INTO tasks(task_name, description)
values ("Painting", "Applying paint or coating to walls, ceilings, and surfaces."), 
("Home Repair", "Fixing general household issues like doors, windows, or drywall."), 
("Moving", "Moving furniture, appliances, or heavy items safely."), 
("Electrician", "Fixing and installing electrical wiring, outlets and lighting."), 
("Plumbing", "Fixing and installing pipes, faucets, toilets and water systems."), 
("Lawn Care", "Maintaining outdoor vicinity by mowing, trimming, and seasonal upkeep.");

INSERT INTO job_status(status)
VALUES ('pending'),
('accepted'),
('in progress'),
('completed'),
('cancelled');
