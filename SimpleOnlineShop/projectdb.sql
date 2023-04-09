-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2023-04-01 00:59:29
-- 伺服器版本： 10.4.27-MariaDB
-- PHP 版本： 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `projectdb`
--

-- --------------------------------------------------------

--
-- 資料表結構 `cart_items`
--

CREATE TABLE `cart_items` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1,
  `hasCheckout` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- 傾印資料表的資料 `cart_items`
--

INSERT INTO `cart_items` (`id`, `user_id`, `product_id`, `quantity`, `hasCheckout`) VALUES
(10, 3, 15, 2, 1),
(11, 3, 14, 2, 1),
(12, 4, 11, 1, 1),
(13, 4, 16, 2, 1),
(14, 5, 10, 2, 1),
(15, 3, 16, 1, 1),
(22, 6, 10, 1, 1),
(23, 11, 14, 5, 1);

-- --------------------------------------------------------

--
-- 資料表結構 `comments`
--

CREATE TABLE `comments` (
  `id` int(11) NOT NULL,
  `content` varchar(255) NOT NULL,
  `product_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- 傾印資料表的資料 `comments`
--

INSERT INTO `comments` (`id`, `content`, `product_id`, `user_id`, `time`) VALUES
(8, 'The price is cheap !!!', 15, 3, '2023-03-30 12:11:58'),
(9, 'I don\'t need to carry back home myself, it\'s really convenient!!!!', 11, 4, '2023-03-30 12:13:53'),
(10, 'The meat is so fresh!', 10, 5, '2023-03-30 12:15:38'),
(12, 'demo', 14, 11, '2023-03-30 12:51:00');

-- --------------------------------------------------------

--
-- 資料表結構 `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `image` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- 傾印資料表的資料 `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `price`, `image`) VALUES
(9, 'Frozon Food', 'Our online shopping collects a variety of high-quality frozen and frozen seafood products from all over the world for you, waiting for you to buy at any time', '50.00', '2023_03_30-09_15_14_PMfrozen_food.jpg'),
(10, 'Meat', 'Our online shopping collects a variety of high-quality meat products from all over the world for you, waiting for you to buy at any time with peace of mind', '70.00', '2023_03_30-09_15_30_PMmeat.jpg'),
(11, 'Rice', 'Our online shopping collects a variety of high-quality rice products for you, waiting for you to buy at any time with peace of mind', '100.00', '2023_03_30-09_15_42_PMrice.jpg'),
(12, 'Personal Care Products', 'Our online shopping collects a variety of high-quality body care products from all over the world for you, waiting for you to buy at any time with peace of mind', '65.90', '2023_03_30-09_16_34_PMPersonal_Care.png'),
(13, 'Snacks', 'Our online shopping collects a variety of high-quality snacks, biscuits, and desserts from all over the world for you, waiting for you to buy at any time with peace of mind.', '19.90', '2023_03_30-09_16_46_PMSnacks.jpg'),
(14, 'Beverage', 'Our online shopping collects a variety of high-quality drinks and instant drinks from all over the world for you, waiting for you to buy at any time with peace of mind.', '9.90', '2023_03_30-09_16_55_PMBeverage.jpg'),
(15, 'Oolong Tea', 'Our online shopping collects a variety of high-quality tea for you, waiting for you to buy at any time with peace of mind.', '11.90', '2023_03_30-09_17_06_PMoolong_tea.jpg'),
(16, 'Toliet Roll & Tissue', 'Our online shopping offers quality Toilet Roll & Tissue products from around the world. Enjoy your shopping anytime.', '35.90', '2023_03_30-09_17_16_PMTissue.jpg');

-- --------------------------------------------------------

--
-- 資料表結構 `role`
--

CREATE TABLE `role` (
  `id` int(11) NOT NULL,
  `role` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- 傾印資料表的資料 `role`
--

INSERT INTO `role` (`id`, `role`) VALUES
(1, 'admin'),
(2, 'customer');

-- --------------------------------------------------------

--
-- 資料表結構 `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL DEFAULT 2,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- 傾印資料表的資料 `users`
--

INSERT INTO `users` (`id`, `role_id`, `username`, `password`, `create_time`) VALUES
(1, 1, 'admin', '$2b$12$6VrOINPjupcDzmUkFBVClOVIyv4ddkLCbyzEGWY.BntqJxmMnM1kK', '2023-03-12 21:38:31'),
(3, 2, 'user1', '$2b$12$bJwh//g22sd6wfGem6tlguC6cKHPk0PUmWEysbqP7.8LnXOksv0sy', '2023-03-12 21:47:07'),
(4, 2, 'user2', '$2b$12$1fGhzl00aDOj2QL32uviQ.SkRB0aw.W.y3W1UjcnyyPfD2O5tNMvC', '2023-03-13 21:08:31'),
(5, 2, 'user3', '$2b$12$oE9NNYGqHEL704W13TM24.J8YxDmeBcyg5acVgRqTftMdxUUdSqmG', '2023-03-13 22:49:15'),
(6, 2, 'user4', '$2b$12$OOysDNBbeDwucBISiRiDJObjcfr5kZ8VoXGl7dxSo.xZd0fvbvKWS', '2023-03-13 23:10:07'),
(11, 2, 'demo', '$2b$12$Iz0PXmujDZbbRAEFtbd9fO1OAk3V4q6xKDvxwu7mN3q4UqZJDsSo.', '2023-03-30 12:50:35');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `cart_items`
--
ALTER TABLE `cart_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `cart_items_ibfk_1` (`user_id`);

--
-- 資料表索引 `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- 資料表索引 `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `role_id` (`role_id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `cart_items`
--
ALTER TABLE `cart_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `comments`
--
ALTER TABLE `comments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `cart_items`
--
ALTER TABLE `cart_items`
  ADD CONSTRAINT `cart_items_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `cart_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- 資料表的限制式 `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- 資料表的限制式 `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
