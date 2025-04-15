-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mar. 15 avr. 2025 à 08:41
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
-- Structure de la table `messages`
--

DROP TABLE IF EXISTS `messages`;
CREATE TABLE IF NOT EXISTS `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `lu` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `messages`
--

INSERT INTO `messages` (`id`, `name`, `email`, `message`, `date`, `lu`) VALUES
(1, 'Inney', 'inneydiop@gmail.com', 'salut', '2025-04-11 19:51:12', 1),
(2, 'fatima', 'mous@gmail.com', 'kjh', '2025-04-12 09:49:20', 1),
(3, 'lalle', 'salma@gmail.com', 'je souhaite m\'inscrire dans votre site', '2025-04-12 10:12:36', 1),
(4, 'Moussa', 'mous@gmail.com', 'ou se trouve votre siège?', '2025-04-12 11:50:16', 1),
(5, 'fatimetou ', 'metou@gmail.com', 'Très bon site.', '2025-04-15 06:21:12', 1);

-- --------------------------------------------------------

--
-- Structure de la table `paiement`
--

DROP TABLE IF EXISTS `paiement`;
CREATE TABLE IF NOT EXISTS `paiement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prestataire_id` int(11) NOT NULL,
  `montant` decimal(10,0) NOT NULL,
  `date_paiement` timestamp NOT NULL,
  `date_expiration` timestamp NOT NULL,
  PRIMARY KEY (`id`),
  KEY `prestataire_id` (`prestataire_id`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `paiement`
--

INSERT INTO `paiement` (`id`, `prestataire_id`, `montant`, `date_paiement`, `date_expiration`) VALUES
(1, 22, '2000', '2025-04-14 08:00:00', '2025-05-14 08:00:00'),
(2, 8, '2000', '2025-04-14 08:00:00', '2025-05-14 08:00:00'),
(3, 20, '2000', '2025-04-14 08:00:00', '2025-05-14 08:00:00');

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
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `prestataire`
--

INSERT INTO `prestataire` (`ID`, `Nom`, `Prenom`, `Téléphone`, `Email`, `statut`, `commune`, `genre`, `Langue`, `service_id`, `image_path`, `catégorie`) VALUES
(23, 'sy', 'Dija', '45968243', 'diez@gmail.com', 'inactive', 'ndb', 'Homme', 'arabe', NULL, 'static/uploads/images_1.jpg', 'femme de menage'),
(22, 'khadi ', 'med salh', '20548695', '23518@isme.esp.mr', 'inactive', 'zoueratt', 'Homme', 'spanish', NULL, 'static/uploads/telechargement_6.jpg', 'babysitter'),
(8, 'alioun', 'fatimetou', '555555', '23517@isme.esp.mr', 'inactive', 'nktt', 'Homme', 'english', 0, 'static/uploads/ndb.jpg', 'chauffeur'),
(21, 'Diop', 'Moussa', '45826332', 'mous@gmail.com', 'inactive', 'nktt', 'Homme', 'wolof', NULL, 'static/uploads/images.jpg', 'jardinier'),
(18, 'Ba', 'Salif', '45856541', 'innediop@gmail.com', 'inactive', 'ndb', 'Homme', 'spanish', NULL, 'static/uploads/telechargement_3.jpg', 'chauffeur'),
(20, 'sylla', 'Omar', '4859652', '23518@isme.esp.mr', 'inactive', 'ndb', 'Homme', 'english', NULL, 'static/uploads/1.jpg', 'jardinier');

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
