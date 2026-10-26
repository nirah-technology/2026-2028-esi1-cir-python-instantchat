# TP : InstantChat, le cœur de la messagerie

**Durée estimée :** 4 h · **Niveau :** M1 Cyber Infra · **Python :** 3.14 (géré avec `uv`)

## Contexte

Tout au long du module, nous construisons **InstantChat**, une messagerie instantanée client / serveur.
Les notions de réseau (sockets) et de concurrence (threads) n'ont pas encore été vues. Ce TP ne les utilise donc pas.

Vous allez construire le **cœur applicatif** : utilisateurs, messages, conversations, modération, configuration, persistance et une interface en ligne de commande.
Tout s'exécute **dans un seul processus**, et un « serveur » simulé en mémoire joue le rôle du futur serveur.

> Le but est que, dans une prochaine séance, il suffise de **remplacer le transport** (appels de méthodes remplacés par des sockets) sans réécrire la logique métier. Soignez donc vos interfaces.

## Objectifs pédagogiques

- Structurer un projet Python (`src/`, modules, paquet installable avec `uv`).
- Utiliser les classes, l'encapsulation, `@property`, l'héritage, les classes abstraites et les `Protocol`.
- Typer son code (`typing`, `list[str]`, `X | None`) et utiliser les `dataclass` et les `Enum`.
- Gérer les fichiers (`pathlib`, `with`), le JSON et les exceptions (dont des exceptions métier).
- Écrire des tests simples avec `pytest`.

## Règles

- Le code est **typé** et lisible (noms explicites, docstrings courtes).
- Pas de `print` dans la logique métier. Seuls `main.py` et la CLI affichent quelque chose.
- Aucune dépendance externe, sauf `pytest` en dépendance de développement.
- Un commit Git par partie, avec un message clair.

## Structure attendue

```
instantchat/
├── config.json
├── forbidden_words.txt
├── pyproject.toml
├── src/instantchat/
│   ├── config.py          # Partie 4
│   ├── users.py           # Partie 1
│   ├── conversations.py   # Parties 2 et 3
│   ├── moderator.py       # Partie 4
│   ├── storage.py         # Partie 5
│   ├── service.py         # Partie 6
│   ├── io.py              # Partie 6
│   ├── cli.py             # Partie 7
│   └── main.py
└── tests/
```

---

## Partie 0 : Prise en main et chasse aux bugs (20 min)

Le dépôt contient une ébauche écrite à la hâte. Elle est **incomplète et contient des erreurs**.

1. Installez le projet et vérifiez qu'il se lance : `uv sync && uv run instantchat`.
2. Lisez chaque module. Dans un fichier `NOTES.md`, listez **au moins 5 problèmes** (bugs, mauvaises pratiques, incohérences), chacun avec le fichier, la ligne et une proposition de correction.
3. Vous corrigerez ces problèmes au fil du TP. Indiquez dans `NOTES.md` dans quelle partie chacun a été traité.

*Indices :* regardez les imports, ce que font réellement `@abstractmethod` et `any`, les doublons d'attributs, et ce que contiennent les chaînes lues dans un fichier.

---

## Partie 1 : Utilisateurs (30 min), `users.py`

Faites évoluer la classe `User`.

