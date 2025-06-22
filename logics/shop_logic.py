from models.user import User


def shop_logic(user: User):
    """Цикл, основная логика меню магазина, можно покупать видеокарты и радиаторы"""
    while True:
        print("=======Майнинг Магазин======")
        user_select = input("Введите:\nGPU чтобы посмотреть доступные видеокарты\nRAD чтобы посмотреть доступные радиаторы\nN - выйти в меню\n").lower()
        
        if user_select == "gpu":
            gpu = user.shop.check_stats_gpu()
            
            if gpu == "shop":
                continue

            select = input(f"Вы выбрали видеокарту {gpu}. Введите:\nB - чтобы купить\nS - вернуться в магазин\n").lower()
            
            if select == "b":
                select = user.inventory.buy_item(gpu)
                
                if select == "nomoney":
                    continue

                print(f"Вы успешно купили видеокарту {gpu} за {gpu.price}!")

            elif select == "s":
                continue
        
        elif user_select == "rad":
            radiator = user.shop.check_stats_radiator()
            
            if radiator == "shop":
                continue
            
            select = input(f"Вы выбрали радиатор {radiator}. Введите:\nB - чтобы купить\nS - вернуться в магазин\n").lower()

            if select == "b":
                select = user.inventory.buy_item(radiator)

                if select == "nomoney": 
                    continue
                
                print(f"Вы успешно купили радиатор {radiator} за {radiator.price}!")

            elif select == "s":
                continue
            
        elif user_select == "n":
            return user