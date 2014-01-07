from pyrobot.simulators.pysim import *
import time

def INIT():
	
	# (width, height), (offset x, offset y), scale:
	sim = TkSimulator((600, 600), (50, 550), 100)
	
	# foco de luz
	sim.addLight(4.75, 3.75, 0.35)
	#en la simulacion grafica cambiar Pioneer por TkPioneer
	sim.addRobot(60000, TkPioneer("RedPioneer",  
					.5, 2.5, 0.00,
					((.225, .225, -.225, -.225),
					(.175, -.175, -.175, .175))))
	# sensores de luz para buscar la puerta
	sim.robots[0].addDevice(PioneerFrontLightSensors())
	
	#sensores de proximidad para evitar obstaculos
	sim.robots[0].addDevice(PioneerFrontSonars())
		
	return sim 


