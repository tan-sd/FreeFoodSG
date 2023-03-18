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
  `post_name` varchar(60),
  `latitude` decimal(10,6),
  `longitude` decimal(10,6),
  `address` varchar(128) NOT NULL,
  `description` varchar(1000) NULL,
  `allergens` varchar(8000) NULL, 
  `is_available` bit,
  `end_time` datetime,

  PRIMARY KEY (`post_id`)
);

INSERT INTO `food_table` (`username`, `post_name`, `latitude`, `longitude`, `description`,
 `allergens`, `is_available`, `end_time`) 
VALUES
( 'faez' ,'laichifan', 1.283125, 103.868825 , 'u broke u come', 'na', 'yes', '2023-03-12 22:00:00'),
( 'rachel' ,'laichimian', 1.183195, 103.898825 , 'a lot indomee pls clear', 'na', 'yes','2023-03-12 22:00:00'),
( 'shengda' ,'di san ge', 1.283374, 103.860726, 'plain water', 'na', 'yes', '2023-03-12 22:00:00');
COMMIT;

SELECT * FROM food_table;