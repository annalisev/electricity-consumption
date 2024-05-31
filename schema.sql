DROP TABLE consumption;



CREATE TABLE consumption (
    consumption_id INT GENERATED ALWAYS AS IDENTITY,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    consumption FLOAT NOT NULL,
    time_difference VARCHAR(5) NOT NULL,
    PRIMARY KEY (consumption_id)
);