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
-- Database: `food_db`
--

DROP DATABASE IF EXISTS `food_db`;
CREATE DATABASE IF NOT EXISTS `food_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `food_db`;

-- --------------------------------------------------------

--
-- Table structure for table `food_table`
--

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
  `end_time` varchar(64),

  PRIMARY KEY (`post_id`)
);

--
-- Dumping data for table `food_table`
--

INSERT INTO `food_table` (`post_id`, `username`, `post_name`, `latitude`, `longitude`, `address`, `description`, `is_available`, `end_time`)
VALUES
('0f8e9bdd-b1a5-445d-95b3-2a4d1f2cb922', 'faezlatiff', 'Free Ice Cream at The Cathay!', '1.299508', '103.847778', '2 Handy Rd, Singapore 229233', 'Come get free ice cream~ Cathay L3', b'1', '2023-10-04 10:23:00'),
('25d47f98-5960-4d94-9f2e-6439f90d9240', 'adambft', 'Free briyani at Esplanade!', '1.289760', '103.856041', '8 Raffles Ave., Singapore 039802', 'Leftovers at esplanade level 3', b'1', '2023-10-04 07:44:00'),
('276c9b8a-1913-4f26-be69-25532e2ff0ec', 'faezlatiff', 'Come get free catered sandwiches!', '1.328867', '103.879286', '47 Kallang Pudding Road #05-15 The Crescent @ Kallang, Singapore 349318', 'Free sandwhich at GRID L1', b'1', '2023-04-04 14:26:00'),
('327fd2fa-19f8-482c-baa6-475a1c54fb01', 'iloveesd', 'test', '1.401252', '103.747928', 'Singapore 680673', 'test', b'0', '2023-04-11 17:21:00'),
('3a6b9818-a6c3-4a49-87c1-66b92b3e2653', 'iloveesd', 'Free Pizza at SOL', '1.294872', '103.849494', '55 Armenian St, Singapore 179943', 'Got a lot of pizza left over at school of law. Pls come and grab urs. FCFS', b'0', '2023-04-04 08:37:00'),
('7064ea15-4bfc-498a-a3ba-94084b615bdd', 'iloveesd', 'Salad & Sides', '1.302285', '103.858964', '3 Muscat St, Singapore 198833', 'Come help to clear @ Masjid Sultan please!', b'1', '2023-10-04 10:29:00'),
('77385fd3-3197-43da-82ba-f63ae920c453', 'tanshengda', 'Cheese platter leftovers @Office Pt Ltd', '1.292892', '103.850384', '10 Coleman St, Singapore 179809', 'Come get it fast - The Office #04-13', b'0', '2023-04-04 11:43:00'),
('a9e15ad3-ddb6-429f-a303-58e5a5dcdee9', 'iloveesd', 'Tasty food!', '1.401252', '103.747928', 'Singapore 680673', 'Tasty food!', b'0', '2023-04-06 18:15:00'),
('bc59025c-b11f-4af3-b927-1b01d1939367', 'tanshengda', 'Free cupcakes!', '1.300532', '103.845236', '68 Orchard Rd, Singapore 238839', 'Come get it fast, plaza singapura #02-03', b'0', '2023-04-04 07:43:00'),
('c15de281-dde0-482a-bfc9-34d385dc2171', 'adambft', 'Leftovers - Tasting Platter', '1.299375', '103.855526', '200 Victoria St, Singapore 188021', 'Come quick, clearing yummy tasting platter soon! Bugis junction L2, #02-13', b'0', '2023-04-04 09:52:00');

--
-- Table structure for table `dietary_table`
--

DROP TABLE IF EXISTS `dietary_table`;
CREATE TABLE IF NOT EXISTS `dietary_table` (
  `post_id` varchar(64) NOT NULL,
  `diets_available` varchar(128),

  PRIMARY KEY (`post_id`, `diets_available`),
  FOREIGN KEY (`post_id`) REFERENCES food_table (`post_id`)
);

SELECT * FROM food_table;

--
-- Dumping data for table `dietary_table`
--

INSERT INTO `dietary_table` (`post_id`, `diets_available`) VALUES
('0f8e9bdd-b1a5-445d-95b3-2a4d1f2cb922', 'halal'),
('0f8e9bdd-b1a5-445d-95b3-2a4d1f2cb922', 'nobeef'),
('0f8e9bdd-b1a5-445d-95b3-2a4d1f2cb922', 'vegetarian'),
('25d47f98-5960-4d94-9f2e-6439f90d9240', 'halal'),
('25d47f98-5960-4d94-9f2e-6439f90d9240', 'nobeef'),
('25d47f98-5960-4d94-9f2e-6439f90d9240', 'vegetarian'),
('276c9b8a-1913-4f26-be69-25532e2ff0ec', 'halal'),
('276c9b8a-1913-4f26-be69-25532e2ff0ec', 'nobeef'),
('3a6b9818-a6c3-4a49-87c1-66b92b3e2653', 'halal'),
('7064ea15-4bfc-498a-a3ba-94084b615bdd', 'halal'),
('7064ea15-4bfc-498a-a3ba-94084b615bdd', 'nobeef'),
('7064ea15-4bfc-498a-a3ba-94084b615bdd', 'vegetarian'),
('77385fd3-3197-43da-82ba-f63ae920c453', 'halal'),
('77385fd3-3197-43da-82ba-f63ae920c453', 'nobeef'),
('77385fd3-3197-43da-82ba-f63ae920c453', 'vegetarian'),
('a9e15ad3-ddb6-429f-a303-58e5a5dcdee9', 'vegetarian');

-- --------------------------------------------------------

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