1. Le nom d'utilisateur doit être **valide** : de 3 à 20 caractères, uniquement lettres, chiffres, `_` et `-`, sans espaces.
2. Si le nom est invalide, levez une exception métier `InvalidUsernameError(ValueError)` avec un message explicite.
3. Deux `User` sont égaux si leur nom est égal, sans tenir compte de la casse. Implémentez `__eq__` **et** `__hash__`.
4. Implémentez `__str__` (pour l'affichage) et `__repr__` (pour le débogage).
5. Ajoutez un attribut `created_at` (type `datetime`), renseigné à la création.
6. Il n'existe qu'un seul accès au nom : la `@property username`. Supprimez `get_username()` et mettez à jour les appels.

**Attendu :**
```python
>>> User("Alice") == User("alice")
True
>>> len({User("Alice"), User("alice")})
1
>>> User("a b")
InvalidUsernameError: ...
```

---

## Partie 2 : Messages (40 min), `conversations.py`

1. Faites de `AbstractMessage` une **vraie classe abstraite** (héritage de `ABC`). Vérifiez qu'on ne peut plus l'instancier.
2. Créez une `Enum` `MessageStatus` avec les valeurs `SENT`, `DISTRIBUTED`, `READ` et `DELETED`.
3. Transformez `Message` pour qu'il :
   - ne stocke `content` qu'**une seule fois** (corrigez la duplication de l'ébauche) ;
   - ait un `status` (initialement `SENT`) et un `timestamp` ;
   - expose ses attributs en lecture seule (`@property`) ;
   - propose `mark_as(status)`, qui n'accepte que les transitions valides : `SENT → DISTRIBUTED → READ`, et `DELETED` depuis n'importe quel état. Toute autre transition lève `InvalidTransitionError`.
4. Implémentez `handle()` pour `Message` : elle retourne la ligne à afficher, par exemple `[14:32] alice → bob : Salut !`. Elle ne fait pas de `print`.
5. Implémentez `SystemMessage.handle()` de façon à ce qu'il retourne une chaîne, sans `print` et sans dépendre d'un `kwargs` obligatoire. Un message système peut avoir une catégorie optionnelle (`INFO`, `WARNING`).
6. **Question de réflexion** (à répondre dans `NOTES.md`) : pourquoi avoir choisi l'héritage plutôt qu'un simple `if type == ...` ? Quel est le coût d'une hiérarchie trop profonde ?

---

## Partie 3 : Conversations (40 min), `conversations.py`

1. Corrigez `Conversation` :
   - `add_participant` ne doit pas ajouter deux fois le même utilisateur (utilisez un type adapté) ;
   - `delete_participant` ne doit pas planter si l'utilisateur est absent. Choisissez : lever `ParticipantNotFoundError` **ou** ignorer. Justifiez votre choix en commentaire ;
   - `add_message` refuse un message dont l'expéditeur ne fait pas partie de la conversation (`NotAParticipantError`).
2. Ajoutez `get_messages_by(username)` et `get_unread_messages(username)`. Ils retournent une liste construite avec une **compréhension de liste**.
3. Ajoutez `Conversation.__len__` (nombre de messages) et `__iter__` (itération sur les messages).
4. Faites de `UserConversations` un vrai gestionnaire :
   - `get_or_create_with(other: User) -> Conversation` ;
   - `find_by_id(identifier)` qui retourne `Conversation | None` ;
   - génération des identifiants **sans doublon** (par exemple avec `itertools.count`).
5. Ajoutez les imports manquants. Le module doit s'importer sans erreur.

---

## Partie 4 : Configuration et modération (40 min)

### 4.1 Configuration, `config.py`

L'ébauche plante si `config.json` n'existe pas ou si `listen_port` manque.

1. Créez un `config.json` à la racine :
   ```json
   {
     "bind_address": "127.0.0.1",
     "listen_port": 6666,
     "forbidden_words_file": "forbidden_words.txt",
     "history_file": "history.json"
   }
   ```
2. Complétez `ApplicationConfiguration` avec les deux nouveaux champs (valeurs par défaut cohérentes).
3. Gérez les erreurs avec une exception `ConfigurationError` qui enveloppe la cause (`raise ... from error`) dans ces cas : fichier absent, JSON invalide, clé obligatoire manquante, port hors de la plage 1 à 65535.

### 4.2 Modérateur, `moderator.py`

Le `Moderator` de l'ébauche a plusieurs défauts : 
- les mots lus par `readlines()` finissent par `\n` ;
- `"ass" in "classe"` donne `True`, donc de faux positifs ;
- il affiche des messages avec `print` ;
- `filter` retourne `True` quand le message est **accepté**, ce qui est contre-intuitif.

