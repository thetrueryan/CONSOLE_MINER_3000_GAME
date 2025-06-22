from typing import Union
from models.item import Item
from models.gpu import GPU
from models.radiator import Radiator
import time


class Inventory():
    """ 
    класс Inventory, инвентарь пользователя (User), 
    куда будут попадать купленные предметы а так же учитываться баланс пользователя
    self.balance = 300 (начальный баланс)
    """
    def __init__(self):
        self.item_list = []
        self.balance = 300


    def buy_item(self, item: Union[GPU, Radiator]):
        """
        проверяем, если хватает денег, то покупаем выбранный предмет и 
        добавляем в инвентарь
        """
        if self.balance >= item.current_price:
            self.balance -= item.current_price
            self.item_list.append(item)

        else:
            print(f"Недостаточно средств! нужно еще {item.current_price - self.balance} $")
            return "nomoney"


    def sell_item(self, item: Union[GPU, Radiator]):
        """продаем выбранный из инвентаря предмет"""
        self.item_list.remove(item)
        self.balance += item.current_price
        print(f"Предмет {item} был продан за {item.current_price}")
        time.sleep(1)


    def fix_profit(self, profit: float):
        """пополняем баланс при продаже BTC"""
        self.balance += profit
    

    def check_inventory(self):
        """
        цикл, просматриваем инвентарь, выводим доступные предметы, можем выбрать
        какой либо предмет и продать его
        """
        while True:
            for item in self.item_list:
                item.status
                user_select = input("Введите:\nR чтобы перейти к следующему предмету\nS чтобы продать данный предмет\nN чтобы вернуться назад\n").lower()

                if user_select == "r":
                    continue
            
                elif user_select == "s":
                    return item

                elif user_select == "n":
                    return


    def check_items_for_add_farm(self, item_type: str):
        """
        проверяем предметы в инвентаре для добавления на ферму (если item_type = "radiator", то 
        добавляем в радиаторы, GPU, то в видеокарты)"""
        while True:
            try:
                for item in self.item_list:

                    if item_type != "radiator":

                        if type(item) == Radiator: 
                            continue
                                
                        else:
                            item.status
                        
                    elif item_type == "radiator":

                        if type(item) != Radiator:
                            continue
                        
                        else:
                            item.status
                            
                    user_select = input("Введите:\nR чтобы перейти к следующему предмету\nY чтобы установить этот предмет на ферму:\n").lower()
                    
                    if user_select == "r":
                        continue

                    elif user_select == "y":
                        return item
            except AttributeError:
                continue