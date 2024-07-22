
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

# Cargar el archivo CSV y dividir los datos en dos partes
if rank == 0:
    data = pd.read_csv(r'../data/tarea2.csv')
    values = data.to_numpy()
    part1 = values[:len(values) // 2]
    part2 = values[len(values) // 2:]
else:
    part1 = None
    part2 = None

# Broadcasting de las partes
part1 = comm.bcast(part1, root=0)
part2 = comm.bcast(part2, root=0)

# Hallar el máximo en cada parte
if rank == 1:
    local_max = np.max(part1)
    print(f"Procesador {rank} encontró el máximo local: {local_max}")
elif rank == 2:
    local_max = np.max(part2)
    print(f"Procesador {rank} encontró el máximo local: {local_max}")
else:
    local_max = None

# Asegurarse de que local_max no sea None
if local_max is None:
    raise ValueError(f"Procesador {rank} no calculó un máximo local válido.")

# El procesador 0 reúne los máximos hallados y encuentra el máximo global
global_max = comm.reduce(local_max, op=MPI.MAX, root=0)

if rank == 0:
    end_time = time.time()
    print(f"Valor máximo usando dos procesadores: {global_max}")
    print(f"Tiempo de demora: {end_time - start_time:.6f} segundos")
