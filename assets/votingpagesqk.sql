create database votingapplication;

use votingapplication;
drop table image;
create table image
(
iid int primary key auto_increment,
iim longblob not null);
drop table nominees;
create table nominees
(
ide int primary key auto_increment,
nomname varchar(50),
nomresult int
);
create table logindetails
(
logername varchar(50),
logertime varchar(50)
);
select * from image;
create table voters
(
votername varchar(50),
voterpass varchar(50)
);

#insert into nominees values (5,"krishna",3);
select * from nominees;

insert into voters values("123456789011","11/11/2023");
insert into voters values("123456789012","11/11/2023");
insert into voters values("123456789013","11/11/20231");
insert into voters values("123456789014","11/11/2023");

insert into logindetails values("rk","therla da");

select * from nominees;


