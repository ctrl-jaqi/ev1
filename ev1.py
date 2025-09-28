from datetime import datetime, timedelta
from tabulate import tabulate 

########### Datos en memoria ###########

clientes = []
salas = []
reservas = []

# Contadores globales
contador_clientes = 1
contador_salas = 1
contador_reservas = 1


########### Clases ###########

class Cliente:
    def _init_(self, id_cliente, nombre):
        self.id_cliente = id_cliente
        self.nombre = nombre

class Sala:
    def _init_(self, id_sala, nombre, capacidad):
        self.id_sala = id_sala
        self.nombre = nombre
        self.capacidad = capacidad

class Reserva:
    def _init_(self, folio, cliente, sala, fecha_evento, turno, nombre_evento):
        self.folio = folio
        self.cliente = cliente
        self.sala = sala
        self.fecha_evento = fecha_evento
        self.turno = turno
        self.nombre_evento = nombre_evento
        self.fecha_reserva = datetime.now().date()


########### Funciones ###########

def registrar_cliente(nombre):
    global contador_clientes
    cliente = Cliente(contador_clientes, nombre)
    clientes.append(cliente)
    print(f"Cliente registrado: {cliente.nombre} (ID: {cliente.id_cliente})")
    contador_clientes += 1
    return cliente

def registrar_sala(nombre, capacidad):
    global contador_salas
    sala = Sala(contador_salas, nombre, capacidad)
    salas.append(sala)
    print(f"Sala registrada: {sala.nombre} (Capacidad: {sala.capacidad}, ID: {sala.id_sala})")
    contador_salas += 1
    return sala

def buscar_cliente(id_cliente):
    return next((c for c in clientes if c.id_cliente == id_cliente), None)

def verificar_disponibilidad(sala, fecha_evento, turno):
    for r in reservas:
        if r.sala.id_sala == sala.id_sala and r.fecha_evento == fecha_evento and r.turno == turno:
            return False
    return True

def generar_folio():
    global contador_reservas
    fecha = datetime.now().strftime("%Y%m%d")
    folio = f"RES-{fecha}-{contador_reservas:04d}"
    contador_reservas += 1
    return folio

def hacer_reserva(id_cliente, id_sala, fecha_evento_str, turno, nombre_evento):
    cliente = buscar_cliente(id_cliente)
    if not cliente:
        print("Error: Cliente no registrado.")
        return

    sala = next((s for s in salas if s.id_sala == id_sala), None)
    if not sala:
        print("Error: Sala no encontrada.")
        return

    if turno not in ["mañana", "tarde", "noche"]:
        print("Error: Turno inválido. Usa 'mañana', 'tarde' o 'noche'.")
        return

    try:
        fecha_evento = datetime.strptime(fecha_evento_str, "%Y-%m-%d").date()
    except ValueError:
        print("Error: Formato de fecha inválido. Usa YYYY-MM-DD.")
        return

    if fecha_evento <= datetime.now().date() + timedelta(days=1):
        print("Error: La reserva debe hacerse al menos con 2 días de anticipación.")
        return

    if not nombre_evento.strip():
        print("Error: El nombre del evento es obligatorio.")
        return

    if not verificar_disponibilidad(sala, fecha_evento, turno):
        print(f"Error: La sala '{sala.nombre}' ya está reservada en esa fecha y turno.")
        return

    folio = generar_folio()
    reserva = Reserva(folio, cliente, sala, fecha_evento, turno, nombre_evento)
    reservas.append(reserva)
    print(f"Reserva exitosa. Folio: {reserva.folio}")

def listar_reservas():
    print("\n=== Reservas ===")
    for r in reservas:
        print(f"[{r.folio}] Cliente: {r.cliente.nombre}, Sala: {r.sala.nombre}, Fecha: {r.fecha_evento}, Turno: {r.turno}, Evento: {r.nombre_evento}")
    print("================\n")

def registrar_cliente_interactivo():
     global contador_clientes
     nombre = input("Nombre del cliente: ").strip()
     apellidos = input("Apellidos del cliente: ").strip()
     if not nombre or not apellidos:
        print("Nombre y apellidos no pueden estar vacíos.")
        return
     cliente = Cliente(contador_clientes, nombre, apellidos)
     clientes.append(cliente)
     print(f"Cliente registrado con éxito. ID: {cliente.id_cliente}")
     contador_clientes += 1

def listar_clientes():
    print("\n=== Clientes Registrados ===")
    if not clientes:
        print("No hay clientes registrados.")
        return
    clientes_ordenados = sorted(clientes, key=lambda c: (c.apellidos.lower(), c.nombre.lower()))
    for c in clientes_ordenados:
        print(f"ID: {c.id_cliente} - {c.apellidos}, {c.nombre}")
    print("=============================\n")

