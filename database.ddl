
CREATE TABLE IF NOT EXISTS segment (
    id INTEGER PRIMARY KEY,
    operating_airline TEXT,
    marketing_airline TEXT,
    flight_number INTEGER,
    equipment TEXT,
    dep_at timestamp with time zone,
    dep_airport TEXT,
    arr_at timestamp with time zone,
    arr_airport TEXT,
    baggage TEXT
);

CREATE TABLE IF NOT EXISTS flight (
    id INTEGER PRIMARY KEY,
    duration INTEGER
);

CREATE TABLE IF NOT EXISTS flight_segment (
    id SERIAL PRIMARY KEY,
    flight_id INTEGER,
    segment_id INTEGER,
    CONSTRAINT fk_segment
                FOREIGN KEY(segment_id)
                    REFERENCES segment(id),
        CONSTRAINT fk_flight
            FOREIGN KEY(flight_id)
                REFERENCES flight(id)
);

CREATE TABLE IF NOT EXISTS booking (
    id INTEGER PRIMARY KEY,
    refundable BOOLEAN,
    validating_airline TEXT,
    total_price DECIMAL,
    currency TEXT
);


CREATE TABLE IF NOT EXISTS booking_flight (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER,
    flight_id INTEGER,
    CONSTRAINT fk_booking
                FOREIGN KEY(booking_id)
                    REFERENCES booking(id),
        CONSTRAINT fk_flight
            FOREIGN KEY(flight_id)
                REFERENCES flight(id)
);


