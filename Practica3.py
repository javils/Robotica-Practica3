# -*- encoding: utf-8 -*-
from pyrobot.brain import Brain
import random

class Individuo:
  def __init__(self, padre):
    # Constantes
    self.CONTROL_BORROSO_SIZE = 12 # tamaño del array controlBorroso
    # Variables
    self.calidad = 0 # calidad del individuo
    self.controlBorroso = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self.initControlBorroso(padre) # array con la funcion de pertenencia [X,X,X,Y,Y,Y,Z,Z,Z,Z,Z,Z] X = Error Y = D.Error Z = Salida
    self.probabilidad = 0 #probabilidad de ser elegido en la mutación

  def initControlBorroso(self, padre):
    if padre is None: #La primera población, sin padre
        # Error
        aux = [random.random() for col in range(3)]
        aux.sort() # ordenamos para que los puntos de corte de la funcion de pertenencia esten ordenados
        self.controlBorroso[0] = aux[0]
        self.controlBorroso[1] = aux[1]
        self.controlBorroso[2] = aux[2]

        # Derivada del error
        aux = [random.random() for col in range(3)]
        aux.sort() # ordenamos para que los puntos de corte de la funcion de pertenencia esten ordenados
        self.controlBorroso[3] = aux[0]
        self.controlBorroso[4] = aux[1]
        self.controlBorroso[5] = aux[2]

        # Salida
        aux = [random.random() for col in range(6)]
        aux.sort() # ordenamos para que los puntos de corte de la funcion de pertenencia esten ordenados
        self.controlBorroso[6] = aux[0]
        self.controlBorroso[7] = aux[1]
        self.controlBorroso[8] = aux[2]
        self.controlBorroso[9] = aux[3]
        self.controlBorroso[10] = aux[4]
        self.controlBorroso[11] = aux[5]
    else: #Las poblaciones descendientes de otras
        # Error
        aux = [random.gauss(0,1) for col in range(3)]
        aux.sort() # ordenamos para que los puntos de corte de la funcion de pertenencia esten ordenados
        self.controlBorroso[0] = aux[0] + padre.controlBorroso[0]
        self.controlBorroso[1] = aux[1] + padre.controlBorroso[1]
        self.controlBorroso[2] = aux[2] + padre.controlBorroso[2]

        # Derivada del error
        aux = [random.gauss(0,1) for col in range(3)]
        aux.sort() # ordenamos para que los puntos de corte de la funcion de pertenencia esten ordenados
        self.controlBorroso[3] = aux[0] + padre.controlBorroso[3]
        self.controlBorroso[4] = aux[1] + padre.controlBorroso[4]
        self.controlBorroso[5] = aux[2] + padre.controlBorroso[5]

        # Salida
        aux = [random.gauss(0,1) for col in range(6)]
        aux.sort() # ordenamos para que los puntos de corte de la funcion de pertenencia esten ordenados
        self.controlBorroso[6] = aux[0] + padre.controlBorroso[6]
        self.controlBorroso[7] = aux[1] + padre.controlBorroso[7]
        self.controlBorroso[8] = aux[2] + padre.controlBorroso[8]
        self.controlBorroso[9] = aux[3] + padre.controlBorroso[9]
        self.controlBorroso[10] = aux[4] + padre.controlBorroso[10]
        self.controlBorroso[11] = aux[5] + padre.controlBorroso[11]


class Control(Brain):

  def setup(self):
    # Constantes
    self.MAX_GEN = 100
    self.MAX_ITR = 1500
    self.MAX_IND = 20

    # Variables
    self.itr = 0 #numero de iteraciones que ha relizado el robot hasta ahora
    self.gen = 0 #generacion en la que estamos
    self.ind = 0 #individuo en el que estamos
    self.poblacion = range(0, self.MAX_IND)

    self.generarPoblacion(esPrimeraGeneracion=True)


  def step(self):
      if self.itr == self.MAX_ITR or luz_alcanzada:
          self.setCalidad(self.poblacion[self.ind], self.itr)
          self.ind = self.ind + 1
          if self.ind == self.MAX_IND:
              self.ind = 0
              self.gen = self.gen + 1
              if self.gen == self.MAX_GEN:
                  done = 1
              else:
                  self.generarPoblacion(esPrimeraGeneracion=False)
          self.colocarIndividuo(self.ind)
          self.itr = 0
      else:
          t,r = determineMove(self.poblacion[self.ind])
          self.robot.move(t,r)
          self.itr = self.itr + 1


  def generarPoblacion(self, esPrimeraGeneracion):
      if esPrimeraGeneracion:
          for i in range(self.MAX_IND):
            self.poblacion[i] = Individuo(None)
          self.mejorIndividuo = self.poblacion[0] # Temporalmente, se coloca el mejor individuo como el primero
      else:
          self.poblacion[0] = self.mejorIndividuo # Se guarda el mejor de todos los individuos para la siguiente generación
          for i in range(1, self.MAX_IND):
            individuoAleatorio = random.uniform(0, self.MAX_IND) # Devuelve un individuo aleatorio del array, que será uno de los que se mutara para la siguiente generación
            self.poblacion[i] = Individuo(i, self.poblacion[individuoAleatorio])

# Asigna calidad a un individuo
  def setCalidad(self, individuoActual, iteracion):
    individuoActual.calidad =  1/iteracion
    if individuoActual.calidad > self.mejorIndividuo.calidad:
        self.mejorIndividuo = individuoActual.calidad


def INIT(engine):
    assert (engine.robot.requires("range-sensor")
			and engine.robot.requires("continuous-movement"))
    return Control('Control', engine)