-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Apr 20, 2025 at 07:35 PM
-- Server version: 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `gestion`
--

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE IF NOT EXISTS `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `lu` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=10 ;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`id`, `name`, `email`, `message`, `date`, `lu`) VALUES
(1, 'Inney', 'inneydiop@gmail.com', 'salut', '2025-04-11 19:51:12', 1),
(3, 'lalle', 'salma@gmail.com', 'je souhaite m''inscrire dans votre site', '2025-04-12 10:12:36', 1),
(4, 'Moussa', 'mous@gmail.com', 'ou se trouve votre siège?', '2025-04-12 11:50:16', 1),
(5, 'fatimetou ', 'metou@gmail.com', 'Très bon site.', '2025-04-15 06:21:12', 1),
(6, 'dehah lalla', '23507@isme.esp.mr', 'merci', '2025-04-15 02:39:00', 1),
(7, 'dehah lalla', '23507@isme.esp.mr', 'bonjour', '2025-04-15 11:22:28', 1);

-- --------------------------------------------------------

--
-- Table structure for table `paiement`
--

CREATE TABLE IF NOT EXISTS `paiement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prestataire_id` int(11) NOT NULL,
  `montant` decimal(10,0) NOT NULL,
  `date_paiement` timestamp NOT NULL,
  `date_expiration` timestamp NOT NULL,
  PRIMARY KEY (`id`),
  KEY `prestataire_id` (`prestataire_id`) USING BTREE
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=63 ;

--
-- Dumping data for table `paiement`
--

INSERT INTO `paiement` (`id`, `prestataire_id`, `montant`, `date_paiement`, `date_expiration`) VALUES
(1, 22, '2000', '2025-04-14 08:00:00', '2025-05-14 08:00:00'),
(2, 8, '2000', '2025-04-14 08:00:00', '2025-05-14 08:00:00'),
(3, 20, '2000', '2025-04-14 08:00:00', '2025-05-14 08:00:00'),
(4, 23, '2000', '2025-04-14 22:00:00', '2025-05-14 22:00:00'),
(5, 25, '2000', '2025-04-14 22:00:00', '2025-05-14 22:00:00'),
(6, 21, '2000', '2025-04-14 22:00:00', '2025-05-14 22:00:00'),
(7, 22, '2000', '2025-04-14 22:00:00', '2025-05-14 22:00:00'),
(8, 26, '2000', '2025-04-14 22:00:00', '2025-05-14 22:00:00'),
(9, 27, '2000', '2025-04-14 22:00:00', '2025-05-14 22:00:00'),
(10, 28, '2000', '2025-04-14 22:00:00', '2025-05-14 22:00:00'),
(11, 29, '2000', '2025-04-14 22:00:00', '2025-04-14 22:00:00'),
(12, 30, '2000', '2025-04-14 22:00:00', '2025-04-14 22:00:00'),
(13, 31, '2000', '2025-04-14 22:00:00', '2025-04-14 22:00:00'),
(14, 30, '2000', '2025-04-14 22:00:00', '2025-04-14 22:00:00'),
(15, 33, '2000', '2025-04-14 22:00:00', '2025-04-14 22:00:00'),
(16, 29, '2000', '2025-04-15 22:00:00', '2025-04-15 22:00:00'),
(17, 30, '2000', '2025-04-15 22:00:00', '2025-04-15 22:00:00'),
(18, 30, '2000', '2025-04-15 22:00:00', '2025-04-15 22:00:00'),
(19, 30, '2000', '2025-04-15 22:00:00', '2025-05-15 22:00:00'),
(20, 34, '2000', '2025-04-15 22:00:00', '2025-05-15 22:00:00'),
(21, 29, '2000', '2025-04-15 22:00:00', '2025-05-15 22:00:00'),
(22, 35, '200', '2025-04-15 22:00:00', '2025-04-15 22:00:00'),
(23, 36, '2000', '2025-04-15 22:00:00', '2025-05-15 22:00:00'),
(24, 29, '5', '2025-04-15 22:00:00', '2025-05-15 22:00:00'),
(25, 29, '6', '2025-04-15 22:00:00', '2025-05-15 22:00:00'),
(26, 30, '4', '2025-04-15 22:00:00', '2025-05-15 22:00:00'),
(27, 33, '3', '2025-04-15 22:00:00', '2025-05-15 22:00:00'),
(28, 34, '3', '2025-04-15 22:00:00', '2025-05-15 22:00:00'),
(29, 27, '4', '2025-04-15 22:00:00', '2025-05-15 22:00:00'),
(30, 36, '4000', '2025-04-15 22:00:00', '2025-05-15 22:00:00'),
(31, 32, '200', '2025-04-15 22:00:00', '2025-05-15 22:00:00'),
(32, 35, '2000', '2025-04-15 22:00:00', '2025-05-15 22:00:00'),
(33, 26, '2000', '2025-04-15 22:00:00', '2025-05-15 22:00:00'),
(34, 38, '2000', '2025-04-16 22:00:00', '2025-05-16 22:00:00'),
(35, 39, '2000', '2025-04-19 00:00:00', '2025-05-19 00:00:00'),
(36, 40, '2000', '2025-04-19 00:00:00', '2025-05-19 00:00:00'),
(37, 41, '2000', '2025-04-19 00:00:00', '2025-05-19 00:00:00'),
(38, 42, '2000', '2025-04-19 00:00:00', '2025-05-19 00:00:00'),
(39, 31, '12000', '2025-04-19 00:00:00', '2025-05-19 00:00:00'),
(40, 43, '2000', '2025-04-19 00:00:00', '2025-05-19 00:00:00'),
(41, 45, '2000', '2025-04-19 00:00:00', '2025-05-19 00:00:00'),
(42, 44, '2000', '2025-04-19 00:00:00', '2025-05-19 00:00:00'),
(43, 46, '2000', '2025-04-19 00:00:00', '2025-05-19 00:00:00'),
(44, 47, '2000', '2025-04-19 00:00:00', '2025-05-19 00:00:00'),
(45, 48, '2000', '2025-04-19 00:00:00', '2025-05-19 00:00:00'),
(46, 49, '2000', '2025-04-19 00:00:00', '2025-05-19 00:00:00'),
(47, 55, '2000', '2025-04-19 00:00:00', '2025-05-19 00:00:00'),
(48, 57, '2000', '2025-04-20 00:00:00', '2025-05-20 00:00:00'),
(49, 58, '20000', '2025-04-20 00:00:00', '2025-05-20 00:00:00'),
(50, 59, '2000', '2025-04-20 00:00:00', '2025-05-20 00:00:00'),
(51, 60, '2000', '2025-04-20 00:00:00', '2025-05-20 00:00:00'),
(52, 61, '2000', '2025-04-20 00:00:00', '2025-05-20 00:00:00'),
(53, 62, '2000', '2025-04-20 00:00:00', '2025-05-20 00:00:00'),
(54, 62, '2000', '2025-04-20 00:00:00', '2025-05-20 00:00:00'),
(55, 67, '2000', '2025-04-20 00:00:00', '2025-05-20 00:00:00'),
(56, 68, '2000', '2025-04-20 00:00:00', '2025-05-20 00:00:00'),
(57, 69, '2000', '2025-04-20 00:00:00', '2025-05-20 00:00:00'),
(58, 71, '2000', '2025-04-20 00:00:00', '2025-05-20 00:00:00'),
(59, 73, '2000', '2025-04-20 00:00:00', '2025-05-20 00:00:00'),
(60, 75, '2000', '2025-04-20 00:00:00', '2025-05-20 00:00:00'),
(61, 76, '2000', '2025-04-20 00:00:00', '2025-05-20 00:00:00'),
(62, 77, '2000', '2025-04-20 00:00:00', '2025-05-20 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `prestataire`
--

CREATE TABLE IF NOT EXISTS `prestataire` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Nom` text NOT NULL,
  `Prenom` text NOT NULL,
  `Téléphone` text NOT NULL,
  `Email` text NOT NULL,
  `statut` text NOT NULL,
  `commune` varchar(300) NOT NULL,
  `genre` text NOT NULL,
  `Langue` text NOT NULL,
  `service_id` int(11) DEFAULT NULL,
  `image_path` varchar(300) DEFAULT NULL,
  `password` varchar(250) NOT NULL,
  `prix` int(250) NOT NULL,
  `carte_identite` varchar(255) DEFAULT NULL,
  `casier_judiciaire` varchar(255) DEFAULT NULL,
  `papier_sejour` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=79 ;

