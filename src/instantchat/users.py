class User:

    def __init__(self, username: str):
        self.__username: str = username #  propriété privée de type string (chaine de caractères)
        
    def get_username(self) -> str:
        return self.__username
        
    @property
    def username(self) -> str:
        return self.get_username()