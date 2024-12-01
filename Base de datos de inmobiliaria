create database if not exists INMOBILIARIA;

USE INMOBILIARIA;

create table zona(
	id_zona int primary key,
    nombre_zona varchar(255) not null
    );

insert into zona(id_zona,nombre_zona) values(1,'Norte'),
											 (2,'Centro'),
                                             (3,'Sur');

create table ciudad(
	id_ciudad int primary key,
    nombre_ciudad varchar(255) not null
    );

insert into ciudad(id_ciudad,nombre_ciudad) values(1,'Sonora'),
												   (2,'CDMX'),
                                                   (3,'Oaxaca');

create table contenedora(
	id_contenedor int auto_increment primary key,
    id_zona int not null,
    id_ciudad int not null, 
    precios int not null,
    direcciones varchar(255) not null,
    dimensiones varchar(255) not null,
    foreign key(id_zona) references zona(id_zona),
	foreign key(id_ciudad) references ciudad(id_ciudad))
