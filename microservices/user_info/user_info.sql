CREATE DATABASE IF NOT EXISTS `user_info` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user_info`;

DROP TABLE IF EXISTS `user_info`;
CREATE TABLE IF NOT EXISTS `user_info` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `username` varchar(20) NOT NULL,
  `number` varchar(12) NOT NULL,
  `email` varchar(128) NOT NULL,
  `password` varchar(64) NOT NULL,
  `address` varchar(128) NOT NULL,
  `latitude` decimal(10,6) ,
  `longitude` decimal(10,6) ,
  `dietary_type` varchar(64) ,
  `travel_appetite` int(11),
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user_info`
--

INSERT INTO `user_info` (`user_id`, `first_name`, `last_name`, `username`, `number`, `email`, `password`, `address`, `latitude`, `longitude`, `dietary_type`, `travel_appetite`) VALUES
(9, 'Sheng Da', 'Tan', 'shengdatan', '92476862', 'shengdatan@gmail.com', '$2b$10$efG2mz/MMdwXckfqkcQph.l5cB.SzTkUdzuw/Sbe.kHcrHe1.0BG2', 'Victoria Street, Singapore Management University, Singapore', 1.296273, 103.850158, '', 0.5),
(10, 'Adam', 'Tan', 'adamtan', '92354902', 'adamft.2021@scis.smu.edu.sg', '$2b$10$BZK3ZvadKLLcOkRoaEr5ouFB8qu3ZpyaXUyCFjJd9MVkNWzSd6uOG', 'Expo Drive, Singapore Expo, Singapore', 1.333525, 103.959537, 'Halal', 2);

COMMIT;

SELECT * FROM user_info;
