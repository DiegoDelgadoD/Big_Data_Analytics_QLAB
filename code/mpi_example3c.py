
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    # Procesador 0 genera la lista y la envía a los otros 3 procesadores
    data = list(range(10))  # Lista de ejemplo
    for i in range(1, 4):
        comm.send(data, dest=i, tag=11)
        print(f"Procesador 0 envió la lista al procesador {i}")
else:
    # Procesadores 1, 2 y 3 reciben la lista y la imprimen
    data = comm.recv(source=0, tag=11)
    print(f"Procesador {rank} recibió la lista: {data}")
