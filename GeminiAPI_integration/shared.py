import threading
import numpy as np

classObjs = {
    'black_hole_2x2':0,
    'blue_plate_2x4': 1,
    'blue_plate_6x10':2, 
    'brown_brick_2x2':3,
    'brown_brick_2x4':4,
    'brown_corner_brick_2x2':5,
    'brown_plate_2x2':6,
    'brown_plate_2x4':7,
    'brown_plate_2x6':8,
    'brown_plate_4x6':9,
    'craft_brick_1x2':10,
    'craft_tile_2x2':11,
    'dark_green_brick_2x2':12,
    'dark_green_brick_2x4':13,
    'dark_green_plate_1stud_2x2':14,
    'dark_green_plate_2studs_2x4':15,
    'green_corner_2x2':16,
    'green_hole_2x2':17,
    'green_plate_4x4':18,
    'red_groove_2x2':19,
    'red_plate_2x2':20,
    'tnt_1x2':21
}

gemini_to_classobj = {
    'brown 2x2 brick': 'brown_brick_2x2',
    'black round plate with four studs': 'black_hole_2x2',
    'brown 4x4 tile with grid pattern': 'craft_tile_2x2'
}


class SharedData:
    def __init__(self):
        self.update = 0
        self.xm = 0
        self.ym = 0
        self.grab = 0

        self.x1 = 0
        self.x2 = 0

        self.y1 = 0
        self.y2 = 0

        self.pos = {
            "x":0.007052, "y":0.178, "z":0.351,
            "roll":-2.812, "pitch":1.489, "yaw":-1.298,
        }
        self.distance = 10
        self.lock = threading.Lock()

        # self.nextObj = 0
        self.objIndex = 0
        self.Index = 0
        self.ass = [0,0,0]

        self.lego_list = []

        self.rotate = np.array([[0.0, 0.0, 1.0],
                        [0.0, 1.0, 0.0],
                        [-1.0, 0.0, 0.0]])

    
    def setRotation(self,rot):
        with self.lock:
            self.rotate = np.array(rot).astype(float).reshape(3, 3)
    
    def getRotation(self):
        return self.rotate
    

    def set_LegoList(self,lst):
        with self.lock: 
            self.lego_list = lst

    def get_LegoList(self):
        return self.lego_list

    def setX1(self,x1):
        with self.lock:
            self.x1 = x1
    
    def getX1(self):
        return self.x1
    

    def setX2(self,x2):
        with self.lock:
            self.x2 = x2
    
    def getX2(self):
        return self.x2
    

    
    def setY1(self,y1):
        with self.lock:
            self.y1 = y1
    
    def getY1(self):
        return self.y1
    
    
    def setY2(self,y2):
        with self.lock:
            self.y2 = y2
    
    def getY2(self):
        return self.y2
    

    
    def setXm(self,xm):
        with self.lock:
            self.xm = xm
    
    def getXm(self):
        return self.xm
    
    def setYm(self,ym):
        with self.lock:
            self.ym = ym
    
    def getYm(self):
        return self.ym

    def setUpdate(self,update):
        with self.lock:
            self.update = update
    
    def getUpdate(self):
        return self.update
    
    def getPos_asDict(self):
        return self.pos
    
    def getPos(self):
        position = [self.pos['x'], self.pos['y'], self.pos['z'], self.pos['roll'], self.pos['pitch'], self.pos['yaw']]
        return position
    
    def setPos(self,pos):
        with self.lock:
            self.pos = pos

    def setDist(self,dist):
        with self.lock:
            self.distance = dist
    
    def getDist(self):
        return self.distance
    
    def getGrab(self):
        return self.grab
    
    def setGrab(self,grab):
        with self.lock:
            self.grab = grab


    # def getNextObj(self):
    #     return self.nextObj
    
    # def setNextObj(self,classid):
    #     with self.lock:
    #         self.nextObj = classid

    def set_PickPlaceObj(self, legos):
        # legos = lego_piece.low_z(self.lego_list)
        self.objIndex = classObjs[gemini_to_classobj[legos[0]]]
        self.ass = [legos[1]['x'],legos[1]['y'],legos[1]['z']]

    def get_ass(self):
        return self.ass[0],self.ass[1],self.ass[2]
    
    def getObjIndex(self):
        return self.objIndex
    


    def dump(self,dict):
        self.setUpdate(dict["update"])
        self.setXm(dict["xm"])
        self.setYm(dict["ym"])