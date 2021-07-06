-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 06, 2021 at 01:08 AM
-- Server version: 10.4.18-MariaDB
-- PHP Version: 7.3.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lung_cancer`
--

-- --------------------------------------------------------

--
-- Table structure for table `ct_scan`
--

CREATE TABLE `ct_scan` (
  `id` int(11) NOT NULL,
  `image_path` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `ct_scan`
--

INSERT INTO `ct_scan` (`id`, `image_path`) VALUES
(5, 'A5137839.dcm'),
(6, 'A1092335.dcm');

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `comment` varchar(150) NOT NULL,
  `Date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`id`, `user_id`, `comment`, `Date`) VALUES
(1, 1, 'your system is very bade ', '2021-07-04 12:22:41'),
(2, 1, '“The doctor of the future will give no medicine, but will instruct his patients in care of the human frame, in diet, and in the cause and prevention o', '2021-07-04 18:55:57');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `User_type` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `User_type`) VALUES
(1, 'aiak', 'Alaa', 'zaher', 'user@gmail.com', 'sha256$XzWLrpOa$b43797cf3fdf52622f2a7fc472c2cc9d6958d53fdc504ecd66205f439bde5606', 2),
(3, 'omar234', 'omar', 'tarek', 'adasdsfds@gmil.com', 'sha256$a5zwSGWo$db7ab2eeddeeca92b8610021e08846b0b7d4bbe53332b58bfae4dd58b6b51c9e', 2),
(4, 'alasawoa', 'Alaa', 'zaher', 'admin@gmail.com', 'sha256$f9YZcnKt$01bc5590bd402964c613b99266213d53adaa8078c9ad89eaf7852de57e7a62f3', 1),
(5, 'omar132', 'omar', 'ragi', 'adminsakda@gmail.com', 'sha256$6mAlo8Lr$4e6f041eff5eaf0d2e3b0a7539a06cc951b732fd150669183eda8bcfd908ace3', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ct_scan`
--
ALTER TABLE `ct_scan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ct_scan`
--
ALTER TABLE `ct_scan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
