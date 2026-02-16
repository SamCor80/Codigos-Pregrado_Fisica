# Creacion de la escena:

from yade import qt
yade.qt.Renderer()
qt.View()

# Creacion de los materiales:

matId_hourglass = O.materials.append(FrictMat(young=70e9, poisson=0.20, density=2230, label = 'hourglassMat'))
matId_sand = O.materials.append(FrictMat(young=60e9, poisson=0.30, density=2634, label = 'sandMat'))


# Importar un mesh:

from yade import ymport
id_HouGL = O.bodies.append(ymport.gmsh("hourglass-P6.mesh", color = (0, 0, 1)))


def read_x_y_z_r_intoList(fileName, shift = Vector3.Zero, scale = 1.0):
	infile = open(fileName, 'r')
	lines = infile.readlines()
	infile.close()
	c1_list = []
	for line in lines:
		data = line.split(',')
		if (data[0][0] == '#'):
			continue
		else:
			pos = Vector3(float(data[0]), float(data[1]), float(data[2]))
			c1_list.append(( shift + scale*pos, scale*float(data[3]) ))
	return c1_list

# Crear una tapa:

wall = utils.wall((0,0,0), 2, material=matId_hourglass)
O.bodies.append(wall)

# Creacion de una distribucion uniforme de granos de silica:

from yade import pack
sp = pack.SpherePack()

sp.makeCloud((-0.0919, -0.0919, 0.2), (0.0919, 0.0919, 0.3), rMean=0.0055, seed=2, num=400)
sp.toSimulation()

# Creacion del motor (movimiento):

O.engines = [
	ForceResetter(),
	InsertionSortCollider([Bo1_Sphere_Aabb(), Bo1_Facet_Aabb(), Bo1_Wall_Aabb()]),
	InteractionLoop(
		[Ig2_Sphere_Sphere_ScGeom(), Ig2_Facet_Sphere_ScGeom(), Ig2_Wall_Sphere_ScGeom()],
		[Ip2_FrictMat_FrictMat_MindlinPhys(en = 0.93)],
		[Law2_ScGeom_MindlinPhys_Mindlin()],
	),
	NewtonIntegrator(damping=0, gravity=[0, 0, -10.0], exactAsphericalRot=True),
]

O.dt = 0.1 * PWaveTimeStep()