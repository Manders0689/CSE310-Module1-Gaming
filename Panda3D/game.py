from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import AmbientLight, DirectionalLight 
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionNode
from panda3d.core import CollisionTube
from panda3d.core import Vec4, Vec3, Vec2
from panda3d.core import WindowProperties
        

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        #self.disableMouse()
        
        properties = WindowProperties()
        # Set screen size.
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)
        
        # LIGHTING
        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = self.render.attachNewNode(ambientLight)
        self.render.setLight(self.ambientLightNodePath)
        
        mainLight = DirectionalLight("main light")
        self.mainLightNodePath = self.render.attachNewNode(mainLight)
        # Turn it around by x degrees, and tilt it down by y degrees
        self.mainLightNodePath.setHpr(45, -45, 0)
        self.render.setLight(self.mainLightNodePath)
        # Activating shader for better lighting
        self.render.setShaderAuto()
        
        # Load the ENVIRONMENT.
        #self.loader.loadModel("models/misc/environment") #need this??
        self.environment = self.loader.loadModel("environments/environment")
        self.environment.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environment.setScale(0.25, 0.25, 0.25)
        self.environment.setPos(-8, 30, 0)
        
        # Set up ACTOR 
        self.tempActor = Actor("models/panda", {"walk" : "models/panda-walk"})
        self.tempActor.reparentTo(self.render)
        # Set position of actor 
        #self.tempActor.setPos(0, 7, 0) #commented out to set character to center of the scene.
        # Rotate Actor
        self.tempActor.getChild(0).setH(180)
        # Loop Actor animation
        self.tempActor.loop("walk")
        
        # CAMERA POSITION/ANGLE
        # Lower/Raise z value to lower/raise camera height.
        self.camera.setPos(0, 0, 800)
        # Tilt the camera down by setting its pitch.
        self.camera.setP(-90)
        
        # KEYMAP
        self.keyMap = {
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False,
            "shoot" : False
        }
        
        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.accept("mouse1", self.updateKeyMap, ["shoot", True])
        self.accept("mouse1-up", self.updateKeyMap, ["shoot", False])
        
        # Ask task-manager to run update loop, calling method named "update".
        self.updateTask = self.taskMgr.add(self.update, "update")       
        
        # COLLISIONS
        # Checks for collisions every update.
        self.cTrav = CollisionTraverser()  
        # Sends collision events.
        self.pusher = CollisionHandlerPusher()
        
        colliderNode = CollisionNode("player")
        # Add a collision-sphere centered on (0, 0, 0), radius of 0.3
        colliderNode.addSolid(CollisionSphere(0, 0, 0, 3))
        collider = self.tempActor.attachNewNode(colliderNode)
        # Shows white dot under actor to show center of collider position.
        #collider.show()
        # The pusher wants a collider, and a NodePath that should be moved by that collider's collisions.
        # In this case, we want our player-Actor to be moved.
        base.pusher.addCollider(collider, self.tempActor)
        # The traverser wants a collider and a handler that responds to that collider's collisions
        base.cTrav.addCollider(collider, self.pusher)
        # Restriction to the horizonal
        self.pusher.setHorizontal(True)
        # Create tubes for borders. (Start-point, End-point, radius)
        # Start-point (0, 0, 0), End-point(0, 0, 0), radius 1
        wallSolid = CollisionTube(-155.0, 0, 0, 155, 0, 0, 1)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(150.0)
        #wall.show()
        
        wallSolid = CollisionTube(-155.0, 0, 0, 155.0, 0, 0, 1)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(-150.0)
        #wall.show()
        
        wallSolid = CollisionTube(0, -155.0, 0, 0, 155.0, 0, 1)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setX(150.0)
        #wall.show()
        
        wallSolid = CollisionTube(0, -155.0, 0, 0, 155.0, 0, 1)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setX(-150.0)
       # wall.show()
        
        # ROCK COLLIDERS  
        rockSolid = CollisionSphere(12, 60, 0, 22)
        rockNode = CollisionNode("rock")
        rockNode.addSolid(rockSolid)
        rock = render.attachNewNode(rockNode)
        #rock.show()
        
        rockSolid = CollisionSphere(53, 59, 0, 13)
        rockNode = CollisionNode("rock")
        rockNode.addSolid(rockSolid)
        rock = render.attachNewNode(rockNode)
        #rock.show()
        
        rockSolid = CollisionSphere(65, -10, 0, 22)
        rockNode = CollisionNode("rock")
        rockNode.addSolid(rockSolid)
        rock = render.attachNewNode(rockNode)
        #rock.show()
        
        rockSolid = CollisionSphere(63, -50, 0, 12)
        rockNode = CollisionNode("rock")
        rockNode.addSolid(rockSolid)
        rock = render.attachNewNode(rockNode)
        #rock.show()
        
        rockSolid = CollisionSphere(-67, -40, 0, 28)
        rockNode = CollisionNode("rock")
        rockNode.addSolid(rockSolid)
        rock = render.attachNewNode(rockNode)
        #rock.show()
        
        rockSolid = CollisionSphere(-70, -80, 0, 25)
        rockNode = CollisionNode("rock")
        rockNode.addSolid(rockSolid)
        rock = render.attachNewNode(rockNode)
        #rock.show()

        
    # Update what's happending when keys are pushed.    
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
        #print (controlName, "set to", controlState) (Un-comment to print to console)
    
    # Store update-task.
    def update(self, task):
        # Get the amount of time since the last update.
        dt = globalClock.getDt()
        

        if self.keyMap["up"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(0, 5.0*dt, 0))
        if self.keyMap["down"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(0, -5.0*dt, 0))    
        if self.keyMap["left"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(-5.0*dt, 0, 0))
        if self.keyMap["right"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(5.0*dt, 0, 0))
        #if self.keyMap["shoot"]:
            #print ("Zap!")
            
        # Tells Panda that we want to run the task again.
        return task.cont
    
    
    
game = Game()
game.run()


