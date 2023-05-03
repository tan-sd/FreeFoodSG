-- this is the database setup file
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `activity_db`
--
DROP DATABASE IF EXISTS `activity_db`;
CREATE DATABASE IF NOT EXISTS `activity_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `activity_db`;

-- --------------------------------------------------------

-- Table structure for table `activity_table`

DROP TABLE IF EXISTS `activity_table`;
CREATE TABLE IF NOT EXISTS `activity_table` (

  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL, -- YYYY-MM-DD HH:MI:SS
  `log_info` varchar(64) NOT NULL,
  
  PRIMARY KEY (`log_id`)
);

-- insert first row so that get_log_id() function works as intended in activity_log.py
INSERT INTO `activity_table` (`log_id`, `created`, `log_info`)
VALUES
( 0 ,'2000-12-31 00:15:30','food_info');
COMMIT;