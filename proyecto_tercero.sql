-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-12-2020 a las 23:55:08
-- Versión del servidor: 10.1.38-MariaDB
-- Versión de PHP: 7.3.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
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
-- Estructura de tabla para la tabla `actividades`
--

CREATE TABLE `actividades` (
  `id_actividades` int(11) NOT NULL,
  `id_modalidad` int(11) NOT NULL,
  `id_entrenador` int(11) NOT NULL,
  `dia_actividad` varchar(40) NOT NULL,
  `horario_actividad` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `actividades`
--

INSERT INTO `actividades` (`id_actividades`, `id_modalidad`, `id_entrenador`, `dia_actividad`, `horario_actividad`) VALUES
(2, 3, 3, 'Lunes', '16:00'),
(3, 10, 4, 'Lunes', '09:00'),
(4, 3, 3, 'Miercoles', '16:00'),
(5, 10, 4, 'Martes', '09:00'),
(6, 10, 4, 'Jueves', '09:00'),
(7, 10, 4, 'Miercoles', '09:00'),
(8, 3, 3, 'Martes', '16:00'),
(9, 3, 3, 'Jueves', '16:00'),
(10, 3, 3, 'Viernes', '16:00'),
(12, 12, 8, 'Lunes', '17:00'),
(13, 13, 4, 'Lunes', '19:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auditoria_inscripciones`
--

CREATE TABLE `auditoria_inscripciones` (
  `id_tabla` int(11) NOT NULL,
  `id_inscripcion` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `usuario` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_hora` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo_accion` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cliente` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_pago` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_pago_auditoria` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_vencimiento` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_vencimiento_auditoria` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `monto` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `monto_auditoria` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `auditoria_inscripciones`
--

INSERT INTO `auditoria_inscripciones` (`id_tabla`, `id_inscripcion`, `usuario`, `fecha_hora`, `tipo_accion`, `cliente`, `fecha_pago`, `fecha_pago_auditoria`, `fecha_vencimiento`, `fecha_vencimiento_auditoria`, `monto`, `monto_auditoria`) VALUES
(9, '1c9bf162-aab6-4abe-9ad9-392f60850a88', 'Admin', '2020-12-21 14:49:42.409000', 'Editado', 'Karen Moreno', '2020-12-21', '2020-12-21', '2020-12-21', '2020-12-22', '120000', '120000'),
(10, 'd7a7bc6a-26d9-4c67-8c2c-c8c79d453887', 'Admin', '2020-12-21 16:29:08.821000', 'Eliminado', 'Leila Gisela Falcon Mascareño', '2020-12-21', '2020-12-21', '2020-12-24', '2020-12-24', '50000', '50000'),
(11, '496a10c6-4192-4f9a-83bd-3f0413a87131', 'Admin', '2020-12-21 18:09:42.879000', 'Eliminado', 'Karen Moreno', '2020-12-21', '2020-12-21', '2020-12-27', '2020-12-27', '50000', '50000');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auditoria_pago`
--

CREATE TABLE `auditoria_pago` (
  `id_tabla` int(11) NOT NULL,
  `id_pago` int(11) NOT NULL,
  `usuario` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_hora` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo_accion` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `esta_pago_anterior` int(4) NOT NULL,
  `estado_actual` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `auditoria_pago`
--

INSERT INTO `auditoria_pago` (`id_tabla`, `id_pago`, `usuario`, `fecha_hora`, `tipo_accion`, `esta_pago_anterior`, `estado_actual`) VALUES
(2, 43, 'Admin', '2020-12-21 15:11:21.470000', 'Eliminado', 1, 0),
(3, 44, 'Admin', '2020-12-21 18:18:53.134000', 'Eliminado', 1, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente_personal`
--

CREATE TABLE `cliente_personal` (
  `id_cliente_personal` int(11) NOT NULL,
  `nombre_cliente` varchar(255) NOT NULL,
  `apellido_cliente` varchar(255) NOT NULL,
  `fecha_nacimiento_cliente` varchar(40) NOT NULL,
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
  `horario_traslado_cliente` varchar(50) NOT NULL,
  `enfermedades_cliente` varchar(255) NOT NULL,
  `pesaje_actual_seguimiento` float NOT NULL,
  `estado_cliente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `cliente_personal`
--

INSERT INTO `cliente_personal` (`id_cliente_personal`, `nombre_cliente`, `apellido_cliente`, `fecha_nacimiento_cliente`, `cedula_cliente`, `telefono_cliente`, `email_cliente`, `direccion_cliente`, `obra_social_cliente`, `contacto_urgencia_cliente`, `telefono_urgencia_cliente`, `grupo_sanguineo_cliente`, `carnet_cliente`, `lugar_traslado_cliente`, `horario_traslado_cliente`, `enfermedades_cliente`, `pesaje_actual_seguimiento`, `estado_cliente`) VALUES
(9, 'Leila Gisela', 'Falcon Mascareño', '2000-03-08', '6229991', '(0972) 215 381', 'leilagisel001@gmail.com', 'Rosalia Candia c/ Cecilio Báez', '1234', 'Patricia Valdez', '(0983) 512 825', '0+', '1234', 'IPS', '14:20', 'NO', 62, 1),
(11, 'Karen', 'Moreno', '1994-04-11', '5501073', '(0975) 256 785', 'karen@gmail.com', 'Pedro Juan Caballero', '', '', '', '', '', '', '', '', 72, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_inscripcion`
--

CREATE TABLE `detalle_inscripcion` (
  `id_detalle_inscripcion` int(11) NOT NULL,
  `id_actividades` int(11) NOT NULL,
  `id_cliente_personal` int(11) NOT NULL,
  `id_inscripcion` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `detalle_inscripcion`
--

INSERT INTO `detalle_inscripcion` (`id_detalle_inscripcion`, `id_actividades`, `id_cliente_personal`, `id_inscripcion`) VALUES
(49, 6, 11, '1c9bf162-aab6-4abe-9ad9-392f60850a88'),
(50, 4, 11, '1c9bf162-aab6-4abe-9ad9-392f60850a88'),
(51, 2, 11, '1c9bf162-aab6-4abe-9ad9-392f60850a88');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entrenador`
--

CREATE TABLE `entrenador` (
  `id_entrenador` int(11) NOT NULL,
  `nombre_entrenador` varchar(255) NOT NULL,
  `cedula_entrenador` varchar(15) NOT NULL,
  `edad_entrenador` varchar(40) NOT NULL,
  `telefono_entrenador` varchar(255) NOT NULL,
  `email_entrenador` varchar(255) NOT NULL,
  `direccion_entrenador` varchar(255) NOT NULL,
  `estado_entrenador` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `entrenador`
--

INSERT INTO `entrenador` (`id_entrenador`, `nombre_entrenador`, `cedula_entrenador`, `edad_entrenador`, `telefono_entrenador`, `email_entrenador`, `direccion_entrenador`, `estado_entrenador`) VALUES
(3, 'Maria Martinez', '123456', '23', '(0981) 446 111', 'cvc@df', 'Prof. Mario Rios', 1),
(4, 'Patricia Valdez', '5335339', '20', '(0985) 123 121 ', 'pati@gmail.com', 'Prof. Mario Rios', 1),
(7, 'Luz', '5335388', '25', '(0975) 147 258', 'luz@gmail.com', 'Pedro Juan Caballero', 1),
(8, 'Jennifer Valdez', '5335237', '18', '(0975) 137 765', 'jennfer@gmail.com', 'Pedro Juan Caballero', 0),
(9, 'Gisselle Valdez', '1122334', '19', '(0975) 125 854', 'gisselle@gmail.com', 'Pedro Juan Caballero', 0),
(10, 'Ivan Varela', '78946656', '25', '(0975) 134 455', 'cvcdf@gmail.com', 'Pedro Juan Caballero', 0),
(11, 'Jennifer Valdez', '5335237', '19', '(0985) 123 121', 'jennfer@gmail.com', 'Pedro Juan Caballero', 0),
(12, 'Fgdfg', '5555', '25', '(0975) 125 854', 'bnng@gmail.com', 'Prof. Mario Rios', 0),
(13, 'Jennifer Valdez', '1122334', '24', '(0981) 446 111', 'jennfer@gmail.com', 'Pedro Juan Caballero', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inscripcion`
--

CREATE TABLE `inscripcion` (
  `id_inscripcion` varchar(40) NOT NULL,
  `fecha_de_pago` varchar(40) NOT NULL,
  `fecha_de_vencimiento` varchar(40) NOT NULL,
  `total_a_pagar` varchar(40) NOT NULL,
  `fecha_vencimiento_actual` date NOT NULL,
  `fecha_pago_anterior_actual` varchar(40) NOT NULL,
  `estado_pago` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `inscripcion`
--

INSERT INTO `inscripcion` (`id_inscripcion`, `fecha_de_pago`, `fecha_de_vencimiento`, `total_a_pagar`, `fecha_vencimiento_actual`, `fecha_pago_anterior_actual`, `estado_pago`) VALUES
('1c9bf162-aab6-4abe-9ad9-392f60850a88', '2020-12-21', '2020-12-22', '120000', '2020-12-28', '2020-12-27', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modalidad`
--

CREATE TABLE `modalidad` (
  `id_modalidad` int(11) NOT NULL,
  `nombre_modalidad` varchar(255) NOT NULL,
  `estado_modalidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `modalidad`
--

INSERT INTO `modalidad` (`id_modalidad`, `nombre_modalidad`, `estado_modalidad`) VALUES
(3, 'Entrenamiento Hit', 0),
(10, 'Funcionales', 1),
(12, 'Localizado', 1),
(13, 'Pilates Reformer', 1),
(14, 'Zumba Fitness', 1),
(16, 'Pesas', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

CREATE TABLE `pagos` (
  `id_pago` int(11) NOT NULL,
  `fecha_de_pago` varchar(40) NOT NULL,
  `pagado_desde` varchar(40) NOT NULL,
  `pagado_hasta` date NOT NULL,
  `monto` varchar(100) NOT NULL,
  `id_inscripcion` varchar(50) NOT NULL,
  `estado_eliminado_pago` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `pagos`
--

INSERT INTO `pagos` (`id_pago`, `fecha_de_pago`, `pagado_desde`, `pagado_hasta`, `monto`, `id_inscripcion`, `estado_eliminado_pago`) VALUES
(41, '2020-12-21', '2020-12-23', '2020-12-24', '120000', '1c9bf162-aab6-4abe-9ad9-392f60850a88', 0),
(42, '2020-12-21', '2020-12-25', '2020-12-26', '120000', '1c9bf162-aab6-4abe-9ad9-392f60850a88', 0),
(43, '2020-12-21', '2020-12-27', '2020-12-28', '120000', '1c9bf162-aab6-4abe-9ad9-392f60850a88', 0),
(44, '2020-12-22', '2020-12-27', '2020-12-30', '120000', '1c9bf162-aab6-4abe-9ad9-392f60850a88', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_entrada`
--

CREATE TABLE `registro_entrada` (
  `id_registro_entrada` int(11) NOT NULL,
  `id_cliente_personal` int(11) NOT NULL,
  `id_modalidad` int(11) NOT NULL,
  `fecha_entrada` varchar(40) NOT NULL,
  `horario_entrada` varchar(30) NOT NULL,
  `horario_salida` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `registro_entrada`
--

INSERT INTO `registro_entrada` (`id_registro_entrada`, `id_cliente_personal`, `id_modalidad`, `fecha_entrada`, `horario_entrada`, `horario_salida`) VALUES
(11, 11, 10, '2020-12-21', '18:10', '22:11');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `seguimiento`
--

CREATE TABLE `seguimiento` (
  `id_seguimiento` int(11) NOT NULL,
  `id_cliente_personal` int(11) NOT NULL,
  `fecha_seguimiento` text NOT NULL,
  `peso_anterior_seguimiento` float NOT NULL,
  `pesaje_seguimiento` float NOT NULL,
  `diferencia_pesaje` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `seguimiento`
--

INSERT INTO `seguimiento` (`id_seguimiento`, `id_cliente_personal`, `fecha_seguimiento`, `peso_anterior_seguimiento`, `pesaje_seguimiento`, `diferencia_pesaje`) VALUES
(17, 11, '2020-12-21', 70, 70, -0),
(18, 11, '2020-12-21', 70, 72, 2),
(19, 11, '2020-12-20', 72, 72, -0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `idUsuario` int(11) NOT NULL,
  `nombreUsuario` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contrasenaUsuario` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`idUsuario`, `nombreUsuario`, `contrasenaUsuario`) VALUES
(5, 'admin', 'sha256$smNCriSt$846c20b3db3a87732da747b9442f3c5b5800322354b185065e6b485a80b6c277'),
(10, 'paty', 'sha256$NFWq5dbc$f46c5470063b22f49b1a3c0f4fb4bc808b8a3f768315b44a248bd18dbf3ff27b'),
(12, 'janette', 'sha256$Q3gfwGGL$a0e295456252422fc09183e9b18108410ab11db6034c5f87554bab9028a66933');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `actividades`
--
ALTER TABLE `actividades`
  ADD PRIMARY KEY (`id_actividades`),
  ADD KEY `id_modalidad` (`id_modalidad`),
  ADD KEY `id_entrenador` (`id_entrenador`);

--
-- Indices de la tabla `auditoria_inscripciones`
--
ALTER TABLE `auditoria_inscripciones`
  ADD PRIMARY KEY (`id_tabla`);

--
-- Indices de la tabla `auditoria_pago`
--
ALTER TABLE `auditoria_pago`
  ADD PRIMARY KEY (`id_tabla`),
  ADD KEY `id_pago` (`id_pago`);

--
-- Indices de la tabla `cliente_personal`
--
ALTER TABLE `cliente_personal`
  ADD PRIMARY KEY (`id_cliente_personal`);

--
-- Indices de la tabla `detalle_inscripcion`
--
ALTER TABLE `detalle_inscripcion`
  ADD PRIMARY KEY (`id_detalle_inscripcion`),
  ADD KEY `id_actividades` (`id_actividades`),
  ADD KEY `id_cliente_personal` (`id_cliente_personal`),
  ADD KEY `id_inscripcion` (`id_inscripcion`);

--
-- Indices de la tabla `entrenador`
--
ALTER TABLE `entrenador`
  ADD PRIMARY KEY (`id_entrenador`);

--
-- Indices de la tabla `inscripcion`
--
ALTER TABLE `inscripcion`
  ADD PRIMARY KEY (`id_inscripcion`);

--
-- Indices de la tabla `modalidad`
--
ALTER TABLE `modalidad`
  ADD PRIMARY KEY (`id_modalidad`);

--
-- Indices de la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD PRIMARY KEY (`id_pago`),
  ADD KEY `id_inscripcion` (`id_inscripcion`);

--
-- Indices de la tabla `registro_entrada`
--
ALTER TABLE `registro_entrada`
  ADD PRIMARY KEY (`id_registro_entrada`),
  ADD KEY `id_cliente_peronal` (`id_cliente_personal`,`id_modalidad`),
  ADD KEY `id_modalidad` (`id_modalidad`);

--
-- Indices de la tabla `seguimiento`
--
ALTER TABLE `seguimiento`
  ADD PRIMARY KEY (`id_seguimiento`),
  ADD KEY `id_cliente_personal` (`id_cliente_personal`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`idUsuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `actividades`
--
ALTER TABLE `actividades`
  MODIFY `id_actividades` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `auditoria_inscripciones`
--
ALTER TABLE `auditoria_inscripciones`
  MODIFY `id_tabla` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `auditoria_pago`
--
ALTER TABLE `auditoria_pago`
  MODIFY `id_tabla` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `cliente_personal`
--
ALTER TABLE `cliente_personal`
  MODIFY `id_cliente_personal` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `detalle_inscripcion`
--
ALTER TABLE `detalle_inscripcion`
  MODIFY `id_detalle_inscripcion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT de la tabla `entrenador`
--
ALTER TABLE `entrenador`
  MODIFY `id_entrenador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `modalidad`
--
ALTER TABLE `modalidad`
  MODIFY `id_modalidad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `pagos`
--
ALTER TABLE `pagos`
  MODIFY `id_pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT de la tabla `registro_entrada`
--
ALTER TABLE `registro_entrada`
  MODIFY `id_registro_entrada` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `seguimiento`
--
ALTER TABLE `seguimiento`
  MODIFY `id_seguimiento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `idUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `actividades`
--
ALTER TABLE `actividades`
  ADD CONSTRAINT `actividades_ibfk_1` FOREIGN KEY (`id_modalidad`) REFERENCES `modalidad` (`id_modalidad`),
  ADD CONSTRAINT `actividades_ibfk_2` FOREIGN KEY (`id_entrenador`) REFERENCES `entrenador` (`id_entrenador`);

--
-- Filtros para la tabla `auditoria_pago`
--
ALTER TABLE `auditoria_pago`
  ADD CONSTRAINT `auditoria_pago_ibfk_1` FOREIGN KEY (`id_pago`) REFERENCES `pagos` (`id_pago`);

--
-- Filtros para la tabla `detalle_inscripcion`
--
ALTER TABLE `detalle_inscripcion`
  ADD CONSTRAINT `detalle_inscripcion_ibfk_1` FOREIGN KEY (`id_actividades`) REFERENCES `actividades` (`id_actividades`),
  ADD CONSTRAINT `detalle_inscripcion_ibfk_2` FOREIGN KEY (`id_cliente_personal`) REFERENCES `cliente_personal` (`id_cliente_personal`),
  ADD CONSTRAINT `detalle_inscripcion_ibfk_3` FOREIGN KEY (`id_inscripcion`) REFERENCES `inscripcion` (`id_inscripcion`);

--
-- Filtros para la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`id_inscripcion`) REFERENCES `inscripcion` (`id_inscripcion`);

--
-- Filtros para la tabla `registro_entrada`
--
ALTER TABLE `registro_entrada`
  ADD CONSTRAINT `registro_entrada_ibfk_1` FOREIGN KEY (`id_modalidad`) REFERENCES `modalidad` (`id_modalidad`),
  ADD CONSTRAINT `registro_entrada_ibfk_2` FOREIGN KEY (`id_cliente_personal`) REFERENCES `cliente_personal` (`id_cliente_personal`);

--
-- Filtros para la tabla `seguimiento`
--
ALTER TABLE `seguimiento`
  ADD CONSTRAINT `seguimiento_ibfk_1` FOREIGN KEY (`id_cliente_personal`) REFERENCES `cliente_personal` (`id_cliente_personal`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
