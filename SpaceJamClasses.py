from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from CollideObjectBase import *
from direct.gui.OnscreenImage import OnscreenImage

class Universe(InverseSphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Universe, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.9)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        
        self.modelNode.setTexture(tex, 1)
        
class Station(CapsuleCollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Station, self).__init__(loader, modelPath, parentNode, nodeName, 1, -1, 5, 1, -1, -5, 10)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        
class Missile(SphereCollideObject):
    fireModels = {}
    cNodes = {}
    collisionSolids = {}
    Intervals = {}
    missileCount = 0
    
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float = 1.0):
        super().__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.0)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setPos(posVec)
        
        Missile.missileCount += 1
        Missile.fireModels[nodeName] = self.modelNode
        Missile.cNodes[nodeName] = self.collisionNode
        Missile.collisionSolids[nodeName] = self.collisionNode.node().getSolid(0)
        Missile.cNodes[nodeName].show()
        print("Fire torpedo #"+ str(Missile.missileCount))
    
class Planet(SphereCollideObject, ShowBase):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super().__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1.5)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        
class Drone(SphereCollideObject, ShowBase):
    # Number of drones spawned
    droneCount = 0
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super().__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3)
        
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        
        self.planetNode = planetNode
        self.orbitRadius = orbitRadius
        self.orbitSpeed = orbitSpeed
        self.angle = random.random() * 2 * math.pi  # random starting position

        # Optional vertical bobbing
        self.bobHeight = random.uniform(20, 50)
        self.bobSpeed = random.uniform(1, 3)
        
        # Add task to update orbit
        taskMgr.add(self.UpdateOrbit, nodeName + "_orbit")

    def UpdateOrbit(self, task):
        if self.planetNode is None:
            return task.done
        
        # Update angle
        self.angle += globalClock.getDt() * self.orbitSpeed
        
        # Center position
        cx, cy, cz = self.planetNode.getPos()
        
        # Circular orbit
        x = cx + self.orbitRadius * math.cos(self.angle)
        y = cy + self.orbitRadius * math.sin(self.angle)
        
        # Vertical bobbing
        z = cz + self.bobHeight * math.sin(self.angle * self.bobSpeed)
        
        self.modelNode.setPos(x, y, z)
        self.modelNode.lookAt(self.planetNode)  # optional: drone faces the planet
        
        return task.cont