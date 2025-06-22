from configs.gpu_configs import gpu_shop
from configs.radiator_configs import radiator_shop
from models.gpu import GPU
from models.radiator import Radiator

class Shop:
    """Класс магазина, нужен для того чтобы покупать внутри игровые предметы
    (видеокарты, радиаторы).
    """
    def __init__(self) -> None:
        self.gpu_shop = gpu_shop
        self.radiator_shop = radiator_shop


    def check_stats_gpu(self):
        """цикл просмотра характеристик видеокарт в магазине. Для просмотра загружаем
        новые GPU из gpu_config, при выборе пользователем "b" осуществляем покупку видеокарты
        """
        while True:
            try:
                for gpu_config in self.gpu_shop:
                    gpu = GPU(**gpu_config)
                    gpu.status
                    user_select = input("Введите:\nR чтобы перейти к следующей видеокарте\nB чтобы купить видеокарту\nS чтобы вернуться в меню магазина\n").lower()
                    
                    if user_select == "r":
                        continue

                    elif user_select == "b":
                        return gpu

                    elif user_select == "s":
                        return "shop" 
            
                    else:
                        print("Введите корректную команду")
                   
            except AttributeError:
                continue
    
    
    def check_stats_radiator(self):
        """цикл просмотра характеристик радиаторов в магазине
        новые Radiator из radiator_config, при выборе пользователем "b" осуществляем покупку радиатора
        """
        while True:
            try:
                for radiator_config in self.radiator_shop:
                    radiator = Radiator(**radiator_config)
                    radiator.status
                    user_select = input("Введите:\nR чтобы перейти к следующему радиатору\nB чтобы купить радиатор\nS чтобы вернуться в меню магазина\n").lower()
                    
                    if user_select == "r":
                        continue

                    elif user_select == "b":
                        return radiator

                    elif user_select == "s":
                        return "shop" 
            
                    else:
                        print("Введите корректную команду")
            except AttributeError:
                continue