--
-- Dumping data for table `prestataire`
--

INSERT INTO `prestataire` (`ID`, `Nom`, `Prenom`, `Téléphone`, `Email`, `statut`, `commune`, `genre`, `Langue`, `service_id`, `image_path`, `password`, `prix`, `carte_identite`, `casier_judiciaire`, `papier_sejour`) VALUES
(73, 'ahmed', 'mohamed', '0123456789', 'ahmed@f', 'inactive', 'tevragh-zeine', 'Homme', 'francais', 39, 'static/uploads/5.png', 'scrypt:32768:8:1$OZdlQsiaFgbJ9IMC$66ed3ea4aeea2f0d25cb460da11b436344795b023a41dacdbde0cbedcca503862c26068ef6fd07e526ec21ed03835dccbe60c5da6469fe530673ef81ef44d130', 25000, 'static/uploads/3.png', 'static/uploads/1.png', 'static/uploads/2.png'),
(74, 'lalla', 'dehah', '29999999', 'd@mm', 'inactive', 'noukchott', 'Homme', 'francais', 39, 'static/uploads/3.png', 'scrypt:32768:8:1$1MKuFtELdo3SOExY$7d225e7c25f51307a0a62a4f61c23c3b17ee2d517872d1bcbf46037a24838265d44909fde54ffa974221af5d262c819f281475d21399714530d8ea1bc952d47f', 25000, 'static/uploads/1.png', 'static/uploads/1.png', 'static/uploads/4.png'),
(75, 'Fatimata', 'Diop', '17171717', 'fatimata@17', 'active', 'bassra', 'Femme', 'francais', 42, 'static/uploads/11.jpg', 'scrypt:32768:8:1$r3ksEogcHMWca5QO$919af7c75872aca44d6935d812f404c959c77b8ef70ea9da2b5d8f1a52ffd5b134731622aa28d4b461992afe7548361ca9d7957dff8504684cd6af3c4cc1846a', 35000, 'static/uploads/0.jpg', 'static/uploads/0.jpg', 'static/uploads/0.jpg'),
(76, 'Khadi ', 'Saleh', '18181818', 'khadi@18', 'active', 'bassra', 'Femme', 'Arabe', 38, 'static/uploads/12.jpg', 'scrypt:32768:8:1$hDm1P0b3TbQw0roV$53bca1136f9e360d2b42159213925d92ab5f08f16a07782d1c891f21034444149a3f8620870bb2bd3dd8fa4991d6c0c6be6e9bcdd6477ed31ec3a1c15ebe4d09', 30000, 'static/uploads/0.jpg', 'static/uploads/0.jpg', 'static/uploads/0.jpg'),
(77, 'Lalla Zahra', 'Dehah', '07070707', 'lalla@07', 'active', 'Dar-Naim', 'Femme', 'Arabe', 41, 'static/uploads/20.jpg', 'scrypt:32768:8:1$VBjWVWfYQjDfTP60$e8c1e193197d1b5461f391cec18ff427d732739c64f5b0c7e17160b1de523f8b076fa1517b18554687deaa3259c257c0a021dd4cffbceb68cd746bb552c3a5b4', 25000, 'static/uploads/0.jpg', 'static/uploads/0.jpg', 'static/uploads/0.jpg'),
(78, 'mariem', 'mohamed', '2350923509', 'vatimetou@09', 'inactive', 'tevragh-zeine', 'Homme', 'Anglais', 44, 'static/uploads/13.jpg', 'scrypt:32768:8:1$cmBg9XwMNwowTrSu$102c656bf42014a4f354aa5919113e2418d6874c928aaa61863a6b8e16c75829b6aace1142cd7ad33344735c226941878669dd784098ff58d9ff9bab817d62aa', 30000, 'static/uploads/0.jpg', 'static/uploads/0.jpg', 'static/uploads/0.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `service`
--

CREATE TABLE IF NOT EXISTS `service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `catégorie` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=45 ;

--
-- Dumping data for table `service`
--

INSERT INTO `service` (`id`, `catégorie`) VALUES
(39, 'Jardinage'),
(38, 'Ménage'),
(40, 'Plomberie'),
(41, 'Garde d’enfants'),
(42, 'Cuisine'),
(43, 'chauffeur'),
(44, 'Entretien à domicile');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
