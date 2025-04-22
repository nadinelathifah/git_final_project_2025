USE homeheroes;

-- VIEW 1: view_tradespeople_by_category
-- The purpose of this view is to support the filter function for when a client searches a tradesperson by category and is shown a
-- list of profiles. And to display general reviews on the reviews webpage.
CREATE VIEW view_tradespeople_by_category AS
SELECT
    t.workerID,
    t.taskID,
    t.townID,
	CONCAT(t.firstname, ' ', t.lastname) AS full_name,
    tk.task_name,
    l.town,
    tp.phone_number,
    tp.hourly_rate,
	tp.business,
    tp.bio,
    ROUND(AVG(r.rating), 2) AS average_rating,
    COUNT(r.reviewID) AS total_reviews
FROM tradespeople AS t
JOIN tradesperson_profile AS tp ON t.workerID = tp.workerID
JOIN tasks AS tk ON t.taskID = tk.taskID
JOIN location AS l ON t.townID = l.townID
LEFT JOIN reviews AS r ON tp.tp_profileID = r.tp_profileID
GROUP BY t.workerID, t.taskID, t.townID, CONCAT(t.firstname, ' ', t.lastname), tk.task_name, l.town, tp.phone_number, tp.hourly_rate, tp.bio;

-- Display all
SELECT * FROM view_tradespeople_by_category;

-- Display all tradespeople in Livingston
SELECT * FROM view_tradespeople_by_category WHERE town = 'Livingston';

-- Display full name & equivalent task specialisation
SELECT task_name, full_name FROM view_tradespeople_by_category;

-- Display the profile of painters in livingston
SELECT * FROM view_tradespeople_by_category
WHERE task_name = 'Painting' AND town = 'Livingston'
ORDER BY hourly_rate ASC;

-- Display gardeners in bathgate
SELECT * FROM view_tradespeople_by_category
WHERE task_name = 'Lawn Care' AND town = 'Bathgate'
ORDER BY hourly_rate ASC;

SELECT * FROM job_booking;
SELECT * FROM job_booking WHERE clientID = 2 AND workerID = 1 AND statusID = 1;
UPDATE job_booking SET statusID = 2 WHERE workerID = 1 AND bookingID = 155;


-- VIEW 2: view_client_info
-- The purpose of this view is to display client's personal information in profile settings
CREATE VIEW view_client_info AS
SELECT
	c.clientID,
    c.firstname,
    c.lastname,
    CONCAT(c.firstname, ' ', c.lastname) AS 'full_name',
    l.townID,
    l.town,
    c.email
FROM clients AS c
JOIN location AS l ON c.townID = l.townID
GROUP BY c.clientID;
    
-- Display client info
SELECT * FROM view_client_info;




-- VIEW 3: view_reviews
-- The purpose of this view is to display some reviews on the 'Reviews' webpage
CREATE VIEW view_reviews AS
-- Common Table Expression (CTE) temporary result set to use in final query. 
-- Inside the CTE, you assign a "rank" to each review within each client’s group. 
WITH ranked_reviews AS (
    SELECT
        r.reviewID,
        r.rating,
        c.clientID,
        CONCAT(c.firstname, ' ', c.lastname) AS full_name,
        r.comment,
        -- ROW_NUMBER() assigns a number to each row within a group. 
        ROW_NUMBER() OVER (
			-- PARTITION BY c.clientID means group all reviews by the same client. 
            PARTITION BY c.clientID
			-- Within each client’s group, sort reviews by rating (highest first) 
            -- If two are the same, use the smallest reviewID as a tiebreaker. 
            ORDER BY r.rating DESC, r.reviewID ASC
		-- Each client’s best-rated review gets rn = 1. 
        ) AS rn
    FROM reviews AS r
    JOIN clients AS c ON r.clientID = c.clientID
)
SELECT
    reviewID,
    rating,
    clientID,
    full_name,
    comment
FROM ranked_reviews
WHERE rn = 1;

-- Display reviews:
SELECT rating, full_name, comment FROM view_reviews;




-- VIEW 4: view_past_bookings
-- The purpose of this view is to display the client booking history on the dashboard.
-- Also helpful for when they make a new booking.
CREATE VIEW view_past_bookings AS
SELECT
	jb.bookingID,
    c.clientID,
    CONCAT(c.firstname, ' ', c.lastname) AS 'client_full_name',
    t.workerID,
    CONCAT(t.firstname, ' ', t.lastname) AS 'tp_full_name',
    tk.taskID,
    tk.task_name,
    DATE_FORMAT(jb.booking_date, '%D %M %Y') AS booking_date,
    DATE_FORMAT(jb.service_start_date, '%D %M %Y') AS ss_date,
    DATE_FORMAT(jb.service_end_date, '%D %M %Y') AS se_date,
    jb.service_start_date,
    jb.task_description,
    s.statusID,
    s.status
FROM job_booking AS jb
JOIN clients AS c ON c.clientID = jb.clientID
JOIN tradespeople AS t ON t.workerID = jb.workerID
JOIN tasks AS tk ON tk.taskID = jb.taskID
JOIN job_status AS s ON s.statusID = jb.statusID
ORDER BY jb.service_start_date DESC;

-- Display full info
SELECT * FROM view_past_bookings;

