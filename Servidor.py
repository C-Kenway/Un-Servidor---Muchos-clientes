import socket
import select
import threading

HOST = 'localhost'
PORT = 65432
BUFFER_SIZE = 1024

def handle_client(client_socket):
    print('Cliente conectado:', client_socket.getpeername())

    while True:
        data = b''
        while True:
            try:
                chunk = client_socket.recv(BUFFER_SIZE)
                if not chunk:
                    print('Cliente desconectado:', client_socket.getpeername())
                    return
                data += chunk
            except:
                print('Error al recibir datos del cliente:', client_socket.getpeername())
                return

        if data:
            print('Texto recibido del cliente', client_socket.getpeername(), ':', data.decode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # permitir la reutilización del socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print('El servidor TCP está disponible y en espera de solicitudes')

    # lista de sockets de cliente
    client_sockets = []

    while True:
        # seleccionar los sockets disponibles para lectura
        read_sockets, _, _ = select.select([server_socket] + client_sockets, [], [])

        for socket in read_sockets:
            # si un nuevo cliente se ha conectado
            if socket == server_socket:
                client_socket, client_address = server_socket.accept()
                print('Nuevo cliente conectado:', client_address)

                # crear un nuevo hilo para manejar la conexión del cliente
                client_thread = threading.Thread(target=handle_client, args=(client_socket,))
                client_thread.start()

                # agregar el nuevo socket de cliente a la lista
                client_sockets.append(client_socket)

            # si hay datos recibidos desde un cliente
            else:
                data = b''
                while True:
                    try:
                        chunk = socket.recv(BUFFER_SIZE)
                        if not chunk:
                            print('Cliente desconectado:', socket.getpeername())
                            client_sockets.remove(socket)
                            break
                        data += chunk
                    except:
                        print('Error al recibir datos del cliente:', socket.getpeername())
                        client_sockets.remove(socket)
                        break

                if data:
                    print('Texto recibido del cliente', socket.getpeername(), ':', data.decode())

"""        # manejar entradas de usuario en la consola
        try:
            user_input = input()
            if user_input == 'q':
                break
        except:
            pass"""