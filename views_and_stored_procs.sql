USE homeheroes12;

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

drop view if exists view_tradespeople_by_category;


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


DELIMITER //
CREATE PROCEDURE BookJob (
	IN p_clientID BIGINT,
    IN p_workerID BIGINT,
    IN p_taskID BIGINT,
    IN p_service_start DATE,
    IN p_service_end DATE,
    IN p_townID BIGINT,
    IN p_task_description TEXT
)

BEGIN
	INSERT INTO job_booking(clientID, workerID, taskID, service_start_date, service_end_date, townID, task_description, statusID)
    VALUES (p_clientID, p_workerID, p_taskID, p_service_start, p_service_end, p_townID, p_task_description, 1);
    
END //

DELIMITER ;


CREATE VIEW view_tp_reviews AS
SELECT
	r.reviewID,
    r.rating,
	c.clientID,
    CONCAT(c.firstname, ' ', c.lastname),
    r.comment
FROM reviews as r
JOIN clients as c ON r.clientID = c.clientID
GROUP BY r.reviewID, r.rating, c.clientID, CONCAT(c.firstname, ' ', c.lastname), r.comment;

SELECT * FROM view_tp_reviews;

SELECT * FROM view_tp_reviews ORDER BY rating DESC;


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

SELECT rating, full_name, comment FROM view_reviews;


    