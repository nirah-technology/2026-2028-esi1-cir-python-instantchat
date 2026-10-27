from threading import Thread
from time import sleep
from typing import override
from socket import socket as Socket

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
    def __init__(self) -> None:
        Thread.__init__(self)
        self.__is_running: bool = False
        
