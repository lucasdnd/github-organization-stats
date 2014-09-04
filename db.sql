CREATE SCHEMA github DEFAULT CHARSET 'utf8' COLLATE 'utf8_general_ci';

USE github;

CREATE TABLE users (
id int primary key not null auto_increment,
gh_user_id int not null unique key,
name varchar(100) not null,
created timestamp not null default current_timestamp
) engine=innodb;

CREATE TABLE repos (
id int primary key not null auto_increment,
gh_repo_id int not null unique key,
gh_repo_name varchar(100) not null,
gh_repo_description varchar(255),
created timestamp not null default current_timestamp
) engine=innodb;

CREATE TABLE contribs (
id int primary key not null auto_increment,
user_id int not null,
repo_id int not null,
w date,
a int,
d int,
c int
) engine=innodb;

CREATE TABLE punchcard (
id int primary key not null auto_increment,
repo_id int not null,
day int not null,
hour int not null,
commits int not null
) engine=innodb;

CREATE TABLE commits (
id int primary key not null auto_increment,
user_id int not null,
repo_id int not null,
sha varchar(255) not null,
message varchar(255),
a int,
d int,
t int,
created_at timestamp not null
) engine=innodb;

CREATE TABLE words (
id int primary key not null auto_increment,
sha varchar(255) not null,
word varchar(255) not null
) engine=innodb;

CREATE TABLE issues (
id int primary key not null auto_increment,
repo_id int not null,
num int not null,
title varchar(255) not null,
body varchar(255),
state varchar(50),
created_at timestamp not null,
closed_at timestamp,
created timestamp not null default current_timestamp
) engine=innodb;

CREATE USER 'gh'@'localhost' IDENTIFIED BY 'gh';
GRANT ALL ON github.* to 'gh'@'localhost';
FLUSH PRIVILEGES;

truncate table issues;
truncate table contribs;
truncate table repos;
truncate table users;
truncate table punchcard;
truncate table commits;
truncate table words;
