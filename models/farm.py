from models.block import Block
from models.gpu import GPU
from models.radiator import Radiator
import requests
import time
import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User


class Farm:
    """Класс Farm, подкласс фермы игрока, именно в нем осуществлен функционал майнинга, с помощью нее
    пользователь зарабатывает деньги, так же может устанавливать и убирать комплектующие на ферму, для повышения / 
    понижения эффективности майнинга. self.Farm_status отвечает за управление фермой и имеет 2 режима (True: ферма включена, ведется майнинг |
    False: ферма выключена, майнинг не ведется)
    Attributes:
        self.Farm_status = False   # Статус фермы
        self.GPUs = []  # видеокарты установленные на ферме
        self.Radiators = [] # радиаторы установленные на ферме
        self.wallet = 0 # кошелек фермы, пополняется после добычи блока (в BTC)
        self.hashrate = 0   # общий хешрейт всех gpu
        self.energy = 0 # потребление энергии за блок
        self.temp = 0 # Общая температура всех GPU
        self.cooling_efficiency = 0 # суммарная эффективность охлаждения от радиаторов
        self.energy_counter = 0   # счетчик энергии
        self.block_counter = 0  # счетчик добытых блоков для халвинга
        self.block_progress = 0 # прогресс добычи блока
        self._tick_time = 4  # время 1 тика
    """
    def __init__(self):
        self.Farm_status = False
        self.GPUs = []  
        self.Radiators = [] 
        self.wallet = 0 
        self.hashrate = 0   
        self.energy = 0 
        self.temp = 0 
        self.cooling_efficiency = 0 
        self.energy_counter = 0
        self.block_counter = 0  
        self.block_progress = 0 
        self._tick_time = 4

    @property
    def status(self) -> None:
        """показывает статус фермы"""
        params = self.params
        print("\033[H\033[J")
        display = f"""
╔═══════════════════════════ MINING FARM STATUS ═══════════════════════════╗
║ █ BTC на кошельке: {params["wallet"]} $BTC                                     
║ █ HASHRATE: {params["hashrate"]} MH/s         ENERGY/B: {params["energy"]} W       
║ █ Охлаждение: -{abs(params["cooling_efficiency"])} °C/тик      Средняя температура: {round(params["temp"], 2)} °C       
║ █ BLOCK_PROGRESS: {params["block_progress"]}%         BLOCKS_TOTAL: {params["block_counter"]}         
║ █ Счетчик энергии: {params["energy_counter"]} Wh  
║ █ FARM_STATUS: {params['status']}                              
╠═════════════════════════════════════════════════════════════════════════╣
"""
        print(display)


    @property
    def params(self):
        """возвращает все текущие параметры фермы"""

        if self.Farm_status:
            status = "ON"

        else:
            status = "OFF"
        return {
            "status": status,
            "gpus": self.GPUs,
            "radiators": self.Radiators,
            "wallet": self.wallet,
            "hashrate": self.hashrate,
            "energy": self.energy,
            "cooling_efficiency": self.cooling_efficiency,
            "temp": self.temp,
            "energy_counter": self.energy_counter,
            "block_counter": self.block_counter,
            "block_progress": self.block_progress,
        }
    

    @property
    def count_energy(self):
        """возвращает счет за энергию"""
        return self.energy_counter
    

    @property
    def wallet_value(self):
        """возвращает количество BTC на кошельке пользователя"""
        return self.wallet


    def clear_energy_counter(self, new_energy_counter) -> None:
        """при оплате пользователем электроэнергии, обновляет счетчик"""
        self.energy_counter = new_energy_counter


    @property
    def clear_wallet(self):
        """при продаже пользователем BTC обнуляет кошелек"""
        self.wallet = 0


    def GPU_list(self):
        """показывает список установленных на ферме видеокарт"""
        if self.GPUs == []:
            print("\033[H\033[J")
            print("На ферме не установлено ни одной видеокарты")
            user_select = input("Введите N чтобы вернуться назад\n")

            if user_select == "n":
                return
            
        for gpu in self.GPUs:
            gpu.status
            user_select = input("Введите:\nR - чтобы перейти к следующей видеокарте\nN - вернуться назад\n")
            
            if user_select == "r":
                continue

            elif user_select == "n":
                return


    def add_GPU(self, user: 'User'):
        """
        Добавляет видеокарту на ферму, если ферма выключена,
        а видеокарта есть в инвентаре
        """
        if self.Farm_status:
            print("Чтобы поставить видеокарту, сначала выключите ферму!")
            return
        
        check_list = []
        for gpu in user.inventory.item_list:
            
            if type(gpu) == GPU:
                check_list.append(gpu)

        if check_list == []:
            while True:
                print("\033[H\033[J")
                print("В инвентаре нет ни одной видеокарты")
                user_select = input("Введите N чтобы вернуться назад\n")
                
                if user_select == "n":
                    return
            
        print("Доступные видеокарты:")
        gpu = user.inventory.check_items_for_add_farm("gpu")
    
        user.inventory.item_list.remove(gpu)
        self.GPUs.append(gpu)
        print(f"Видеокарта {gpu} успешно установлена и готова для майнинга")
        return


    def remove_GPU(self, user: 'User'):
        """
        Убираем видеокарту с фермы, если она выключена в инвентарь
        """
        if self.Farm_status:
            print("Чтобы убрать видеокарту, сначала выключите ферму!")
            return
        
        elif self.GPUs == []:
            print("\033[H\033[J")
            print("На ферме не установлено ни одной видеокарты")
            user_select = input("Введите N чтобы вернуться назад\n")
            
            if user_select == "n":
                return
        
        for gpu in self.GPUs:
            gpu.status
            user_select = input("Введите:\nR чтобы перейти к следующему предмету\nY чтобы убрать этот предмет с фермы\n").lower()
            
            if user_select == "r":
                continue

            elif user_select == "y":
                self.GPUs.remove(gpu)
                user.inventory.item_list.append(gpu)
                print(f"Видеокарта {gpu} успешно убрана с фермы и перемещена в инвентарь")
                return


    def add_RAD(self, user: 'User'):
        """Взаимодействие с радиатором по аналогии с add_GPU у видеокарты"""
        if self.Farm_status: 
            print("Чтобы поставить радиатор, сначала выключите ферму!")
            return
        
        check_list = []
        for radiator in user.inventory.item_list:
            
            if type(radiator) == Radiator:
                check_list.append(radiator)

        if check_list == []:
            while True:
                print("\033[H\033[J")
                print("В инвентаре нет ни одного радиатора")
                user_select = input("Введите N чтобы вернуться назад\n")
                
                if user_select == "n":
                    return
                
        print("Доступные радиаторы:")
        radiator = user.inventory.check_items_for_add_farm("radiator")     
        
        if len(self.Radiators) < 10:
            user.inventory.item_list.remove(radiator)
            self.Radiators.append(radiator)
            print(f"Радиатор {radiator} успешно установлен.")

        else:
            print("Вы не можете установить на ферму больше 10 радиаторов!")


    def remove_RAD(self, user: 'User'):
        """Взаимодействие с радиатором по аналогии с remnove_GPU у видеокарты"""

        if self.Farm_status:
            print("Чтобы убрать радиатор, сначала выключите ферму!")
            return

        elif self.Radiators == []:
            print("\033[H\033[J")
            print("На ферме не установлено ни одного радиатора")
            user_select = input("Введите N чтобы вернуться назад\n")

        for radiator in self.Radiators:
            radiator.status
            user_select = input("Введите:\nR чтобы перейти к следующему предмету\nY чтобы убрать этот предмет с фермы\n").lower()
            
            if user_select == "r":
                continue
            
            elif user_select == "y":
                self.Radiators.remove(radiator)
                user.inventory.item_list.append(radiator)
                print(f"Радиатор {radiator} успешно убран с фермы и перемещён в инвентарь.")
                return

    
    def _mining_loop(self):
        """
        Основная функция механики майнинга. Запускаем цикл, берем курс BTC с coingecko (если недоступно, то 
        берем запасной курс 80000$ за 1 BTC)
        и начинаем майнинг (генерируем блок, считаем халвинг, обновляем температуру видеокарт)
        """
        while self.Farm_status:
            try:
                response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
                btc_price = float(response.json()["bitcoin"]["usd"])
            except Exception:
                print("Не удалось получить актуальную цену BTC, используем запасное значение")
                btc_price = 80000 
            block = Block(btc_price)

            if self.block_counter % 10 == 0:
                block.halving

            block_dificulty_full = block.dificulty
            while block.dificulty > 0:
                
                if not self.Farm_status:  
                    return

                time.sleep(self._tick_time)

                if not self.GPUs:
                    self.Farm_status = False
                    return
                
                block.dificulty -= self.hashrate
                self.block_progress = 100 - (block.dificulty / block_dificulty_full * 100)
                self.block_progress = int(self.block_progress // 5) * 5  
                cooling_per_gpu = self.cooling_efficiency / len(self.GPUs) if self.GPUs else 0
                self.temp = sum(gpu.get_temp() for gpu in self.GPUs) / len(self.GPUs) if self.GPUs else 0
                for gpu in self.GPUs:
                    gpu.update(cooling_per_gpu)
                    gpu.durability_set()

            if self.Farm_status:
                self.energy_counter += self.energy
                self.wallet += block.block_reward        
                self.block_counter += 1
                print(f"BLOCK_PROGRESS: Блок #{self.block_counter} успешно добыт!")



    def start_mining(self):
        """
        Запускаем отдельный поток, и начинаем в нем майнинг (_mining_loop()). В основном
        потоке ждем пока пользователь введет stop для остановки майнинга.
        """
        if self.Farm_status == True:
            print("Ферма уже включена!")
            return
        
        if self.GPUs == []:
            print("Вы не можете начать майнинг! На ферме нет ни одной видеокарты!")
            return

        else:
            self.Farm_status = True

            self.hashrate = sum(gpu.get_hashrate() for gpu in self.GPUs)
            self.energy = sum(gpu.get_energy() for gpu in self.GPUs)
            self.temp = (sum(gpu.get_temp() for gpu in self.GPUs) / len(self.GPUs))
            self.cooling_efficiency = sum(radiator.get_cooling() for radiator in self.Radiators)
            mining_thread = threading.Thread(target=self._mining_loop, daemon=True)
            mining_thread.start()

        def display_loop():
            while self.Farm_status:
                self.status
                print("Майнинг запущен. Введите:\nstop - для остановки\ngpu - для просмотра состояния видеокарт\n")
                time.sleep(5)

        display_thread = threading.Thread(target=display_loop, daemon=True)
        display_thread.start()

        
        while self.Farm_status:
            user_input = input()
            
            if user_input.lower() == 'stop':
                self.stop_mining()
                break

            elif user_input.lower() == 'gpu':
                for gpu in self.GPUs:
                    gpu.status
                    select = input("Введите:\nR чтобы перейти к следующей видеокарте\nN - вернуться к дисплею фермы\n").lower()
                    
                    if select == "r":
                        continue
                    
                    elif select == "n":
                        break



    def stop_mining(self):
        """При вводе пользователем в start_mining() stop останавливаем майнинг (меняем статус фермы на False)"""
        if self.Farm_status == False:
            print("Ферма уже выключена!")

        else:
            for gpu in self.GPUs:
                gpu.off()
            self.hashrate = 0
            self.energy = 0
            self.cooling_efficiency = 0
            self.temp = 0
            self.block_progress = 0
            self.Farm_status = False
            print("Ферма выключена")

    
