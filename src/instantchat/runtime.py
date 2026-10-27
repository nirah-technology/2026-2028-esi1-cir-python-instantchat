from threading import Thread
from time import sleep
from typing import override
from socket import socket as Socket, AF_INET, SOCK_STREAM

import numpy as np
import sounddevice as sd

from .config import ApplicationConfiguration

class Metronome(Thread):
    def __init__(self, interval_in_seconds: float):
        Thread.__init__(self)
        self.__interval: float = interval_in_seconds
        self.__is_running: bool = False
    
    def beep(self, frequency: float, duration: float, volume: float = 0.5):
        sample_frequency: float = 44_100
        
        t = np.linspace(0, duration, int(sample_frequency * duration), endpoint=False)
        wave = volume * np.sin(2 * np.pi * frequency * t)
        sd.play(wave, sample_frequency)
        sd.wait()
    
    @override
    def run(self) -> None:
        if self.__is_running == False:
            self.__is_running = True
            while (self.__is_running):
                self.beep(440, 0.5)
                sleep(self.__interval)
    
    def terminate(self):
        self.__is_running = False

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
        self.clients_connection: list = []
        
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
                    
    def terminate(self):
        if self.__is_running:
            self.__is_running = False
        if self.__socket:
            try:
                self.__socket.close()
            except Exception as error:
                print(f"Error closing server. Reason: {error}")
            self.__socket = None