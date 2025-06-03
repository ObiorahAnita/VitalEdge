CREATE TABLE records(
	device_id TEXT NOT NULL,
	record_time TEXT NOT NULL,
	steps INT,
	heartrate INT,
	oxygen INT,
	PRIMARY KEY (device_id, record_time)
);

CREATE TRIGGER validate_datetime_insert
BEFORE INSERT ON records
FOR EACH ROW
WHEN strftime('%Y-%m-%d %H:%M:%S', NEW.record_time) IS NULL
BEGIN
    SELECT RAISE(FAIL, 'Invalid datetime format');
END;