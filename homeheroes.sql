CREATE DATABASE homeheroes10;
USE homeheroes10;

drop database if exists homeheroes9;


SHOW TABLES;
SELECT * FROM location;

CREATE TABLE location (
townID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
town VARCHAR(150),
council VARCHAR(200),
country VARCHAR(150)
);

SELECT * FROM clients;

CREATE TABLE clients (
clientID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
firstname VARCHAR(100),
lastname VARCHAR(100),
date_of_birth date,
townID BIGINT,
email VARCHAR(100) UNIQUE NOT NULL,
password VARCHAR(255) NOT NULL,
registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
FOREIGN KEY (townID) REFERENCES location(townID)
);

SELECT * FROM tasks;

CREATE TABLE tasks (
taskID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
task_name VARCHAR(200),
description VARCHAR(200)
);

SELECT * FROM tradespeople;

CREATE TABLE tradespeople (
workerID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
firstname VARCHAR(100),
lastname VARCHAR(100),
date_of_birth date,
taskID BIGINT,
townID BIGINT,
email VARCHAR(100) UNIQUE NOT NULL,
password VARCHAR(255) NOT NULL,
registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
FOREIGN KEY (taskID) references tasks(taskID),
FOREIGN KEY (townID) REFERENCES location(townID)
);


SELECT * FROM tradesperson_profile;

CREATE TABLE tradesperson_profile (
tp_profileID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
workerID BIGINT,
phone_number VARCHAR(20),
hourly_rate DECIMAL(10,2),
business VARCHAR(300),
bio TEXT,
FOREIGN KEY (workerID) REFERENCES tradespeople(workerID),
UNIQUE(workerID)
);


SELECT * FROM job_status;

CREATE TABLE job_status (
statusID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
status VARCHAR(50) NOT NULL
);


SELECT * FROM job_booking;

CREATE TABLE job_booking (
bookingID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
clientID BIGINT,
workerID BIGINT,
taskID BIGINT,
booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
service_start_date DATE,
service_end_date DATE,
task_description TEXT,
statusID BIGINT DEFAULT 1,
FOREIGN KEY (taskID) REFERENCES tasks(taskID),
FOREIGN KEY (clientID) REFERENCES clients(clientID),
FOREIGN KEY (workerID) REFERENCES tradespeople(workerID),
FOREIGN KEY (statusID) REFERENCES job_status(statusID)
);


SELECT * FROM reviews;

CREATE TABLE reviews (
reviewID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
clientID BIGINT,
tp_profileID BIGINT,
rating INT CHECK (rating BETWEEN 1 AND 5),
comment TEXT,
review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
FOREIGN KEY (clientID) REFERENCES clients(clientID),
FOREIGN KEY (tp_profileID) REFERENCES tradesperson_profile(tp_profileID)
);


INSERT INTO location(town, council, country)
VALUES('Livingston', 'West Lothian', 'Scotland'),
('Bathgate', 'West Lothian', 'Scotland'),
('Broxburn', 'West Lothian', 'Scotland'),
('Armadale', 'West Lothian', 'Scotland'),
('Whitburn', 'West Lothian', 'Scotland'),
('East Calder', 'West Lothian', 'Scotland'),
('West Calder', 'West Lothian', 'Scotland'),
('Uphall', 'West Lothian', 'Scotland');


INSERT INTO tasks(task_name, description)
values ("Painting", "Applying paint or coating to walls, ceilings, and surfaces."), 
("Home Repair", "Fixing general household issues like doors, windows, or drywall."), 
("Moving", "Moving furniture, appliances, or heavy items safely."), 
("Electrician", "Fixing and installing electrical wiring, outlets and lighting."), 
("Plumbing", "Fixing and installing pipes, faucets, toilets and water systems."), 
("Lawn Care", "Maintaining outdoor vicinity by mowing, trimming, and seasonal upkeep.");

INSERT INTO job_status(status)
VALUES ('pending'),
('accepted'),
('in progress'),
('completed'),
('cancelled');


