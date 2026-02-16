# Creacion de la escena:

from yade import qt
yade.qt.Renderer()
qt.View()

# Creacion del material del que estara hecho el objeto:

matId = O.materials.append(FrictMat())

# Creacion del objeto (esfera):

O.bodies.append(utils.sphere(Vector3(0,0,5), 1.0, material=matId))

#Creacion de una pared:

wall = utils.wall((0,0,0), 2, material=matId)
O.bodies.append(wall)

# Creacion del motor (movimiento):

O.engines = [
	ForceResetter(),
	InsertionSortCollider([Bo1_Sphere_Aabb(), Bo1_Wall_Aabb()]),
	InteractionLoop(
		[Ig2_Sphere_Sphere_ScGeom(), Ig2_Wall_Sphere_ScGeom()],
		[Ip2_FrictMat_FrictMat_MindlinPhys()],
		[Law2_ScGeom_MindlinPhys_Mindlin()],
	),
	NewtonIntegrator(damping=0, gravity=[0, 0, -10.0]),
]

# Paso del tiempo:

O.dt = 1e-6