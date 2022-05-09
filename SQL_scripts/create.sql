DROP TABLE IF EXISTS tour;
DROP TABLE IF EXISTS flight;
DROP TABLE IF EXISTS room_availability;
DROP TABLE IF EXISTS room_offer;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS offer;

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

CREATE TABLE offer (
    offer_id SERIAL NOT NULL,
    user_id VARCHAR(255),
    num_of_adult INT,
    num_of_children_3 INT,
    num_of_children_10 INT,
    num_of_children_18 INT,
    board_type VARCHAR(255),
    own_transport BOOLEAN,
    is_paid_off BOOLEAN,
    tour_id INT REFERENCES tour(tour_id),
    first_flight_id INT REFERENCES flight(flight_id),
    second_flight_id INT REFERENCES flight(flight_id),
    PRIMARY KEY (offer_id)
);

CREATE TABLE room_offer (
    room_offer_id SERIAL NOT NULL,
    room_id INT REFERENCES room(room_id),
    offer_id INT REFERENCES offer(offer_id),
    PRIMARY KEY (room_offer_id)
);

