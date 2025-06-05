CREATE TABLE records(
	device_id TEXT NOT NULL,
	record_date TEXT NOT NULL,
	steps INT,
	heartrate REAL,
	avg_heartrate REAL,
	peak_heartrate REAL,
	oxygen REAL,
	avg_oxygen REAL,
	humidity REAL,
	avg_humidity REAL,
	temp REAL,
	avg_temp REAL,
	co2 INT,
	avg_co2 INT,
	lat REAL,
	lon REAL,
	emerg INT CHECK (emerg IN (0, 1)),
	PRIMARY KEY (device_id, record_date)
);

CREATE TRIGGER validate_datetime_insert
BEFORE INSERT ON records
FOR EACH ROW
WHEN strftime('%Y-%m-%d', NEW.record_date) IS NULL
BEGIN
    SELECT RAISE(FAIL, 'Invalid date format');
END;

CREATE TRIGGER validate_datetime_update
BEFORE UPDATE ON records
FOR EACH ROW
WHEN strftime('%Y-%m-%d', NEW.record_date) IS NULL
BEGIN
    SELECT RAISE(FAIL, 'Invalid date format');
END;