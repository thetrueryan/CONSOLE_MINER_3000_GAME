from models.user import User


def user_logic(user: User):
    """Цикл, меню пользователя можно продавать и смотреть предметы из инвентаря, и оплачивать электроэнергию"""
    while True:
        user.status
        user_select = input("Введите:\nI - чтобы посмотреть инвентарь\nE - чтобы оплатить счет за электроэнергию\nS - чтобы продать предметы из инвентаря\nN - чтобы вернуться назад\n").lower()
    
        if user_select == "i":
            item = user.inventory.check_inventory()
            
            if item:
                user.inventory.sell_item(item)

        elif user_select == "e":
            user = pay(user)

        elif user_select == "s":
            user = sell_items(user)

        elif user_select == "n":
            return user


def pay(user: User):
    """цикл, меню оплаты электроэнергии"""
    while True:
        print(f"Ваш счет за электроэнергию: {user.farm.energy_counter}, что равняется {user.farm.energy_counter * user.WBprice} $")
        user_select = input("Введите:\nE чтобы оплатить\nN - вернуться назад\n").lower()
        
        if user_select == "e":
            user.pay_to_energy

            return user

        elif user_select == "n":
            return user


def sell_items(user: User):
    """продаем выбранный предмет из инвентаря"""
    item = user.inventory.check_inventory()

    if item:
        user.inventory.sell_item(item)
        
    return user