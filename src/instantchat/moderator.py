from pathlib import Path
from typing import List

class Moderator:
    def __init__(self, black_list_words_file: Path):
        self.__black_list_words_file: Path = black_list_words_file
        self.__black_list_words_cache: List[str] = []
        self.__load_black_list_words_from_file()
    
    def __load_black_list_words_from_file(self):
        file_content: list[str] = []
        try:
            if (self.__black_list_words_file.exists()):
                with open(self.__black_list_words_file, "r") as file:
                    file_content = file.readlines()
        except FileNotFoundError as error:
            print(f"Le fichier n'a pas été trouvé: {self.__black_list_words_file}")
        except PermissionError as error:
            print(f"Pas les authorisations pour accéder à : {self.__black_list_words_file}")
        except Exception as error:
            print(f"Une erreur est survenue: {error}")
        
        else:
            print("Les mots interdits ont parfaitement été chargés")
            self.__black_list_words_cache = file_content
        finally:
            print("Chargement terminé.")

    def filter(self, content: str) -> bool:
        for forbidden_word in self.__black_list_words_cache:
            is_found = forbidden_word.lower() in content.lower()
            if is_found:
                return False
        return True