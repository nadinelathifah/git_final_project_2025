USE homeheroes12;

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




-- VIEW 2: view_reviews
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

-- TESTING:
SELECT rating, full_name, comment FROM view_reviews;



-- VIEW 2: view_client_bookings
-- The purpose of this view is to display the client booking history on the dashboard.
-- Also helpful for when they make a new booking.
CREATE VIEW view_client_bookings AS
SELECT
	jb.bookingID,
    c.clientID,
    CONCAT(c.firstname, ' ', c.lastname) AS 'client_full_name',
    t.workerID,
    CONCAT(t.firstname, ' ', t.lastname) AS 'tp_full_name',
    tk.taskID,
    tk.task_name,
    jb.booking_date,
    jb.service_start_date,
    jb.service_end_date,
    jb.task_description,
    s.statusID,
    s.status
FROM job_booking AS jb
JOIN clients AS c ON c.clientID = jb.clientID
JOIN tradespeople AS t ON t.workerID = jb.workerID
JOIN tasks AS tk ON tk.taskID = jb.taskID
JOIN job_status AS s ON s.statusID = jb.statusID
ORDER BY jb.bookingID, c.clientID, CONCAT(c.firstname, ' ', c.lastname), t.workerID, CONCAT(t.firstname, ' ', t.lastname), tk.taskID, tk.task_name, jb.booking_date, jb.service_start_date, jb.service_end_date, jb.task_description, s.statusID, s.status;

-- Display full info
SELECT * FROM view_client_bookings;

-- Display info to be shown on client dashboard
SELECT tp_full_name, task_name, booking_date, service_start_date, service_end_date, task_description, status FROM view_client_bookings;


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



-- VIEW 3: STILL IN PROGRESS PLEASE DO NOT LIGHTNING BOLT
CREATE VIEW view_booking_requests AS
SELECT
    CONCAT(c.firstname, ' ', c.lastname) AS full_name,
    tk.task_name,
    l.town,
    jb.booking_date,
    jb.service_start_date,
    DATEDIFF(jb.service_start_date, jb.service_end_date) AS working_days,
    jb.task_description
FROM job_booking AS jb 
JOIN clients AS c ON jb.clientID = c.clientID
JOIN tasks AS tk ON jb.taskID = tk.taskID
JOIN location AS l ON l.townID = jb.townID
GROUP BY CONCAT(c.firstname, ' ', c.lastname), task_name, booking_date, service_start_date, DATEDIFF(jb.service_start_date, jb.service_end_date), task_description; 
