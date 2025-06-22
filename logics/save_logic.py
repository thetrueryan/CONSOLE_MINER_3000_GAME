import pickle
from models.user import User
import time


def save_game(user: User):
    """сохраняем данные пользователя"""
    with open("./data/game_data.pkl", "wb") as f:
        pickle.dump(user, f)
    print("Игра успешно сохранена!")
    time.sleep(2)
    

def load_game() -> User:
    """загружаем данные пользователя"""
    with open("./data/game_data.pkl", "rb") as f: 
        user: User = pickle.load(f)
    print(f"Пользователь {user.name} успешно загружен!")
    time.sleep(2)
    return user