INSERT INTO tradespeople (firstname, lastname, date_of_birth, taskID, townID, email, password, registration_date)
VALUES ('Lucy', 'Lacquer', '1991-06-12', 1, 1, 'lucy@edc.com', '$2b$12$l4GKZcdsmgvp9pG.6O42z.VEIzosl3whBdB8CkMTTp4l9Bok4RSs2', '2005-03-31'),
('Anita', 'Brush', '1985-11-03', 1, 6, 'anita@edc.com', '$2b$12$By9nQmXOVL5al7P5Hym1ceXbBzdCrfFNTau.A9lCLOjVpiQNI1gvO', '2006-09-25'),
('Matt', 'Finish', '1999-04-22', 1, 2, 'matt@nuwalls.com', 'mattfinish123', '2006-03-16'),
('Rick', 'O''Shade', '1990-02-17', 1, 4, 'rick-@nuwalls.com', 'rickie123', '2006-07-03'),
('Annie', 'Gloss', '1987-08-29', 1, 2, 'annie@nodram.com', 'annie123', '2006-08-21'),
('Wett', 'Stain', '1995-12-10', 1, 3, 'wett@nodram.com', 'stains123', '2006-06-20'),
('Wally', 'Wonka', '1979-03-04', 1, 1, 'wally@brushandhammer.com', 'wally123', '2006-03-18'),
('Paige', 'Roller', '1983-09-16', 1, 3, 'paige@caseydecorating.com', 'paige123', '2006-12-08'),
('Hue', 'Jackman', '1996-01-08', 1, 1, 'hue@gtipainting.com', 'huehue123', '2006-07-04'),
('Dusty', 'Sanders', '1988-07-24', 1, 4, 'dusty@dunbarpanting.com', 'dusty123', '2007-03-31'),
('Tessa', 'Texture', '1992-05-30', 1, 6, 'tessa@caseydecorating.com', 'tessa123', '2007-04-03'),
('Daisy', 'Tint', '2001-10-14', 1, 8, 'daisy@wcdecorators.com', 'daisy123', '2007-03-19'),
('Vinny', 'Varnish', '1994-03-19', 1, 8, 'vinny@prodec.com', 'vinny123', '2007-03-30'),
('Gloria', 'Coates', '1980-12-01', 1, 5, 'gloria@grayandsons.com', 'gloria123', '2007-09-07'),
('Paula', 'Paper', '1998-06-26', 1, 7, 'paula@swishdecorators.com', 'paula123', '2007-03-23'),
('Manny', 'Patterns', '1986-02-09', 1, 5, 'manny@grayandsons.com', 'manny123', '2007-12-17'),
('Penny', 'Petals', '2003-01-08', 6, 1, 'penny@kingsburylawncare.com', 'penny123', '2024-01-01'),
('Chloe', 'Clover', '2001-09-30', 6, 2, 'chloe@acorngardening.com', 'chloe123', '2024-01-15'),
('Rosemary', 'Greene', '1996-09-08', 6, 3, 'rosemary@bilawncare.com', 'rosemary123', '2024-01-25'),
('Chris', 'Hedges', '1994-03-10', 6, 5, 'chris@stewartgardening.com', 'chris123', '2024-02-05'),
('Jack', 'Sprout', '1999-07-22', 6, 1, 'jack@kingsburylawncare.com', 'jackie123', '2024-02-20'),
('Faye', 'Fern', '1995-07-28', 6, 7, 'faye@edengardening.com', 'ferns123', '2024-03-01'),
('Hank', 'Greenhouse', '1982-05-30', 6, 8, 'hank@lieverlandscapes.com', 'hankie123', '2024-03-10'),
('Vera', 'Vines', '1986-06-20', 6, 6, 'vera@bcstrees.com', 'vines123', '2024-03-25'),
('Luke', 'Bush', '1998-01-13', 6, 6, 'luke@bcstrees.com', 'bushie123', '2024-04-05'),
('Pat', 'Lawnmore', '1987-09-13', 6, 3, 'Pat@greenthumbcarlisle.com', 'lawnie123', '2024-04-15'),
('Misty', 'Moss', '1991-01-11', 6, 5, 'misty@humbiefencing.com', 'misty123', '2024-05-01'),
('Charlotte', 'Shrubsworth', '2004-03-13', 6, 1, 'charlotte@groundcare.com', 'charlotte123', '2024-05-10'),
('Cameron', 'Sprinkler', '1998-05-18', 6, 2, 'cameron@acorngardening.com', 'cameron123', '2024-06-01'),
('Poppy', 'Moore', '2002-02-21', 6, 4, 'poppy@wksolutions.com', 'poppy123', '2024-07-01'),
('Olive', 'Bloomfield', '1997-02-16', 6, 4, 'olive@gardenbros.com', 'olive123', '2024-10-01'),
('Tommy', 'Tulip', '1983-04-29', 6, 7, 'tommy@mwgardening.com', 'tommy123', '2025-04-01'),
('David', 'Dunn', '1982-05-06', 3, 7, 'david.dunn@upliftlogistics.com', 'david123', '2024-06-20'),
('Sean', 'Hill', '1981-06-01', 3, 8, 'sean.hill@atlashaulers.com', 'sean123', '2023-02-20'),
('Sheila', 'Mcintosh', '1999-10-12', 3, 8, 'sheila.mcintosh@packmasters.com', 'sheila123', '2023-08-22'),
('Kimberly', 'Martin', '1997-04-19', 3, 1, 'kimberly.martin@titantransit.com', 'kimberly123', '2023-12-08'),
('Candace', 'Thomas', '1988-11-09', 9, 3, 'candace.thomas@rocketrelocations.com', 'candace123', '2023-09-02'),
('Nathan', 'Garcia', '1991-04-10', 3, 5, 'nathan.garcia@boldmovehaulers.com', 'nathan123', '2024-09-29'),
('Seth', 'Warner', '1987-12-02', 3, 8, 'seth.warner@silverlineshifters.com', 'seth123', '2024-09-20'),
('Rebecca', 'Lane', '2000-06-20', 3, 3, 'rebecca.lane@silverlineshifters.com', 'rebecca123', '2024-02-01'),
('Monica', 'Wolf', '1998-02-08', 3, 1, 'monica.wolf@metromaxrelocations.com', 'monica123', '2024-07-20'),
('Danielle', 'Collins', '1996-12-02', 3, 8, 'danielle.collins@rocketrelocations.com', 'danielle123', '2024-12-22'),
('Nicole', 'West', '1996-10-11', 3, 8, 'nicole.west@firstclassfreight.com', 'nicole123', '2024-04-15'),
('Kaitlyn', 'Rivera', '1984-10-03', 3, 5, 'kaitlyn.rivera@anchorwavemovers.com', 'kaitlyn123', '2023-04-17'),
('Anthony', 'Reed', '1994-03-07', 3, 4, 'anthony.reed@boldmovehaulers.com', 'anthony123', '2024-11-13'),
('Bryan', 'Barrett', '1983-03-02', 3, 2, 'bryan.barrett@urbantrekrelocations.com', 'bryan123', '2024-02-04'),
('Michael', 'Rice', '1984-09-02', 3, 6, 'michael.rice@summithauling.com', 'michael123', '2023-09-01'),
('Daniel', 'Deleon', '2002-12-12', 3, 7, 'daniel.deleon@urbantrekrelocations.com', 'daniel123', '2024-04-29'),
('Matthew', 'Bray', '1994-11-10', 3, 7, 'matthew.bray@peakpointmovers.com', 'matthew123', '2023-08-08');


