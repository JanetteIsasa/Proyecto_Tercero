-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 07-02-2023 a las 01:06:48
-- Versión del servidor: 10.4.27-MariaDB
-- Versión de PHP: 8.0.25

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
-- Estructura de tabla para la tabla `actividades`
--

CREATE TABLE `actividades` (
  `id_actividades` int(11) NOT NULL,
  `id_modalidad` int(11) NOT NULL,
  `id_entrenador` int(11) NOT NULL,
  `dia_actividad` varchar(40) NOT NULL,
  `horario_actividad` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auditoria_inscripciones`
--

CREATE TABLE `auditoria_inscripciones` (
  `id_tabla` int(11) NOT NULL,
  `id_inscripcion` varchar(40) NOT NULL,
  `usuario` varchar(40) NOT NULL,
  `fecha_hora` varchar(40) NOT NULL,
  `tipo_accion` varchar(40) NOT NULL,
  `cliente` varchar(100) NOT NULL,
  `fecha_pago` varchar(40) NOT NULL,
  `fecha_pago_auditoria` varchar(40) NOT NULL,
  `fecha_vencimiento` varchar(40) NOT NULL,
  `fecha_vencimiento_auditoria` varchar(40) NOT NULL,
  `monto` varchar(40) NOT NULL,
  `monto_auditoria` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auditoria_pago`
--

CREATE TABLE `auditoria_pago` (
  `id_tabla` int(11) NOT NULL,
  `id_pago` int(11) NOT NULL,
  `usuario` varchar(40) NOT NULL,
  `fecha_hora` varchar(40) NOT NULL,
  `tipo_accion` varchar(40) NOT NULL,
  `esta_pago_anterior` int(4) NOT NULL,
  `estado_actual` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_inscripcion`
--

CREATE TABLE `detalle_inscripcion` (
  `id_detalle_inscripcion` int(11) NOT NULL,
  `id_actividades` int(11) NOT NULL,
  `id_cliente_personal` int(11) NOT NULL,
  `id_inscripcion` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modalidad`
--

CREATE TABLE `modalidad` (
  `id_modalidad` int(11) NOT NULL,
  `nombre_modalidad` varchar(255) NOT NULL,
  `estado_modalidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `idUsuario` int(11) NOT NULL,
  `nombreUsuario` varchar(80) NOT NULL,
  `contrasenaUsuario` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`idUsuario`, `nombreUsuario`, `contrasenaUsuario`) VALUES
(10, 'paty', 'sha256$NFWq5dbc$f46c5470063b22f49b1a3c0f4fb4bc808b8a3f768315b44a248bd18dbf3ff27b'),
(13, 'admin', 'sha256$Kn2QuBefWYVh624U$1394f516fd17fbb8f27a3521ec0119cdd1397aa31aec3cb79d4fa449');

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
  MODIFY `id_cliente_personal` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `detalle_inscripcion`
--
ALTER TABLE `detalle_inscripcion`
  MODIFY `id_detalle_inscripcion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT de la tabla `entrenador`
--
ALTER TABLE `entrenador`
  MODIFY `id_entrenador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `modalidad`
--
ALTER TABLE `modalidad`
  MODIFY `id_modalidad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `pagos`
--
ALTER TABLE `pagos`
  MODIFY `id_pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT de la tabla `registro_entrada`
--
ALTER TABLE `registro_entrada`
  MODIFY `id_registro_entrada` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `seguimiento`
--
ALTER TABLE `seguimiento`
  MODIFY `id_seguimiento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `idUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

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
