from pathlib import Path
from models.user import User
from logics.shop_logic import shop_logic
from logics.farm_logic import farm_logic
from logics.user_menu_logic import user_logic
from logics.save_logic import save_game, load_game


def run_game():
    """
    вначале инициализируем пользователя, а затем
    попадаем в основной цикл игры (главное меню)
    """
    user = game_start()
    while True:
        print("\033[H\033[J")
        print(r""" 
   _____ ____  _   _  _____  ____  _      ______ 
  / ____/ __ \| \ | |/ ____|/ __ \| |    |  ____|
 | |   | |  | |  \| | (___ | |  | | |    | |__   
 | |   | |  | | . ` |\___ \| |  | | |    |  __|  
 | |___| |__| | |\  |____) | |__| | |____| |____ 
  \_____\____/|_|_\_|_____/_\____/|______|______|
       |  \/  |_   _| \ | |  ____|  __ \         
       | \  / | | | |  \| | |__  | |__) |        
       | |\/| | | | | . ` |  __| |  _  /         
       | |  | |_| |_| |\  | |____| | \ \         
       |_|  |_|_____|_| \_|______|_|  \_\        
           |___ \ / _ \ / _ \ / _ \              
             __) | | | | | | | | | |             
            |__ <| | | | | | | | | |             
            ___) | |_| | |_| | |_| |             
           |____/ \___/ \___/ \___/                                                                                                        
""")
        user_select = input("Введите:\nS чтобы пойти в магазин видеокарт\nF - чтобы посмотреть ферму\nU - чтобы перейти в профиль игрока\nSAVE - сохранить игру\nEXIT - выйти\n").lower()
        
        if user_select == "s":
            user = shop_logic(user)

        elif user_select == "f":
            user = farm_logic(user)

        elif user_select == "u":
            user = user_logic(user)
        
        elif user_select == "save":
            save_game(user)

        elif user_select == "exit":
            print("Пока пока!")
            break   


def game_start():
    """
    Проверяем, есть ли файл с сохранением, если есть то предлагаем пользователю
    загрузить игру из него, либо создать нового персонажа.
    """
    print("\033[H\033[J")
    print(r""" 
   _____ ____  _   _  _____  ____  _      ______ 
  / ____/ __ \| \ | |/ ____|/ __ \| |    |  ____|
 | |   | |  | |  \| | (___ | |  | | |    | |__   
 | |   | |  | | . ` |\___ \| |  | | |    |  __|  
 | |___| |__| | |\  |____) | |__| | |____| |____ 
  \_____\____/|_|_\_|_____/_\____/|______|______|
       |  \/  |_   _| \ | |  ____|  __ \         
       | \  / | | | |  \| | |__  | |__) |        
       | |\/| | | | | . ` |  __| |  _  /         
       | |  | |_| |_| |\  | |____| | \ \         
       |_|  |_|_____|_| \_|______|_|  \_\        
           |___ \ / _ \ / _ \ / _ \              
             __) | | | | | | | | | |             
            |__ <| | | | | | | | | |             
            ___) | |_| | |_| | |_| |             
           |____/ \___/ \___/ \___/                                                                                                        
""")
    while True:
        save_path = Path("./data/game_data.pkl")

        if save_path.is_file():
            while True:
                user_select = input("У вас есть сохранение. Введите:\nL - чтобы загрузить сохраненную игру\nP - чтобы начать с начала\n").lower()
                
                if user_select == "l":
                    user = load_game()
                    return user
                
                elif user_select == "p":
                    break
            
        nickname = input("Представьтесь, как вас называть?\n")
        confirm_select = input(f"Вас зовут {nickname} вы уверены?\nY - да\nN - нет\n").lower()
        
        if confirm_select == "y":
            return User(nickname)
            
        elif confirm_select == "n":
            continue
        
        else:
            print("Неправильная команда, введите ваше имя заново")
