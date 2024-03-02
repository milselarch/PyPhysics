from Tkinter import *
from tkFileDialog import askopenfilename

import webbrowser
import traceback
import threading
import Tkinter
import thread
import random
import time
import math
import copy
import ast
import sys

import vectorMath2
import penMaker8 as penMaker

vectorMath = vectorMath2.mathy()

"""
simul.pens['bugs'].pt2
"""

class loop(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.master.resizable(width=False,height=False)
        self.running = False
        self.start = 0
        self.oldTime = 0
        self.nowTime = 0
        self.cheakDelay = 10
        self.interval = 0
        self.delay = 0
        self.boundary = {}
        self.cpens = []
        self.pens = {}
        self.temp = None

        """
        104 104.1
        """
        self.data = {
        'settings':{
            'chunk-x': 65
            ,'chunk-y': 65
            ,'bounds': (16,9)
            ,'lag': 1 #0.08 #1
            ,'interval':20
            ,'cheakDelay':5
            ,'depth-deltav':0.8
            ,'damper':0.01
            ,'fps': 60 #104 #61
            ,'bg':'white'
            },
        'pens': {
            'object1':{
                'length':100,'breath':15
                ,'mass':11,'colour':'#679ec1'
                ,'x':300,'y':440,'vx':152,'vy':-35
                ,'fx':lambda t:0,'fy':lambda t:0 #t*0.15
                ,'a':66,'va':22,'fa':lambda t:0 #t**0.5
                ,'e':1
                },
            'derpy':{
                'length':80,'breath':20
                ,'mass':12,'colour':'#f5d564'
                ,'x':390,'y':200,'vx':187,'vy':15
                ,'fx':lambda t:0 #t #**0.5
                ,'fy':lambda t:0 #-t**0.1
                ,'a':72,'va':31,'fa':lambda t:0 #-t**0.3+2
                ,'e':1
                }
            }
        }

    def initGui(self):
        self.menuBar = Menu(self)
        self.fileMenu1 = Menu(self.menuBar)
        
        self.master.config(menu=self.menuBar)
        self.fileMenu1.add_command(
            label="Open...",command=self.openFileNm
            )
        self.fileMenu1.add_command(
            label="may contain cupcakes",command=self.cupcakes
            )
        self.fileMenu1.add_command(
            label="about",command=self.showAbout
            )
        self.menuBar.add_cascade(
            label="File",menu=self.fileMenu1
            )

    def openFileNm(self):
        filename = askopenfilename(
            filetypes=[("Text files","*.txt")]
            )
        try:
            data = open(filename).read()
            print data
            self.data = eval(data)
            #print self.data
            
            self.pens = {}
            self.canvas.delete('all')
            self.canvas.destroy()
            self.make()
            self.initDraw()
            self.startGame()
        except Exception as e:
            self.parser.errorInfo(e)
            print 'file could not be opened'
            
    def showAbout(self):
        print('physics simulator. wahts there to talk about? 0.o')

    def cupcakes(self):
        num = random.choice(range(1,8))
        if num == 1:
            siteNm = 'https://www.youtube.com/watch?v=_AbtCTbSWTk'
        elif num == 2:
            siteNm = 'https://www.youtube.com/watch?v=N_708QY7Obk'
        elif num == 3:
            siteNm = 'http://youtu.be/hPokJFyUq1s'
        elif num == 4:
            siteNm = 'https://www.youtube.com/watch?v=ELnn9V01EiI'
        elif num == 5:
            siteNm = 'https://www.youtube.com/watch?v=Ki_Af_o9Q9s'
        elif num == 6:
            siteNm = [
            'https://www.youtube.com/watch?v=oHOR9_yMakU'
            ,'https://www.youtube.com/watch?v=SjFbhE-NPZs'
            ,'https://www.youtube.com/watch?v=u2oJPMdiAZc'
            ,'https://www.youtube.com/watch?v=IeOYJO-jFGs'
            ]
        elif num == 7:
            siteNm = 'https://www.youtube.com/watch?v=oHOR9_yMakU'
            
        if type(siteNm) == str:
            webbrowser.open(siteNm)
        else:
            for string in siteNm:
                webbrowser.open(string)
                
    def derp(self):
        print 'HERRO'
        
    def make(self):
        self.parser = safeParse(self)
        #self.after(100,self.parser.run)
        thread.start_new_thread(self.parser.run,())
        self.parser.grid(row=200,column=100)
        
        penData = self.data['pens']
        data = self.data['settings']
        for row in range(data['bounds'][0]+1):
            for column in range(data['bounds'][1]+1):
                bound = (
                    row*data['chunk-x']
                    ,column*data['chunk-y']
                    ,(row+1)*data['chunk-x']
                    ,(column+1)*data['chunk-y']
                    )
                self.boundary[bound] = []
                
        for penName in penData:
            temp = penData[penName]
            pen = penMaker.pen(
                name=penName
                ,mass   = temp['mass'  ]
                ,length = temp['length']
                ,breath = temp['breath']
                ,colour = temp['colour']
                ,damper = self.data['settings']['damper']
                ,x  = temp['x' ]
                ,y  = temp['y' ]
                ,vx = temp['vx']
                ,vy = temp['vy']
                ,fx = temp['fx']
                ,fy = temp['fy']
                ,a  = temp['a' ]
                ,va = temp['va']
                ,fa = temp['fa']
                ,e  = temp['e' ]
                )
            pen.makePoints(
                self.data['settings']['chunk-x']
                ,self.data['settings']['chunk-y']
                ,self.boundary,[0,0]
                  
                ,self.data['settings']['chunk-x']
                *self.data['settings']['bounds'][0]
                ,self.data['settings']['chunk-y']
                *self.data['settings']['bounds'][1]
                ,self.interval
                )
            self.pens[penName] = pen

        #print self.boundary
        self.maxx = (
            self.data['settings']['chunk-x']
            *self.data['settings']['bounds'][0]
            )
        self.maxy = (
            self.data['settings']['chunk-y']
            *self.data['settings']['bounds'][1]
            )
        self.cheakDelay = data['cheakDelay']
        self.interval = data['interval']
        self.delay = 1.0/data['fps']
        self.canvas = Canvas(self
            ,width  = data['chunk-x']*data['bounds'][0]
            ,height = data['chunk-y']*data['bounds'][1]
            ,bg=data['bg']#,selectbackground='pink'
            )
        self.canvas.grid(row=100,column=100)

        self.canvasLength = data['chunk-x']*data['bounds'][0]
        self.canvasBreath = data['chunk-y']*data['bounds'][1]
        try:
            self.adjust = data['depth-deltav']
        except KeyError:
            self.adjust =  0.1
        try:
            self.lag = data['lag']
        except KeyError:
            self.lag = 1
        try:
            self.debug = data['__DEBUG__']
        except KeyError:
            self.debug = False
        try:
            self.anchor = data['anchor']
        except KeyError:
            self.anchor = 'sw'

        if type(self.anchor) == str:
            assert(len(self.anchor)==2)
            self.disp = []
            if self.anchor[1] == 'w':
                self.disp.append((0,1))
            elif self.anchor[1] == 'e':
                self.disp.append(
                    (self.canvasLength,-1)
                    )
            else:
                raise ValueError
            
            if self.anchor[0] == 's':
                self.disp.append(
                    (self.canvasBreath,-1)
                    )
            elif self.anchor[0] == 'n':
                self.disp.append((0,1))
            else:
                raise ValueError
            
        elif type(self.anchor) in (list,tuple):
            self.disp = (
                (-self.anchor[0],1)
                ,(self.canvasBreath-self.anchor[1],-1)
                )
        else: raise ValueError

        #print self.disp

        chunkx = self.data['settings']['chunk-x']
        chunky = self.data['settings']['chunk-y']
        cols,rows = self.data['settings']['bounds']
        for col in range(cols):
            self.canvas.create_line(
                col*chunkx,0,col*chunkx,self.maxy
                ,tags=('GRID::COL',)
                ,fill='grey92'
                )
        for row in range(rows):
            self.canvas.create_line(
                0,row*chunky,self.maxx,row*chunky
                ,tags=('GRID::COL',)
                ,fill='grey92'
                )
        
    def initDraw(self):
        for penName in self.pens:
            points = []
            pen = self.pens[penName]
            for point in pen.points:
                point = tuple(point)
                point = self.adjustPt(point)
                points.extend(
                    (int(point[0]),int(point[1]))
                    )

            #print Tkinter._flatten(points)
            self.canvas.create_polygon(
                points,tags=('PEN:'+penName,)
                ,fill=self.pens[penName].colour
                )
            
        """
        for penName in self.pens:
            self.canvas.create_polygon((
                self.pens[penName].points[0][0]+1
                ,self.pens[penName].points[0][1]+1
                ,self.pens[penName].points[1][0]+1
                ,self.pens[penName].points[1][1]+1
                ,self.pens[penName].points[2][0]+1
                ,self.pens[penName].points[2][1]+1
                ,self.pens[penName].points[3][0]+1
                ,self.pens[penName].points[3][1]+1
                )
                ,tags=('PEN:'+penName,)
                ,fill=self.pens[penName].colour
                )
        """

    def startGame(self):
        self.start = time.clock()
        self.oldTime = 0
        self.running = True
        self.update()

    def update(self):
        self.nowTime = (time.clock()-self.start)*self.lag
        timey = (self.oldTime,self.oldTime+self.delay)
        draw = False

        while self.nowTime-self.oldTime >= self.delay:
            #self.updatePhysics([self.oldTime,self.nowTime])
            self.updatePhysics(timey)
            #self.cheakWalls([self.oldTime,self.nowTime])

            #self.oldTime = self.nowTime
            self.oldTime += self.delay
            #self.canvas.update_idletasks()
            draw = True

        if draw == True:
            #self.canvas.update_idletasks()
            #self.canvas.delete('cheak')
            #self.canvas.delete('TEMP')
            #self.after(250,self.removeLines,timey)
            self.updateDraw()

        if self.running == True:
            self.after(self.cheakDelay,self.update)
                
    def updatePhysics(self,timey):
        """
        print(self.pens['object1'].x
            ,random.choice(range(100))
            )
        """
        cheak = []
        for penName in self.pens:
            #print self.pens[penName].vx
            self.pens[penName].update(
                self.data['settings']['chunk-x']
                *self.data['settings']['bounds'][0]
                ,self.data['settings']['chunk-y']
                *self.data['settings']['bounds'][1]
                ,timey
                )
            #print self.pens[penName].vx
            self.pens[penName].makePoints(
                self.data['settings']['chunk-x']
                ,self.data['settings']['chunk-y']
                ,self.boundary,timey
                
                ,self.data['settings']['chunk-x']
                *self.data['settings']['bounds'][0]
                ,self.data['settings']['chunk-y']
                *self.data['settings']['bounds'][1]
                ,interval=self.interval
                ,cheak=cheak
                )

        pensList = []
        for region in cheak: #cheak
            if len(self.boundary[region]) <= 1:
                pass
            else:
                pens = sorted(self.boundary[region])
                if pens not in pensList:
                    pensList.append(pens)
                    
                self.drawBound(region,timey)
                """
                self.collideResolve(
                    pens,timey
                    )
                """

        for pens in pensList:
            self.collideCheak(
                pens,timey,[]
                )

    def drawBound(self,region,timey):
        new1 = self.adjustPt((region[0],region[1]))
        new2 = self.adjustPt((region[2],region[3]))
        
        self.canvas.create_rectangle(
            new1[0],new1[1],new2[0],new2[1]
            ,fill='grey96'
            ,outline='grey92'
            ,tags=('CHEAK','CHEAK::'+str(timey))
            )
        self.canvas.lower('CHEAK')
        self.after(50,self.removeCheaks,timey)

    def removeCheaks(self,timey):
        #print timey
        self.canvas.delete('CHEAK::'+str(timey))

    def makeLines(self,timey,lines=(),fill='purple',kill=True):
        """
        #print '::::::: ',lines
        
        for k in range(len(lines)):
            line = lines[k]
            new1 = self.adjustPt(line[0])
            new2 = self.adjustPt(line[1])
            #print k,line
            self.canvas.create_line(
                new1[0],new1[1],new2[0],new2[1]
                ,fill=fill
                ,tags=('TEMP','TEMP::'+str(timey))
                )

        self.canvas.lift('TEMP')
        if kill == True:
            self.after(250,self.removeLines,timey)
        """
        pass
        
    def removeLines(self,timey):
        self.canvas.delete('TEMP::'+str(timey))

    def drawPoints(self,points,pen,timey):
        for point in points:
            self.makeLines(
                timey
                ,(
                (pen.points[point]
                ,pen.points[(point+1)%(len(pen.points))])
                ,)
                ,fill='black'
                ,kill=False
                )

    def getBestEdge(self,normal,center,points):
        """
        simul.getBestEdge(
        (0,-1),(11,17),((8,20),(14,20),(14,4),(8,4)))
        )
        ((8, 4), (14, 4), (8, 4))
        test.getBestEdge(
        (0,1),(8,2),[(4,5),(12,5),(12,-1),(4,-1)])
        )
        ((12, 5), (12, 5), (4, 5))
        """
        index = 0
        normal = vectorMath.normalise(normal)
        maxNum = -float('inf')

        """
        note ambiguity towards definition of "v"
        (implemented as vector) in tutorial code
        """

        #print '-'*50
        #print 'INIT EDGE',pen.name,normal
        x,y = center
        
        for i in range(len(points)):
            endi = (i+1)%len(points)
            """
            vector = vectorMath.toVector(
                pen.points[i][0]
                ,pen.points[i][1]
                ,pen.points[endi][0]
                ,pen.points[endi][1]
                )
            """
            
            vector = vectorMath.toVector(
                x,y
                ,points[i][0]
                ,points[i][1]
                )
            
            """
            note the "???" modifications made
            to compensate for downwards y axis
            and winding direction 
            """
            vector = list(points[i])
            #vector[1] = self.canvasBreath-vector[1]
            #vector = vectorMath.minVector((0,0),vector)
            vector = vectorMath.normalise(vector)
            projection = vectorMath.dotProduct(
                normal,(vector[0],vector[1]*-1) #??? #*-1
                )
            if (projection > maxNum):
                maxNum = projection
                index = i

        v = points[index]
        v1 = points[(index+1)%len(points)]
        v0 = points[index-1]
        #v0,v1 = v1,v0 #???

        cmLine = vectorMath.toVector(
            x,y,v[0],v[1]
            )
        cmLine = vectorMath.normalise(cmLine)
        """
        if vectorMath.dotProduct(cmLine,normal) < 0:
            normal[0] *= -1
            normal[1] *= -1
        """ 
        #print v0,v,v1
        
        lVector = list(vectorMath.minVector(v,v1))
        rVector = list(vectorMath.minVector(v,v0))
        #lVector[1] *= -1
        #rVector[1] *= -1
        lVector = vectorMath.normalise(lVector)
        rVector = vectorMath.normalise(rVector)

        rDot = vectorMath.dotProduct(normal,rVector)
        lDot = vectorMath.dotProduct(normal,lVector)
        #print 'PREP RDOT LDOT RVEC LVEC'
        #print rDot,lDot,rVector,lVector
        
        rDot = abs(rDot)
        lDot = abs(lDot)
        assert(rDot>=0)
        assert(lDot>=0)
        
        if (rDot <= lDot):
            return(v,v0,v)
        else:
            return(v,v,v1)

    def getRefInc(self,edge1,edge2,normal):
        #print 'HOLLOW DEPR',edge1,edge2,normal
        #print ''
        #print edge1
        toEdge1 = vectorMath.toVector(
            edge1[0][0],edge1[0][1]
            ,edge1[1][0],edge1[1][1]
            )
        toEdge2 = vectorMath.toVector(
            edge2[0][0],edge2[0][1]
            ,edge2[1][0],edge2[1][1]
            )
        flip = False
        dot1 = vectorMath.dotProduct(toEdge1,normal)
        dot2 = vectorMath.dotProduct(toEdge2,normal)

        if abs(dot1) <= abs(dot2):
            ref = toEdge1
            inc = toEdge2
        else:
            ref = toEdge2
            inc = toEdge1
            flip = True

        return(ref,inc,flip)

    def getClipPts(self,v1,v2,n,o,flip=True):
        """
        simul.getClipPts((12,5),(4,5),(1,0),8)
        -> [(12,5),(8,5)]
        simul.getClipPts((12,5),(8,5),(-1,0),-14)
        -> [(12,5),(8,5)]
        simul.getClipPts((2,8),(6,4),(-1,0),-12)
        -> [(2,8),(6,4)]
        simul.getClipPts((2,8),(6,4),(1,0),4)
        -> [(6,4),(4,6)]
        simul.getClipPts((12,5),(4,5),(0.97,-0.24),7.77)
        -> [(12,5),(9.28,5)]
        
        """
        """
        if flip == True:
            n = (n[0],-n[1])
        """
        cp = []
        d1 = vectorMath.dotProduct(n,v1)-o
        d2 = vectorMath.dotProduct(n,v2)-o

        #print 'V1 V2 N O D1 D2'
        #print v1,v2,n,o,d1,d2
    
        if d1 >= 0: cp.append(v1)
        if d2 >= 0: cp.append(v2)

        if d1*d2 < 0:
            e = vectorMath.minVector(v2,v1)
            #print 'E = > %s'%str(e)
            u = float(d1)/(d1-d2)
            # prevent interger rounding error
            #print 'U => %s'%str(u)
            e = vectorMath.scale(u,e)
            #print 'E = > %s'%str(e)
            e = vectorMath.addVector(e,v1)
            #print 'E = > %s'%str(e)
            cp.append(e)

        return(cp)

    def getMaxRef(self,refNorm,ref):
        length = -float('inf')
        best = None

        for point in ref:
            drct = vectorMath.dotProduct(point,refNorm)
            if drct > length:
                length = drct
                best = point

        return(point)
        
    def collideResolve(self,data,pen1,pen2
        ,timey,detimey=None
        ):
        #print '-'*50
        #print 'PEN NAMES',[pen1.name,pen2.name]
        self.updateDraw()
        #print 'NORMAL+DEPTH ->',data
        #self.canvas.create_rectangle(
        #    0,0,20,20,fill='red',outline='red'
        #    ,tags=('WTF')
        #    )
        #self.after(200,self.canvas.delete,'WTF')
        
        if detimey == None:
            detimey = timey

        cmLine = vectorMath.toVector(
            pen1.x,pen1.y,pen2.x,pen2.y
            )

        normal,depth = data
        #normal = list(normal)
        #normal = tuple(normal)
        #normal = vectorMath.normalise(normal)
        #print normal,depth,'POTATO'
        
        if vectorMath.dotProduct(cmLine,normal) >= 0:
            #print 'FALPPER',normal
            normal = vectorMath.minVector((0,0),normal)
            #print 'FALPPER2',normal
        #normal = vectorMath.normalise(normal)

        #normal = vectorMath.minVector((0,0),normal)
        cmLine = vectorMath.toVector(
            pen1.x,pen1.y,pen2.x,pen2.y
            )
        cmLine = vectorMath.normalise(cmLine)
        if vectorMath.dot(cmLine,normal) < 0:
            normal = (-normal[0],-normal[1])

        #print 'YYYYYYYYYYYYYYYYYYY'
        edge1 = vectorMath.getBestEdge(
            normal,(pen1.x,pen1.y)
            ,pen1.points
            )
        edge2 = vectorMath.getBestEdge(
            [-normal[0],-normal[1]]
            ,(pen2.x,pen2.y)
            ,pen2.points
            )
        #assert(edge1[0]==edge2[0])
        #v = edge1[0]
        #cmLine = vectorMath.toVector(pen1.x,pen)

        #print '-'*50
        #print 'EDGE CHEAK'
        #print 'E1:',edge1
        #print 'E2:',edge2
        
        self.makeLines(
            timey
            ,lines = (
                (edge1[1],edge1[2])
                ,(edge2[1],edge2[2])
                )
            ,fill='black'
            ,kill=False
            )
        
        self.canvas.update_idletasks()
        
        ref,inc,flip = self.getRefInc(
            edge1[1:],edge2[1:],normal
            )
        #print 'XXXXXXXXXXXXXXX'

        if flip == True:
            ref_v1,ref_v2 = edge2[1:]
            inc_v1,inc_v2 = edge1[1:]
        else:
            inc_v1,inc_v2 = edge2[1:]
            ref_v1,ref_v2 = edge1[1:]
            
        #print ref
        refv = vectorMath.normalise(
            vectorMath.toVector(
                ref_v1[0],ref_v1[1]
                ,ref_v2[0],ref_v2[1]
                )
            )
        nRef = vectorMath.normalise(
            vectorMath.perp(ref)
            )

        #self.getClipPts((2,8),(6,4),(-1,0),-12)
        nRef = vectorMath.minVector((0,0),nRef)
        #print '\n',nRef
        o1 = vectorMath.dotProduct(refv,ref_v1)
        #print inc
        #print ref,'REDAOPSDJO'
        #print 'PRE SYSTEMS NOMINAL'
        #print inc_v1,inc_v2,nRef,o1
        cp = self.getClipPts(inc_v1,inc_v2,refv,o1)
        #print 'CHEAK SYSTEMS NOMINAL',cp
        if len(cp) < 2: return(None)
        
        o2 = vectorMath.dotProduct(refv,ref_v2)
        #print 'O2',o2
        """
        if cp == []:
            #collide = False
            print 'ERROR: CLIP FAILURE #1'
            print 'PEN ONE ->',pen1.name
            print 'PEN TWO ->',pen2.name
            print 'NORMAL ->',normal
            print 'EDGE1 ->',edge1
            print 'EDGE2 ->',edge2
            print 'REFV ->',refv
        """
        
        cp = self.getClipPts(
            cp[0],cp[1],(-refv[0],-refv[1]),-o2 #o1?
            )
        if len(cp) < 2: return(None)

        refNorm = vectorMath.perp(nRef)
        if flip == True:
            refNorm = vectorMath.minVector((0,0),refNorm)

        refNorm = nRef
        maxRef = edge1[0] #self.getMaxRef(refNorm,ref)
        maxNum = vectorMath.dotProduct(refNorm,maxRef)
        try:
            if vectorMath.dot(cp[0],refNorm)-maxNum < 0:
                cp.remove(cp[0])
            if vectorMath.dot(cp[1],refNorm)-maxNum < 0:
                cp.remove(cp[1])
        except IndexError:
            pass
        
        #print cp
        #assert(len(cp)<=2)
        collide = True
        #cp = cp[0]
        if cp == []:
            #collide = False
            """
            print 'ERROR: CLIP FAILURE #2'
            print 'PEN ONE ->',pen1.name
            print 'PEN TWO ->',pen2.name
            print 'NORMAL ->',normal
            print 'EDGE1 ->',edge1
            print 'EDGE2 ->',edge2
            print 'REFV ->',refv
            """
            raise AssertionError
        
        elif type(cp) == list and len(cp) == 2:
            cp = vectorMath.midVector(cp[0],cp[1])
        try:
            if type(cp[0]) != float:
                cp = cp[0]
                
        except IndexError:
            pass

        self.makeLines(
            timey
            ,lines = (
                ((pen1.x,pen1.y),cp)
                ,((pen2.x,pen2.y),cp)
                )
            ,fill='orange'
            ,kill=True #False
            )
        
        rap = vectorMath.toVector(
            pen1.x,pen1.y,cp[0],cp[1]
            )
        rbp = vectorMath.toVector(
            pen2.x,pen2.y,cp[0],cp[1]
            )
        #print 'END CP FINDER'

        self.updateDraw()
        
        #print ''
        #print edge1,edge2
        #print normal
        try:
            mfill
        except:
            mfill = 'pink'

        if self.debug == True:
            print('COLLISION REPORT @ '+str(timey))
            print('NAMES: %s %s'%(pen1.name,pen2.name))
            print('-'*50)
            print('PAST: '+str([pasta1,pasta3,pastb1,pastb2]))
            try:
                print('IN: '
                +str([in1,in2,in3,in4,parallel1,parallel2])
                )
            except:
                pass
            print('-'*50)
            print('')
        
        pen1.unUpdate(
            self.maxx,self.maxy,detimey
            )
        pen2.unUpdate(
            self.maxx,self.maxy,detimey
            )
        #raise Exception
    
        vap = vectorMath.addVector(
            (pen1.vx,pen1.vy)
            ,vectorMath.scale(
                math.radians(pen1.va)
                ,vectorMath.perp(rap)
                )
            )
        vbp = vectorMath.addVector(
            (pen2.vx,pen2.vy)
            ,vectorMath.scale(
                math.radians(pen2.va)
                ,vectorMath.perp(rbp)
                )
            )
        vab = vectorMath.minVector(vap,vbp)
        if vab > 0:
            #normal = vectorMath.normalise(normal)
            e = pen1.e*pen2.e
            j = vectorMath.collide(
                e,vab,rap,rbp,pen1.inertia
                ,pen2.inertia,normal,pen1.mass
                ,pen2.mass
                )
            
            #print vab
            nvx1 = (j/pen1.mass)*normal[0]
            nvy1 = (j/pen1.mass)*normal[1]
            nva1 = (
                vectorMath.dotProduct(
                vectorMath.perp(rap)
                ,vectorMath.scale(j,normal)
                )/pen1.inertia
                )
            nvx2 = (j/pen2.mass)*normal[0]
            nvy2 = (j/pen2.mass)*normal[1]
            nva2 = (
                vectorMath.dotProduct(
                vectorMath.perp(rbp)
                ,vectorMath.scale(j,normal)
                )/pen2.inertia
                )
            pen1.vx += nvx1
            pen1.vy += nvy1
            pen1.va += nva1

            pen2.vx -= nvx2
            pen2.vy -= nvy2
            pen2.va -= nva2
            
            """
            print('---------------')
            print('ONE NEW =>',pen1.vx,pen1.vy,pen1.va)
            print('TWO NEW =>',pen2.vx,pen2.vy,pen2.va)
            """
            
        pen1.update(self.maxx,self.maxy,timey)
        pen2.update(self.maxx,self.maxy,timey)
        #self.seperate(i,j2,pen1,pen2,timey,normal)

        pen1.makePoints(
            self.data['settings']['chunk-x']
            ,self.data['settings']['chunk-y']
            ,self.boundary,timey
            
            ,self.data['settings']['chunk-x']
            *self.data['settings']['bounds'][0]
            ,self.data['settings']['chunk-y']
            *self.data['settings']['bounds'][1]
            ,self.interval
            )
        pen2.makePoints(
            self.data['settings']['chunk-x']
            ,self.data['settings']['chunk-y']
            ,self.boundary,timey
            
            ,self.data['settings']['chunk-x']
            *self.data['settings']['bounds'][0]
            ,self.data['settings']['chunk-y']
            *self.data['settings']['bounds'][1]
            ,self.interval
            )
        self.seperate(pen1,pen2)

    def seperate(self,pen1,pen2):
        pass
        past = self.satCheak(pen1,pen2)
        #print past
        if past != False:
            normal,depth = past
            cmLine = vectorMath.toVector(
                pen1.x,pen1.y,pen2.x,pen2.y
                )
            cmLine = vectorMath.normalise(cmLine)
            normal = vectorMath.normalise(normal)
            if vectorMath.dot(cmLine,normal) < 0:
                normal = (-normal[0],-normal[1])

            normal = vectorMath.scale(depth,normal)
            pen1.x -= normal[0]
            pen1.y -= normal[1]
            pen2.x += normal[0]
            pen2.y += normal[1]
            
            """
            print 'ERROR: CLIP FAILURE'
            print 'PEN ONE ->',pen1.name
            print 'PEN TWO ->',pen2.name
            print 'NORMAL ->',normal
            print 'DEPTH ->',depth
            raise AssertionError
            """
            
    def projPenAxis(self,axis,pen):
        d = vectorMath.dotProduct(
            axis,vectorMath.minVector(
                pen.points[0],(pen.x,pen.y)
                )
            )
        minNum = maxNum = d
        
        for i in range(0,len(pen.points)):
            d = vectorMath.dotProduct(
                axis,vectorMath.minVector(
                    pen.points[i],(pen.x,pen.y)
                    )
                )

            #print d
            if d < minNum: minNum = d
            elif d > maxNum: maxNum = d

        return(minNum,maxNum)

    def projPenAxis2(self,axis,pen):
        d = vectorMath.dotProduct(
            axis,pen.points[0]
            )
        minNum = maxNum = d
        
        for i in range(0,len(pen.points)):
            d = vectorMath.dotProduct(
                axis,pen.points[i]
                )

            #print d
            if d < minNum: minNum = d
            elif d > maxNum: maxNum = d

        return(minNum,maxNum)
 
    def collideCheak(self,pens,timey,pensList=None):
        #print '-----------------'
        #pens = self.boundary[region]
        k = 0
        #pens = sorted(pens)
        
        #print pens,timey
        while k < len(pens):
            n = k+1
            while n < len(pens):
                #print n,k,'FARLANDSAA'
                pen1 = pens[k]
                pen2 = pens[n]

                points1 = pen1.points
                points2 = pen2.points

                allPast = True
                axes1,axes2 = [],[]
                data = self.satCheak(pen1,pen2)
                    
                if data != False:
                    #self.collideUpdate(
                    #    i,j,pen1,pen2,timey
                    #    )
                    """
                    i,j = cpoints[0]
                    self.collideResolve(
                        i,j,pen1,pen2,timey
                        ,cpoints
                        )
                    """
                    #print p1,p2
                    #self.updateDraw()
                    self.collideResolve(
                        data,pen1,pen2,timey
                        )
                    #raise Exception
                    
                n += 1
                #if n==k: n=k+1

            k += 1

    def satCheak(self,pen1,pen2):
        """
        collision detector seems give false negatives
        """
        cmLine = vectorMath.toVector(
            pen1.x,pen1.y,pen2.x,pen2.y
            )
        smallest = None
        minOverlap = float('inf')
        colour = None
        
        for i in range(len(pen1.points)):
            endi = (i+1)%len(pen1.points)
            axis = vectorMath.toVector(
                pen1.points[i][0]
                ,pen1.points[i][1]
                ,pen1.points[endi][0]
                ,pen1.points[endi][1]
                )
            axis = vectorMath.normalise(axis)
            #axis = vectorMath.perp(axis) #AEP-1
            #axis = vectorMath.minVector((0,0),axis)
            #if vectorMath.dotProduct(cmLine,axis) <= 0:
            #    axis = (-axis[0],-axis[1])
            
            p1 = self.projPenAxis2(axis,pen1)
            p2 = self.projPenAxis2(axis,pen2)
            if not vectorMath.overlap(p1,p2):
                return(False)
            else:
                #print i,'COUNT',p1,p2
                overlap = vectorMath.getOverlap(p1,p2)
                cond1 = vectorMath.ifContains(p1,p2)
                cond2 = vectorMath.ifContains(p2,p1)
                
                if (cond1 or cond2) == True:
                    mins = abs(min(p1)-min(p2))
                    maxs = abs(max(p1)-max(p2))
                    #print i,'MINMAX',mins,maxs
                    if (mins<maxs):
                        overlap += mins
                    else:
                        overlap += maxs
                
                if overlap < minOverlap:
                    #print i,'PURPLE:',overlap,axis
                    minOverlap = overlap
                    smallest = axis
                    c1,c2 = pen1.points[i],pen1.points[endi]
                    colour = 'purple'

        for j in range(len(pen2.points)):
            endj = (j+1)%(len(pen2.points))
            axis = vectorMath.toVector(
                pen2.points[j][0]
                ,pen2.points[j][1]
                ,pen2.points[endj][0]
                ,pen2.points[endj][1]
                )
            axis = vectorMath.normalise(axis)
            #axis = vectorMath.perp(axis) #AEP-1
            #axis = vectorMath.minVector((0,0),axis)
            #if vectorMath.dotProduct(cmLine,axis) >= 0:
            #    axis = (-axis[0],-axis[1])
            
            p1 = self.projPenAxis2(axis,pen1)
            p2 = self.projPenAxis2(axis,pen2)
            if not vectorMath.overlap(p1,p2):
                return(False)
            else:
                #print j,p1,p2
                overlap = vectorMath.getOverlap(p1,p2)
                cond1 = vectorMath.ifContains(p1,p2)
                cond2 = vectorMath.ifContains(p2,p1)
                
                if (cond1 or cond2) == True:
                    mins = abs(min(p1)-min(p2))
                    maxs = abs(max(p1)-max(p2))
                    #print j,mins,maxs
                    if (mins<maxs):
                        overlap += mins
                    else:
                        overlap += maxs
                        
                if overlap < minOverlap:
                    #print j,'BLUE:',overlap,axis
                    
                    minOverlap = overlap
                    smallest = axis
                    c1,c2 = pen2.points[j],pen2.points[endj]
                    colour = 'pink'

        self.makeLines(
            (0,0)
            ,(
            (c1,c2)
            ,) 
            ,fill=colour
            ,kill=True #False
            )

        #print smallest,overlap,'SGAVUIKFA IUSF'
        #if vectorMath.dotProduct(cmLine,smallest) < 0:
        #    smallest = vectorMath.minVector((0,0),smallest)
        return(smallest,minOverlap)

    def adjustPt(self,point):
        ans = (
            self.disp[0][0]+point[0]*self.disp[0][1],
            self.disp[1][0]+point[1]*self.disp[1][1]
            )
        #print self.disp[0][1],self.disp[1][1]
        #print point,ans
        return(ans)
    
            
    def updateDraw(self):
        #print(random.choice(range(100)))
        """
        apparently tkinter accepts config coordinates
        as a tuple in the form of (x1,y1,x2,y2,x3,y3...)
        """
        for penName in self.pens:
            points = []
            pen = self.pens[penName]
            for point in pen.points:
                point = tuple(point)
                point = self.adjustPt(point)
                points.extend(
                    (int(point[0]),int(point[1]))
                    )

            #print Tkinter._flatten(points)
            self.canvas.coords(
                'PEN:'+penName,tuple(points)
                )

class safeParse(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid(pady=(2,4))
        self.count = 0
    
    def run(self):
        self.entry = Text(self
            ,relief='flat',height=2
            ,fg='grey22',selectbackground='#79e0bb'
            ,insertbackground='grey12'
            )
        self.entry.grid(
            row=100,column=100,sticky='ew'
            ,pady=(1,1)
            )
        self.bttn1 = Label(self
            ,text='Enter'
            ,font=('calibri',14),relief='flat'
            ,fg='grey95',bg='grey22'
            )
        self.bttn1.bind('<ButtonPress-1>'   ,self.pressOnn  )
        self.bttn1.bind('<ButtonRelease-1>' ,self.pressOff  )
        self.bttn1.bind('<Enter>'           ,self.enter     )
        self.bttn1.bind('<Leave>'           ,self.leave     )
        self.bttn1.grid(
            row=100,column=200
            ,sticky='ns'
            ,ipadx=13
            )

    def enter(self,event):
        self.bttn1.config(text='> Enter')
    def leave(self,event):
        self.bttn1.config(text='Enter')

    def pressOnn(self,event):
        self.bttn1.config(bg='grey12')
        self.execData()

    def pressOff(self,event):
        self.bttn1.config(bg='grey22')
    
    def execData(self):
        self.entry.config(relief='flat')
        data = self.entry.get(1.0,END)[:-1].strip()
        print 'IN[%s]: '%self.count,data
            
        try:
            #data = self.entry.get(1.0,END)[:-1].strip()
            #print 'INN[%s]: '%self.count,data
            if data != '':
                exec(data)
                #print 'OUT[%s]: '%self.count,eval(data)
            else: pass

            #self.count += 1
            
        except Exception as e:
            self.errorInfo(e)

        finally:
            self.count += 1

    def errorInfo(self,inst):
        error = (traceback.format_tb(sys.exc_info()[2]))
        print '--------------------'*2
        error[-1] = error[-1][:-1]
        for piece in error:
            print piece
        print '--------------------'*2+'\n'
        
        print type(inst)   
        print inst.args 
        print inst
            
if __name__ == '__main__':
    root = Tk()
    root.title('pyPhysics 0-30')
    simul = loop(root)

    simul.initGui()
    simul.make()
    pens = simul.pens
    simul.grid()
    simul.initDraw()
    simul.after(100,simul.startGame)
    #thread.start_new_thread(simul.mainloop,())
    simul.mainloop()
    raw_input('press enter to leave ')
