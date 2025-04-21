from cmath import polar
from datetime import datetime
import time

#--------------------
#execiones
#--------------------

class ProductError(Exception):
    pass

class stock_insuficiente(Exception):
    def __init__(self, mensaje="no hay suficiente stock"):
        self.mensaje = mensaje
        super().__init__(mensaje)  

#--------------------
#decoradores
#--------------------

def registrar_operacion(func):
    def wrapper(*args, **kwargs):
        print(f"\n[LOG] Ejecutando: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def medir_tiempo(func):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"[TIEMPO] {func.__name__} tomó {fin - inicio:.4f} segundos")  # Falta un espacio después de __name__
        return resultado
    return wrapper

class producto:
    def __init__(self, codigo, nombre, precio, stock, categoria,
    tipo=None, fecha_vencimiento=None, garantia=None):  # 'none' debe ser 'None'
        self.codigo = codigo
        self._nombre = nombre
        self.__precio = precio
        self.stock = stock
        self.categoria = categoria
        self.tipo = tipo
        self.fecha_vencimiento = fecha_vencimiento
        self.garantia = garantia
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre):
        if nuevo_nombre:
            self._nombre = nuevo_nombre
    
    @property
    def precio(self):
        return self.__precio
    
    @precio.setter
    def precio(self, nuevo_precio):
        if nuevo_precio > 0:
            self.__precio = nuevo_precio
    
    def mostrar_info(self):
        return f"{self.codigo}: {self._nombre}, Precio: {self.__precio}, Stock: {self.stock}"

#--------------------
#funciones del sistema
#--------------------

@registrar_operacion
@medir_tiempo
def cargar_productos(listas_tuplas):
    return [producto(*datos) for datos in listas_tuplas]

@registrar_operacion
def aplicar_descuento(producto, porcentaje):
    def descuento(p):
        p.precio = round(p.precio * (1 - porcentaje / 100), 2)
        return p
    return list(map(descuento, producto))

@registrar_operacion
def valor_total_inventario(producto):
    return sum(p.precio * p.stock for p in producto)

@registrar_operacion
def vender_producto(producto, cantidad):
    if producto.stock < cantidad:
        raise stock_insuficiente()
    producto.stock -= cantidad
    return "venta realizada"

@registrar_operacion
def generar_reporte(producto):
    reporte = list(map(lambda p: (p.codigo, p.nombre, p.precio, p.stock), producto))
    for codigo, nombre, precio, stock in reporte:
        print(f"{codigo} - {nombre}: ${precio}, Stock: {stock}")
    return reporte

def mostrar_menu():
    print("\n--- Menú del Sistema de Gestión de Productos ---")
    print("1. Cargar productos")
    print("2. Ver productos")
    print("3. Aplicar descuento")
    print("4. Calcular valor total del inventario")
    print("5. Vender producto")
    print("6. Generar reporte")
    print("0. Salir")


#----------------------
#prueba del sistema
#----------------------

if __name__ == "__main__":
    productos = []
    datos_productos = [
        (101, "Laptop", 2500.0, 10, "Electrónica", "Portátil", None, 12),
        (102, "Leche", 3.5, 50, "Alimentos", "Lácteo", "2025-01-01", None),
        (103, "Smartphone", 1200.0, 5, "Electrónica", "Móvil", None, 24)
    ]

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            productos = cargar_productos(datos_productos)
            print("Productos cargados con éxito.")
        elif opcion == "2":
            if not productos:
                print("Primero debe cargar los productos.")
            else:
                for p in productos:
                    print(p.mostrar_info())
        elif opcion == "3": 
            if not productos:
                print("Primero debe cargar los productos.")
            else: 
                try:
                    porcentaje = float(input("Ingrese el porcentaje de descuento: "))
                    productos = aplicar_descuento(productos, porcentaje)
                    print("Descuento aplicado con éxito.")
                except ValueError:
                    print("Ingrese un valor numérico válido para el descuento.")
        elif opcion == "4":
            if not productos:
                print("Primero debe cargar los productos.")
            else:
                total = valor_total_inventario(productos)
                print(f"Valor total del inventario: ${total:.2f}")
        elif opcion == "5":
            if not productos:
                print("Primero debe cargar los productos.")
            else:
                try:
                    cod = int(input("Ingrese el código del producto a vender: "))
                    cantidad = int(input("Ingrese la cantidad a vender: "))
                    producto = next(p for p in productos if p.codigo == cod)
                    vender_producto(producto, cantidad)
                    print("Venta realizada con éxito.")
                except StopIteration:
                    print("Producto no encontrado.")
                except ValueError:
                    print("Ingrese valores numéricos válidos para el código y la cantidad.")
                except stock_insuficiente as e:
                    print(f"Error: {e.mensaje}")
        elif opcion == "6":
            if not productos:
                print("Primero debe cargar los productos.")
            else:
                generar_reporte(productos)
        elif opcion == "0":
            print("Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

#provando para git hub
#prueba de mergin



    