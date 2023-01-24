-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Czas generowania: 10 Sty 2023, 12:11
-- Wersja serwera: 10.4.27-MariaDB
-- Wersja PHP: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `projekt`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `import`
--

CREATE TABLE `import` (
  `id_o` int(11) NOT NULL,
  `obraz` longtext NOT NULL,
  `id_uz` int(11) NOT NULL,
  `czy_adnotacja` tinyint(1) DEFAULT 0 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `logowanie`
--

CREATE TABLE `logowanie` (
  `id` int(11) NOT NULL,
  `login` varchar(15) NOT NULL,
  `haslo` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `import`
--
ALTER TABLE `import`
  ADD PRIMARY KEY (`id_o`),
  ADD KEY `id_uz` (`id_uz`);

--
-- Indeksy dla tabeli `logowanie`
--
ALTER TABLE `logowanie`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT dla zrzuconych tabel
--

--
-- AUTO_INCREMENT dla tabeli `import`
--
ALTER TABLE `import`
  MODIFY `id_o` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT dla tabeli `logowanie`
--
ALTER TABLE `logowanie`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `import`
--
ALTER TABLE `import`
  ADD CONSTRAINT `userIDfk` FOREIGN KEY (`id_uz`) REFERENCES `logowanie` (`id`);

CREATE TABLE info (
    `id_o` int(11) NOT NULL,
    `rodz_kam` varchar(50),
    `pochodzenie` varchar(50),
    `nazwa_pliku` varchar(255) NOT NULL
);

ALTER TABLE `info`
  ADD CONSTRAINT `imgIDfk` FOREIGN KEY (`id_o`) REFERENCES `import` (`id_o`) ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE TABLE kategorie (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `nazwa` char(50) NOT NULL,
    `szkic_kolor` char(30),
    `wyp_kolor` char(30),
    `id_uz` int(11) NOT NULL
);

ALTER TABLE `kategorie`
	ADD CONSTRAINT `katIDuz` FOREIGN KEY (`id_uz`) REFERENCES `logowanie` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE TABLE adnotacje (
    `id_adn` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `id_kat` int NOT NULL,
    `id_o` int NOT NULL,
    `x_start` int NOT NULL,
    `y_start` int NOT NULL,
    `szer` int NOT NULL,
    `wys` int NOT NULL
);

ALTER TABLE `adnotacje`
  ADD CONSTRAINT `annoIDfk` FOREIGN KEY (`id_kat`) REFERENCES `kategorie` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE `adnotacje`
  ADD CONSTRAINT `imgIDfk2` FOREIGN KEY (`id_o`) REFERENCES `import` (`id_o`) ON DELETE RESTRICT ON UPDATE CASCADE;
COMMIT;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
