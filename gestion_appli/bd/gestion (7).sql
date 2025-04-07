-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : Dim 06 avr. 2025 à 10:38
-- Version du serveur :  5.7.36
-- Version de PHP : 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `gestion`
--

-- --------------------------------------------------------

--
-- Structure de la table `paiement`
--

DROP TABLE IF EXISTS `paiement`;
CREATE TABLE IF NOT EXISTS `paiement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prestataire_id` int(11) NOT NULL,
  `montant` decimal(10,0) NOT NULL,
  `date` timestamp NOT NULL,
  `capture` text NOT NULL,
  `mode` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `prestataire_id` (`prestataire_id`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `prestataire`
--

DROP TABLE IF EXISTS `prestataire`;
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
  `catégorie` varchar(300) NOT NULL,
  `password` varchar(11) NOT NULL,
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `prestataire`
--

INSERT INTO `prestataire` (`ID`, `Nom`, `Prenom`, `Téléphone`, `Email`, `statut`, `commune`, `genre`, `Langue`, `service_id`, `image_path`, `catégorie`, `password`) VALUES
(16, 'Diop', 'Djeinaba', '48903781', 'diez@gmail.com', 'active', 'Nouadhibou', 'Femme', 'francais', 0, 'static/uploads/WIN_20220106_12_14_59_Pro.jpg', 'cuisinière', '0'),
(14, 'Diop', 'lalle', '444444444', 'inneydiop@gmail.com', 'inactive', 'nktt', 'Femme', 'english', 0, 'static/uploads/2.jpg', 'plombierère', '0'),
(9, 'khadi ', 'med salh', '20372284', '23518@isme.esp.mr', 'active', 'nktt', 'Femme', 'francais', 0, 'static/uploads/1.jpg', 'electrician', '0'),
(8, 'alioune', 'fatimetou', '555555', '23517@isme.esp.mr', 'inactive', 'nktt', 'Femme', 'english', 0, 'static/uploads/ndb.jpg', 'cuisinière', '0');

-- --------------------------------------------------------

--
-- Structure de la table `service`
--

DROP TABLE IF EXISTS `service`;
CREATE TABLE IF NOT EXISTS `service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `catégorie` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=38 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `service`
--

INSERT INTO `service` (`id`, `catégorie`) VALUES
(37, 'Maison'),
(36, 'Corolla');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
