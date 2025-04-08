create database tradespeopledb;
use tradespeopledb;

create table clients (
clientID int not null primary key auto_increment,
firstname varchar(100),
lastname varchar(100),
date_of_birth date,
email varchar(100),
password varchar(100),
registration_date date
);

create table profession (
ProfessionID int not null primary key auto_increment,
role varchar(200),
description varchar(200)
);

create table tradespeople (
WorkerID int not null primary key auto_increment,
firstname varchar(100),
lastname varchar(100),
date_of_birth date,
ProfessionID int,
town varchar(150),
email varchar(100),
password varchar(100),
registration_date date,
foreign key (ProfessionID) references profession(ProfessionID)
);


INSERT INTO profession(role, description)
values ("Painting", "Applying paint or coating to walls, ceilings, and surfaces."), 
("Home Repair", "Fixing general household issues like doors, windows, or drywall."), 
("Assembly & Installation", "Assembling furniture and installing home fixtures and appliances."), 
("Transportation", "Moving furniture, appliances, or heavy items safely."), 
("Electrician", "Fixing and installing electrical wiring, outlets and lighting."), 
("Cleaning", "Cleaning and maintaining homes, offices, or other spaces."),
("Plumbing", "Fixing and installing pipes, faucets, toilets and water systems."), 
("Lawn Care", "Maintaining outdoor vicinity by mowing, trimming, and seasonal upkeep.");


