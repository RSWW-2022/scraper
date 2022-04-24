DROP TABLE IF EXISTS "tour";
CREATE TABLE Tour (
    id SERIAL NOT NULL,
    hotel_name varchar(255),
    region varchar(255),
    board_types varchar(255),
    transport_types varchar(255),
    departure_destinations varchar(255),
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS "flight";
CREATE TABLE Flight (
    id SERIAL NOT NULL,
    flight_date date,
    departure_destination varchar(255),
    arrival_destination varchar(255),
    number_of_seats int,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS "room";
CREATE TABLE Room (
    id SERIAL NOT NULL,
    hotel_name varchar(255),
    room_type varchar(255),
    room_date date,
    number_of_rooms int,
    PRIMARY KEY (id)
);