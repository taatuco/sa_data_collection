-- phpMyAdmin SQL Dump
-- version 4.8.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 10, 2018 at 04:51 AM
-- Server version: 10.1.33-MariaDB
-- PHP Version: 7.2.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smartalpha`
--

-- --------------------------------------------------------

--
-- Table structure for table `asset_class`
--

CREATE TABLE `asset_class` (
  `asset_class_id` varchar(10) NOT NULL,
  `asset_class_name` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `instruments`
--

CREATE TABLE `instruments` (
  `symbol` varchar(100) NOT NULL,
  `fullname` text NOT NULL,
  `asset_class` text NOT NULL,
  `market` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `price_instruments_data`
--

CREATE TABLE `price_instruments_data` (
  `id` int(11) NOT NULL,
  `symbol` text NOT NULL,
  `date` date NOT NULL,
  `price_close` double DEFAULT NULL,
  `price_open` double DEFAULT NULL,
  `price_low` double DEFAULT NULL,
  `price_high` double DEFAULT NULL,
  `volume` double DEFAULT NULL,
  `price_type` varchar(5) NOT NULL,
  `price_forecast` double DEFAULT NULL,
  `price_low_75` double DEFAULT NULL,
  `price_high_75` double DEFAULT NULL,
  `price_low_85` double DEFAULT NULL,
  `price_high_85` double DEFAULT NULL,
  `price_low_95` double DEFAULT NULL,
  `price_high_95` double DEFAULT NULL,
  `mt_trend_high` double NOT NULL DEFAULT '0',
  `mt_trend_low` double NOT NULL DEFAULT '0',
  `st_trend_high` double NOT NULL DEFAULT '0',
  `st_trend_low` double NOT NULL DEFAULT '0',
  `ma200` double NOT NULL DEFAULT '0',
  `lowest_20d` double NOT NULL DEFAULT '0',
  `highest_20d` double NOT NULL DEFAULT '0',
  `change_1d` double NOT NULL DEFAULT '0',
  `gain_1d` double NOT NULL DEFAULT '0',
  `loss_1d` double NOT NULL DEFAULT '0',
  `avg_gain` double NOT NULL DEFAULT '0',
  `avg_loss` double NOT NULL DEFAULT '0',
  `rs14` double NOT NULL DEFAULT '0',
  `rsi14` double NOT NULL DEFAULT '0',
  `rsi_overbought` double NOT NULL DEFAULT '0',
  `rsi_oversold` double NOT NULL DEFAULT '0',
  `fib_0` double NOT NULL DEFAULT '0',
  `fib_23_6` double NOT NULL DEFAULT '0',
  `fib_38_2` double NOT NULL DEFAULT '0',
  `fib_61_8` double NOT NULL DEFAULT '0',
  `fib_76_4` double NOT NULL DEFAULT '0',
  `fib_100` double NOT NULL DEFAULT '0',
  `is_ta_calc` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `symbol_list`
--

CREATE TABLE `symbol_list` (
  `symbol` varchar(100) NOT NULL,
  `tradingview` text NOT NULL,
  `investing_com` text NOT NULL,
  `r_quantmod` text NOT NULL,
  `yahoo_finance` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `firstname` text NOT NULL,
  `lastname` text NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` text NOT NULL,
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `default_profile` text NOT NULL,
  `last_logon` date NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `asset_class`
--
ALTER TABLE `asset_class`
  ADD PRIMARY KEY (`asset_class_id`),
  ADD UNIQUE KEY `asset_class_id` (`asset_class_id`);

--
-- Indexes for table `instruments`
--
ALTER TABLE `instruments`
  ADD PRIMARY KEY (`symbol`),
  ADD UNIQUE KEY `symbol` (`symbol`);

--
-- Indexes for table `price_instruments_data`
--
ALTER TABLE `price_instruments_data`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `symbol_list`
--
ALTER TABLE `symbol_list`
  ADD PRIMARY KEY (`symbol`),
  ADD UNIQUE KEY `symbol` (`symbol`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `price_instruments_data`
--
ALTER TABLE `price_instruments_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
