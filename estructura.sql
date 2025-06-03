
DROP TABLE IF EXISTS `correos`;
CREATE TABLE `correos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_conversacion` longtext,
  `id_correo` varchar(500) DEFAULT NULL,
  `remitente` varchar(450) DEFAULT NULL,
  `asunto` longtext,
  `fecha_recibido` varchar(450) DEFAULT NULL,
  `categorias` longtext,
  `marcaciones` longtext,
  `archivos` longtext,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_correo_UNIQUE` (`id_correo`)
) ENGINE=InnoDB AUTO_INCREMENT=132 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
