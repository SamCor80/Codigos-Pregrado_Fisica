# Creacion de la escena:

from yade import qt
yade.qt.Renderer()
qt.View()

# Creacion del material del que estara hecho el objeto:

matId = O.materials.append(FrictMat())

# Creacion de la caja:

O.bodies.append(geom.facetBox((.5, .5, .5), (.5, .5, .5), wallMask=31))

# Creacion de una distribucion uniforme de esferas:

from yade import pack
sp = pack.SpherePack()

sp.makeCloud((0, 0, 0.5), (1, 1, 1.5), rMean=0.05, rRelFuzz=0.5, seed=2)
sp.toSimulation()

# Creacion del motor (movimiento):

O.engines = [
	ForceResetter(),
	InsertionSortCollider([Bo1_Sphere_Aabb(), Bo1_Facet_Aabb()]),
	InteractionLoop(
		[Ig2_Sphere_Sphere_ScGeom(), Ig2_Facet_Sphere_ScGeom()],
		[Ip2_FrictMat_FrictMat_MindlinPhys()],
		[Law2_ScGeom_MindlinPhys_Mindlin()],
	),
	NewtonIntegrator(damping=0, gravity=[0, 0, -10.0]),
]

# Paso del tiempo (2.5071888534866675e-06): 

O.dt = 0.1 * PWaveTimeStep()

# Plot Energia:

O.trackEnergy = True

from yade import plot
plot.plots = {'i': ('total', 'potential', 'kinetic')}
plot.plot()

def addData():
	plot.addData(
		i = O.iter,
		total = O.energy.total(),
		potential = O.energy['gravWork'],
		kinetic = O.energy['kinetic']
	)
O.engines += [PyRunner(command = 'addData()', iterPeriod = 50)]

# Reiniciar la simulacion:

O.saveTmp()