-- Display info to be shown on client dashboard
SELECT booking_date, tp_full_name, task_name, service_start_date, service_end_date, task_description, status FROM view_past_bookings WHERE clientID = 1 ORDER BY booking_date;

SELECT booking_date, tp_full_name, task_name, ss_date, se_date FROM view_past_bookings WHERE clientID = 1;



-- VIEW 5: vuew_booking_requests
-- The purpose of this view is to display client booking requests (showing tradesperson's booking request history) via see_bookings URL
CREATE VIEW view_booking_requests AS
SELECT
	jb.bookingID,
    c.clientID,
    CONCAT(c.firstname, ' ', c.lastname) AS 'client_full_name',
    t.workerID,
    CONCAT(t.firstname, ' ', t.lastname) AS 'tp_full_name',
    tk.taskID,
    tk.task_name,
    DATE_FORMAT(jb.booking_date, '%D %M %Y') AS booking_date,
    DATE_FORMAT(jb.service_start_date, '%D %M %Y') AS ss_date,
    DATE_FORMAT(jb.service_end_date, '%D %M %Y') AS se_date,
    TIMEDIFF(jb.service_end_date, jb.service_start_date) AS 'total_hours',
    IF(jb.service_start_date = jb.service_end_date, TIMEDIFF(jb.service_end_date, jb.service_start_date), NULL) AS 'same_day_hours',
    IF(DATEDIFF(jb.service_end_date, jb.service_start_date) = 0, 'same day',
       DATEDIFF(jb.service_end_date, jb.service_start_date)) AS 'working_days',
    jb.service_start_date,
    jb.task_description,
    s.statusID,
    s.status
FROM job_booking AS jb
JOIN clients AS c ON c.clientID = jb.clientID
JOIN tradespeople AS t ON t.workerID = jb.workerID
JOIN tasks AS tk ON tk.taskID = jb.taskID
JOIN job_status AS s ON s.statusID = jb.statusID
ORDER BY jb.service_start_date DESC;

-- Display all
SELECT * FROM view_booking_requests;

-- Display specific columns for see_booking tradesperson page
SELECT booking_date, client_full_name, task_name, ss_date, se_date, working_days, task_description, status FROM view_booking_requests WHERE workerID = 1;


-- VIEW 6: view_personal_reviews
-- Display only the personal reviews 
CREATE VIEW view_personal_reviews AS
SELECT
    r.reviewID,
    c.clientID,
    CONCAT(c.firstname, ' ', c.lastname) AS client_full_name,
    r.tp_profileID,
    t.workerID,
    CONCAT(t.firstname, ' ', t.lastname) AS tp_full_name,
    tk.task_name,
    l.town,
    r.rating,
    r.comment,
    DATE_FORMAT(r.review_date, '%D-%M-%Y') AS rv_date,
    r.review_date
FROM reviews AS r
JOIN clients AS c ON r.clientID = c.clientID
JOIN tradesperson_profile AS tp ON r.tp_profileID = tp.tp_profileID
JOIN tradespeople AS t ON tp.workerID = t.workerID
JOIN tasks AS tk ON t.taskID = tk.taskID
JOIN location AS l ON t.townID = l.townID;

-- Display all:
SELECT * FROM view_personal_reviews;

-- Display client personal reviews
SELECT rv_date, tp_full_name, task_name, town, rating, comment FROM view_personal_reviews WHERE clientID = 13;

-- Display tradesperson personal reviews
SELECT rv_date, client_full_name, task_name, town, rating, comment FROM view_personal_reviews WHERE workerID = 14;




-- STORED PROCEDURE 1: BookJob
-- The purpose of this proc is to insert a new row in job_booking table when a client books a tradesperson.
DELIMITER //
CREATE PROCEDURE BookJob (
	IN p_clientID BIGINT,
    IN p_workerID BIGINT,
    IN p_taskID BIGINT,
    IN p_service_start DATE,
    IN p_service_end DATE,
    IN p_task_description TEXT
)

BEGIN
	INSERT INTO job_booking(clientID, workerID, taskID, service_start_date, service_end_date, task_description, statusID)
    VALUES (p_clientID, p_workerID, p_taskID, p_service_start, p_service_end, p_task_description, 1);
    
END //

DELIMITER ;

-- TESTING:
call BookJob(2, 1, 1, '2026-01-01', '2026-02-01', 'paint wall');
SELECT * from job_booking;



-- STORED PROCEDURE 2: set_tp_profile_info
-- The purpose of this proc is to insert a new row in tradesperson_profile table when a tradesperson sets up their account.
DELIMITER //
CREATE PROCEDURE set_tp_profile_info (
	IN p_workerID BIGINT,
    IN p_phone_number VARCHAR(20),
    IN p_hourly_rate DECIMAL(10,2),
    IN p_business VARCHAR(300),
    IN p_bio TEXT
)
BEGIN
	INSERT INTO tradesperson_profile(workerID, phone_number, hourly_rate, business, bio)
    VALUES (p_workerID, p_phone_number, p_hourly_rate, p_business, p_bio);
    
END //

DELIMITER ;

-- TESTING:
call set_tp_profile_info(85, '+44 1001 100001', 20.50, 'lovely lawnmowers', 'lush lush gardens');
SELECT * FROM tradesperson_profile;

