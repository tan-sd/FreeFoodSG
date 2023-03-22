CREATE DATABASE IF NOT EXISTS `forum_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `forum_db`;

-- --------------------------------------------------------

-- Table structure for table `forum_table` in database `forum_db`

DROP TABLE IF EXISTS `forum_table`;
CREATE TABLE IF NOT EXISTS `forum_table` (
  
  `forum_id` int(11) NOT NULL auto_increment,
  `username` varchar(64) NOT NULL,
  `title` varchar(64),
  `description` varchar(1000) NULL,
  `datetime` datetime,

  PRIMARY KEY (`forum_id`)
);

-- INSERT INTO `forum_table` (`username`, `title`, `description`, `datetime`) 
-- VALUES
-- ( 'test_username', 'title', 'description', '2023-03-12 22:00:00'),
-- ( 'SJB123', 'title1', 'description1', '2021-01-01 15:10:10');
-- COMMIT;

DROP TABLE IF EXISTS `comments_table`;
CREATE TABLE IF NOT EXISTS `comments_table` (
  
  `forum_id` int(11) NOT NULL,
  `commentor_username` varchar(64) NOT NULL,
  `comment` varchar(1000),
  `datetime` datetime,

  PRIMARY KEY (`forum_id`,`commentor_username`, `datetime`),
  FOREIGN KEY (`forum_id`) REFERENCES forum_table(`forum_id`)
);

INSERT INTO `forum_table` (`username`, `title`, `description`, `datetime`) 
VALUES
('SJB123', 'title1', 'description1', '2021-01-01 15:10:10'),
('SJB123', 'title2', 'description2', '2021-01-01 15:10:10'),
('SJB123', 'title3', 'description3', '2022-01-01 15:10:10');
COMMIT;
SELECT * FROM forum_table;

INSERT INTO `comments_table` (`forum_id`, `commentor_username`, `comment`, `datetime`) 
VALUES
(1, 'SJB123', 'comment2', '2020-01-01 15:10:10'),
(1, 'SJB123', 'comment1', NOW()),
(2, 'DA123', 'comment1', NOW());
COMMIT;


-- SELECT * FROM forum_db;
SELECT * FROM comments_table;
