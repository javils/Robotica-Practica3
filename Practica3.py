# -*- encoding: utf-8 -*-
from pyrobot.brain import Brain
import random
import math

class Individuo:
    def __init__(self, IndId):
        # Constantes
        self.CONTROL_BORROSO_SIZE = 12  # tamaño del array controlBorroso

        # Variables
        self.id = IndId  # Id para diferenciar un individuo de otro
        self.calidad = 0  # calidad del individuo
        self.controlBorroso = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.initControlBorroso()  # array con la funcion de pertenencia [X,X,X,Y,Y,Y,Z,Z,Z,Z,Z,Z] X = Error Y = D.Error Z = Salida
        self.probabilidad = 0  # probabilidad de ser elegido en la mutación
        self.funcionError = range(0, 7)  # Hay 7 puntos de corte con el eje
        self.funcionDError = range(0, 7)  # Hay 7 puntos de corte con el eje
        self.funcionSalida = range(0, 12)   # Hay 12 puntos de corte con el eje

        self.actualizaFunciones()

    def initControlBorroso(self):
        # Error
        aux = [random.random() for col in range(3)]
        aux.sort()  # ordenamos para que los puntos de corte de la funcion de pertenencia esten ordenados
        self.controlBorroso[0] = aux[0]
        self.controlBorroso[1] = aux[1]
        self.controlBorroso[2] = aux[2]

        # Derivada del error
        aux = [random.random() for col in range(3)]
        aux.sort()  # ordenamos para que los puntos de corte de la funcion de pertenencia esten ordenados
        self.controlBorroso[3] = aux[0]
        self.controlBorroso[4] = aux[1]
        self.controlBorroso[5] = aux[2]

        # Salida
        aux = [random.random() for col in range(6)]
        aux.sort()  # ordenamos para que los puntos de corte de la funcion de pertenencia esten ordenados
        self.controlBorroso[6] = aux[0]
        self.controlBorroso[7] = aux[1]
        self.controlBorroso[8] = aux[2]
        self.controlBorroso[9] = aux[3]
        self.controlBorroso[10] = aux[4]
        self.controlBorroso[11] = aux[5]

    # Actualiza los valores de las funciones
    def actualizaFunciones(self):
        # Error
        self.funcionError[0] = -self.controlBorroso[2]
        self.funcionError[1] = -self.controlBorroso[1]
        self.funcionError[2] = -self.controlBorroso[0]
        self.funcionError[3] = 0  # Este valor siempre va a ser 0, es el eje de simetria de la funcion
        self.funcionError[4] = self.controlBorroso[0]
        self.funcionError[5] = self.controlBorroso[1]
        self.funcionError[6] = self.controlBorroso[2]

        # Derivada del error
        self.funcionDError[0] = -self.controlBorroso[5]
        self.funcionDError[1] = -self.controlBorroso[4]
        self.funcionDError[2] = -self.controlBorroso[3]
        self.funcionDError[3] = 0  # Este valor siempre va a ser 0, es el eje de simetria de la funcion
        self.funcionDError[4] = self.controlBorroso[3]
        self.funcionDError[5] = self.controlBorroso[4]
        self.funcionDError[6] = self.controlBorroso[5]

        # Salida
        self.funcionSalida[0] = -self.controlBorroso[11]
        self.funcionSalida[1] = -self.controlBorroso[10]
        self.funcionSalida[2] = -self.controlBorroso[9]
        self.funcionSalida[3] = -self.controlBorroso[8]
        self.funcionSalida[4] = -self.controlBorroso[7]
        self.funcionSalida[5] = -self.controlBorroso[6]
        self.funcionSalida[6] = self.controlBorroso[6]
        self.funcionSalida[7] = self.controlBorroso[7]
        self.funcionSalida[8] = self.controlBorroso[8]
        self.funcionSalida[9] = self.controlBorroso[9]
        self.funcionSalida[10] = self.controlBorroso[10]
        self.funcionSalida[11] = self.controlBorroso[11]

    # muta aleatoriamente un numero aleatorio de genes
    def muta(self):
        numMutaciones = (int(random.random()*self.CONTROL_BORROSO_SIZE))%self.CONTROL_BORROSO_SIZE

        for i in range(numMutaciones):
            genMutado = (int(random.random()*self.CONTROL_BORROSO_SIZE))%self.CONTROL_BORROSO_SIZE
            self.mutaGen(genMutado)
        self.actualizaFunciones()

    # muta un gen dado.
    def mutaGen(self, pos):
        newGen = self.controlBorroso[pos] + random.gauss(0, 1)  # Ahora el gen puede ser negativo, hay que tenerlo en cuenta, no nos interesa
        genPost = 0
        genAnt = 0
        if pos < self.CONTROL_BORROSO_SIZE:
            genPost = self.controlBorroso[pos+1]
        if pos > 0:
            genAnt = self.controlBorroso[pos-1]

        # Verificamos que sigue siendo una funcion de pertenencia borrosa
        if (pos == 0 or pos == 3 or pos == 6):  # Primeras posiciones de cada "bloque" (Error, Derivada, Salida)
            if (newGen > genPost or newGen < 0):
                newGen = genPost/2  # Asi nos aseguramos que siempre sera menor.
        elif (pos == 2 or pos == 5 or pos == 11):  # Ultimas posiciones de cada "bloque"
            if (newGen < genAnt):
                newGen = genAnt + (self.controlBorroso[pos] - genAnt)/2 # Nos aseguramos que sea mayor
        else:
            if (newGen > genPost or newGen < genAnt):  # Posiciones intermedias de cada "bloque"
                newGen = genAnt + (genPost - genAnt)/2 # Aseguramos que el valor este entre medias.

        self.controlBorroso[pos] = newGen


