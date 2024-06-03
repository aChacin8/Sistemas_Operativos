import threading
import time
import random

semaforo = threading.Semaphore(4)

class Cliente(threading.Thread):
    def __init__(self, nombre, num_cliente, cuenta_bancaria, saldo):
        super().__init__()
        self.nombre = nombre
        self.num_cliente = num_cliente
        self.cuenta_bancaria = cuenta_bancaria
        self.saldo = saldo
        self.atendido = False

    def run(self):
        self.llego()
        with semaforo:
            self.atendido_si()

    def llego(self):
        print(f"Cliente {self.nombre} {self.num_cliente} está esperando su turno")

    def atendido_si(self):
        self.atendido = True
        print(f"El cliente {self.nombre} {self.num_cliente} está siendo atendido en ventanilla")
        print(f"Su número de cuenta es {self.cuenta_bancaria}\nTiene ${self.saldo} disponible")
        self.realizar_operacion()
        time.sleep(3)

    def realizar_operacion(self):
        operacion = random.choice(['depositar', 'retirar'])
        if operacion == 'depositar':
            cantidad = random.randint(100, 1000)  # Simulando un depósito aleatorio
            print(f"Cliente {self.nombre} elige depositar ${cantidad}")
            ventanilla = random.choice(ventanillas)
            ventanilla.depositar(self, cantidad)
        else:
            cantidad = random.randint(50, 500)  # Simulando un retiro aleatorio
            if self.saldo >= cantidad:
                print(f"Cliente {self.nombre} elige retirar ${cantidad}")
                ventanilla = random.choice(ventanillas)
                ventanilla.retirar(self, cantidad)
            else:
                print(f"Cliente {self.nombre} intentó retirar ${cantidad} pero no tiene suficiente saldo")

    def actualizar_saldo(self, saldo):
        self.saldo = saldo

    def obtener_saldo(self):
        return self.saldo

class Ventanillas:
    def __init__(self, ventana):
        self.ventana = ventana
        self.atendiendo = False

    def atender(self):
        self.atendiendo = True
        print(f"La ventanilla {self.ventana} está ocupada")

    def depositar(self, cliente, deposito):
        saldo_actual = cliente.obtener_saldo()
        cliente.actualizar_saldo(saldo_actual + deposito)
        print(f"Cliente {cliente.nombre} está realizando un depósito de ${deposito}")

    def retirar(self, cliente, retiro):
        saldo_actual = cliente.obtener_saldo()
        cliente.actualizar_saldo(saldo_actual - retiro)
        print(f"Cliente {cliente.nombre} está realizando un retiro de ${retiro}")
        print(f"El saldo de {cliente.nombre} es de ${saldo_actual - retiro}")

clientes = [
    Cliente("Villagran", "01", 200600, 2500),
    Cliente("Chacin", "02", 1233066, 3600),
    Cliente("Medina", "03", 1783024, 1245),
    Cliente("Villela", "04", 1534066, 850),
    Cliente("Barrios", "05", 1930878, 850),
]

ventanillas = [
    Ventanillas("1"),
    Ventanillas("2"),
    Ventanillas("3"),
    Ventanillas("4"),
]

for cliente in clientes:
    time.sleep(random.randint(1, 3))  # Tiempo de espera aleatorio antes de que el siguiente cliente llegue
    cliente.start()

# Esperar a que todos los clientes terminen de ser atendidos
for cliente in clientes:
    cliente.join()

print ("\nCerró el Bnaco \n")