À faire :

1. Chargez les mots avec `strip()`, en ignorant les lignes vides et celles qui commencent par `#`. Stockez-les dans un `frozenset` en minuscules.
2. Ne recherchez que des **mots entiers**, sans tenir compte de la casse ni de la ponctuation. Utilisez le module `re` (`\b`) ou `str.split` avec nettoyage.
3. Renommez `filter` en `is_allowed(text) -> bool` (`True` = message autorisé). Ajoutez `find_forbidden_words(text) -> list[str]` qui retourne les mots interdits trouvés.
4. Ajoutez `censor(text) -> str` qui remplace chaque mot interdit par des `*` de même longueur (`"quel idiot"` → `"quel *****"`).
5. Remplacez les `print` par une exception `ModeratorError`, ou par le module `logging`. Une erreur de fichier ne doit **jamais** être silencieuse.

**Attendu :**
```python
>>> m = Moderator(Path("forbidden_words.txt"))   # contient "idiot" et "ass"
>>> m.is_allowed("Ma classe est super")
True
>>> m.censor("Quel IDIOT !")
'Quel ***** !'
```

---

## Partie 5 : Persistance JSON (30 min), `storage.py`

On veut conserver l'historique entre deux exécutions.

1. Ajoutez à `Message` et à `Conversation` les méthodes `to_dict()` et `from_dict()`. La date est sérialisée au format ISO 8601 et le statut par son nom.
2. Écrivez la classe `HistoryStorage(path: Path)` avec :
   - `save(conversations: list[Conversation]) -> None` ;
   - `load() -> list[Conversation]`, qui retourne une liste vide si le fichier n'existe pas encore.
3. L'écriture doit être **sûre** : écrivez d'abord dans un fichier temporaire, puis `Path.replace()` vers la cible, pour qu'un crash ne corrompe pas l'historique.
4. Un fichier JSON corrompu lève `StorageError` avec la cause d'origine. Le programme ne doit pas s'arrêter brutalement avec une trace Python.

**Attendu :** après `save` puis `load`, les conversations rechargées sont identiques aux originales (mêmes messages, mêmes statuts, mêmes dates).

---

## Partie 6 : Service et interfaces (40 min), `service.py` et `io.py`

C'est la partie qui prépare le réseau. Elle ne l'implémente pas.

1. Dans `io.py`, corrigez les `Protocol` :
   - remplacez `any` par `Message` (ou `typing.Any` si vous justifiez le choix) ;
   - corrigez la faute `recive_message` ;
   - retirez les `@abstractmethod`, inutiles sur un `Protocol` ;
   - faites retourner à `send_message` un `int` : l'identifiant du message.
2. Créez `ChatService`, **le serveur simulé en mémoire**. Il doit :
   - enregistrer des utilisateurs (`register(user)`, refus des doublons avec `UserAlreadyExistsError`) ;
   - recevoir un message (`send(sender, recipient, content) -> Message`) :
     1. il vérifie que les deux utilisateurs existent ;
     2. il passe le contenu au `Moderator` : s'il est interdit, il lève `MessageRejectedError` qui liste les mots fautifs ;
     3. il crée le message, l'ajoute à la bonne conversation et passe son statut à `DISTRIBUTED` ;
   - consulter la boîte de réception : `inbox(user)` retourne les messages non lus qui lui sont destinés ;
   - `read(user, message_id)` : passe le message à `READ` (uniquement par son destinataire).
3. Faites que `ClientMessenger` implémente réellement ses méthodes en appelant un `ChatService`, au lieu d'afficher des `print`. Le client **ne connaît que le service**, pas ses détails internes.
4. **Question de réflexion** : si on remplace plus tard `ChatService` par un vrai serveur distant, quelles parties de votre code faut-il modifier ? Lesquelles ne bougent pas ? Répondez dans `NOTES.md`.

