-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : Dim 20 avr. 2025 à 07:24
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `paiement`
--

INSERT INTO `paiement` (`id`, `prestataire_id`, `montant`, `date_paiement`, `date_expiration`) VALUES
(17, 38, '2000', '2025-04-18 08:00:00', '2025-05-18 08:00:00'),
(18, 39, '2000', '2025-04-18 08:00:00', '2025-05-18 08:00:00'),
(19, 40, '2000', '2025-04-18 08:00:00', '2025-05-18 08:00:00'),
(20, 41, '2000', '2025-04-18 08:00:00', '2025-05-18 08:00:00'),
(21, 43, '2000', '2025-04-18 08:00:00', '2025-05-18 08:00:00'),
(22, 43, '2000', '2025-04-18 08:00:00', '2025-05-18 08:00:00'),
(23, 43, '2000', '2025-04-18 08:00:00', '2025-05-18 08:00:00'),
(24, 44, '2000', '2025-04-19 08:00:00', '2025-05-19 08:00:00'),
(25, 42, '2000', '2025-04-19 08:00:00', '2025-05-19 08:00:00');

-- --------------------------------------------------------

--
-- Structure de la table `prestataire`
--

DROP TABLE IF EXISTS `prestataire`;
CREATE TABLE IF NOT EXISTS `prestataire` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) NOT NULL,
  `Prenom` text NOT NULL,
  `Téléphone` text NOT NULL,
  `Email` text NOT NULL,
  `statut` text NOT NULL,
  `commune` varchar(300) NOT NULL,
  `genre` text NOT NULL,
  `Langue` text NOT NULL,
  `id_service` int(11) NOT NULL,
  `image_path` varchar(300) DEFAULT NULL,
  `hashed_password` varchar(255) DEFAULT NULL,
  `carte_identité` varchar(255) DEFAULT NULL,
  `casier_judiciaire` varchar(255) DEFAULT NULL,
  `papier_séjour` varchar(255) DEFAULT NULL,
  `prix` varchar(300) NOT NULL,
  PRIMARY KEY (`ID`) USING BTREE,
  KEY `fk_prestataire_service` (`id_service`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `prestataire`
--

INSERT INTO `prestataire` (`ID`, `nom`, `Prenom`, `Téléphone`, `Email`, `statut`, `commune`, `genre`, `Langue`, `id_service`, `image_path`, `hashed_password`, `carte_identité`, `casier_judiciaire`, `papier_séjour`, `prix`) VALUES
(38, 'Sall', 'Moussa', '46529632', 'inneydiop@gmail.com', 'active', 'ndb', 'Homme', 'arab', 43, 'static/uploads/a02.png', NULL, NULL, NULL, NULL, ''),
(39, 'Sall', 'lalle', '456253', 'metou@gmail.com', 'active', 'Nouadhibou', 'Homme', 'spanish', 45, 'static/uploads/Capture_decran_2024-01-14_193039.png', NULL, NULL, NULL, NULL, ''),
(40, 'sylla', 'fatimetou', '45', 'diez@gmail.com', 'active', 'zoueratt', 'Homme', 'pulaar', 46, 'static/uploads/Capture_decran_2024-01-14_194138.png', NULL, NULL, NULL, NULL, ''),
(41, 'Sall', 'lalle', '5', 'innediop@gmail.com', 'active', 'Nouadhibou', 'Homme', 'spanish', 45, 'static/uploads/Capture_decran_2024-01-14_194138.png', NULL, NULL, NULL, NULL, ''),
(42, 'm', 'p', '46570612', 'innediop@gmail.com', 'active', 'Nouakchott', 'Homme', 'arabe', 45, 'static/uploads/Capture_decran_2024-01-14_193952.png', NULL, NULL, NULL, NULL, ''),
(43, 'sylla', 'lalle', '20325436', '23517@isme.esp.mr', 'active', 'zoueratt', 'Homme', 'arabe', 45, 'static/uploads/Capture_decran_2024-01-14_194138.png', NULL, NULL, NULL, NULL, ''),
(44, 'sylla', 'lalle', '46519639', '23518@isme.esp.mr', 'active', 'zoueratt', 'Homme', 'francais', 47, 'static/uploads/Capture_decran_2024-01-14_193039.png', NULL, NULL, NULL, NULL, ''),
(45, 'Sall', 'lalle', '46859632', 'innediop@gmail.com', 'inactive', 'nktt', 'Homme', 'english', 43, 'static/uploads/Capture_decran_2024-01-14_195047.png', 'scrypt:32768:8:1$d1GRt7UadILvju3u$e0c09fcc4da78891d0d86613718b0ce3cf5dc77edf35b103ae4987cc1e84503db467ac9a287e3bbd0769aa48a328b50b4876cce9e5fd8569137c7754f8c6e51d', NULL, NULL, NULL, ''),
(46, 'sylla', 'Moussa', '32564187', 'salma@gmail.com', 'inactive', 'Nouakchott', 'Homme', 'arabe', 43, 'static/uploads/Capture_decran_2024-01-14_193039.png', 'scrypt:32768:8:1$7INYRv9nTarUgjZf$270ac3b02b60d89a029597fe592e3d43e248d97894765c0bf1cc6d00d39dfe3101f19b94b5ff87466bb49daed424b7713689c11eceb8af8a7acb51d17091e987', NULL, NULL, NULL, ''),
(47, 'alioun', 'adama', '20325435', 'inneydiop@gmail.com', 'inactive', 'Rosso', 'Homme', 'english', 50, 'static/uploads/Capture_decran_2024-01-14_195047.png', 'scrypt:32768:8:1$B2i6KETr2oJ8dpBf$79b44acb0249998c6cd3e59ca71842a0ac21b0d7039b14c39745164f252176394d072f105a0cf7c90bde333fabe47640debd71dc31e6c130d2fa773901de7817', NULL, NULL, NULL, ''),
(48, 'sy', 'fatim', '41569874', 'fatim@gmail.com', 'active', 'Rosso', 'Homme', 'spanish', 47, 'static/uploads/a02.png', 'static/uploads/Capture_decran_2024-01-14_195147.png', 'static/uploads/Capture_decran_2024-12-25_004953.png', 'static/uploads/Capture_decran_2024-01-14_193039.png', 'static/uploads/Capture_decran_2024-01-14_193421.png', '');

-- --------------------------------------------------------

--
-- Structure de la table `service`
--

DROP TABLE IF EXISTS `service`;
CREATE TABLE IF NOT EXISTS `service` (
  `id_service` int(11) NOT NULL AUTO_INCREMENT,
  `catégorie` text NOT NULL,
  PRIMARY KEY (`id_service`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `service`
--

INSERT INTO `service` (`id_service`, `catégorie`) VALUES
(43, 'Plombier'),
(45, 'Jardinier'),
(46, 'Cuisinier'),
(47, 'Ménage'),
(50, 'garde d\'enfant'),
(51, 'Electricien');

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `paiement`
--
ALTER TABLE `paiement`
  ADD CONSTRAINT `paiement_ibfk_1` FOREIGN KEY (`prestataire_id`) REFERENCES `prestataire` (`ID`);

--
-- Contraintes pour la table `prestataire`
--
ALTER TABLE `prestataire`
  ADD CONSTRAINT `fk_prestataire_service` FOREIGN KEY (`id_service`) REFERENCES `service` (`id_service`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
