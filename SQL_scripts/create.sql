DROP TABLE IF EXISTS tour;
DROP TABLE IF EXISTS flight;
DROP TABLE IF EXISTS room_availability;
DROP TABLE IF EXISTS room;

CREATE TABLE tour (
    tour_id SERIAL NOT NULL,
    hotel_name VARCHAR(255),
    region VARCHAR(255),
    own_transport BOOLEAN,
    board_types VARCHAR(255),
    PRIMARY KEY (tour_id)
);

CREATE TABLE flight (
    flight_id SERIAL NOT NULL,
    flight_date DATE,
    departure_destination VARCHAR(255),
    arrival_destination VARCHAR(255),
    number_of_seats INT,
    PRIMARY KEY (flight_id)
);

CREATE TABLE room (
    room_id SERIAL NOT NULL,
    hotel_name VARCHAR(255),
    room_type VARCHAR(255),
    PRIMARY KEY (room_id)
);

CREATE TABLE room_availability (
    room_availability_id SERIAL NOT NULL,
    room_id INT REFERENCES room(room_id),
    date DATE,
    PRIMARY KEY (room_availability_id)
);

