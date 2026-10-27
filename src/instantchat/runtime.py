from threading import Thread
from time import sleep
from typing import override
from socket import socket as Socket, AF_INET, SOCK_STREAM
from json import loads, dumps

from .config import ApplicationConfiguration
from .conversations import Message

class ClientConnection(Thread):

    all_users_connections: dict[str, Socket] = {}

    def __init__(self, client_socket: Socket):
        Thread.__init__(self)
        self.__client_socket: Socket = client_socket
        self.__is_running: bool = True
    
    def run(self):
        try:
            username = self.__client_socket.recv(1024).decode()
            ClientConnection.all_users_connections[username] = self.__client_socket
            usernames = list(ClientConnection.all_users_connections.keys())
            uns = ",".join(usernames)
            self.__client_socket.send(uns.encode())
            while  self.__is_running:
                message_as_string =  self.__client_socket.recv(4096).decode()
                message_as_dict = loads(message_as_string)
                message_as_object: Message = Message(**message_as_dict)
                destinataire_client_socket: Socket = ClientConnection.all_users_connections[
                    message_as_object.destinataire_username
                ]
                destinataire_client_socket.send(message_as_string.encode())

        except:
            pass
        

class Client(Thread):
    def __init__(self, server_config: ApplicationConfiguration) -> None:
        Thread.__init__(self)
        self.__is_running: bool = False
        self.__server_config: ApplicationConfiguration  = server_config
        self.__socket: Socket = None
        
    def connect(self):
        if self.__socket is None:
            self.__socket = Socket((AF_INET, SOCK_STREAM))
            try:
                self.__socket.connect((
                    self.__server_config.bind_address,
                    self.__server_config.listen_port
                ))
            except Exception as error:
                print(f"Unable to connect to server. Reason: {error}")

    def disconnect(self):
        if self.__socket:
            try:
                self.__socket.close()
            except Exception as error:
                print(f"Unable to close connection. Reason: {error}")
            self.__socket = None
    
    def send_message(self, message_to_send: str):
        if self.__socket:
            try:
                self.__socket.send(message_to_send.encode())
            except Exception as error:
                print(f"Unable to send message. Reason: {error}")
    
    
    def run(self):
        if not self.__is_running:
            self.__is_running = True
            while self.__is_running:
                if self.__socket:   
                    try:
                        self.__socket.settimeout(1)
                        received_data: bytes = self.__socket.recv(4096)
                    except TimeoutError:
                        pass
                    except Exception as error:
                        print(f"Unable to retrieve data. Reason: {error}")
                    else:
                        if received_data:
                            received_message = received_data.decode()
                            print(received_message)

class Server(Thread):
    def __init__(self, configuration: ApplicationConfiguration):
        self.__configuration: ApplicationConfiguration = configuration
        self.__is_running: bool = False
        self.__socket : Socket = None
        self.__clients_connections: list = []
        
    def run(self):
        if not self.__is_running:
            self.__is_running = True
            if self.__socket == None:
                self.__socket = Socket(AF_INET, SOCK_STREAM)
                self.__socket.bind((
                    self.__configuration.bind_address,
                    self.__configuration.listen_port
                ))
                self.__socket.listen(5)
                while self.__is_running:
                    client, infos = self.__socket.accept()
                    client_connection: ClientConnection(client)
                    self.__clients_connections.append(client_connection)  
                    client_connection.start()
                    
    def terminate(self):
        if self.__is_running:
            self.__is_running = False
        if self.__socket:
            try:
                for client in self.__clients_connections:
                    client.terminate()
                self.__socket.close()
            except Exception as error:
                print(f"Error closing server. Reason: {error}")
            self.__socket = None