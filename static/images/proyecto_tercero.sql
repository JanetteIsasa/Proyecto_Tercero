-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-09-2020 a las 23:22:40
-- Versión del servidor: 10.4.11-MariaDB
-- Versión de PHP: 7.2.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyecto_tercero`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente_personal`
--

CREATE TABLE `cliente_personal` (
  `id_cliente_persona` int(11) NOT NULL,
  `nombre_cliente` varchar(255) NOT NULL,
  `apellido_cliente` varchar(255) NOT NULL,
  `fecha_nacimiento_cliente` date NOT NULL,
  `cedula_cliente` varchar(20) NOT NULL,
  `telefono_cliente` varchar(25) NOT NULL,
  `email_cliente` varchar(255) NOT NULL,
  `direccion_cliente` varchar(255) NOT NULL,
  `obra_social_cliente` varchar(255) NOT NULL,
  `contacto_urgencia_cliente` varchar(255) NOT NULL,
  `telefono_urgencia_cliente` varchar(25) NOT NULL,
  `grupo_sanguineo_cliente` varchar(200) NOT NULL,
  `carnet_cliente` varchar(100) NOT NULL,
  `lugar_traslado_cliente` varchar(255) NOT NULL,
  `horario_traslado_cliente` time NOT NULL,
  `enfermedades_cliente` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `cliente_personal`
--

INSERT INTO `cliente_personal` (`id_cliente_persona`, `nombre_cliente`, `apellido_cliente`, `fecha_nacimiento_cliente`, `cedula_cliente`, `telefono_cliente`, `email_cliente`, `direccion_cliente`, `obra_social_cliente`, `contacto_urgencia_cliente`, `telefono_urgencia_cliente`, `grupo_sanguineo_cliente`, `carnet_cliente`, `lugar_traslado_cliente`, `horario_traslado_cliente`, `enfermedades_cliente`) VALUES
(1, 'Patricia Janette', 'Valdez Isasa', '0000-00-00', '5335339', '0983512825', '', 'Pedro Juan Caballero c/ Mario Rios y Santa Clara', '5231', 'jj', '00112233', '0+', '2222', 'CMS', '20:00:00', ''),
(2, 'Patricia Janette', 'Valdez Isasa', '0000-00-00', '5335339', '0983512825', '', 'Pedro Juan Caballero c/ Mario Rios y Santa Clara', '5231', 'jj', '00112233', '0+', '2222', 'CMS', '20:00:00', ''),
(3, 'Jennifer', 'Valdez', '2000-09-01', '1234568', '456132', 'jennifer@gmail.com', 'aaaaaaaaaaaa', 'aaaaaaaaaaaaa', 'aaaaaaaaaa', 'aaaaaaaaaaaaa', 'aaaaaaaaa', 'aaaaaaaaaa', 'aaaaaaaaaaa', '00:00:00', 'aaaaaaaaaaaaa'),
(4, 'Jennifer', 'Valdez', '2000-09-01', '1234568', '456132', 'jennifer@gmail.com', 'aaaaaaaaaaaa', 'aaaaaaaaaaaaa', 'aaaaaaaaaa', 'aaaaaaaaaaaaa', 'aaaaaaaaa', 'aaaaaaaaaa', 'aaaaaaaaaaa', '00:00:00', 'aaaaaaaaaaaaa');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entrenador`
--

CREATE TABLE `entrenador` (
  `id_entrenador` int(11) NOT NULL,
  `nombre_entrenador` varchar(255) NOT NULL,
  `cedula_entrenador` varchar(15) NOT NULL,
  `telefono_entrenador` varchar(255) NOT NULL,
  `email_entrenador` varchar(255) NOT NULL,
  `direccion_entrenador` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `entrenador`
--

INSERT INTO `entrenador` (`id_entrenador`, `nombre_entrenador`, `cedula_entrenador`, `telefono_entrenador`, `email_entrenador`, `direccion_entrenador`) VALUES
(3, 'Maria', '123456', '2255336', 'cvc@df', 'Prof. Mario Rios'),
(4, 'Patricia', '5335339', '1478523', 'pati@gmail.com', 'Prof. Mario Rios'),
(7, 'Luz', '5335388', '2255336', 'luz@gmail.com', 'Pedro Juan Caballero');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modalidad`
--

CREATE TABLE `modalidad` (
  `id_modalidad` int(11) NOT NULL,
  `nombre_modalidad` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `modalidad`
--

INSERT INTO `modalidad` (`id_modalidad`, `nombre_modalidad`) VALUES
(2, 'Zumba');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cliente_personal`
--
ALTER TABLE `cliente_personal`
  ADD PRIMARY KEY (`id_cliente_persona`);

--
-- Indices de la tabla `entrenador`
--
ALTER TABLE `entrenador`
  ADD PRIMARY KEY (`id_entrenador`);

--
-- Indices de la tabla `modalidad`
--
ALTER TABLE `modalidad`
  ADD PRIMARY KEY (`id_modalidad`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cliente_personal`
--
ALTER TABLE `cliente_personal`
  MODIFY `id_cliente_persona` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `entrenador`
--
ALTER TABLE `entrenador`
  MODIFY `id_entrenador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `modalidad`
--
ALTER TABLE `modalidad`
  MODIFY `id_modalidad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
