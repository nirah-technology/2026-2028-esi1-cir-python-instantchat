from .users import User
from .conversations import Message


def main():
    username_choice: str = input("Choice your username: ")
    me: User = User(username_choice)
    
    message: Message = Message(
        1,
        content="Hello world!",
        destinataire_username=me.get_username(), 
        senser_username=me.get_username(), 
    )

if (__name__ == "__main__"):
    main()
    