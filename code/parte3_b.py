
from mpi4py import MPI
import numpy as np
import pandas as pd
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Solo se necesitan 3 procesadores para esta tarea
if size != 3:
    raise ValueError("Este programa requiere exactamente 3 procesadores.")

# Procesador 0 carga el archivo CSV y divide los datos en dos partes
if rank == 0:
    data = pd.read_csv(r'../data/tarea2.csv')
    data.columns = ['A']
    #data = data.astype(float)  # Asegurarse de que todos los datos sean float
    values = data.to_numpy()
    part1 = values[:len(values) // 2]
    part2 = values[len(values) // 2:]
    start_time = time.time()  # Registrar el tiempo antes de comenzar el procesamiento
else:
    part1 = None
    part2 = None

# Broadcasting de las partes
part1 = comm.bcast(part1, root=0)
print(f"Procesador {rank} recibió part1")
part2 = comm.bcast(part2, root=0)
print(f"Procesador {rank} recibió part2")

# Hallar el máximo en cada parte
if rank == 1:
    local_max = np.max(part1)
    print(f"Procesador {rank} encontró el máximo local: {local_max}")
elif rank == 2:
    local_max = np.max(part2)
    print(f"Procesador {rank} encontró el máximo local: {local_max}")
else:
    local_max = float('-inf')
    print(f"Procesador {rank} no calcula el máximo local")

# Asegurarse de que local_max es un float en todos los procesadores
local_max = float(local_max)

# El procesador 0 reúne los máximos hallados y encuentra el máximo global
global_max = comm.reduce(local_max, op=MPI.MAX, root=0)

if rank == 0:
    end_time = time.time()  # Registrar el tiempo después de completar el procesamiento
    print(f"Valor máximo usando dos procesadores: {global_max}")
    print(f"Tiempo de demora: {end_time - start_time:.6f} segundos")
else:
    print(f"Procesador {rank} terminó")