---

## Partie 7 : Interface en ligne de commande (30 min), `cli.py` et `main.py`

Écrivez une boucle interactive qui utilise **uniquement** `ClientMessenger`.

Commandes à supporter :

| Commande | Effet |
|---|---|
| `/help` | affiche l'aide |
| `/login <nom>` | change d'utilisateur courant (le crée si besoin) |
| `/to <nom> <message>` | envoie un message |
| `/inbox` | liste les messages non lus |
| `/history <nom>` | affiche la conversation avec un utilisateur |
| `/quit` | sauvegarde l'historique et quitte |

Contraintes :
- Une commande inconnue ou un argument manquant affiche un message d'erreur. Le programme ne plante pas.
- Toutes les exceptions métier des parties précédentes sont **interceptées** et affichées proprement.
- La CLI utilise `dict[str, Callable]` pour associer une commande à son gestionnaire. Pas de longue chaîne de `if/elif`.
- Au démarrage, l'historique est rechargé. À `/quit` et sur `Ctrl+C`, il est sauvegardé.

Exemple de session :
```
> /login alice
Connecté en tant que alice
> /login bob
Connecté en tant que bob
> /to alice Salut, quel idiot ce serveur !
Message refusé : mots interdits ['idiot']
> /to alice Salut Alice
Message envoyé (#1)
> /login alice
> /inbox
[14:32] bob → alice : Salut Alice
```

---

## Partie 8 : Tests (20 min), `tests/`

1. Ajoutez `pytest` en dépendance de développement : `uv add --dev pytest`.
2. Écrivez **au moins 12 tests** qui couvrent au minimum :
   - la validation et l'égalité de `User` ;
   - les transitions autorisées et interdites de `Message` ;
   - le modérateur : mot entier, casse, faux positif `classe`/`ass`, fichier absent ;
   - un aller-retour de `HistoryStorage` (utilisez la fixture `tmp_path`) ;
   - un scénario complet dans `ChatService`.
3. Utilisez `pytest.raises` pour vérifier les exceptions et `@pytest.mark.parametrize` au moins une fois.

Lancement : `uv run pytest -v`

---

## Bonus (au choix)

- **Journalisation :** remplacez les affichages techniques par `logging`, avec un niveau configurable dans `config.json`.
- **Salons :** ajoutez des conversations de groupe (plus de deux participants) et la commande `/create`, `/join`.
- **Recherche :** `/search <mot>` dans tout l'historique, avec un générateur (`yield`) plutôt qu'une liste complète.
- **Anti-spam :** refusez plus de N messages par minute pour un même utilisateur.
- **Hachage des noms :** stockez dans l'historique une empreinte (`hashlib.sha256`) plutôt que le nom en clair. Discutez des limites de cette approche.

---

## Livrables

- Le dépôt Git (historique de commits lisible, un commit par partie).
- `NOTES.md` : liste des bugs de la partie 0 et réponses aux questions de réflexion.
- `uv run instantchat` et `uv run pytest` fonctionnent depuis un clone propre.

## Barème indicatif (/20)

| Critère | Points |
|---|---|
| Partie 0 : bugs identifiés et corrigés | 2 |
| Parties 1 à 3 : modèle (User, Message, Conversation) | 5 |
| Partie 4 : configuration et modérateur | 3 |
| Partie 5 : persistance | 2 |
| Partie 6 : service et interfaces | 3 |
| Partie 7 : CLI | 2 |
| Partie 8 : tests | 2 |
| Qualité (typage, lisibilité, gestion d'erreurs, Git) | 1 |
| **Bonus** | jusqu'à +2 |

## Et ensuite ?

La séance suivante remplacera l'appel direct à `ChatService` par un échange réseau (sockets), puis par plusieurs clients simultanés (threads). Si votre architecture est propre, seules les couches `io.py` et `service.py` changeront.
