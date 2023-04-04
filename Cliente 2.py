import socket
import time

HOST = "127.0.0.1"  # Hostname o dirección IP del servidor
PORT = 65432  # Puerto del servidor
BUFFER_SIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Enviando mensaje...")
    with open("Mensaje2.txt", "r") as archivo:
        for linea in archivo:
            print(linea)
            TCPClientSocket.sendall(str.encode(linea))
            time.sleep(1)  # Espera para evitar sobrecargar el servidor
    TCPClientSocket.shutdown(socket.SHUT_WR)
    print("Terminé")