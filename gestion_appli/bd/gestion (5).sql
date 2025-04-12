-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Client :  127.0.0.1
-- Généré le :  Sam 12 Avril 2025 à 18:01
-- Version du serveur :  5.6.17
-- Version de PHP :  5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données :  `gestion`
--

-- --------------------------------------------------------

--
-- Structure de la table `admin`
--

CREATE TABLE IF NOT EXISTS `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Structure de la table `paiement`
--

CREATE TABLE IF NOT EXISTS `paiement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prestataire_id` int(11) NOT NULL,
  `montant` decimal(10,0) NOT NULL,
  `date_paiement` date NOT NULL,
  `date_expiration` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `prestataire_id` (`prestataire_id`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Structure de la table `prestataire`
--

CREATE TABLE IF NOT EXISTS `prestataire` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Nom` varchar(250) NOT NULL,
  `Prenom` varchar(250) NOT NULL,
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
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=37 ;

--
-- Contenu de la table `prestataire`
--

INSERT INTO `prestataire` (`ID`, `Nom`, `Prenom`, `Téléphone`, `Email`, `statut`, `commune`, `genre`, `Langue`, `service_id`, `image_path`, `catégorie`, `password`) VALUES
(27, 'lalla', 'dehah', '21345633', 'lalla@dehah', 'active', 'noukchott', 'Homme', 'arabe', NULL, 'uploads/OIP.jpeg', 'None', '07'),
(32, 'mariem', 'mohamed', '0123456789', '23507@isme.esp.mr', 'inactive', 'tevragh-zeine', 'Homme', 'anglais', NULL, 'static/uploads/Capture_2_TP.png', 'chauffeur', '456789'),
(33, 'lalla', 'dehah', '0222222222', '23507@isme.esp.mr', 'active', 'noukchott', 'Homme', 'anglais', NULL, 'static/uploads/Capture_tp.png', 'menage', '66666666666'),
(34, 'lalla', 'dehah', '0222222222', '23507@isme.esp.mr', 'inactive', 'noukchott', 'Homme', 'anglais', NULL, 'static/uploads/cas_1.png', 'menage', '456789'),
(30, 'lalla', 'dehah', '0222222222', '23507@isme.esp.mr', 'active', 'noukchott', 'Homme', 'arabe', NULL, 'static/uploads/cas_1.png', 'menage', '12121212'),
(36, 'lalla', 'dehah', '0222222222', '23507@isme.esp.mr', 'inactive', 'noukchott', 'Homme', 'anglais', NULL, 'static/uploads/cas_1.png', 'menage', '456789'),
(24, 'mariem', 'lalla', '56666656', 'lalla@dehah', 'active', 'tevragh-zeine', 'Homme', 'anglais', NULL, 'static/uploads/OIP.jpeg', 'chauffeur', '07'),
(31, 'mariem', 'mohamed', '123456789', '23507@isme.esp.mr', 'active', 'tevragh-zeine', 'Femme', 'anglais', NULL, 'static/uploads/OIP.jpeg', 'chauffeur', '456789');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
