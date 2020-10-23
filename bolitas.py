import threading
import time
import logging
import random

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

cantChicos = 10

class Chicos(threading.Thread):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor

    def cantBolitas(self):
        return random.randint(1, 10)

    def ponerBolitas(self):
        cant = self.cantBolitas()
        with self.monitor:
            for _ in range(cant):
                listaBolitas.append(0)
            self.monitor.notify()
            logging.info(f'Puse {cant} bolitas. Quedan {len(listaBolitas)}')
            time.sleep(2)

    def sacarBolitas(self):
        cant = self.cantBolitas()
        with self.monitor:
            while(True):
                while len(listaBolitas) < cant:
                    self.monitor.wait()
                for _ in range(cant):
                    listaBolitas.pop(0)
                logging.info(f'Saqué {cant} bolitas. Quedan {len(listaBolitas)}')
                time.sleep(2)

    def run(self):
        while (True):
            moneda = random.choice([0, 1])

            if (moneda == 0):
                self.ponerBolitas()
            else:
                self.sacarBolitas()


listaBolitas = []

listaBolitas_monit = threading.Condition()

for c in range(cantChicos):
    Chicos(listaBolitas_monit).start()