def registrar_sala_interactivo():
    global contador_salas
    nombre = input("Ingrese el nombre de la sala: ").strip()
    try:
        capacidad = int(input("Ingrese la capacidad de la sala: "))
    except ValueError:
        print("Capacidad debe ser un número.")
        return
    sala = Sala(contador_salas, nombre, capacidad)
    salas.append(sala)
    print(f"Sala registrada con éxito. ID: {sala.id_sala}")
    contador_salas += 1

def hacer_reserva_interactivo():
    while True:
        listar_clientes()
        try:
            id_cliente = int(input("Ingrese el ID del cliente o 0 para cancelar: "))
        except ValueError:
            print("ID inválido.")
            continue
        if id_cliente == 0:
            return
        cliente = buscar_cliente(id_cliente)
        if cliente:
            break
        else:
            print("ID de cliente no encontrado.")

    fecha_str = input("Fecha del evento (YYYY-MM-DD): ")
    try:
        fecha_evento = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        print("Fecha inválida.")
        return

    if fecha_evento <= datetime.now().date() + timedelta(days=1):
        print("La reserva debe hacerse con al menos 2 días de anticipación.")
        return

    salas_disponibles = []
    for sala in salas:
        for turno in ["mañana", "tarde", "noche"]:
            if verificar_disponibilidad(sala, fecha_evento, turno):
                salas_disponibles.append((sala, turno))

    if not salas_disponibles:
        print("Lo sentimos no hay salas disponibles para esa fecha.")
        return

    print("\n=== Salas disponibles ===")
    for idx, (sala, turno) in enumerate(salas_disponibles, 1):
        print(f"{idx}) Sala: {sala.nombre}, Capacidad: {sala.capacidad}, Turno: {turno}")
    print("=========================")

    try:
        seleccion = int(input("Seleccione una opción por número: "))
        sala, turno = salas_disponibles[seleccion - 1]
    except (ValueError, IndexError):
        print("Selección inválida.")
        return

    nombre_evento = input("Nombre del evento: ").strip()
    if not nombre_evento:
        print("El nombre del evento no puede estar vacío.")
        return

    folio = generar_folio()
    reserva = Reserva(folio, cliente, sala, fecha_evento, turno, nombre_evento)
    reservas.append(reserva)
    print(f"Su reserva se ah realizada con éxito. Folio: {folio}")

def consultar_reservas_por_fecha():
    fecha_str = input("Ingrese la fecha a consultar (YYYY-MM-DD): ")
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        print("Fecha inválida.")
        return
    
    reservas_en_fecha=[r for r in reservas if r.fecha_evento == fecha]

    if not reservas_en_fecha:
        print("Lo sentimos, no hay reservas para esta fecha.")

    print(f"\n=== Reporte de reservas para {fecha} ===")

    tabla = []
    for r in reservas_en_fecha:
        tabla.append([
            r.folio,
            f"{r.cliente.nombre} {r.cliente.apellidos}",
            r.sala.nombre,
            r.turno,
            r.nombre_evento,
            r.fecha_reserva.strftime("%Y-%m-%d")
        ])
    
    headers = ["Folio", "Cliente", "Sala", "Turno", "Evento", "Fecha Reserva"]
    print(tabulate(tabla, headers=headers, tablefmt="grid"))

    print("*******************************************\n")

def editar_nombre_evento():
    fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ")
    fecha_fin = input("Fecha de fin (YYYY-MM-DD): ")
    try:
        f_ini = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        f_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    except ValueError:
        print("Fechas inválidas.")
        return

    eventos = [r for r in reservas if f_ini <= r.fecha_evento <= f_fin]
    if not eventos:
        print("No hay eventos en ese rango.")
        return

    print("\n=== Estos son los eventos encontrados ===")
    for r in eventos:
        print(f"{r.folio} - {r.nombre_evento} ({r.fecha_evento})")
    print("===========================")

    while True:
        folio = input("Ingrese el folio del evento a editar o 0 para cancelar: ").strip()
        if folio == "0":
            return
        reserva = next((r for r in eventos if r.folio == folio), None)
        if reserva:
            nuevo_nombre = input("Nuevo nombre del evento: ").strip()
            if not nuevo_nombre:
                print("El nombre no puede estar vacío.")
                continue
            reserva.nombre_evento = nuevo_nombre
            print("Nombre del evento actualizado.")
            return
        else:
            print("Folio no encontrado en el rango.")

########### Menú principal ###########
def menu():
    while True:
        print("\n===== Menú Principal =====")
        print("1. Registrar reservación")
        print("2. Editar nombre del evento")
        print("3. Consultar reservaciones por su fecha")
        print("4. Registrar un nuevo cliente")
        print("5. Registrar una nueva sala")
        print("6. Salir")
        opcion = input("Porfavor seleccione una opción: ")

        if opcion == "1":
            hacer_reserva_interactivo()
        elif opcion == "2":
            editar_nombre_evento()
        elif opcion == "3":
            consultar_reservas_por_fecha()
        elif opcion == "4":
            registrar_cliente_interactivo()
        elif opcion == "5":
            registrar_sala_interactivo()
        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

if __name__ == "_main_":
    menu()
