from typing import Protocol, override
from abc import abstractmethod

from .config import ApplicationConfiguration

class SendMessageFeature(Protocol):
    @abstractmethod
    def send_message(self, message: any) -> int: ...

class ReceiveMessageFeature(Protocol):
    @abstractmethod
    def recive_message(self, message: any): ...
    
class MarkMessageAsDistributedFeature(Protocol):
    @abstractmethod
    def mark_message_as_distributed(self, message: any): ...
    
class MarkMessageAsReadFeature(Protocol):
    @abstractmethod
    def mark_message_as_read(self, message: any): ...

class MarkMessageAsDeletedFeature(Protocol):
    @abstractmethod
    def mark_message_as_deleted(self, message: any): ...

    
class ClientMessenger(
    SendMessageFeature,
    ReceiveMessageFeature,
    MarkMessageAsDistributedFeature,
    MarkMessageAsReadFeature,
    MarkMessageAsDeletedFeature):
    
    def __init__(self, configuration: ApplicationConfiguration):
        self.__configuration: ApplicationConfiguration = configuration
     
    @override   
    def send_message(self, message: any) -> int:
        print("Sending message to server...")
    
    @override   
    def recive_message(self, message: any):
        print("Receiving message from server...")
    
    @override   
    def mark_message_as_distributed(self, message: any):
        print("Marking message as distributed...")
    
    @override   
    def mark_message_as_read(self, message: any):
        print("Marking message as read...")
    
    @override   
    def mark_message_as_deleted(self, message: any):
        print("Deleting message from server...")