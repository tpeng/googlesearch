drop database if exists postal_address_corpus;

create database postal_address_corpus;
use   postal_address_corpus;

create table page (
  url VARCHAR(500) not null,
  name VARCHAR(100) not null,
  html BLOB,
  text BLOB,
  country VARCHAR(100) not null,
  address VARCHAR(500) not null
) engine=innodb default charset=utf8;

CREATE INDEX page_url on page(url);