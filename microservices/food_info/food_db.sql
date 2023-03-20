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
  
  `post_id` int(11) NOT NULL auto_increment,
  `username` varchar(64) NOT NULL,
  `post_name` varchar(64),
  `latitude` decimal(10,6),
  `longitude` decimal(10,6),
  `address` varchar(128) NOT NULL,
  `description` varchar(1000),
  `dietary_type` varchar(8000), 
  `is_available` bit,
  `end_time` datetime,

  -- if post has photo, store photo into food_images folder, then store file path in SQL table
  `photo_name` varchar(64),
  `photo_path` varchar(128),

  PRIMARY KEY (`post_id`)
);

DROP TABLE IF EXISTS `dietary_table`;
CREATE TABLE IF NOT EXISTS `dietary_table` (
  
  `post_id` int(11) NOT NULL auto_increment,
  `dietary_type` varchar(8000), 

  PRIMARY KEY (`post_id`, `dietary_type`),
  FOREIGN KEY (`post_id`) REFERENCES food_table (`post_id`)
);


INSERT INTO `food_table` (`username`, `post_name`, `latitude`, `longitude`, `address`, `description`,
 `is_available`, `end_time`, `photo_name`, `photo_path`) 
VALUES
( 'test_username' ,'test_post_name', 1.283125, 103.868825 ,'81 Victoria St, Singapore 188065' , 'test_description', 'yes', '2023-03-12 22:00:00', 'buffet', 'food_images/buffet.jpg');
COMMIT;

SELECT * FROM food_table;