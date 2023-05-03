-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: May 03, 2023 at 07:33 AM
-- Server version: 5.7.34
-- PHP Version: 7.4.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `user_info`
--

DROP DATABASE IF EXISTS `user_info`;
CREATE DATABASE IF NOT EXISTS `user_info` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user_info`;

-- --------------------------------------------------------

--
-- Table structure for table `user_info`
--

DROP TABLE IF EXISTS `user_info`;
CREATE TABLE IF NOT EXISTS `user_info` (
  `user_id` int(11) NOT NULL,
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `username` varchar(20) NOT NULL,
  `number` varchar(12) NOT NULL,
  `email` varchar(128) NOT NULL,
  `password` varchar(64) NOT NULL,
  `address` varchar(128) NOT NULL,
  `latitude` decimal(10,6),
  `longitude` decimal(10,6),
  `dietary_type` varchar(64),
  `travel_appetite` int(11),
  `sms_notif` bit,
  `email_notif` bit,

  PRIMARY KEY (`user_id`)
);

--
-- Dumping data for table `user_info`
--

INSERT INTO `user_info` (`user_id`, `first_name`, `last_name`, `username`, `number`, `email`, `password`, `address`, `latitude`, `longitude`, `dietary_type`, `travel_appetite`, `sms_notif`, `email_notif`) VALUES
(1, 'Sheng Boon', 'Sng', 'iloveesd', '6588180849', 'adambft98@gmail.com', '$2b$10$52JpGkV6ZQoZO9p9BsmbaeaILxvaUQd.u5rIej.i2NKsHHS38V3fS', 'Stamford Road, SMU School of Economics/Computing & Information Systems 2, Singapore', '1.297819', '103.849010', 'vegetarian', 20, b'0', b'1'),
(2, 'Adam', 'Tan', 'adambft', '92354902', 'adambft98@gmail.com', '$2b$10$BqFA1Krin9/U7krVgJNRgOKvhNElBc1iIX5n9jRqYlqpJsHl9oQi6', 'Prinsep Street, Prinsep Street Residences, Singapore', '1.301935', '103.851259', 'halal', 2, b'1', b'1'),
(3, 'Faez', 'Latiff', 'faezlatiff', '97125758', 'faezweirdguy@gmail.com', '$2b$10$R/hMaiJC/rYWHhM5tuh/F.5ALQ3cgP2UHb/dxQxCxbbgcpnYALuSa', 'City Hall MRT, Singapore', '1.293116', '103.852013', 'nobeef', 10, b'1', b'1'),
(4, 'Sheng Da', 'Tan', 'tanshengda', '92476862', 'shengdatan@gmail.com', '$2b$10$MOjui/6a8AvDee4XbTP83ep1cf7po5ta347z3b5TEkoqm86f8jTj.', 'Stamford Road, SMU Lee Kong Chian School of Business, Singapore', '1.295079', '103.850320', 'vegetarian', 10, b'1', b'1'),
(5, 'test', 'test', 'testing', '91234123', 'shengdatan@gmail.com', '$2b$10$FbrxmCZr9/FqV.qqddD.wuiTI4vq78/8K0eb5ACNx2lgDHqoNZ63.', 'Stadium Walk, Singapore Indoor Stadium, Singapore', '1.300571', '103.874394', 'vegetarian', 1, b'1', b'1');

COMMIT;

SELECT * FROM user_info;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
