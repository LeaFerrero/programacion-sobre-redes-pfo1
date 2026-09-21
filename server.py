import sqlite3
import socket
import datetime


def inicializar_db(nombre_db="chat_server.db"):
    # Inicialización y configuración de la base de datos SQLite
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    # Creación de la tabla para almacenar los mensajes con los campos solicitados
    tabla_mensajes = """
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        """

    # Guardar los cambios
    cursor.execute(tabla_mensajes)
    conexion.commit()
    print("Base de datos inicializada correctamente.")

    return conexion


def guardar_mensaje_db(conexion, contenido, fecha, ip_cliente):
    try:
        cursor = conexion.cursor()

        # Consulta parametrizada para evitar inyección SQL
        consulta = """
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        """

        cursor.execute(consulta, (contenido, fecha, ip_cliente))
        conexion.commit()
        print(f"Mensaje registrado: {contenido}")

    except sqlite3.Error as e:
        print(f"Error en la base de datos durante la inserción. Detalle: {e}")


def inicializar_socket(host="localhost", port=5000):
    # Configuración del socket TCP/IP
    # Se instancia el socket definiendo la familia de direcciones y el protocolo
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configuración opcional para evitar el error "Address already in use" al reiniciar el script
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Se enlaza el socket a la dirección y puerto especificados
    server_socket.bind((host, port))

    # Se pone el socket en modo de escucha (el parámetro 5 indica la cola de conexiones máximas en espera)
    server_socket.listen(5)

    print(f"Servidor escuchando en {host}:{port}...")

    return server_socket


def iniciar_server(host="localhost", port=5000):
    conexion = None
    server_socket = None


    try:
        # Inicialización de recursos
        conexion = inicializar_db()
        server_socket = inicializar_socket(host, port)
        print("El servidor está activo y en espera de clientes...")

        # Bucle principal para aceptar conexiones entrantes
        while True:
            try:
                conexion_cliente, direccion_cliente = server_socket.accept()
                ip_cliente = direccion_cliente[0]
                print(f"Conexión establecida desde {direccion_cliente}")

                try:
                    # Bucle secundario para recibir múltiples mensajes del mismo cliente
                    while True:
                        datos = conexion_cliente.recv(1024)

                        # Si recv() devuelve un bloque vacío, el cliente cerró la conexión
                        if not datos:
                            print(f"El cliente {ip_cliente} se ha desconectado.")
                            break

                        # Decodificar el mensaje a texto
                        contenido = datos.decode("utf-8")

                        # Generar el timestamp actual
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        # Guardar el mensaje en la base de datos SQLite
                        guardar_mensaje_db(conexion, contenido, timestamp, ip_cliente)

                        # Enviar la confirmación al cliente con el formato estricto
                        respuesta = f"Mensaje recibido: {timestamp}"
                        conexion_cliente.sendall(respuesta.encode("utf-8"))

                except socket.error as e:
                    print(f"Error de transmisión con el cliente {ip_cliente}. Detalle: {e}")

                finally:
                    # Liberar el socket ESPECÍFICO de este cliente
                    conexion_cliente.close()

            except socket.error as e:
                print(f"Error al intentar aceptar una conexión: {e}")

    except sqlite3.Error as e:
        print(f"Error crítico de Base de Datos al iniciar: {e}")
    except socket.error as e:
        print(f"Error crítico de Red al iniciar (¿Puerto {5000} ocupado?): {e}")

    finally:
        # Liberar los recursos generales del servidor solo si llegaron a crearse
        if server_socket:
            server_socket.close()
        if conexion:
            conexion.close()
        print("Recursos liberados. Servidor cerrado.")


if __name__ == "__main__":
    iniciar_server()
