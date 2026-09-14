import sqlite3
import socket
import datetime

def inicializar_db(nombre_db="chat_server.db"):
  # Inicialización y configuración de la base de datos SQLite
  try:
    # Se establece la conexión (el archivo se crea automáticamente si no existe)
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    # Creación de la tabla para almacenar los mensajes con los campos solicitados
    tabla_mensajes = '''
              CREATE TABLE IF NOT EXISTS mensajes (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  contenido TEXT NOT NULL,
                  fecha_envio TEXT NOT NULL,
                  ip_cliente TEXT NOT NULL
              )
          '''

    # Guardar los cambios
    cursor.execute(tabla_mensajes)
    conexion.commit()
    print("Base de datos inicializada correctamente.")
    return conexion

  except sqlite3.Error as e:
    # Manejo de errores en caso de que la DB no sea accesible
    print(f"Error crítico: No se pudo acceder o crear la base de datos. Detalle: {e}")
    return None

def enviar_mensaje(conexion, contenido, fecha, ip_cliente):
  try:
    cursor = conexion.cursor()

    # Consulta parametrizada para evitar inyección SQL
    consulta = '''
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        '''

    cursor.execute(consulta, (contenido, fecha, ip_cliente))
    conexion.commit()
    print(f"Mensaje registrado: {contenido}")

  except sqlite3.Error as e:
    print(f"Error en la base de datos durante la inserción. Detalle: {e}")

def inicializar_socket(host="localhost", port=5000):
  # Configuración del socket TCP/IP
  try:
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
  except socket.error as e:
    print(f"Error crítico: No se pudo abrir el puerto {port} (¿Puerto ocupado?). Detalle: {e}")
    return None

def iniciar_server():
  # Inicialización de recursos
  conexion = inicializar_db()
  if conexion is None:
    return

  server_socket = inicializar_socket()
  if server_socket is None:
    return

  print("El servidor está activo y en espera de clientes...")

  # Bucle principal para aceptar conexiones entrantes
  while True:
    conn, addr = server_socket.accept()
    ip_cliente = addr[0]
    print(f"Conexión establecida desde {addr}")

    try:
        # Bucle secundario para recibir múltiples mensajes del mismo cliente
        while True:
          datos = conn.recv(1024)

          # Si recv() devuelve un bloque vacío, el cliente cerró la conexión
          if not datos:
            print(f"El cliente {ip_cliente} se ha desconectado.")
            break

          # Decodificar el mensaje a texto
          contenido = datos.decode("utf-8")

          # Generar el timestamp actual
          timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

          # Guardar el mensaje en la base de datos SQLite
          enviar_mensaje(conexion, contenido, timestamp, ip_cliente)

          # Enviar la confirmación al cliente con el formato estricto
          respuesta = f"Mensaje recibido: {timestamp}"
          conn.sendall(respuesta.encode("utf-8"))

    except socket.error as e:
      print(f"Error de transmisión con el cliente {ip_cliente}. Detalle: {e}")
    finally:
      # Liberar el recurso de red del cliente al terminar el intercambio
      conn.close()

if __name__ == "__main__":
  iniciar_server()