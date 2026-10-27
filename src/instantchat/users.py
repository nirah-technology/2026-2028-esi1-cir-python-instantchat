from typing import override


class InvalidUsernameError(ValueError):
    def __init__(self, reason_message: str) -> None:
        super().__init__(reason_message)

class _UsernameValidator:
    @staticmethod
    def validate(username: str) -> str:
        allowed_characters = [
            45, 95
        ]
        allowed_characters.extend(range(48, 57+1))
        allowed_characters.extend(range(65, 90+1))
        allowed_characters.extend(range(97, 122+1))
        
        allowed_characters.sort()
        for character in username:
            if not ord(character) in allowed_characters:
                raise InvalidUsernameError("Not allowed character found in username.")
        
        if (3 <= len(username) <= 20) == False:
            raise InvalidUsernameError(f"User name length not valid [3 - 20]: {len(username)}")

        return username
        
            
class User:

    def __init__(self, username: str):
        self.__username: str = _UsernameValidator.validate(username)
        
    @override
    def __eq__(self, value: object, /) -> bool:
        if not (type(self) == type(value)):
            return False
        return self.username.lower() == value.username.lower()
        
    @override
    def __hash__(self) -> int:
        return hash((self.__username,))
        
    @override
    def __repr__(self) -> str:
        return f"'username': '{self.__username}'"
        
    @override
    def __str__(self) -> str:
        return self.__repr__()
        
    def get_username(self) -> str:
        return self.__username
        
    @property
    def username(self) -> str:
        return self.get_username()

user1 = User("Nico")
user2 = User("Nicolas")

print(user1 == user2)