create database tradespeopledb;
use tradespeopledb;

create table clients (
ClientID int not null primary key auto_increment,
firstname varchar(100),
lastname varchar(100),
email varchar(100),
password varchar(100)
);
