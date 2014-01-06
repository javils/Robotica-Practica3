from pyrobot.brain import Brain
import random

class Individuo :
  def __init__(self, IndId):
    # Constantes
    self.CONTROL_BORROSO_SIZE = 12 # tamaño del array controlBorroso
    # Variables
    self.id = IndId #Id para diferenciar un individuo de otro
    self.calidad = 0 # calidad del individuo
    self.controlBorroso = initControlBorroso() # array con la funcion de pertenencia [X,X,X,Y,Y,Y,Z,Z,Z,Z,Z,Z] X = Error Y = D.Error Z = Salida
    self.probabilidad = 0 #probabilidad de ser elegido en la mutación

  def initControlBorroso(self):
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


class Control(Brain):
  
  def __init__(self):

    # Constantes
    self.MAX_GEN = 100
    self.MAX_ITR = 1500
    self.MAX_IND = 20

    # Variables
    self.itr = 0; #numero de iteraciones que ha relizado el robot hasta ahora
    self.gen = 0; #generacion en la que estamos
    self.ind = 0; #individuo en el que estamos
    self.poblacion = range(0, MAX_IND)
    self.elite = Individuo(-1)
    probTotal = 0

    # Inicializamos la primera población
    for i in range MAX_IND:
      self.poblacion[i] = Individuo(i)
      self.poblacion[i].calidad = self.setCalidad(1) # Para que no crashe por dividir entre 0 mas adelante
      probTotal = probTotal + self.poblacion[i].calidad

      # Elitismo
      if (i == 0):
        self.elite = self.poblacion[i]
      elif (self.elite.calidad < self.poblacion[i].calidad)
        self.elite = self.poblacion[i]

    # Asignamos la probabilidad que tiene de ser elegido cuando se vaya a mutar.
    for i in range MAX_IND:
      self.poblacion[i].probabilidad = float((self.poblacion[i].calidad)/probTotal)

  def setup(self):
      

  def step(self):
      

  
  def INIT(engine):
    assert (engine.robot.requires("range-sensor") and
           engine.robot.requires("continuous-movement"))
    return Practica3('Practica3', engine)
