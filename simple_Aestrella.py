import math
import matplotlib.pyplot as plt

def graficarMapa(mapa, camino, inicio, objetivo):
    """
    Grafica el mapa con las estanterías, el camino recorrido, el punto de inicio y el objetivo.
    
    :param mapa: Lista de celdas del mapa, donde cada celda es [x, y, valor].
    :param camino: Lista de nodos que forman el camino recorrido.
    :param inicio: Coordenadas del punto de inicio [x, y].
    :param objetivo: Coordenadas del punto objetivo [x, y].
    """
    # Crear una figura y un eje
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Dibujar las estanterías (celdas no explorables)
    for celda in mapa:
        x, y, valor = celda
        if valor == float('inf'):  # Estanterías
            ax.add_patch(plt.Rectangle((x, y), 1, 1, color='gray'))
    
    # Dibujar el camino recorrido
    for nodo in camino:
        x, y = nodo[0], nodo[1]
        ax.add_patch(plt.Rectangle((x, y), 1, 1, color='blue', alpha=0.5))
    
    # Marcar el punto de inicio
    ax.add_patch(plt.Rectangle((inicio[0], inicio[1]), 1, 1, color='green', label='Inicio'))
    
    # Marcar el punto objetivo
    ax.add_patch(plt.Rectangle((objetivo[0], objetivo[1]), 1, 1, color='red', label='Objetivo'))
    
    # Configurar el gráfico
    ax.set_xlim(-1, max([celda[0] for celda in mapa]) + 2)
    ax.set_ylim(-1, max([celda[1] for celda in mapa]) + 2)
    ax.set_aspect('equal')
    ax.set_xticks(range(0, max([celda[0] for celda in mapa]) + 1))
    ax.set_yticks(range(0, max([celda[1] for celda in mapa]) + 1))
    ax.grid(True, which='both', color='black', linestyle='--', linewidth=0.5)
    ax.legend()
    
    # Mostrar el gráfico
    plt.title("Mapa con estanterías y camino recorrido")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()


def hacerMapa(columnas:int,filas:int,inicio =[0,0]):
    mapa = [[x,y,1] for x in range(columnas) for y in range(filas)]
    #Coloca las estanterias, definiendo los espacios que son explorables y los que no lo son
    for i in range(len(mapa)):
        if (mapa[i][1]%5 != 0) and (mapa[i][0]%3 != 0):
            mapa[i][2] = float('inf')
        if (mapa[i][0] == inicio[0]) and (mapa[i][1] == inicio[1]):
            mapa[i] = [inicio[0],inicio[1],1]
    return mapa

#Tengo pensado definir la funcion G a partir del numero de pasos que se hayan hecho, simplemente
#La heuristica, definida en este caso como la distancia en linea recta entre dos puntos
def funcionH(x1:int, y1:int, x2:int, y2:int):
    distY = y2-y1
    distX = x2-x1
    distSquared = (distX**2) + (distY**2)
    return math.sqrt(distSquared)
def funcionG(x1:int, y1:int, x2:int, y2:int):
        distX = x2-x1
        distY = y2-y1
        if(distX != 0):
            tita = math.atan(distY/distX)
        else:
            tita = math.pi/2
        modulo = math.sqrt((distX**2) + (distY**2))
        return abs(modulo*math.cos(tita))+abs(modulo*math.sin(tita))
#x2 e y2 siempre representan las coordenadas del nodo objetivo
def funcionNodo(x1:int, y1:int, x2:int, y2:int,gn:float):
    if(gn == 0): #Para cuando ambos puntos tengan el mismo nivel
        gn = abs((x2-x1)*2)
    hn = funcionH(x1,y1,x2,y2)
    return (gn+hn)
