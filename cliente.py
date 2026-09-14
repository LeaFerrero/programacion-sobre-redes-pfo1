import socket

def iniciar_cliente(host="localhost", port=5000):
  try:
    # Inicialización del socket TCP/IP del cliente
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conexión al servidor
    cliente_socket.connect((host, port))
    print(f"Conectado exitosamente al servidor en {host}:{port}")

    # Bucle para enviar múltiples mensajes
    while True:
      mensaje = input("Escriba el mensaje: ").strip()

      # Condición de salida estricta
      if mensaje.lower() == "éxito" or mensaje.lower() == "exito":
        print("Finalizando conexión...")
        break

      # Evitar enviar mensajes vacíos
      if not mensaje:
        continue

      # Enviar el mensaje codificado en bytes
      cliente_socket.sendall(mensaje.encode("utf-8"))

      # Recibir la confirmación del servidor y mostrarla
      respuesta = cliente_socket.recv(1024).decode("utf-8")
      print(f"Respuesta del servidor: {respuesta}")
  except socket.error as e:
    print(f"Error de red: No se pudo conectar o comunicar con el servidor. Detalle: {e}")
  finally:
    # Liberar el recurso
    cliente_socket.close()

if __name__ == "__main__":
  iniciar_cliente()