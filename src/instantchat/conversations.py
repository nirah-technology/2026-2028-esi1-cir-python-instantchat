from typing import List

class Message:
    """
        - Identifier unique du message (int)
        - Expéditeur / Autheur du message (str - User.username)
        - Destinataire (str - User.username)
        - Contenu du message (str)
        Vous devez créer des propriété imuable
    """
    ...
    def __init__(self, identifier: int, senser_username: str, destinataire_username: str, content: str):
        self.__identifier: int = identifier
        self.__sender_username: str = senser_username
        self.__destinataire_username: str = destinataire_username
        self.__content: str = content
        
    @property
    def identifier(self) -> int: 
        return self.__identifier 
        
    @property
    def sender_username(self) -> str:
        return self.__sender_username

    @property
    def destinataire_username(self) -> str:
        return self.__destinataire_username

    @property
    def content(self) -> str:
        return self.__content
    
class Conversation:
    """
        - Identifiant unique de la conversations (int)
        - Liste de participants (List[User])
        - Liste des messages (List[Message])
    """
    def __init__(self, identifier: int) -> None:
        self.__identifier: int = identifier
        self.__participants: List[str] = []
        self.__messages : List[Message] = []
        
    def add_participant(self, username: str) -> None:
        self.__participants.append(username)
        
    def delete_participant(self, username: str) -> None:
        self.__participants.remove(username)
        
    def add_message(self, message: Message) -> None:
        self.__messages.append(message)
        
    def get_participants(self) -> List[str]:
        return self.__participants.copy()
        
    def get_messages(self) -> List[Message]:
        return self.__messages.copy()
    
    @property
    def identifier(self) -> int: 
        return self.__identifier 
        
class UserConversations:
    def __init__(self, user: User):
        self.__user: User = user
        self.__conversations: List[Conversation] = []
    
    @property
    def user(self) -> User:
        return self.__user
    
    def get_conversations(self) -> List[Conversation]:
        return self.__conversations.copy()
    
    def add_conversation(self, conversation: Conversation):
        self.__conversations.append(conversation)