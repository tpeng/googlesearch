drop database if exists corpus;

create database corpus;
use corpus;

create table page (
  id MEDIUMINT not null AUTO_INCREMENT,
  name VARCHAR(100) not null,
  url VARCHAR(2046) not null,
  html BLOB,
  region VARCHAR(10) not null,
  query VARCHAR(100) not null,
  crawled DATETIME not null,
  PRIMARY KEY (id)
) engine=innodb default charset=utf8;

CREATE INDEX page_id on page(id);
CREATE INDEX page_url on page(url);