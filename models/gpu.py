import random
from models.item import Item
import time


class GPU(Item):
    """класс GPU (подкласс абстрактного класса item), используется на ферме для добычи BTC,
    видеокарта так же, по мере добычи изнашивается и постепенно теряет свою цену и прочность
    """
    def __init__(self, 
                 name: str,  
                 price: float, 
                 energy: int, 
                 hashrate: int, 
                 max_temp: float,
                 cooling_modificator: float,
                 ):

        self.name = name    # Название видеокарты
        self.price = price  # Цена 
        self.energy = energy    # WB/block
        self.hashrate = hashrate    # hashrate (мощность)
        # прочность
        self.max_durability = 100
        self.durability = 100

        # температура
        self.max_temp = max_temp
        self.temp = 0
        self.cooling_modificator = cooling_modificator
    

    def __str__(self):
        """возвращаем название видеокарты"""
        return self.name
    

    @property
    def current_price(self):
        """возвращаем текущую цену видеокарты"""
        if self.durability == 0:
            return 0
        return round(self.price * (self.durability / self.max_durability), 2)
    

    @property
    def status(self) -> None:
        """показываем статус видеокарты"""
        print("\033[H\033[J")
        print(f"""
╔══════════════════════ GPU ─ {self.name} ══════════════════════════════════════════════════════════════════
║ █ Цена: {self.current_price} $                          Текущая температура: {self.temp:.1f} / {self.max_temp} °C  
║ █ HASHRATE: {self.hashrate} MH/s                Встроенное охлаждение: -{self.cooling_modificator} °C/T    
║ █ Энергопотребление: {self.energy} W/b          Прочность: {self.durability}/{self.max_durability}         
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════
    """)


    def get_hashrate(self):
        """возвращаем хэшрейт видеокарты"""
        return 0 if self.durability == 0 else self.hashrate
    

    def get_energy(self):
        """возвращаем энергопотребление видеокарты"""
        return self.energy


    def get_temp(self):
        """возвращаем температуру видеокарты"""
        return self.temp

        

    def update(self, cooling_efficiency) -> None:
        """
        Изменение температуры видеокарты каждый тик (расчитываем на сколько изменится температура за тик в зависимости
        от эффективности охлаждения и других факторов, после чего меняем ее)"""
        Traw = (self.energy * 0.05) - random.uniform(-1, 1) # Расчет сырого нагрева от энергии
        cooling_total = cooling_efficiency - self.cooling_modificator # Охлаждение (активное и встроенное)
        # Пассивное охлаждение при высокой температуре
        if self.temp < 20:
            passive_cooling = 0
        
        elif self.temp > 20 and self.temp < 40:
            passive_cooling = 2
        
        elif self.temp > 40 and self.temp < 60:
            passive_cooling = 4
        
        else:
            passive_cooling = 6

        Tdelta = Traw + cooling_total - passive_cooling # Общий прирост температуры

        self.temp += Tdelta # Обновление температуры

        if self.temp > self.max_temp:
            print(f"Видеокарта {self.name} перегрелась! Добавьте радиаторов или отключите её!")
        
        if self.temp < 0:
            self.temp = 0


    
    def off(self) -> None:
        """При выключении фермы, отключение видеокарты"""
        self.temp = 0


    def durability_set(self):
        """
        Изменение прочности видеокарты каждый тик, если температура выше максимально допустимой, то
        прочность снимается в 10 раз быстрее
        """
        if self.temp < self.max_temp:
            Ddelta = 0.5

        else:
            Ddelta = 5
        self.durability -= Ddelta
        
        if self.durability < 0 or self.durability == 0:
            self.durability = 0
            self.hashrate = 0
            print(f"Прочность видеокарты {self.name} упала до 0!")