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
-- Database: `forum_db`
--

DROP DATABASE IF EXISTS `forum_db`;
CREATE DATABASE IF NOT EXISTS `forum_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `forum_db`;

-- --------------------------------------------------------

--
-- Table structure for table `forum_table`
--

DROP TABLE IF EXISTS `forum_table`;
CREATE TABLE IF NOT EXISTS `forum_table` (
  `forum_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `title` varchar(64),
  `description` varchar(1000) NULL,
  `is_available` bit,
  `datetime` varchar(64),

  PRIMARY KEY (`forum_id`)
);

--
-- Dumping data for table `forum_table`
--

INSERT INTO `forum_table` (`forum_id`, `username`, `title`, `description`, `is_available`, `datetime`) VALUES
(1, 'iloveesd', 'Salesforce Event Happening on 10 Apr! Free food will be provided', 'We will be inviting guests from all around the world to discuss the best CRM practices worldwide. Come for great networking opportunities along with free food and drinks', b'1', '2023-04-04 00:48:45'),
(2, 'adambft', '10 Apr: Student Networking Event @ SMU SOSS B1', 'Come for amazing networking opportunities with seniors and alumnis in our first ever physical gathering in 3 years~ Free dinner will be provided!', b'1', '2023-04-04 00:51:28'),
(3, 'faezlatiff', '6 Apr: Free Ice Cream when you follow us on Insta!', 'Come to Zalora\'s pop up store at Plaza Singapura on 6 Apr and show us you are following us on Instagram to redeem 1 free ice cream flavour of your choice! While stocks lasts~', b'1', '2023-04-04 00:53:01'),
(4, 'tanshengda', 'Free Bubble Tea for 1st 100 Customers', 'Come visit our newly opened Bober store at Funan Mall and claim 1 free bubble tea per customer, limited to first 100 redemptions. Come quick! We\'re at Funan Mall #B1-03', b'1', '2023-04-04 00:55:30'),
(5, 'iloveesd', 'TEST', 'TEST', b'0', '2023-04-06 17:23:06'),
(6, 'iloveesd', 'Test', 'Test', b'0', '2023-04-06 18:02:11'),
(7, 'iloveesd', 'title', 'title', b'0', '2023-04-06 18:17:23');

--
-- Table structure for table `comments_table`
--

DROP DATABASE IF EXISTS `comments_table`;
CREATE TABLE IF NOT EXISTS `comments_table` (
  `forum_id` int(11) NOT NULL,
  `commentor_username` varchar(64) NOT NULL,
  `comment` varchar(1000),
  `datetime` varchar(64),

  PRIMARY KEY (`forum_id`, `commentor_username`, `datetime`),
  FOREIGN KEY (`forum_id`) REFERENCES forum_table(`forum_id`)
);

--
-- Dumping data for table `comments_table`
--

INSERT INTO `comments_table` (`forum_id`, `commentor_username`, `comment`, `datetime`) VALUES
(1, 'adambft', 'Me too!', '2023-04-04 00:56:11'),
(1, 'faezlatiff', 'Amazing! I\'ll be there~', '2023-04-04 00:55:56'),
(1, 'iloveesd', 'See you!', '2023-04-06 18:04:55'),
(1, 'iloveesd', 'Are yall there?', '2023-04-06 18:06:09'),
(1, 'iloveesd', 'Hello!', '2023-04-06 18:09:23'),
(1, 'iloveesd', 'Hello!', '2023-04-07 12:08:04'),
(1, 'iloveesd', 'Hello again', '2023-04-07 12:11:43'),
(1, 'iloveesd', 'Does it work?', '2023-04-07 12:12:19'),
(1, 'iloveesd', 'It should be working now!', '2023-04-07 12:15:04'),
(1, 'iloveesd', 'Does it work?', '2023-04-07 14:03:41'),
(1, 'iloveesd', 'Hello!', '2023-04-07 14:13:46'),
(1, 'iloveesd', 'Hello world.', '2023-04-07 14:15:13'),
(1, 'iloveesd', 'Should be working now.', '2023-04-07 14:17:42'),
(2, 'faezlatiff', 'OMG so excited! Can\'t wait to socialize my heart away <3', '2023-04-04 00:57:21'),
(2, 'faezlatiff', 'Can\'t wait', '2023-04-04 01:01:50'),
(3, 'tanshengda', 'Omg Zalora is bae, slayyyyy', '2023-04-04 01:00:49'),
(4, 'faezlatiff', 'Cominggg, save for me plsss', '2023-04-04 00:57:49'),
(4, 'iloveesd', 'Coming over too!', '2023-04-06 17:23:26'),
(4, 'iloveesd', 'I\'m here!', '2023-04-07 11:49:57'),
(4, 'iloveesd', 'Does it work?', '2023-04-07 11:56:00'),
(4, 'iloveesd', 'Hello', '2023-04-07 11:57:47'),
(4, 'tanshengda', 'Woah running over now, class can wait hahahaha', '2023-04-04 00:58:10'),
(5, 'iloveesd', 'HELLO', '2023-04-06 17:23:12'),
(6, 'iloveesd', 'Hello!', '2023-04-06 18:02:29'),
(7, 'iloveesd', 'hdsadjdsadh', '2023-04-06 18:17:27'),
(7, 'iloveesd', 'HELLO', '2023-04-06 18:24:13'),
(7, 'iloveesd', 'Hello', '2023-04-06 18:25:06'),
(7, 'iloveesd', 'hi', '2023-04-06 18:26:50'),
(7, 'iloveesd', 'hi', '2023-04-06 18:30:31'),
(7, 'iloveesd', 'YOOOOO', '2023-04-06 18:33:17'),
(7, 'iloveesd', 'HELLO', '2023-04-06 18:35:36'),
(7, 'iloveesd', 'hello', '2023-04-06 18:46:15'),
(7, 'iloveesd', 'hello', '2023-04-06 18:52:38'),
(7, 'iloveesd', 'hi', '2023-04-06 19:00:09'),
(7, 'iloveesd', 'hello', '2023-04-06 19:20:03'),
(7, 'iloveesd', 'hi', '2023-04-06 19:22:38'),
(7, 'iloveesd', 'IT WORKS', '2023-04-06 19:42:31'),
(7, 'iloveesd', 'hello', '2023-04-06 19:50:07'),
(7, 'iloveesd', 'yoooo', '2023-04-06 19:51:41'),
(7, 'iloveesd', 'helloooooo', '2023-04-06 20:00:42'),
(7, 'iloveesd', 'hihi', '2023-04-06 20:03:22'),
(7, 'iloveesd', 'Hello there!', '2023-04-06 20:10:56');

-- --------------------------------------------------------

SELECT * FROM comments_table;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
