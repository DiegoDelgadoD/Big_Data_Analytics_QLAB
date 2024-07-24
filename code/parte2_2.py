
from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Parte a: Broadcasting
cursos_favoritos = {
    0: "Econometría avanzada",
    1: "Introduccion al Machine Learning",
    2: "Estadística",
    3: "Python Intermedio"
}

# Solo el procesador 0 define el diccionario
if rank == 0:
    data = cursos_favoritos
else:
    data = None

# Registrar el tiempo antes del broadcasting
start_time = time.time()

# Broadcasting del diccionario
data = comm.bcast(data, root=0)

# Registrar el tiempo después del broadcasting
end_time = time.time()
broadcast_time = end_time - start_time

# Imprimir el diccionario recibido y el tiempo de demora en cada procesador
print(f"Procesador {rank} recibió el diccionario: {data} en {broadcast_time:.6f} segundos")

# Parte b: Scattering
# Definir una secuencia de valores {0, 1, 2, ..., n}
if rank == 0:
    valores = np.arange(size, dtype='i')
else:
    valores = None

# Preparar un array para recibir el valor dispersado
valor_recibido = np.zeros(1, dtype='i')

# Dispersar los valores
comm.Scatter(valores, valor_recibido, root=0)

# Imprimir el valor recibido y comprobar si coincide con el rango del procesador
print(f"Procesador {rank} recibió el valor {valor_recibido[0]}. Coincide con el rango: {valor_recibido[0] == rank}")
