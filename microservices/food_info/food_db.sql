-- this is the database setup file
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `food_db`
--
DROP DATABASE IF EXISTS `food_db`;
CREATE DATABASE IF NOT EXISTS `food_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `food_db`;

-- --------------------------------------------------------

-- Table structure for table `food_table` in database `food_db`

DROP TABLE IF EXISTS `food_table`;
CREATE TABLE IF NOT EXISTS `food_table` (
  
  `post_id` varchar(64) NOT NULL,
  `username` varchar(64) NOT NULL,
  `post_name` varchar(64),
  `latitude` decimal(10,6),
  `longitude` decimal(10,6),
  `address` varchar(128) NOT NULL,
  `description` varchar(248),
  `is_available` bit,
  `end_time` datetime,

  PRIMARY KEY (`post_id`)
);

DROP TABLE IF EXISTS `dietary_table`;
CREATE TABLE IF NOT EXISTS `dietary_table` (
  
  `post_id` varchar(64) NOT NULL,
  `diets_available` varchar(128), 

  PRIMARY KEY (`post_id`, `diets_available`),
  FOREIGN KEY (`post_id`) REFERENCES food_table (`post_id`)
);

SELECT * FROM food_table;