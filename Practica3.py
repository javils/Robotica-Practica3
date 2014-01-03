__author__ = 'SergioMac'

from pyrobot.brain import Brain
import random

kMax_steps = 1000
kMax_individuos = 10
kMax_generaciones = 100
individuo = 0
gen = 0
poblacion = []
valoracionPoblacion = []

class Practica3(Brain):


  def setup(self):
      done = 0
      iter = 0
      poblacion = self.genera_primera_poblacion()
      self.coloca_individuo(individuo)

  def step(self):
      if iter == kMax_steps or luz_alcanzada:
          self.asigna_calidad_individuo(individuo, iter)
          individuo = individuo + 1
          if individuo == kMax_individuos:
              individuo = 0
              gen = gen + 1
              if gen == kMax_generaciones:
                  done = 1
              else:
                  self.generar_nueva_poblacion
          self.coloca_individuo(individuo)
          iter = 0
      else:
          t,r = determineMove(individuo)
          self.robot.move(t,r)
          iter = iter + 1

  def genera_primera_poblacion(self):
    array = []
    genes = {"ErrorA":0,"ErrorB":0,"ErrorC":0,"ErrorD":0,"DerErrorA":0,"DerErrorB":0,"DerErrorC":0,"DerErrorD":0,"Salida1":0,"Salida2":0,"Salida3":0,"Salida4":0,"Salida5":0,"Salida6":0}

    for i in 0..kMax_Individuos:
        genes["ErrorA"] = random.random
        genes["ErrorB"] = genes["ErrorA"] + random.random
        genes["ErrorC"] = genes["ErrorB"] + random.random
        genes["ErrorD"] = genes["ErrorC"] + random.random

        genes["DerErrorA"] = random.random
        genes["DerErrorB"] = genes["DerErrorA"] + random.random
        genes["DerErrorC"] = genes["DerErrorB"] + random.random
        genes["DerErrorD"] = genes["DerErrorC"] + random.random

        genes["Salida1"] = random.random
        genes["Salida2"] = genes["Salida1"] + random.random
        genes["Salida3"] = genes["Salida2"] + random.random
        genes["Salida4"] = genes["Salida3"] + random.random
        genes["Salida5"] = genes["Salida4"] + random.random
        genes["Salida6"] = genes["Salida5"] + random.random

        array[i] = genes

    return array


def asigna_calidad_individuo(self,individuo,iter):
    if iter == kMax_steps:
        valoracionPoblacion[individuo] = 0
    else:
        valoracionPoblacion[individuo] = 1 / iter


def genera_nueva_poblacion(self):
    individuo = mejorIndividuo()

    array = []
    genes = {"ErrorA":0,"ErrorB":0,"ErrorC":0,"ErrorD":0,"DerErrorA":0,"DerErrorB":0,"DerErrorC":0,"DerErrorD":0,"Salida1":0,"Salida2":0,"Salida3":0,"Salida4":0,"Salida5":0,"Salida6":0}

    for i in 0..kMax_Individuos:

        #Falta comprobar si el valor es valido

        genes["ErrorA"] = poblacion[individuo]["ErrorA"] + random.gauss(0,1)
        genes["ErrorB"] = poblacion[individuo]["ErrorB"] + random.gauss(0,1)
        genes["ErrorC"] = poblacion[individuo]["ErrorC"] + random.gauss(0,1)
        genes["ErrorD"] = poblacion[individuo]["ErrorD"] + random.gauss(0,1)

        genes["DerErrorA"] = poblacion[individuo]["DerErrorA"] + random.gauss(0,1)
        genes["DerErrorB"] = poblacion[individuo]["DerErrorB"] + random.gauss(0,1)
        genes["DerErrorC"] = poblacion[individuo]["DerErrorC"] + random.gauss(0,1)
        genes["DerErrorD"] = poblacion[individuo]["DerErrorD"] + random.gauss(0,1)

        genes["Salida1"] = random.random
        genes["Salida2"] = genes["Salida1"] + random.random
        genes["Salida3"] = genes["Salida2"] + random.random
        genes["Salida4"] = genes["Salida3"] + random.random
        genes["Salida5"] = genes["Salida4"] + random.random
        genes["Salida6"] = genes["Salida5"] + random.random

        array[i] = genes

    return array


def INIT(engine):
   assert (engine.robot.requires("range-sensor") and
           engine.robot.requires("continuous-movement"))
   return Practica3('Practica3', engine)