# Error
MD = 0 # Error negativo
D = 1
Z = 2
I = 3
MI = 4 # Error Positivo

# DError
MP = 0  # DError Positiva
P = 1
Z = 2
N = 3
MN = 4  # DError Negativa

# Salida
GMD = 0  # Girar mucho a la derecha
GD = 1  # Girar derecha
SR = 2  # Seguir rect
GI = 3  # Girar izquierda
GMI = 4  # Girar mucho a la izquierda

class Control(Brain):

    def setup(self):
        # Constantes
        self.MAX_GEN = 100
        self.MAX_ITR = 200
        self.MAX_IND = 20
        self.MIN_DIST = 0.5  # Por poner un valor, habra que ver cual es mejor.

        # Array de posiciones aleatorias
        self.POSICIONES = [[12.75746, 4.69842, 190.0714], [5.18442, 9.84676, 274.06364], [3.30373, 0.303278, 167.53044], [1.75536, 5.111311, 305.59911]]
        self.POS_LUZ = [4.75, 4.75]

        # Esto es recomendable hacerlo mejor, creo que no esta puesto bien
        """
        self.FAM = [[GMI, GMI, GD, GMD, GMD],
                    [GI,  GI,  GD, GD,  GD ],
                    [GI,  GI,  SR, GD,  GD ],
                    [GMI, SR,  GI, GD,  GMD],
                    [GI,  SR,  GI, SR,  GD ]]
                    """
        self.FAM = [[SR, GD, GMI, GI,  GMI],
                    [GD,  GD,  GI,  SR,  GI ],
                    [GMD, GD,  SR,  GI,  GMI ],
                    [GD,  GD,  GD,  GI,  GI],
                    [GMD,  GMD, GMD, SR,  SR ]]
        # Contiene el error y la derivada del erro borrosificadas
        self.errorBorrosificado = range(0, 5)
        self.derrorBorrosificado = range(0, 5)

        # Variables
        self.itr = 0  # numero de iteraciones que ha relizado el robot hasta ahora
        self.gen = 0  # generacion en la que estamos
        self.ind = 0  # individuo en el que estamos
        self.poblacion = range(0, self.MAX_IND)
        self.probTotal = 0
        self.error = 0
        self.errorAnt = 0
        self.derror = 0
        self.elite = Individuo(-1)
        self.initPoblacion()
        self.posiciona()

    # Inicializa la primera poblacion que se usara con individuos
    def initPoblacion(self):
        # Inicializamos la primera población
        for i in range(self.MAX_IND):
            self.poblacion[i] = Individuo(i)
            self.poblacion[i].calidad = 1  # Para que no crashe por dividir entre 0 mas adelante
            self.probTotal = self.probTotal + self.poblacion[i].calidad

            # Elitismo
            if (i == 0):
                self.elite = self.poblacion[i]
            elif (self.elite.calidad < self.poblacion[i].calidad):
                self.elite = self.poblacion[i]

        # Asignamos la probabilidad que tiene de ser elegido cuando se vaya a mutar.
        for i in range(self.MAX_IND):
            self.poblacion[i].probabilidad = float((self.poblacion[i].calidad) / self.probTotal)

    # Asigna calidad a un individuo
    def setCalidad(self):
        return self.MAX_ITR / self.itr

    # Crea una nueva poblacion de individuos mutandolos.
    def nuevaPoblacion(self):
        # El primer individuo el mejor de la generacion anterior
        nuevapoblacion = range(0, self.MAX_IND)
        nuevapoblacion[0] = self.elite

        # Creamos la "ruleta" de probabilidades
        tablaProb = range(0, self.MAX_IND)
        probAcum = 0  # Probabilidad acumulada hasta el momento.
        for i in range(0, self.MAX_IND):
            probAcum = probAcum + self.poblacion[i].probabilidad
            tablaProb[i] = [self.poblacion[i].id, probAcum]

        # Mutamos los individuos y los añadimos a la nueva poblacion
        for i in range(1, self.MAX_IND):
            prob = random.random()

            pos = 0  # elemento de la tabla que ha "tocado"
            # Buscamos el individuo en la tabla
            for j in range (0, self.MAX_IND):
                if (prob < tablaProb[j][1]):
                   pos = j

            newIndividuo = self.poblacion[pos]
            newIndividuo.id = tablaProb[pos][0]
            newIndividuo.muta()

            nuevapoblacion[i] = newIndividuo

    # Posiciona al robot en una posicion aleatoria de entre 4 recolectadas.
    def posiciona(self):
        r = (int(random.random()*3))%3
        self.robot.simulation[0].setPose(self.robot.name, self.POSICIONES[r][0],self.POSICIONES[r][1],self.POSICIONES[r][2])

    # Devuelve 1 si el robot ha encontrado la luz, 0 en caso contrario
    def luzEncontrada(self):
        pos = self.robot.simulation[0].getPose(self.engine.brain.robot.name)
        # d = sqrt((x-x0)^2 + (y-y0)^2)
        d = math.sqrt((pos[0] - self.POS_LUZ[0])**2 + (pos[1] - self.POS_LUZ[1])**2)

        if (d < self.MIN_DIST):
            return 1

        return 0
    # Asigna un elite en la poblacion
    def setElite(self):
        for i in range(0, self.MAX_IND):
            if (self.poblacion[i].calidad > self.elite.calidad):
                self.elite = self.poblacion[i].calidad

    def getDErrorBorroso(self, error, parte):
        # Funcion de pertenencia de muy a la derecha
        arrayDError = self.poblacion[self.ind].funcionDError
        if parte == MP:
            if error <= arrayDError[0]:
                return 1.0
            elif error > arrayDError[1]:
                return 0.0
            else:
                return (arrayDError[1] - error)/(arrayDError[1] - arrayDError[0])
        elif parte == P:
            if error <= arrayDError[0]:
                return 0.0
            elif (error > arrayDError[0] and error < arrayDError[1]):
                return (error - arrayDError[0])/(arrayDError[1] - arrayDError[0])
            elif (error >= arrayDError[1] and error <= arrayDError[2]):
                return 1.0
            elif (error > arrayDError[2]  and error < arrayDError[3]):
                return (arrayDError[3] - error)/(arrayDError[3] - arrayDError[2])
            else:
                return 0.0
        elif parte == Z:
            if error <= arrayDError[2]:
                return 0.0
            elif (error > arrayDError[2] and error < arrayDError[3]):
                return (error - arrayDError[2])/(arrayDError[3] - arrayDError[2])
            elif (error > arrayDError[3]  and error < arrayDError[4]):
                return (arrayDError[4] - error)/(arrayDError[4] - arrayDError[3])
            else:
                return 0.0
        elif parte == N:
            if error <= arrayDError[3]:
                return 0.0
            elif (error > arrayDError[3] and error < arrayDError[4]):
                return (error - arrayDError[3])/(arrayDError[4] - arrayDError[3])
            elif (error >= arrayDError[4] and error <= arrayDError[5]):
                return 1.0
            elif (error > arrayDError[5]  and error < arrayDError[6]):
                return (arrayDError[6] - error)/(arrayDError[6] - arrayDError[5])
            else:
                return 0.0
        elif parte == MN:
            if error <= arrayDError[5]:
                return 1.0
            elif error > arrayDError[6]:
                return 0.0
            else:
                return (error - arrayDError[5])/(arrayDError[6] - arrayDError[5])
        else:
            print "DError"

    def getErrorBorroso(self, error, parte):
        # Funcion de pertenencia de muy a la derecha
        arrayError = self.poblacion[self.ind].funcionError
        if parte == MD:
            if error <= arrayError[0]:
                return 1.0
            elif error > arrayError[1]:
                return 0.0
            else:
                return (arrayError[1] - error)/(arrayError[1] - arrayError[0])
        elif parte == D:
            if error <= arrayError[0]:
                return 0.0
            elif (error > arrayError[0] and error < arrayError[1]):
                return (error - arrayError[0])/(arrayError[1] - arrayError[0])
            elif (error >= arrayError[1] and error <= arrayError[2]):
                return 1.0
            elif (error > arrayError[2]  and error < arrayError[3]):
                return (arrayError[3] - error)/(arrayError[3] - arrayError[2])
            else:
                return 0.0
        elif parte == Z:
            if error <= arrayError[2]:
                return 0.0
            elif (error > arrayError[2] and error < arrayError[3]):
                return (error - arrayError[2])/(arrayError[3] - arrayError[2])
            elif (error > arrayError[3]  and error < arrayError[4]):
                return (arrayError[4] - error)/(arrayError[4] - arrayError[3])
            else:
                return 0.0
        elif parte == I:
            if error <= arrayError[3]:
                return 0.0
            elif (error > arrayError[3] and error < arrayError[4]):
                return (error - arrayError[3])/(arrayError[4] - arrayError[3])
            elif (error >= arrayError[4] and error <= arrayError[5]):
                return 1.0
            elif (error > arrayError[5]  and error < arrayError[6]):
                return (arrayError[6] - error)/(arrayError[6] - arrayError[5])
            else:
                return 0.0
        elif parte == MI:
            if error <= arrayError[5]:
                return 1.0
            elif error > arrayError[6]:
                return 0.0
            else:
                return (error - arrayError[5])/(arrayError[6] - arrayError[5])
        else:
            print "Error"

    # Borrosifica el error y la derivada del error
    def borrosifica(self, e, de):
        self.errorBorrosificado = [self.getErrorBorroso(e,MD), self.getErrorBorroso(e,D), self.getErrorBorroso(e,Z),
                                   self.getErrorBorroso(e,I), self.getErrorBorroso(e,MI)]

        self.derrorBorrosificado = [self.getDErrorBorroso(de,MP), self.getDErrorBorroso(de,P), self.getDErrorBorroso(de,Z),
                                    self.getDErrorBorroso(de,N), self.getDErrorBorroso(de,MN)]

    # Aplicamos las reglas de inferencia en la tabla FAM para desborrosificar
    def desborrosifica(self):
        # Array que contiene el valor y la salida
        reglas =[[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],
				[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],
				[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],
				[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],
				[0, 0],[0, 0],[0, 0],[0, 0],[0, 0]]

        # Inferencia
        count = 0
        for i in range(0,5):
            for j in range(0,5):
                salida = self.FAM[i][j]
                valor = min(self.errorBorrosificado[i], self.derrorBorrosificado[j])
                reglas[count][0] = valor
                reglas[count][1] = salida
                count = count + 1

        # Contribucion de cada cada regla en la salida
        contGMI = 0
        contGI = 0
        contSR = 0
        contGD = 0
        contGMD = 0

        for i in range(0,25):
            tipo = reglas[i][1]
            valor = reglas[i][0]

            if tipo == GMI:
                contGMI = contGMI + valor**2
            elif tipo == GI:
                contGI = contGI + valor**2
            elif tipo == SR:
                contSR = contSR + valor**2
            elif tipo == GD:
                contGD = contGD + valor**2
            else:
                contGMD = contGMD + valor**2

        contGMD = math.sqrt(contGMD)
        contGD = math.sqrt(contGD)
        contSR = math.sqrt(contSR)
        contGI = math.sqrt(contGI)
        contGMI = math.sqrt(contGMI)

        # Centro de gravedad
        self.funcionOut = self.poblacion[self.ind].funcionSalida
        desborrosificacion = ((self.funcionOut[0]+(self.funcionOut[3]-self.funcionOut[0])/2)*contGMI + (self.funcionOut[2]+(self.funcionOut[5]-self.funcionOut[2])/2)*contGI  +  (self.funcionOut[4]+(self.funcionOut[7]-self.funcionOut[4])/2)*contSR  +  (self.funcionOut[6]+(self.funcionOut[9]-self.funcionOut[6])/2)*contGD + (self.funcionOut[8]+(self.funcionOut[11]-self.funcionOut[8])/2)*contGMD)/\
                      (contGMI+contGI+contSR+contGD+contGMD)

        return desborrosificacion


    # movera el robot segun el control borroso que tenga
    def determineMove(self, error, derror):
        self.borrosifica(error,derror)

        leftSpeed = 0.5
        rightSpeed = 0.5
        valor = self.desborrosifica()

        #print "Valor %d" ,(valor)
        if valor < 0:
            leftSpeed = -valor*leftSpeed
        else:
            rightSpeed = valor*rightSpeed
        #print "Motor derecho %d  Motor izquierdo %d" ,rightSpeed, leftSpeed
        self.motors(leftSpeed, rightSpeed)

    def step(self):
        if self.itr == self.MAX_ITR or self.luzEncontrada() == 1:
            self.poblacion[self.ind].calidad = self.setCalidad()
            self.itr = 0
            self.ind = self.ind + 1
            self.posiciona()
            print self.ind
            if self.ind == self.MAX_IND:
                self.ind = 0
                self.gen = self.gen + 1
                self.setElite()
                print self.gen
                if self.gen == self.MAX_GEN:
                    print "Finalizado"
                    done = 1
                else:
                    self.nuevaPoblacion()
        else:
            self.robot.light[0].units = "SCALED"
            ls = max([s.value for s in self.robot.light[0]["left"]])
            rs = max([s.value for s in self.robot.light[0]["right"]])
            self.error = ls - rs
            self.derror = self.errorAnt - self.error
            #print "Iteracion %d, Error %d DError %d", self.itr, self.error,self.derror
            self.determineMove(self.error, self.derror)

            self.errorAnt = self.error
            self.itr = self.itr + 1

def INIT(engine):
    assert (engine.robot.requires("range-sensor")
            and engine.robot.requires("continuous-movement"))
    return Control('Control', engine)