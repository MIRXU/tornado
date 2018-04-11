CREATE database artdb;

USE artdb;

CREATE TABLE if not EXISTS admin(
  id INT unsigned NOT NULL auto_increment KEY ,
  name VARCHAR (255),
  pad CHAR (32),
  addtime TIMESTAMP
)engine=InnoDB DEFAULT charset =utf8;

CREATE TABLE if not EXISTS tag(
  id INT unsigned NOT NULL auto_increment KEY ,
  name VARCHAR (255),
  info VARCHAR (300),
  addtime TIMESTAMP
)engine=InnoDB DEFAULT charset =utf8;

CREATE TABLE if not EXISTS art(
  id INT unsigned NOT NULL auto_increment KEY ,
  title VARCHAR (255),
  info VARCHAR (300),
  content mediumtext,
  tag int unsigned,
  img VARCHAR (255),
  addtime TIMESTAMP
)engine=InnoDB DEFAULT charset =utf8;