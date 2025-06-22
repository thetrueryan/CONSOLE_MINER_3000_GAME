import time
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.user import User


def farm_logic(user: 'User'):
    """цикл, основная логика меню фермы пользователя. Можно начать майнинг, продать BTC, либо перейти в настройки фермы"""
    while True:
        user.farm.status
        user_select = input("Введите:\nM - чтобы начать майнинг\nO - чтобы перейти в настройки фермы\nE - чтобы вывести биткоины\nN - чтобы выйти\n").lower()
        
        if user_select == "m":

            if user.farm.count_energy >= 10000:
                print("Задолженность за электричество! вы не можете начать майнинг, пока не оплатите счет за электричество!")
                time.sleep(5)

            else:
                user.farm.start_mining()
                time.sleep(2)

        elif user_select == "o":
            farm_options(user)

        elif user_select == "n":
            return user
        
        elif user_select == "e":
            exchange_btc(user)



def farm_options(user: 'User'):
    """цикл, меню настроек фермы. Можно добавлять и убирать предметы с фермы."""
    while True:
        print("======Настройки фермы======")
        user_select = input("Введите:\nN - вернуться в главное меню фермы\nADDGPU/REMOVEGPU - чтобы добавить/убрать видеокарту с фермы\nADDRAD/REMOVERAD - чтобы добавить/убрать радиатор с фермы\nGPULIST - чтобы посмотреть состояние установленных видеокарт\n").lower()
        
        if user_select == "n":
            break

        elif user_select == "addgpu":
            user.farm.add_GPU(user)

        elif user_select == "removegpu":
            user.farm.remove_GPU(user)
        
        elif user_select == "addrad":
            user.farm.add_RAD(user)
        
        elif user_select == "removerad":
            user.farm.remove_RAD(user)

        elif user_select == "gpulist":
            user.farm.GPU_list()


def exchange_btc(user: 'User'):
    """цикл, меню обмена заработанных пользователем BTC на $"""
    farm_balance = user.farm.wallet
    while True:
        print("=====Меню обмена======")
        print(f"Сейчас на кошельке: {farm_balance} $BTC")
        user_select = input(f"Введите:\nY - чтобы обменять {farm_balance} по текущему курсу\nN - чтобы перейти в меню фермы\n").lower()
        
        if user_select == "n":
            break

        elif user_select == "y":
            user.exchange_btc()
            
    