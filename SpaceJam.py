from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionHandlerEvent
import math, sys, random
import DefensePaths as defensePaths
import SpaceJamClasses as spaceJamClasses
import Player as Player
from direct.showbase.Audio3DManager import Audio3DManager

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.SetupScene()
        self.SetCamera()

        self.backgroundMusic = self.loader.loadMusic('./Assets/Audio/background_music.mp3')
        self.backgroundMusic.setLoop(True)
        self.backgroundMusic.setVolume(0.2)
        self.backgroundMusic.play()
        
        self.audio3d = Audio3DManager(self.sfxManagerList[0], self.camera)
        self.taskMgr.add(lambda task: (self.audio3d.update(), task.cont)[1], "updateAudio")
        self.audio3d.setDropOffFactor(5)
        self.audio3d.setDistanceFactor(2)

        self.droneSound = self.audio3d.loadSfx("./Assets/Audio/drone.mp3")
        self.droneSound.setVolume(.3)
        self.droneSound.setLoop(True)
        
        fullCycle = 60
                
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        
        
        self.eventHandler = CollisionHandlerEvent()
        self.eventHandler.addInPattern('%fn-into-%in')

        self.cTrav.addCollider(self.Ship.collisionNode, self.eventHandler)


        self.cTrav.addCollider(self.Ship.collisionNode, self.pusher)
        self.pusher.addCollider(self.Ship.collisionNode, self.Ship.modelNode)
        
        self.cTrav.showCollisions(self.render)
        self.cTrav.traverse(self.render)
        
        for j in range(fullCycle):

            spaceJamClasses.Drone.droneCount += 1
            nickName1 = "Drone1" + str(spaceJamClasses.Drone.droneCount)
            nickName2 = "Drone2" + str(spaceJamClasses.Drone.droneCount)
            self.DrawCloudDefense(self.Planet1, nickName1)
            self.DrawBaseballSeams(self.Station, nickName2, j, fullCycle, 2)

            spaceJamClasses.Drone.droneCount += 1
            nickName1 = "Drone1" + str(spaceJamClasses.Drone.droneCount)
            nickName2 = "Drone2" + str(spaceJamClasses.Drone.droneCount)
            self.DrawCloudDefense(self.Planet2, nickName1)

            spaceJamClasses.Drone.droneCount += 1
            nickName1 = "Drone1" + str(spaceJamClasses.Drone.droneCount)
            nickName2 = "Drone2" + str(spaceJamClasses.Drone.droneCount)
            self.DrawCloudDefense(self.Planet3, nickName1)
            
            spaceJamClasses.Drone.droneCount += 1
            nickName1 = "Drone1" + str(spaceJamClasses.Drone.droneCount)
            nickName2 = "Drone2" + str(spaceJamClasses.Drone.droneCount)
            self.DrawCloudDefense(self.Planet4, nickName1)

            spaceJamClasses.Drone.droneCount += 1
            nickName1 = "Drone1" + str(spaceJamClasses.Drone.droneCount)
            nickName2 = "Drone2" + str(spaceJamClasses.Drone.droneCount)
            self.DrawCloudDefense(self.Planet5, nickName1)

            spaceJamClasses.Drone.droneCount += 1
            nickName1 = "Drone1" + str(spaceJamClasses.Drone.droneCount)
            nickName2 = "Drone2" + str(spaceJamClasses.Drone.droneCount)
            self.DrawCloudDefense(self.Planet6, nickName1)
            
            spaceJamClasses.miniDrone.droneCount += 1
            nickName1 = "Mini1" + str(spaceJamClasses.miniDrone.droneCount)
            nickName2 = "Mini2" + str(spaceJamClasses.miniDrone.droneCount)
            self.DrawCloudDefense(spaceJamClasses.Drone, nickName1)
            
            spaceJamClasses.miniDrone.droneCount += 1
            nickName1 = "Mini1" + str(spaceJamClasses.miniDrone.droneCount)
            nickName2 = "Mini2" + str(spaceJamClasses.miniDrone.droneCount)
            self.DrawCloudDefense(spaceJamClasses.Drone, nickName1)
            
            spaceJamClasses.miniDrone.droneCount += 1
            nickName1 = "Mini1" + str(spaceJamClasses.miniDrone.droneCount)
            nickName2 = "Mini2" + str(spaceJamClasses.miniDrone.droneCount)
            self.DrawCloudDefense(spaceJamClasses.Drone, nickName1)
            
            spaceJamClasses.miniDrone.droneCount += 1
            nickName1 = "Mini1" + str(spaceJamClasses.miniDrone.droneCount)
            nickName2 = "Mini2" + str(spaceJamClasses.miniDrone.droneCount)
            self.DrawCloudDefense(spaceJamClasses.Drone, nickName1)
            
            spaceJamClasses.miniDrone.droneCount += 1
            nickName1 = "Mini1" + str(spaceJamClasses.miniDrone.droneCount)
            nickName2 = "Mini2" + str(spaceJamClasses.miniDrone.droneCount)
            self.DrawCloudDefense(spaceJamClasses.Drone, nickName1)
            
            spaceJamClasses.miniDrone.droneCount += 1
            nickName1 = "Mini1" + str(spaceJamClasses.miniDrone.droneCount)
            nickName2 = "Mini2" + str(spaceJamClasses.miniDrone.droneCount)
            self.DrawCloudDefense(spaceJamClasses.Drone, nickName1)
        
        self.taskMgr.add(self.updateCollisions, "update-collisions")
        self.accept('escape', self.quit)

    def SetupScene(self):
        # Scenes Background
        self.Universe = spaceJamClasses.Universe(self.loader,'./Assets/Universe/Universe.x', self.render, 'Universe', "./Assets/Universe/Universe.jpg", (0, 0, 0), 15000)
        # Space Station
        self.Station = spaceJamClasses.Station(self.loader,'./Assets/SpaceStation/spaceStation.x', self.render, "Space Station", "./Assets/SpaceStation/SpaceStation1_Dif2.png", (50, 3000, 575), 10)
        # Space Ship
        self.Ship = Player.Ship(self.loader, './Assets/Spaceships/Dumbledore.x', self.render, "Ship", "./Assets/Spaceships/spacejet_C.png", (0, 500, -30), 10)        
        # Planets
        self.Planet1 = spaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, "Planet1", "./Assets/Planets/Planet-1.png", (-1500, 4300, 70), 350)
        self.Planet2 = spaceJamClasses.Planet(self.loader,'./Assets/Planets/protoPlanet.x', self.render, "Planet2", "./Assets/Planets/Planet-2.png", (-270, 1000, -300), 72)
        self.Planet3 = spaceJamClasses.Planet(self.loader,'./Assets/Planets/protoPlanet.x', self.render, "Planet3", "./Assets/Planets/Planet-3.png", (400, 2500, 250), 135)
        self.Planet4 = spaceJamClasses.Planet(self.loader,'./Assets/Planets/protoPlanet.x', self.render, "Planet4", "./Assets/Planets/Planet-4.png", (1000, 10000, -1180), 239)
        self.Planet5 = spaceJamClasses.Planet(self.loader,'./Assets/Planets/protoPlanet.x', self.render, "Planet5", "./Assets/Planets/Planet-5.png", (2000, 6000, -90), 60)
        self.Planet6 = spaceJamClasses.Planet(self.loader,'./Assets/Planets/protoPlanet.x', self.render, "Planet6", "./Assets/Planets/Planet-6.png", (-1116, 5000, 1500), 240)
    
        self.Sentinal1 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj", self.render, "Drone", 6.0, "./Assets/Drone Defender/octotoad1_auv.png", self.Planet5, 900, "MLB", self.Ship)
        self.Sentinal2 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj", self.render, "Drone", 6.0, "./Assets/Drone Defender/octotoad1_auv.png", self.Planet2, 500, "Cloud", self.Ship)
        self.Sentinal3 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj", self.render, "Drone", 6.0, "./Assets/Drone Defender/octotoad1_auv.png", self.Planet6, 300, "MLB", self.Ship)
        self.Sentinal4 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj", self.render, "Drone", 6.0, "./Assets/Drone Defender/octotoad1_auv.png", self.Planet3, 400, "Cloud", self.Ship)
        self.Sentinal5 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj", self.render, "Drone", 6.0, "./Assets/Drone Defender/octotoad1_auv.png", self.Planet1, 600, "MLB", self.Ship)
        self.Sentinal6 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj", self.render, "Drone", 6.0, "./Assets/Drone Defender/octotoad1_auv.png", self.Planet3, 800, "Cloud", self.Ship)
        self.Sentinal7 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj", self.render, "Drone", 6.0, "./Assets/Drone Defender/octotoad1_auv.png", self.Planet6, 700, "MLB", self.Ship)
        self.Sentinal8 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj", self.render, "Drone", 6.0, "./Assets/Drone Defender/octotoad1_auv.png", self.Planet2, 500, "Cloud", self.Ship)
        self.Sentinal9 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj", self.render, "Drone", 6.0, "./Assets/Drone Defender/octotoad1_auv.png", self.Planet4, 200, "MLB", self.Ship)

    def SetCamera(self):
        "self.disableMouse()"
        self.camera.reparentTo(self.Ship.modelNode)
        self.camera.setFluidPos(0, 0, 0)

    def DrawBaseballSeams(self, centeralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 250 + centeralObject.modelNode.getPos()
        drone = spaceJamClasses.Drone(self.loader,"./Assets/Drone Defender/DroneDefender.obj", self.render, droneName, "./Assets/Drone Defender/octotoad1_auv.png", position, 5)
        
        self.audio3d.attachSoundToObject(self.droneSound, drone.modelNode)
        self.droneSound.play()
        
    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        drone = spaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.obj", self.render, droneName, "./Assets/Drone Defender/octotoad1_auv.png", position, 10)
        
        self.audio3d.attachSoundToObject(self.droneSound, drone.modelNode)
        self.droneSound.play()
        
    
    def updateCollisions(self, task):
        self.cTrav.traverse(self.render)
        return task.cont

    # Prepare message if server wants to quit 
    def quit(self):
        sys.exit()
        
app = MyApp()
app.run()
