# -*- encoding: utf-8 -*-
from pyrobot.brain import Brain
import random
import math

class Individuo:
    def __init__(self, IndId):
        # Variables
        self.id = IndId  # Identificador para diferenciar individuos
        self.calidad = 0  # Calidad del individuo
        self.genes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # Array con la funcion de pertenencia. Los 3 primeros valores son el error,
        # los 3 siguientes la derivada del error y los 6 restantes la salida
        self.generarGenes()
        self.probabilidad = 0  # Probabilidad de ser elegido para la próxima generación
        #Inicializamios las funciones
        self.funcionError = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.funcionDError = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.funcionSalida = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.generarFunciones()

    # Devuelve los genes del individuo, generados aleatoriamente.
    def generarGenes(self):
        # Error
        aux = [random.random() for col in range(3)]
        aux.sort()  # a < b < c
        self.genes[0] = aux[0]
        self.genes[1] = aux[1]
        self.genes[2] = aux[2]

        # Derivada del error
        aux = [random.random() for col in range(3)]
        aux.sort()  # d < e < f
        self.genes[3] = aux[0]
        self.genes[4] = aux[1]
        self.genes[5] = aux[2]

        # Salida
        aux = [random.random() for col in range(6)]
        aux.sort()  # g < h < i < j < k < l
        self.genes[6] = aux[0]
        self.genes[7] = aux[1]
        self.genes[8] = aux[2]
        self.genes[9] = aux[3]
        self.genes[10] = aux[4]
        self.genes[11] = aux[5]

    # Usando los genes, crea las funciones del error, derivada de error y salida.
    def generarFunciones(self):
        # Error
        self.funcionError[0] = -self.genes[2]
        self.funcionError[1] = -self.genes[1]
        self.funcionError[2] = -self.genes[0]
        self.funcionError[3] = 0  # Eje de simetria de la funcion, siempre 0
        self.funcionError[4] = self.genes[0]
        self.funcionError[5] = self.genes[1]
        self.funcionError[6] = self.genes[2]

        # Derivada del error
        self.funcionDError[0] = -self.genes[5]
        self.funcionDError[1] = -self.genes[4]
        self.funcionDError[2] = -self.genes[3]
        self.funcionDError[3] = 0  # Eje de simetria de la funcion, siempre 0
        self.funcionDError[4] = self.genes[3]
        self.funcionDError[5] = self.genes[4]
        self.funcionDError[6] = self.genes[5]

        # Salida
        self.funcionSalida[0] = -self.genes[11]
        self.funcionSalida[1] = -self.genes[10]
        self.funcionSalida[2] = -self.genes[9]
        self.funcionSalida[3] = -self.genes[8]
        self.funcionSalida[4] = -self.genes[7]
        self.funcionSalida[5] = -self.genes[6]
        self.funcionSalida[6] = self.genes[6]
        self.funcionSalida[7] = self.genes[7]
        self.funcionSalida[8] = self.genes[8]
        self.funcionSalida[9] = self.genes[9]
        self.funcionSalida[10] = self.genes[10]
        self.funcionSalida[11] = self.genes[11]

    # funcion para mutar aleatoriamente un numero aleatorio de genes
    def mutar(self):
        for i in range(len(self.genes)):
            newGen = self.genes[i] + random.gauss(0, 1)  # Ahora el gen puede ser negativo, hay que tenerlo en cuenta, no nos interesa
        genPost = 0
        genAnt = 0
        if i < len(self.genes) - 1:
            genPost = self.genes[i +1]
        if i > 0:
            genAnt = self.genes[i-1]

        # Verificamos que sigue siendo una funcion de pertenencia borrosa
        if (i == 0 or i == 3 or i == 6):  # Primeras posiciones de cada "bloque" (Error, Derivada, Salida)
            if (newGen > genPost or newGen < 0):
                newGen = genPost/2  # Asi nos aseguramos que siempre sera menor.
        elif (i == 2 or i == 5 or i == 11):  # Ultimas posiciones de cada "bloque"
            if (newGen < genAnt):
                newGen = genAnt + (self.genes[i] - genAnt)/2 # Nos aseguramos que sea mayor
        else:
            if (newGen > genPost or newGen < genAnt):  # Posiciones intermedias de cada "bloque"
                newGen = genAnt + (genPost - genAnt)/2 # Aseguramos que el valor este entre medias.

        self.genes[i] = newGen
        self.generarFunciones(self)

