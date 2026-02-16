# Creacion de la escena:

from yade import qt
yade.qt.Renderer()
qt.View()

# Creacion del material del que estara hecho el objeto:

matId = O.materials.append(FrictMat())

# Importar un mesh:

from yade import ymport
id_HouGL = O.bodies.append(ymport.gmsh("hourglass.mesh", scale = 1000.0, color = (0, 0, 1)))