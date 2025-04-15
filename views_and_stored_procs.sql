USE homeheroes2;

CREATE VIEW view_tradespeople_by_category AS
SELECT
    t.workerID,
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
JOIN reviews AS r ON tp.tp_profileID = r.tp_profileID
GROUP BY CONCAT(t.firstname, ' ', t.lastname), tk.task_name, l.town, tp.phone_number, tp.hourly_rate, tp.bio;
    
SELECT * FROM view_tradespeople_by_category;

SELECT * FROM view_tradespeople_by_category 
WHERE task_name = 'Painting' AND town = 'Livingston'
ORDER BY hourly_rate ASC;


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


DELIMITER //
CREATE PROCEDURE getBooking ()


    