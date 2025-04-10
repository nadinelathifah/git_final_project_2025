show tables;

select * from tradespeople;
select * from profession;
select * from clients;

create database homeheroes1;
use homeheroes1;

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
professionID int not null primary key auto_increment,
role varchar(200),
description varchar(200)
);


show tables;
select * from location;

create table location (
townID int not null primary key auto_increment,
town_name varchar(150),
council varchar(200),
country_name varchar(150)
);


create table tradespeople (
workerID int not null primary key auto_increment,
firstname varchar(100),
lastname varchar(100),
date_of_birth date,
professionID int,
townID int,
email varchar(100),
password varchar(100),
registration_date date,
foreign key (professionID) references profession(professionID),
foreign key (townID) references location(townID)
);


create table booking (
bookingID int not null primary key auto_increment,
clientID int,
workerID int,
booking_date date, 
service_start_date date,
service_end_date date,
foreign key (clientID) references clients(clientID),
foreign key (workerID) references tradespeople(workerID)
);


INSERT INTO profession(role, description)
values ("Painting", "Applying paint or coating to walls, ceilings, and surfaces."), 
("Home Repair", "Fixing general household issues like doors, windows, or drywall."), 
("Moving", "Moving furniture, appliances, or heavy items safely."), 
("Electrician", "Fixing and installing electrical wiring, outlets and lighting."), 
("Plumbing", "Fixing and installing pipes, faucets, toilets and water systems."), 
("Lawn Care", "Maintaining outdoor vicinity by mowing, trimming, and seasonal upkeep.");