INSERT INTO tradesperson_profile (workerID, phone_number, hourly_rate, business, bio)
VALUES (1, '+44 7392-647595', 28.75, 'EDC Painters', 'Hi there! I''m Lucy, and I live for vibrant, flawless finishes. I bring passion and precision to every paint job, transforming your space into a work of art.'),
(2, '+44 7392-647595', 24.60, 'EDC Painters', 'Let’s get to work! Anita here, and I believe in precision with every brushstroke. Whether it’s wallpaper removal or a fresh coat, I make sure your walls are done right.'),
(3, '+44 7894-267044', 26.30, 'Nu-Walls', 'Looking for a smooth, perfect finish? I’m Matt, and I’ll take care of your walls with expertise and attention to detail. No imperfections here, just sleek surfaces.'),
(4, '+44 1501-730457', 23.90, 'Nu-Walls', 'Want your house to look like it’s in the spotlight? Rick O’Shade here, and I specialize in exterior painting that’ll have your home shining brighter than the sun on a summer day. Let’s add some curb appeal!'),
(5, '+44 1506-633333', 25.45, 'Nodram Decorators', 'Got walls that need glowing? Annie Gloss here, and I’m here to make your interiors sparkle! Let’s add a touch of shine to your space and make your home the gloss of the block.'),
(6, '+44 1463-418015', 27.10, 'Nodram Decorators', 'Let’s get to the root of the matter. Wett Stain here, and I bring out the richness of every surface with a deep, lasting stain. Whether it’s wood or stone, I’ll make it look wet with color and charm.'),
(7, '+44 7496-635174', 29.25, 'Brush & Hammer', 'Step into my candy-colored world! Wally Wonka here, where every wallpaper I install is like a golden ticket to a wall of wonders. From whimsical designs to classy looks, I’ve got something sweet for every space.'),
(8, '+44 7467-399011', 26.80, 'Casey Decorating', 'Roll with the best! Paige Roller here, and when it comes to even coats, I’m the roll model you need. Let me smooth out your space and give it that perfect, professional finish.'),
(9, '+44 1506-494932', 28.20, 'GTI Painting & Decorating', 'Let’s color outside the lines! Hue Jackman, the wall hero, at your service. With my expert color consultations, I’ll help you choose the perfect shade to take your home from dull to dynamic!'),
(10, '+44 7590-614411', 24.25, 'A. Dunbar Painter & Decorator', 'Need a little dusting off? Dusty Sanders here! I’ve been around the block a few times, and I’ll bring your walls back to life with an impeccable paint job that’ll have your space looking sharp, fresh, and brand-new.'),
(11, '+44 7467-399011', 23.75, 'Casey Decorating', 'Looking for layers of beauty? Tessa Texture here, and I specialize in adding dimension and depth to your walls with the perfect textures. It’s time to give your space some tactile charm!'),
(12, '+44 7864-366748', 25.90, 'W C Decorators', 'Let’s tint your world beautiful! Daisy Tint here, and I’ve got the perfect shades for your walls that will make your space feel like a blooming garden. Ready for a fresh new look?'),
(13, '+44 1506-890892', 26.10, 'Prodec', 'Let’s make your surfaces shine brighter than your future! Vinny Varnish here, bringing the best finish to your woodwork. No more dull corners, just beautifully polished perfection.'),
(14, '+44 1324-632418', 22.95, 'Gray & Sons', 'You deserve the best coat in town! Gloria Coates here, ready to help you pick out and install the finest wallpaper to give your space a sophisticated touch. Quality and craftsmanship that’s been around for decades!'),
(15, '+44 7584-902930', 24.10, 'Swish Decorators', 'Time to get your walls looking paper-perfect! Paula Paper here, with premium wallpaper designs that’ll make your room feel like a masterpiece. You’ll love every inch of it!'),
(16, '+44 1324-632418', 23.30, 'Gray & Sons', 'Pattern perfection? You’ve got it! Manny Patterns here, bringing you bold, beautiful designs that’ll make your walls the talk of the town. No more boring walls—let’s create something unforgettable!'),
(17, '+44 1827-826123', 24.90, 'Kingsbury Lawn Care', 'Does your garden need a little tending? I''m here, ready to fill your space with delicate blooms and lush greenery.'),
(18, '+44 7796-624310', 23.80, 'Acorn Garden Services', 'Your garden deserves the luck of the Irish. Here to bring charm, color, and a little green magic to your outdoor space!'),
(19, '+44 7539-995053', 24.30, 'Blue Iris Lawn Care Ltd', 'Here to help you grow the garden of your dreams, from aromatic herbs to vibrant flowerbeds—your outdoor space will be fragrant and full of life!'),
(20, '+44 1506-870949', 22.75, 'Stewart Garden Services', 'Looking for reliable, expert care for your hedges and yard? Chris Hedges here, ready to shape and maintain your outdoor space with precision and care, making sure your garden always looks its best.'),
(21, '+44 1827-826123', 25.00, 'Kingsbury Lawn Care', 'Got weeds popping up where they don’t belong? I’ll root ''em out and give your garden room to grow.'),
(22, '+44 1313-335295', 23.40, 'Eden Garden Services', 'Let’s transform your yard into a lush oasis. I’m here to give your plants the care they need to thrive!'),
(23, '+44 1875-821621', 23.95, 'Liever Landscapes', 'No garden too big or small—I''ll make sure your plants thrive, and your yard stays looking strong and healthy.'),
(24, '+44 1313-346800', 24.10, 'B C S Trees', 'Let’s get your vines climbing and your yard lush. I’ll bring your climbing plants to life with expert care.'),
(25, '+44 1313-346800', 23.85, 'B C S Trees', 'Ready to give your yard the attention it deserves? I’ll handle the hard work so you can enjoy a well-kept, vibrant outdoor space.'),
(26, '+44 1313-227314', 24.50, 'Greenthumb Carlisle', 'From mowing stripes to crisp edges—I don’t just cut grass, I give lawns a fresh haircut with pride.'),
(27, '+44 1506-885171', 22.90, 'Humbie Fencing', 'Add some natural charm to your yard. I’ll create a beautiful green space with moss and thoughtful landscaping.'),
(28, '+44 1506-429118', 24.75, 'Groundcare Scotland Ltd', 'Creating a perfect backyard retreat one shrub at a time. Let’s turn your yard into a cozy, vibrant space.'),
(29, '+44 7796-624310', 23.60, 'Acorn Garden Services', 'Keeping your greens quenched and blooming. Sprinklers, hoses, or hands-on care—I’ve got watering down to a science.'),
(30, '+44 1324-804102', 22.50, 'Wise Knotweed Solutions', 'I''m Poppy and my work is a national treasure. I’ll turn your outdoor space into a blooming beauty.'),
(31, '+44 7495-234871', 22.80, 'Garden Bros', 'Bringing lush greenery and blooming beauty to your garden. I’ll help you create a peaceful retreat with vibrant plants.'),
(32, '+44 1506-834109', 23.20, 'Martin Watt Gardens', 'Need a hand with your garden? I’ll get it looking sharp and organized—strong, reliable care that lets your space shine.'),
(35, '+44 7620 567 890', 28.75, 'Uplift Logistics', 'Need a move that\'s fast and flawless? I\'m David, and I’ll handle your relocation with the care and energy it deserves. Let’s get you moving!'),
(36, '+44 7709 234 567', 24.60, 'Atlas Haulers', 'Hey there! I\'m Sean, your go-to for stress-free moves. I make relocating smooth, swift, and simple — your belongings are in expert hands!'),
(37, '+44 7561 123 987', 26.30, 'PackMasters', 'Hi! Sheila here — moving isn’t just a job; it\'s my passion. I make transitions easy, treating every item as if it’s my own.'),
(38, '+44 7420 987 654', 23.90, 'Titan Transit', 'Hi! Kimberly here — moving isn’t just a job; it\'s my passion. I make transitions easy, treating every item as if it’s my own.'),
(39, '+44 7799 876 543', 25.45, 'Rocket Relocations', 'Hi! Candace here — moving isn’t just a job; it\'s my passion. I make transitions easy, treating every item as if it’s my own.'),
(40, '+44 7623 489 230', 27.10, 'BoldMove Haulers', 'Hey there! I\'m Nathan, your go-to for stress-free moves. I make relocating smooth, swift, and simple — your belongings are in expert hands!'),
(41, '+44 7754 123 987', 29.25, 'SilverLine Shifters', 'Hey there! I\'m Seth, your go-to for stress-free moves. I make relocating smooth, swift, and simple — your belongings are in expert hands!'),
(42, '+44 7609 876 543', 26.80, 'SilverLine Shifters', 'Ready to roll? I\'m Rebecca, and moving day is my specialty. From packing to unpacking, I’ll get your treasures safely to their new home.'),
(43, '+44 7901 345 678', 25.90, 'MetroMax Relocations', 'Need a move that\'s fast and flawless? I\'m Monica, and I’ll handle your relocation with the care and energy it deserves. Let’s get you moving!'),
(44, '+44 7832 234 567', 25.10, 'Rocket Relocations', 'Need a move that\'s fast and flawless? I\'m Danielle, and I’ll handle your relocation with the care and energy it deserves. Let’s get you moving!'),
(45, '+44 7712 345 678', 22.95, 'FirstClass Freight', 'Hey there! I\'m Nicole, your go-to for stress-free moves. I make relocating smooth, swift, and simple — your belongings are in expert hands!'),
(46, '+44 7654 987 654', 24.10, 'AnchorWave Movers', 'Looking for a reliable mover? I\'m Kaitlyn, and I know how to turn moving day into a smooth and stress-free experience. Let’s make it happen!'),
(47, '+44 7745 890 123', 22.75, 'BoldMove Haulers', 'Ready to roll? I\'m Anthony, and moving day is my specialty. From packing to unpacking, I’ll get your treasures safely to their new home.'),
(48, '+44 7534 789 012', 25.00, 'Urban Trek Relocations', 'Ready to roll? I\'m Bryan, and moving day is my specialty. From packing to unpacking, I’ll get your treasures safely to their new home.'),
(49, '+44 7823 678 901', 23.40, 'Summit Hauling', 'Need a move that\'s fast and flawless? I\'m Michael, and I’ll handle your relocation with the care and energy it deserves. Let’s get you moving!'),
(50, '+44 7412 567 890', 23.95, 'Urban Trek Relocations', 'Need a move that\'s fast and flawless? I\'m Daniel, and I’ll handle your relocation with the care and energy it deserves. Let’s get you moving!'),
(51, '+44 7701 456 789', 24.75, 'PeakPoint Movers', 'Need a move that\'s fast and flawless? I\'m Matthew, and I’ll handle your relocation with the care and energy it deserves. Let’s get you moving!');