# Tipos de errores, de muy negativo a muy positivo
MD = 0	# Muy Derecha
D = 1	# Derecha
Z = 2	# Cero
I = 3	# Izquierda
MI = 4	# Muy Izquierda

# Tipos de derivadas de errores, de muy negativa a muy positivas
MP = 0  # DError Muy Positiva
P = 1	# DError Positiva
Z = 2	# DError cero
N = 3	# DError Negativa
MN = 4  # DError Muy Negativa

# Tipos de salidas, de girar mucho a la derecha a girar mucho a la izquierda
GMD = 0  # Girar mucho a la derecha
GD = 1  # Girar a la derecha
SR = 2  # Seguir recto
GI = 3  # Girar a la izquierda
GMI = 4  # Girar mucho a la izquierda

class Control(Brain):

    def setup(self):
        # Constantes
        self.MAX_GEN = 100
        self.MAX_ITR = 200
        self.MAX_IND = 10
        self.POSICIONES = [[12.75746, 4.69842, 190.0714], [5.18442, 9.84676, 274.06364], [3.30373, 0.303278, 167.53044], [1.75536, 5.111311, 305.59911]]  # Array de posiciones aleatorias
        self.FAM = [[SR, GD, GMI, GI,  GMI],
                    [GD,  GD,  GI,  SR,  GI ],
                    [GMD, GD,  SR,  GI,  GMI ],
                    [GD,  GD,  GD,  GI,  GI],
                    [GMD,  GMD, GMD, SR,  SR ]]
        self.errorBorrosificado = range(0, 5) # Error borrosificado
        self.dErrorBorrosificado = range(0, 5) # Derivada del error desborrosificadas
        # Variables
        self.iteracion = 0  # Número de steps que lleva el robot
        self.generacion = 0  # Generación actual
        self.individuo = 0  # Individuo actual
        self.done = False # Variable que indica cuando se ha terminado con el programa
        self.poblacion = range(0, self.MAX_IND) # Array con los individuos de la población actual
        self.probTotal = 0
        self.error = 0
        self.errorAnt = 0
        self.derror = 0
        self.mejorIndividuo = Individuo(-1)
        self.ficheroSalida = open("Salida.txt" , "w")
        self.initPoblacion()
        self.posiciona()

    # Inicializa la primera poblacion
    def initPoblacion(self):
        # Inicializamos la primera población
        for i in range(self.MAX_IND):
            self.poblacion[i] = Individuo(i)
            self.poblacion[i].calidad = 1
            self.probTotal = self.probTotal + self.poblacion[i].calidad

            # Elitismo
            if (i == 0):
                self.mejorIndividuo = self.poblacion[i]
            elif (self.mejorIndividuo.calidad < self.poblacion[i].calidad):
                self.mejorIndividuo = self.poblacion[i]

        # Asignamos la probabilidad que tiene de ser elegido cuando se vaya a mutar.
        for i in range(self.MAX_IND):
            self.poblacion[i].probabilidad = float((self.poblacion[i].calidad) / float(self.probTotal))

    # Crea una nueva poblacion de individuos mutandolos.
    def nuevaPoblacion(self):
        # El primer individuo el mejor de la generacion anterior
        nuevapoblacion = range(0, self.MAX_IND)
        nuevapoblacion[0] = self.mejorIndividuo

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
                   break
            print pos

            newIndividuo = self.poblacion[pos]
            newIndividuo.id = tablaProb[pos][0]
            newIndividuo.mutar()

            nuevapoblacion[i] = newIndividuo
        self.poblacion = nuevapoblacion

    # Posiciona al robot en una posicion aleatoria de entre 4 recolectadas.
    def posiciona(self):
        r = (int(random.uniform(0,3)))
        self.robot.simulation[0].setPose(0, self.POSICIONES[r][0],self.POSICIONES[r][1],self.POSICIONES[r][2])

    # Devuelve True si el robot ha encontrado la luz, False en caso contrario
    def luzEncontrada(self,ls, rs):
        if ls > 0.25 or rs > 0.25:
            return True
        return False

    # Asigna Probabilidad a los individuos
    def setProb(self):
    	self.probTotal = 0
    	for i in range(0, self.MAX_IND):
    		self.probTotal = self.probTotal + self.poblacion[i].calidad

    	print self.probTotal

    	for i in range(0, self.MAX_IND):
    		self.poblacion[i].probabilidad = float((self.poblacion[i].calidad) / float(self.probTotal))

    # Asigna un elite en la poblacion
    def setElite(self):
        for i in range(0, self.MAX_IND):
            if (self.poblacion[i].calidad > self.mejorIndividuo.calidad):
                self.mejorIndividuo = self.poblacion[i]

    def getDErrorBorroso(self, error, parte):
        # Funcion de pertenencia de muy a la derecha
        arrayDError = self.poblacion[self.individuo].funcionDError
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
        arrayError = self.poblacion[self.individuo].funcionError
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

        self.dErrorBorrosificado = [self.getDErrorBorroso(de,MP), self.getDErrorBorroso(de,P), self.getDErrorBorroso(de,Z),
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
                valor = min(self.errorBorrosificado[i], self.dErrorBorrosificado[j])
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
        
        denom = 0
        if (contGMI+contGI+contSR+contGD+contGMD) == 0:
        	denom = 0.0001
        else:
        	denom = (contGMI+contGI+contSR+contGD+contGMD)

        # Centro de gravedad
        self.funcionOut = self.poblacion[self.individuo].funcionSalida
        desborrosificacion = ((self.funcionOut[0]+(self.funcionOut[3]-self.funcionOut[0])/2)*contGMI + (self.funcionOut[2]+(self.funcionOut[5]-self.funcionOut[2])/2)*contGI  +  (self.funcionOut[4]+(self.funcionOut[7]-self.funcionOut[4])/2)*contSR  +  (self.funcionOut[6]+(self.funcionOut[9]-self.funcionOut[6])/2)*contGD + (self.funcionOut[8]+(self.funcionOut[11]-self.funcionOut[8])/2)*contGMD)/\
                      (denom)
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
        if self.done:
            self.ficheroSalida.flush()
            self.ficheroSalida.close()
            self.stop()
            return;
        self.robot.light[0].units = "SCALED"
        ls = max([s.value for s in self.robot.light[0]["left"]])
        rs = max([s.value for s in self.robot.light[0]["right"]])
        if self.iteracion == self.MAX_ITR or self.luzEncontrada(ls, rs):
            self.poblacion[self.individuo].calidad = float(self.MAX_ITR / float(self.iteracion))
            self.iteracion = 0
            self.individuo = self.individuo + 1
            self.posiciona()
            print self.individuo
            if self.individuo == self.MAX_IND:
                self.individuo = 0
                self.generacion = self.generacion + 1
                self.setElite()
                self.setProb()
                self.ficheroSalida.write("Generacion: " + str(self.generacion) + " : \n" + "Calidad : " + str(self.mejorIndividuo.calidad) + "\n"
                                        + "Individuo: \n" + str(self.mejorIndividuo.controlBorroso) + "\n")
                self.ficheroSalida.flush()
                print self.generacion
                if self.generacion == self.MAX_GEN:
                    print "Finalizado"
                    self.done = True
                else:
                    self.nuevaPoblacion()
        else:            
            self.error = ls - rs
            self.derror = self.errorAnt - self.error
            #print "Iteracion %d, Error %d DError %d", self.itr, self.error,self.derror
            self.determineMove(self.error, self.derror)

            self.errorAnt = self.error
            self.iteracion = self.iteracion + 1

def INIT(engine):
    assert (engine.robot.requires("range-sensor")
            and engine.robot.requires("continuous-movement"))
    return Control('Control', engine)
