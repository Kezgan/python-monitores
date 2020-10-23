import threading
import time
import logging
import random

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

cantConsumidores = 5

def productor(monitor):
    print("Voy a producir")
    for i in range(30):
        with monitor:          # hace el acquire y al final un release
            items.append(i)    # agrega un ítem
            monitor.notify()   # Notifica que ya se puede hacer acquire
        time.sleep(2) # simula un tiempo de producción


class Consumidor(threading.Thread):
    def __init__(self, monitor, cantConsumir):
        super().__init__()
        self.monitor = monitor
        self.cantConsumir = cantConsumir

    def run(self):
        while (True):
            
            with self.monitor:          # Hace el acquire y al final un release    
                while len(items)<self.cantConsumir:
                    self.monitor.wait()  # espera la señal, es decir el notify
                for _ in range(self.cantConsumir):
                    x = items.pop(0)     # saca (consume) el primer ítem
                    logging.info(f'Consumí {x}')

            time.sleep(1)


# la lista de ítems a consumir
items = []

# El monitor
items_monit = threading.Condition()

# lista de consumidores
listaConsumidores = []
for c in range(cantConsumidores):
    listaConsumidores.append(c)

# cantidad de consumidores
for c in listaConsumidores:
    cantConsumir = random.randint(1, 6)
    cons1 = Consumidor(items_monit, cantConsumir)
    cons1.start()

# El productor
productor(items_monit)



        
