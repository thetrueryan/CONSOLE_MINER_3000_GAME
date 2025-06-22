from models.item import Item


class Radiator(Item):
    """класс радиатор, является подклассом абстрактного класса Item 
    и используется для охлаждения фермы (максимум 10 радиаторов на ферму)
    """
    def __init__(self, name: str, price: float, rcooling: float):
        self.name = name
        self.price = price
        self.rcooling = rcooling
        

    def __str__(self):
        """возвращаем название радиатора (self.name)"""
        return self.name
    

    @property
    def current_price(self):
        """возвращаем цену радиатора"""
        return self.price
    

    def get_cooling(self):
        """возвращаем параметр охлаждения радиатора"""
        return self.rcooling

    @property
    def status(self) -> None:
        """выводим статус радиатора"""
        print("\033[H\033[J")
        print(f""" 
╔═══════════════════════ RADIATOR ─ {self.name} ═══════════════════════╗
║ █ Price: {self.price} $          █ Cooling Power: {self.rcooling} °C/тик            ║
╚═════════════════════════════════════════════════════════════════════╝
""")
    