INSERT INTO clients (firstname, lastname, date_of_birth, townID, email, password, registration_date)
VALUES ('Miranda', 'Fanta', '1999-04-22', 1, 'miranda@gmail.com', '$2b$12$oLZGoyy/usxIaevDg5VTtOaoeBcVgoYirqdbMZm16kzi.VVIpU4A2', '2000-01-01'),
('Nadine', 'Vimto', '1997-01-08', 1, 'nadine@gmail.com', '$2b$12$KDLed2NMC6s/1x3kI7CVgu4XM0Mkou7fMePfHUEBM.qRLgsKIVelK', '2000-01-05'),
('Liya', 'Pepsi', '2002-02-21', 1,  'liya@gmail.com', '$2b$12$lM1OMgQSqiVQWZclujOxGOu20znOzFv3kkk5/jpgAeYBPQOR3HIrq', '2000-01-03'),
('Malvina', 'Cola', '2001-09-30', 1, 'malvina@gmail.com', '$2b$12$qj2CgpTx4Ub22zUYkhqCgODPg4OtbHR9nLWqd9Qh2llB.nUK9Xlmy', '2000-01-04'),
('Ayishat', 'Sprite', '1998-06-26', 1, 'ayishat@gmail.com', '$2b$12$k2CNP06eWduhT5zyhEP9ee/OeHt8Qyj3GIIFXxSoPAEyrNhRSWyN2', '2000-01-02'),
('Ailsa', 'Stewart', '1981-07-22', 2, 'ailsa@gmail.com', '$2b$12$v30ro78rF4NBBy5UM3sklODXRR/jbShVRCoyan0JxDWfMnRfTLaM.', '2000-01-06'),
('Angus', 'Murray', '1973-04-29', 3, 'angus@gmail.com', '$2b$12$LODremmPYZehdvW9aEEF6ekajYDvvSlOXxoB8.E5exJJd4A0Vfe7S', '2000-01-07'),
('Kirsty', 'Sinclair', '1986-06-20', 4, 'kirsty@gmail.com', '$2b$12$tSvlTi6Q7nkoU/Sy8A.g.utVhCNrAn69kq649UslFzGWxqam3y5wa', '2000-01-08'),
('Rory', 'Campbell', '1996-01-08', 5, 'rory@gmail.com', '$2b$12$XoqMtGn5eGu6v6KIJdtY3uOPII810ZcrevswJhkNXhhEum.rwdRKS', '2000-01-09'),
('Fiona', 'MacLeod', '1994-03-13', 6, 'fiona@gmail.com', '$2b$12$fjBAyW6hlCfRg4MshxTRhOn1H/tktria4f8xCJJL1ijyQV7lOY4gq', '2000-01-10'),
('Iain', 'Wallace', '1970-12-01', 2, 'iain@gmail.com', '$2b$12$ZyFxIlUXBx6gBn7RiKF2xepwth9OKuHs/KjrD8qYfJNiicnfaG.6i', '2000-01-13'),
('Skye', 'MacPherson', '1988-07-24', 8, 'skye@gmail.com', '$2b$12$wwsYCsXlPRtD53Bsu89LeeVnAnQTkikJKSmRuXKCHoMohoe4hp4Ha', '2000-01-12'),
('Finlay', 'McArthur', '2000-03-13', 2, 'finlay@gmail.com', '$2b$12$1DT6uvCD9WulCVAheoVtY.hOnDqBD82usbXQ3XtWPOEajBMt90Z6u', '2000-01-13'),
('Lachlan', 'Fraser', '1983-11-28', 3, 'lachlan@gmail.com', '$2b$12$5ZXeuWPSCYuvve9UoBuJk.uB.WE/LPJk2IRUGgeCgAzFiIUhmZycu', '2000-01-14'),
('Isla', 'Buchanan', '2003-05-13', 4, 'isla@gmail.com', '$2b$12$e74zoQ6WYDCWUkIn5c1teudTpzdbXrSbBfHVqypw0jBAM6uoWn3Mu', '2000-01-15');

