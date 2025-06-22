from models.farm import Farm
from models.inventory import Inventory
from models.shop import Shop
import requests



# класс Игрока
class User:
    """
    Главный класс, представляющий пользователя.
    Управляет профилем пользователя, включая ферму, инвентарь и магазин.
    Обрабатывает: обмен BTC, оплата электроэнергии.
    """
    def __init__(self, name: str):
        self.name = name
        self.farm = Farm()
        self.inventory = Inventory()
        self.shop = Shop()
        self.WBprice = 0.005
    
    
    @property
    def status(self) -> None:
        """Выводит в консоль ASCII арт с текущим статусом игрока"""
        print("\033[H\033[J")
        print(fr"""
     ________
   -------+  \
   \\\\\\\\\  \
   //_//__\\\  |
   /\0' `0~ |\ /
   (|^<, ^  .)|
    ( ._.  ||/
     \ .  / |
      +--/  |    
              
USER: {self.name}
BALANCE : {self.inventory.balance}
""")


           
    def exchange_btc(self) -> None:
        """Обменивает добытые на ферме BTC на доллары по актуальному курсу
        (получаем с API coingecko). Если недоступно, то обмен происходит по курсу
        80000 за 1 BTC. Так же за обмен снимается комиссия в 3%"""
        btc_value = self.farm.wallet_value
        try:
            response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
            btc_price = float(response.json()["bitcoin"]["usd"])
        except Exception:
            print("Не удалось получить актуальную цену BTC, используем запасное значение")
            btc_price = 80000 
        profit = btc_value * btc_price * 0.97
        self.farm.clear_wallet
        self.inventory.fix_profit(profit)
        print(f"Вы продали {btc_value} и получили {profit}$ (комиссия 3%)")


    def pay_to_energy(self, energy_to_pay: float) -> None:
        """оплачиваем накопленный на ферме счет за электро энергию"""
        energy_counter = self.farm.count_energy
        energy_to_pay_price = energy_to_pay * self.WBprice
        energy_remains = energy_counter - energy_to_pay
        print(f"Вы заплатили за электроэнергию {energy_to_pay_price}$")
        self.farm.clear_energy_counter(energy_remains)