
class Block:
    """Класс блок (является подклассом у класса Farm). Отвечает за расчет сложности блока, награды"""
    def __init__(self, btc_price: float):
        self.btc_price = btc_price
        self.dificulty = 1000
        self.block_number = 0
        self.block_reward = (self.btc_price / self.dificulty) / self.btc_price


    @property
    def halving(self):
        """применяем "халвинг" к блоку, увеличиваем его сложность добычи"""
        self.dificulty += self.dificulty * 0.2