select * from clients;


-- Reviews for Painting Services -- 
INSERT INTO reviews (clientID, tp_profileID, rating, comment, review_date) 
VALUES (1, 1, 5, "Lucy did an amazing job with our interior painting. She has such an eye for detail, and the finish was flawless. Our living room looks like a brand new space! Highly recommend!", '2008-03-15'),
(2, 1, 5, "Lucy helped us with a color consultation, and we couldn’t be happier with her recommendations! She really listened to our preferences and guided us toward the perfect shades for our home. The space looks incredible, and the atmosphere is so much warmer and inviting now.", '2008-06-22'),
(10, 2, 5, "Anita was fantastic with the wallpaper removal in our bedroom. She worked efficiently, and there wasn’t a speck of mess left behind. Very professional and easy to communicate with. Thank you, Anita!", '2008-09-30'),
(10, 2, 4, "Anita recently assisted us with recoating the walls in our hallway, and the result is fantastic! She made sure every corner was covered, and the walls look smooth and flawless. We were impressed with her professionalism and care, and will definitely hire her again!", '2008-12-08'),
(6, 3, 5, "Matt really transformed our kitchen with his drywall repair and fresh coat of paint. The quality of work is top-notch, and the entire process was smooth from start to finish. Extremely satisfied!", '2009-02-11'),
(13, 3, 5, "Matt took care of our exterior painting, and the job turned out amazing. His attention to detail was top-notch, and he made sure to carefully cover every inch. We were really impressed with how neat and professional the work looked in the end.", '2009-04-18'),
(8, 4, 5, "Rick's work on the exterior painting of our house was outstanding. He was punctual, professional, and the attention to detail was perfect. Our house now has a fresh new look, and we couldn't be happier!", '2009-07-05'),
(15, 4, 4, "Rick did a beautiful job with our fence painting. He paid close attention to every detail, ensuring that the entire surface was evenly painted. The finish is flawless, and we’re so pleased with how much better our yard looks now.", '2009-10-09'),
(13, 5, 5, "Annie’s work is incredible! She helped us with a complete re-coating of the walls in our living room and even provided us with expert advice on color selection. The space looks vibrant and refreshed. Highly recommend her services!", '2010-01-27'),
(6, 5, 5, "Annie helped us select the perfect colors for our new office space, and the results are stunning! She provided expert advice, and the room now feels fresh, vibrant, and inspiring. She truly understands how color affects mood and space.", '2010-03-14'),
(7, 6, 4, "Wett did a fantastic job on our concrete wall painting. The results were beyond what we expected, and his expertise showed in every brushstroke. We couldn’t be more pleased!", '2010-05-19'),
(14, 6, 5, "Wett was fantastic when it came to staining our wooden deck. The finish is smooth, even, and has really brought out the natural beauty of the wood. His expertise in staining was clear, and the transformation is beautiful!", '2010-08-03'),
(3, 7, 5, "Wally was a joy to work with! He helped us pick out a beautiful premium wallpaper design for our dining room, and the installation was perfect. We love how it complements our furniture. Excellent job!", '2010-11-20'),
(4, 7, 5, "Wally installed a custom premium wallpaper in our living room, and it looks gorgeous! He helped us choose a design that perfectly matched our aesthetic. The install was seamless, and it truly elevated the entire room’s look. So happy with the final result!", '2011-01-09'),
(7, 8, 1, "I was disappointed with Paige's work on the roller application for our exterior painting. The coverage was uneven in some areas, and we had to redo certain parts ourselves. It took longer than anticipated, and there were issues with the finish. Would have hoped for better results.", '2011-04-25'),
(14, 8, 4, "Paige did a good job rolling on the paint in our kitchen. The coverage was even, and she made sure there were no streaks or uneven spots. The fresh paint really brightened up the space, and she worked efficiently and professionally. I had hoped it would be a faster job, but overall pleased with the results.", '2011-07-17'),
(5, 9, 5, "Hue was an absolute pleasure to work with! He assisted us with color consultation and helped choose the perfect shades for our house. His expertise made all the difference, and the space looks amazing!", '2011-10-01'),
(1, 9, 3, "Hue helped us with concrete and brick painting, and while the quality of work was solid, it did take longer than we expected to finish. There were a few touch-ups needed along the way, but in the end, the finish looks fantastic, and the space has a fresh new look. We’re happy with the result, just wished for a quicker turnaround.", '2011-12-16'),
(8, 10, 4, "Dusty did a solid job repainting our bedroom walls. While it took a little longer than expected, the final result is good. We’re happy with how it turned out overall, but it could have been more efficient.", '2012-02-22'),
(15, 10, 3, "Dusty did a nice job painting our living room, though there were a few areas that required extra attention. The finish is good, but it did take a bit longer than expected. Communication was fine, and we’re happy with the results overall.", '2012-04-10'),
(10, 11, 3, "Tessa's drywall repair and texturing work was generally fine. It took a bit more time than anticipated, but she was professional and friendly. The room looks good now, just wish it had been a bit quicker.", '2012-06-26'),
(10, 11, 5, "Tessa did an amazing job with our premium wallpaper design! She took the time to understand our style and recommended a design that perfectly complements our living room. The installation was smooth, and the finish is flawless. We're so happy with how it turned out—it truly transformed the space. Highly recommend Tessa for any wallpaper projects!", '2012-09-08'),
(8, 12, 3, "Daisy’s tinting on our walls was well-done, and she provided useful advice on color tones. However, there were a couple of spots that needed a second touch-up. Overall, happy with the results.", '2012-11-14'),
(8, 12, 3, "Daisy did a great job with wallpaper removal in our bedroom. The process took a little longer than expected, but she was very thorough and careful, ensuring that the walls were properly prepped afterward. There were a few small spots where the removal didn’t go as smoothly, but she quickly fixed them. In the end, the walls were in great condition, and we’re happy with the result.", '2013-01-30'),
(8, 13, 3, "Vinny did a good job with varnishing our wooden trim, though it took a little longer than planned. The finish looks great now, but I would have preferred a quicker turnaround.", '2013-04-12'),
(8, 13, 4, "Vinny did a solid job with painting the exterior of our house. The coverage is smooth and the colors look great, though it took a bit longer than expected to finish. He was professional and careful throughout the process, and while the job could have been completed a little faster, we’re very pleased with the final result. Our house looks refreshed and vibrant!", '2013-07-19'),
(9, 14, 2, "Gloria did a nice job with wallpaper installation in our living room. The results were alright, but the process took longer than expected. Communication was solid, and the work was good, but timing could be improved.", '2013-10-05'),
(9, 14, 4, "Gloria did a fantastic job with recoating our living room walls. The finish looks smooth and refreshed, and the color really pops now. It took a bit longer than we anticipated, but Gloria made sure everything was done right, with careful attention to detail. There were a few minor touch-ups needed, but she was prompt in addressing them. We’re really pleased with the results!", '2013-12-09'),
(11, 15, 1, "Unfortunately, the wallpaper removal process didn’t go as smoothly as I had hoped. There was a lot more damage to the wall than anticipated, and it took longer than expected to fix. Not the best experience.", '2014-03-02'),
(11, 15, 2, "Paula’s color consultation was excellent—she helped us choose the perfect shades for our room. However, the execution of the premium wallpaper design didn’t meet our expectations. While the design was great, the installation had a few issues that needed touch-ups. Paula was professional and worked to fix them, but the process wasn’t as smooth as we had hoped.", '2014-05-22'),
(9, 16, 1, "I wasn't very happy with Manny’s work. The pattern placement was a bit off, and there were some areas that weren’t properly smoothed out. I appreciate his effort, but I expected better attention to detail.", '2014-08-15'),
(9, 16, 3, "Manny did a good job with both the concrete and brick painting, as well as the exterior painting of our stables. The coverage was decent, but there were a few areas that could have been more thorough. It wasn’t a bad job, but we had hoped for a bit more attention to detail. Manny was professional and did his best, but the final result wasn’t as polished as we expected.", '2014-11-28');


