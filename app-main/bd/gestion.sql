-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Client :  127.0.0.1
-- Généré le :  Dim 30 Mars 2025 à 18:26
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
-- Structure de la table `prestataire`
--

CREATE TABLE IF NOT EXISTS `prestataire` (
  `ID_prestataire` int(11) NOT NULL AUTO_INCREMENT,
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
  `emploi` varchar(300) NOT NULL,
  PRIMARY KEY (`ID_prestataire`) USING BTREE,
  KEY `service_id` (`service_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

--
-- Contenu de la table `prestataire`
--

INSERT INTO `prestataire` (`ID_prestataire`, `Nom`, `Prenom`, `Téléphone`, `Email`, `statut`, `commune`, `genre`, `Langue`, `service_id`, `image_path`, `emploi`) VALUES
(1, 'Diop', 'Fatimata', '47015266', 'inneydiop@gmail.com', 'inactive', 'Nouackchott', 'Femme', 'français', NULL, NULL, ''),
(2, 'Diop', 'Fatimata', '47015266', 'inndi@gmail.com', 'active', 'Nouackchott', 'Homme', 'français', NULL, NULL, ''),
(3, 'lalla', 'dehah', '22222220555555', '23507@isme.esp.mr', 'active', 'Nouakchott', 'Femme', 'arabe', NULL, NULL, 'femme a menage'),
(4, 'mariem', 'mohamed', '22222220555555', '23507@isme.esp.mr', 'active', 'tevragh-zeine', 'Femme', 'francais', NULL, 'static/uploads/Capture_decran_2025-01-22_101315.png', 'femme a menage'),
(5, 'melike', 'dehah', '27252725', 'melikedh@gmail.com', 'active', 'tevragh-zeine', 'Femme', 'arabe', NULL, 'static/uploads/Capture_2_TP.png', 'femme a menage'),
(6, 'fatimetou ', 'alioune', '22666666', 'fatimooo@gmil.com', 'active', 'tevragh-zeine', 'Femme', 'anglais', NULL, 'static/uploads/capture_examen.png', 'chauffeur'),
(7, 'lalla', 'dehah', '22222222', '23507@isme.esp.mr', 'active', 'noukchott', 'Femme', 'francais', NULL, 'static/uploads/cas_2.png', 'femme a menage'),
(8, 'lalla', 'dehah', '22222222', '23507@isme.esp.mr', 'active', 'noukchott', 'Homme', 'francais', NULL, 'static/uploads/Capture_tp.png', 'femme a menage');

-- --------------------------------------------------------

--
-- Structure de la table `service`
--

CREATE TABLE IF NOT EXISTS `service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `catégorie` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=38 ;

--
-- Contenu de la table `service`
--

INSERT INTO `service` (`id`, `catégorie`) VALUES
(37, 'Maison'),
(36, 'Corolla');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