#El metodo A* en si
def Aestrella(objetivo:list, inicio:list, mapa:list, listaAb:list, listaCerr:list, listaAbMen:list):
    salir = False
    estAct = inicio
    while(estAct != objetivo):
        estXm = [estAct[0]-1, estAct[1]]
        estXM = [estAct[0]+1, estAct[1]]
        estYm = [estAct[0], estAct[1]-1]
        estYM = [estAct[0], estAct[1]+1]
        if(estXm == objetivo or estXM == objetivo or estYm== objetivo or estYM==objetivo):
            salir = True
        for i in range(len(mapa)):
            if (estXm == [mapa[i][0], mapa[i][1]]) and (salir != True) and (estXm != inicio):
                estXm.append(1)
                if(mapa.count(estXm)):
                    estXm.append(funcionNodo(estXm[0],estXm[1],objetivo[0],objetivo[1],funcionG(inicio[0],inicio[1],estXm[0],estXm[1])))
                    listaAb.append(estXm)
            if (estXM == [mapa[i][0], mapa[i][1]]) and (salir != True) and (estXM != inicio):
                estXM.append(1)
                if(mapa.count(estXM)):
                    estXM.append(funcionNodo(estXM[0],estXM[1],objetivo[0],objetivo[1],funcionG(inicio[0],inicio[1],estXM[0],estXM[1])))
                    listaAb.append(estXM)
            if (estYm == [mapa[i][0], mapa[i][1]]) and (salir != True) and (estYm != inicio):
                estYm.append(1)
                if(mapa.count(estYm)):
                    estYm.append(funcionNodo(estYm[0],estYm[1],objetivo[0],objetivo[1],funcionG(inicio[0],inicio[1],estYm[0],estYm[1])))
                    listaAb.append(estYm)
            if (estYM == [mapa[i][0], mapa[i][1]]) and (salir != True) and (estYM != inicio):
                estYM.append(1)
                if(mapa.count(estYM)):
                    estYM.append(funcionNodo(estYM[0],estYM[1],objetivo[0],objetivo[1],funcionG(inicio[0],inicio[1],estYM[0],estYM[1])))
                    listaAb.append(estYM)
        removible = []
        for i in range(len(listaAb)):
            if(listaCerr.count(listaAb[i])) and (salir != True):
                    removible.append(listaAb[i])
        for i in range(len(removible)):
            if(listaAb.count(removible[i])) and (salir != True):
                listaAb.remove(removible[i])
        listaAbMen = listaAb[0]
        
        for i in range(len(listaAb)):
            if (listaAb[i] != None) and (listaAb[i][3] < listaAbMen[3]) and (salir != True):
                listaAbMen = listaAb[i]
        if(salir != True):
            listaCerr.append(listaAbMen)
            estAct = [listaAbMen[0], listaAbMen[1]]
        else:
            objetivo.append(1)
            objetivo.append(funcionNodo(objetivo[0],objetivo[1],objetivo[0],objetivo[1],funcionG(inicio[0],inicio[1],objetivo[0],objetivo[1])))
            listaCerr.append(objetivo)
            estAct = objetivo
    return listaCerr
#Pedido de datos del arreglo de estanterias. Quitar comentarios si se quiere 
#que el usuario ingrese los datos
estFilas = 5#int(input("Numero de estanterias en fila: "))
estColumn = 3#int(input("Numero de estanterias en columna: "))
Xin = 0#int(input("X inicio: "))
Yin = 0#int(input("Y inicio: "))
Xob = 15#int(input("X objetivo: "))
Yob = 13#int(input("Y objetivo: "))
#Variables iniciales del problema
filas = 5*estColumn+1
columnas = 3*estFilas+1
mapa = []
listaAb = []
listaCerr = []
listaAbMen = []
objetivo = [Xob,Yob]
inicio = [Xin,Yin]
estAct = inicio
inicio.append(1)
inicio.append(funcionH(inicio[0],inicio[1],objetivo[0],objetivo[1]))
listaAb.append(inicio)
listaCerr.append(inicio)
inicio = [Xin,Yin]

camino = Aestrella(objetivo,inicio,hacerMapa(columnas,filas,inicio),
                listaAb,listaCerr,listaAbMen)
# Ejemplo de uso
mapa = hacerMapa(columnas, filas, inicio)
#camino = Aestrella(objetivo, inicio, mapa, listaAb, listaCerr, listaAbMen)
graficarMapa(mapa, camino, inicio, objetivo)