-- Reviews for Lawn Care Services -- 
INSERT INTO reviews (clientID, tp_profileID, rating, comment, review_date)
VALUES (4, 17, 5, 'Penny turned our dull backyard into a blooming paradise! Her attention to flower selection and planting made everything feel so thoughtfully designed. My mother absolutely loved the orchards!', '2015-03-20'),
(5, 17, 5, 'Penny has got such a gentle, caring approach with plants—you can tell she loves what she does. Our front garden has never looked more colorful and alive. Perfect for brunch with our neighbours!', '2015-03-21'),
(13, 18, 4, 'Friendly and hardworking —Chloe handled our weed problem like a pro, though there were some missing spots. But overall, pleased. Would absolutely recommend her again.', '2015-03-22'),
(6, 18, 5, 'Chloe gave our lawn the refresher it desperately needed. From mowing to edging, everything looks neat, green, and healthy—she even added some sweet clover touches!', '2015-03-23'),
(7, 19, 5, 'Rosemary completely refreshed our landscaping. From trimming hedges to rearranging our garden beds. My daughter was delighted to learn how to trim a minnie mouse shaped hedge. Would hire again.', '2015-03-24'),
(14, 19, 5, 'Rosemary helped my wife replant our herb garden and gave tips to keep it thriving. Knowledgeable, professional, and an absolute delight to work with.', '2015-03-25'),
(9, 20, 5, 'Chris is the kind of guy you want handling your hedges. Straightforward, on time, and left my yard looking sharp and clean.', '2015-03-26'),
(9, 20, 5, 'He trimmed everything with precision and even hauled the clippings without me asking. Top-notch work—will definitely have him back.', '2015-03-27'),
(1, 21, 5, 'Jack made weed removal look easy—and somehow still charming while doing it! My garden’s never looked so fresh and tidy.', '2015-03-28'),
(2, 21, 4, 'He was super sweet and thorough with every corner of the yard. Fast, focused, and had great planting tips too. Total garden hero!', '2015-03-29'),
(11, 22, 5, 'All I know is that I wanted to revamp my garden and Faye did exactly that. She brought our backyard back to life with her planting and care—it looks like a totally new space, ready for my relatives to visit.', '2015-03-30'),
(11, 22, 5, 'Super professional and had a great eye for design. She added subtle touches that made the garden feel peaceful and polished. Great energy too!', '2015-03-31'),
(12, 23, 3, 'Hank was friendly and clearly knows a lot about plants, but the landscaping took longer than I expected. The yard looks nice now, just wish the process had been smoother.', '2015-04-01'),
(12, 23, 4, 'He gave good advice on plant care and did a decent job overall, though I had to follow up a couple times to get things finished. Solid results, just room for improvement.', '2015-04-02'),
(10, 24, 4, 'Vera was sweet and attentive with my climbing plants, but there were a few spots she missed. She came back to fix them, though, so I appreciated that.', '2015-04-03'),
(10, 24, 4, 'She’s got a good eye for greenery, but the vine trimming could’ve been a little neater. Still, she was kind and professional the whole time.', '2015-04-04'),
(10, 25, 3, 'Luke definitely brought the energy, and he was fun to talk to, but the bush shaping wasn’t as tidy as I hoped. Still, he was quick and very polite.', '2015-04-05'),
(10, 25, 4, 'He helped with some yard cleanup and trimming—it was okay, just not super detailed. Great attitude, though, and easy to work with.', '2015-04-06'),
(14, 26, 5, 'Pat got the lawn mowed and made sure everything was watered, which was solid. Paid great attention to the edges and covered the entire golfing area. Great guy, would hire again.', '2015-04-07'),
(7, 26, 3, 'He showed up on time and got the job done. Nothing fancy, just a decent mow and water—did what I needed, was quite late the first day.', '2015-04-08'),
(9, 27, 4, 'Misty helped clear out the weeds and got rid of the algae buildup in our pond. Had to point out some missing spots, but she was polite and made sure everything was completed in the end.', '2015-04-09'),
(9, 27, 3, 'She’s definitely knowledgeable about landscaping, but the end result wasn’t quite what I pictured. That said, the space does look slightly cleaner and put-together now.', '2015-04-10'),
(3, 28, 4, 'Charlotte helped with aerating and reseeding the lawn—something I hadn’t thought about, but she recommended it. She knows her stuff, though the results are still coming in.', '2015-04-11'),
(5, 28, 4, 'She was enthusiastic and suggested dethatching the yard, which was cool. Execution was okay, just a bit uneven in spots, but she definitely gave it effort.', '2015-04-12'),
(6, 29, 3, 'Cameron was super friendly and did a decent job checking our sprinkler system and watering schedule. The sprinkler did break at some point but he was swift to find a replacement and fix it with no extra costs. Did some decent lawn mowing.', '2015-04-13'),
(13, 29, 4, 'He knew his way around the hose setup and got our system running again. A couple of zones needed re-tweaking later, but overall it was good.', '2015-04-14'),
(8, 30, 4, 'Poppy has a great eye for color and helped brighten up our flower beds, but a few of the plants didn’t take as well as I hoped. Still, she was lovely to work with and super respectful of our space.', '2015-04-15'),
(15, 30, 4, 'She brought a lot of energy and ideas to the yard, which I appreciated. A few parts of the garden felt a bit undone, but overall she did a decent job.', '2015-04-16'),
(8, 31, 2, 'Unfortunately, working with Olive didn’t meet our expectations. While she was pleasant, the planting wasn’t well thought out, some areas looked sparse. We were hoping for a more polished and lasting result.', '2015-04-17'),
(15, 31, 3, 'Olive brought some bright ideas to our landscaping project and was a pleasure to work with. While the layout turned out nice, some of the plant placements felt a bit off and a few areas needed a second pass.', '2015-04-18'),
(11, 32, 2, 'We hired Tommy to help with flower bed planning and planting, but the results were underwhelming. Some of the choices didn’t suit the space or season, and it felt a bit rushed overall. He was friendly, but the execution just didn’t deliver what we hoped for.', '2015-04-19'),
(11, 32, 3, 'Tommy handled our front yard landscaping. He clearly knows his plants, but the overall design felt a bit basic for what we discussed. It looks good now, just not quite as polished as we expected.', '2015-04-20');

