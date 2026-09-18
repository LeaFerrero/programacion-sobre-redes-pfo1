# Implementación de un Chat Básico Cliente-Servidor

Este proyecto es una implementación de un sistema de chat básico utilizando la arquitectura Cliente-Servidor con sockets en Python. Fue desarrollado como parte de la Propuesta Formativa Obligatoria (PFO) de la materia "Programación sobre redes".

Descripción del Proyecto

La aplicación permite la comunicación unidireccional de mensajes desde múltiples clientes hacia un servidor central. El servidor escucha en el puerto 5000 (por defecto en localhost), recibe los mensajes, los almacena de forma persistente en una base de datos local (SQLite) y devuelve al cliente una confirmación de recepción con la marca de tiempo exacta (timestamp).

## Características Principales

- Arquitectura Modular: El servidor está estructurado para inicializar los sockets y la base de datos de manera independiente.

- Manejo Centralizado de Errores: Las inicializaciones delegan las fallas críticas al ciclo principal, asegurando que cualquier error de red o de base de datos impida un arranque defectuoso.

- Cierre Seguro de Recursos: Implementa validaciones en el bloque finally para asegurar la correcta liberación del puerto de red y el archivo de base de datos, evitando bloqueos de sistema (database is locked o Address already in use).

- Persistencia de Datos: Utiliza sqlite3 para almacenar cada mensaje recibido, registrando id, contenido, fecha_envio e ip_cliente.

- Cliente Interactivo: Permite enviar múltiples mensajes en una misma sesión. Maneja errores de conexión proactivamente y finaliza de manera controlada al escribir la palabra clave éxito (o exito).

Sin Dependencias Externas: Construido íntegramente con los módulos estándar de Python (socket, sqlite3, datetime).

## Requisitos

- Python 3.x instalado en el sistema.

## Instrucciones de Ejecución

Para el correcto funcionamiento del sistema, se debe respetar el orden de inicialización:

1. Iniciar el Servidor

Abrir una terminal en el directorio del proyecto y ejecutar:

python server.py


Se vera un mensaje indicando que la DB fue inicializada y el servidor está escuchando.

2. Iniciar el Cliente

Abrir una nueva terminal y ejecutar:

python cliente.py


Si la conexión es exitosa, se podra comenzar a enviar mensajes.

3. Finalizar la Conexión

Para cerrar el cliente: Escribir la palabra éxito (o exito) en la consola del cliente y presionar Enter.

Para cerrar el servidor: Se debe interrumpir el proceso desde la terminal o cerrar la ventana de comandos.

Archivos del Proyecto

server.py: Script principal del servidor (escucha, manejo de base de datos y clientes).

cliente.py: Script del cliente (envío de mensajes y recepción de confirmaciones).

chat_server.db: Base de datos SQLite (se genera automáticamente en la primera ejecución).

## Autor

- Leandro Raúl Ferrero

- Propuesta Formativa Obligatoria (PFO 1) - Programación sobre redes