from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from CollideObjectBase import *
from direct.gui.OnscreenImage import OnscreenImage
from SpaceJamClasses import *
from direct.task import Task

from panda3d.core import CollisionHandlerEvent
from direct.interval.LerpInterval import LerpFunc
from direct.particles.ParticleEffect import ParticleEffect

# Regex module import for string editing
import re

class Ship(SphereCollideObject, ShowBase):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super().__init__(loader, modelPath, parentNode, nodeName, Vec3(.3, 0, 0), 1.3)
        self.loader = loader
        self.taskManager = taskMgr # type: ignore
        self.render = parentNode  
        self.SetKeyBindings()      
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        
        self.EnableHUD()
        self.reloadTime = .25
        self.missileDistance = 4000
        self.missileBay = 1
        self.SetParticles()
        
        self.taskManager.add(self.CheckIntervals, 'checkMissiles', 34)
        
        self.cntExplode = 0
        self.explodeIntervals = {}
        self.traverser = CollisionTraverser()
        self.handler = CollisionHandlerEvent()
        
        self.handler.addInPattern('into')
        self.accept('into', self.HandleInto)
        
    def SetKeyBindings(self):
        self.accept('space', self.Thrust, [1])
        self.accept('space-up', self.Thrust, [0])
        self.accept('a', self.LeftTurn, [1])
        self.accept('a-up', self.LeftTurn, [0])
        self.accept('d', self.RightTurn, [1])
        self.accept('d-up', self.RightTurn, [0])        
        self.accept('w', self.UpTurn, [1])
        self.accept('w-up', self.UpTurn, [0])
        self.accept('s', self.DownTurn, [1])
        self.accept('s-up', self.DownTurn, [0])
        self.accept('q', self.RollLeft, [1])
        self.accept('q-up', self.RollLeft, [0])
        self.accept('e', self.RollRight, [1])
        self.accept('e-up', self.RollRight, [0])
        self.accept('f', self.Fire, [1])
        self.accept('f-up', self.Fire, [0])
        
    def Thrust(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyThrust, 'forward-thrust')
            self.thrustSound = self.loader.loadSfx('./Assets/Audio/thrust.mp3')
            self.thrustSound.setLoop(True)
            self.thrustSound.setVolume(0.6)
            self.thrustSound.play()
        else:
            self.taskManager.remove('forward-thrust')
            self.thrustSound.stop()
                    
    def ApplyThrust(self, task):
        rate = 7
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()
        
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)

        return Task.cont

    def LeftTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyLeftTurn, 'a')
            
        else:
            self.taskManager.remove('a')
    
    def ApplyLeftTurn(self, task):
        rate = 1
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont
           
    def RightTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRightTurn, 'd')
            
        else:
            self.taskManager.remove('d')
    
    def ApplyRightTurn(self, task):
        rate = 1
        self.modelNode.setH(self.modelNode.getH() - rate)
        return Task.cont
    
    def UpTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyUpTurn, 'w')
            
        else:
            self.taskManager.remove('w')
    
    def ApplyUpTurn(self, task):
        rate = 1
        self.modelNode.setP(self.modelNode.getP() + rate)
        return Task.cont

    def DownTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyDownTurn, 's')
            
        else:
            self.taskManager.remove('s')
    
    def ApplyDownTurn(self, task):
        rate = 1
        self.modelNode.setP(self.modelNode.getP() - rate)
        return Task.cont
    
    def RollLeft(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRollLeft, 'q')
            
        else:
            self.taskManager.remove('q')
    
    def ApplyRollLeft(self, task):
        rate = 1
        self.modelNode.setR(self.modelNode.getR() + rate)
        return Task.cont
    
    def RollRight(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRollRight, 'e')
            
        else:
            self.taskManager.remove('e')
    
    def ApplyRollRight(self, task):
        rate = 1
        self.modelNode.setR(self.modelNode.getR() - rate)
        return Task.cont

    def EnableHUD(self):
        self.Hud = OnscreenImage(image = "./Assets/Hud/Reticle3b.png", pos = Vec3(0, 0, 0), scale = 0.1)
        self.Hud.setTransparency(TransparencyAttrib.MAlpha)
        
    def Fire(self, keyDown):
        if not keyDown:
            return
        
        if self.missileBay:
            travRate = self.missileDistance
            self.fireSound = self.loader.loadSfx('./Assets/Audio/fire.mp3')
            self.fireSound.setVolume(0.4)
            self.fireSound.play()
        else:
            if not self.taskManager.hasTaskNamed('reload'):
                print('Initialzing reload...')
                self.taskManager.doMethodLater(0, self.Reload, 'reload')
                return Task.cont
    
        aim = self.render.getRelativeVector(self.modelNode, Vec3.forward())
        aim.normalize()    
        
        fireSolution = aim * travRate
        inFront = aim * 150
        
        travVec = fireSolution + self.modelNode.getPos()
        self.missileBay -= 1
        tag = 'Missile' + str(Missile.missileCount)
        
        posVec = self.modelNode.getPos() + inFront
        currentMissile = Missile(self.loader, './Assets/Phaser/phaser.egg', self.render, tag, posVec, 4.0)
        self.traverser.addCollider(currentMissile.collisionNode, self.handler)
        
        Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
        Missile.Intervals[tag].start()

    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 1
            print("Reload complete.")

        if self.missileBay > 1:
            self.missileBay = 1
            return Task.done
        
        elif task.time <= self.reloadTime:
            print("Reload proceeding...")
            return Task.cont
        
    def CheckIntervals(self, task):
        self.traverser.traverse(self.render)
        
        for i in list(Missile.Intervals):
            if not Missile.Intervals[i].isPlaying():
                Missile.cNodes[i].detachNode()
                Missile.fireModels[i].detachNode()
            
                print(i + 'has reached the end of its fire solution')
                del Missile.Intervals[i]
                del Missile.fireModels[i]
                del Missile.cNodes[i]
                del Missile.collisionSolids[i]
                
                break
    

        return Task.cont
        
    def HandleInto(self, entry):
        fromNode = entry.getFromNodePath().getName()
        print("fromNode: " + fromNode)
        intoNode = entry.getIntoNodePath().getName()
        print("intoNode: " + intoNode)
        
        intoPosition = Vec3(entry.getSurfacePoint(self.render))
        
        tempVar = fromNode.split('_')
        print("tempVar: " + str(tempVar))
        shooter = tempVar[0]
        print("Shooter" + str(shooter))
        tempVar = intoNode.split('_')
        print("TempVar1: "+ str(tempVar))
        tempVar = intoNode.split('_')
        print("TempVar2: "+ str(tempVar))
        victim = tempVar[0]
        print("Victim: " + str(victim))
        
        pattern = r'[0-9]'
        strippedString = re.sub(pattern, '', victim)
        
        """if (strippedString == "Drone" or strippedString == "Planet" or strippedString == "Station"):"""
        if ("Drone" in strippedString):
            print(victim, ' hit at ', intoPosition)
            
            """if (strippedString == "Drone"):"""
            self.hitDrone(intoPosition)
                
            """else:
                self.DestroyObject(victim, intoPosition)"""
                
        print(shooter + ' is DONE.')
        Missile.Intervals[shooter].finish()

    def hitDrone(self, entry):
        droneNP = entry.getIntoNodePath().getName()
        drone = droneNP.getPythonTag("owner")

        drone.Health.Damage(1)

        intoPosition = Vec3(entry.getSurfacePoint(self.render))
        
        if drone.Health.val <= 0:
            self.DestroyObject(drone, intoPosition)

    def DestroyObject(self, hitID, hitPosition):
        nodeID = self.render.find(hitID)
        nodeID.detachNode()
        
        self.explodeNode.setPos(hitPosition)
        self.Explode()
        print("Drone Destroyed: ", hitID)
        
    def Explode(self):
        self.cntExplode += 1
        tag = 'particles-' +str(self.cntExplode)
        
        self.explodeIntervals[tag] = LerpFunc(self.ExplodeLight, duration = 4.0)
        self.explodeIntervals[tag].start()
        self.SetParticles()
        
    def ExplodeLight(self, t):
        if t == 1.0 and self.explodeEffect:
            self.explodeEffect.disable()
            
        elif t == 0:
            self.explodeEffect.start(self.explodeNode)
            
    def SetParticles(self):
        base.enableParticles() # type: ignore
        self.explodeEffect =  ParticleEffect()
        self.explodeEffect.loadConfig("./Assets/Part-Efx/basic_xpld_efx.ptf")
        self.explodeEffect.setScale(20)
        self.explodeNode = self.render.attachNewNode('ExplosionEffects')