-- Reviews for Moving Services --
INSERT INTO reviews (clientID, tp_profileID, rating, comment, review_date)
VALUES (5, 35, 5, 'David Dunn communicated well and completed the move quicker than expected.', '2024-08-02'),
(11, 35, 5, 'David Dunn took great care with our belongings. Very professional service.', '2024-11-22'),
(7, 36, 4, 'Sean Hill took great care with our belongings. Very professional service.', '2025-01-31'),
(12, 36, 5, 'Sean Hill provided excellent packing and delivery services.', '2024-05-27'),
(13, 37, 5, 'Sheila Mcintosh provided excellent packing and delivery services.', '2024-01-18'),
(7, 37, 5, 'Sheila Mcintosh provided excellent packing and delivery services.', '2024-01-02'),
(12, 38, 4, 'Kimberly Martin took great care with our belongings. Very professional service.', '2024-02-23'),
(5, 38, 5, 'Kimberly Martin communicated well and completed the move quicker than expected.', '2024-11-28'),
(14, 39, 1, 'Candace Thomas delivered incomplete service, leaving many items behind.', '2024-03-20'),
(6, 39, 2, 'Candace Thomas communication was poor, and the move was stressful and chaotic.', '2025-02-11'),
(9, 40, 5, 'Nathan Garcia handled our move flawlessly! Everything arrived safely and on time.', '2024-04-03'),
(11, 40, 4, 'Nathan Garcia communicated well and completed the move quicker than expected.', '2024-05-02'),
(13, 41, 5, 'Seth Warner took great care with our belongings. Very professional service.', '2024-02-28'),
(1, 41, 4, 'Seth Warner took great care with our belongings. Very professional service.', '2024-01-29'),
(10, 42, 5, 'Rebecca Lane communicated well and completed the move quicker than expected.', '2024-02-09'),
(8, 42, 4, 'Rebecca Lane took great care with our belongings. Very professional service.', '2024-05-23'),
(1, 43, 5, 'Monica Wolf made our relocation smooth and stress-free. Highly recommended!', '2024-08-08'),
(13, 43, 4, 'Monica Wolf took great care with our belongings. Very professional service.', '2024-06-08'),
(6, 44, 5, 'Danielle Collins communicated well and completed the move quicker than expected.', '2024-12-01'),
(6, 44, 5, 'Danielle Collins provided excellent packing and delivery services.', '2024-05-02'),
(12, 45, 4, 'Nicole West communicated well and completed the move quicker than expected.', '2024-06-29'),
(4, 45, 5, 'Nicole West took great care with our belongings. Very professional service.', '2024-09-23'),
(15, 46, 5, 'Kaitlyn Rivera communicated well and completed the move quicker than expected.', '2024-04-20'),
(10, 46, 5, 'Kaitlyn Rivera took great care with our belongings. Very professional service.', '2025-02-10'),
(7, 47, 3, 'Anthony Reed was polite and professional, though the move took longer than planned.', '2024-04-03'),
(9, 47, 4, 'Anthony Reed took great care with our belongings. Very professional service.', '2024-02-18'),
(3, 48, 4, 'Bryan Barrett provided excellent packing and delivery services.', '2025-01-30'),
(9, 48, 5, 'Bryan Barrett communicated well and completed the move quicker than expected.', '2025-03-22'),
(10, 49, 4, 'Michael Rice took great care with our belongings. Very professional service.', '2024-10-24'),
(15, 49, 4, 'Michael Rice made our relocation smooth and stress-free. Highly recommended!', '2024-02-02'),
(4, 50, 4, 'Daniel Deleon handled our move flawlessly! Everything arrived safely and on time.', '2024-07-02'),
(4, 50, 5, 'Daniel Deleon handled our move flawlessly! Everything arrived safely and on time.', '2024-05-01'),
(8, 51, 5, 'Matthew Bray provided excellent packing and delivery services.', '2024-07-10'),
(2, 51, 4, 'Matthew Bray handled our move flawlessly! Everything arrived safely and on time.', '2025-02-05');

