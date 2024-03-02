import vectorMath2
import math

vectorMath = vectorMath2.mathy()

class pen(object):
    def __init__(self
        ,name,length,breath
        ,mass=22
        ,colour='grey22'
        ,damper=1
        ,x=0,y=0,vx=0,vy=0
        ,a=0,va=0
        ,fx=lambda x:0
        ,fy=lambda x:0
        ,fa=lambda x:0
        ,e=1
        ,anchor=lambda x:x
        ):
        self.name = name
        self.colour = colour
        if type(length) != list:
            length = [length/2.0,length/2.0]
        if type(breath) != list:
            breath = [breath/2.0,breath/2.0]
            
        self.length = length
        self.breath = breath
        self.invMass = mass**-1
        self.inertia = 0
        self.mass = float(mass)
        
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.fx = fx
        self.fy = fy

        self.a = a
        self.va = va
        self.fa = fa
        self.e = e

        self.points = ()
        self.anchor = anchor
        self.makeInertia(damper)

    def changeAnchor(self,func):
        self.anchor = func        

    def makeInertia(self,damper=1):
        h1,h2 = self.breath
        b1,b2 = self.length
        h1 = float(h1)
        h2 = float(h2)
        b1 = float(b1)
        b2 = float(b2)
        m1,m2,m3,m4 = vectorMath.chopMass(
            self.length,self.breath
            ,self.mass/(damper*(b1+b2)*(h1+h2))
            )

        i1 = b1*h1*(b1**2+h1**2)*m1/12
        i2 = b2*h1*(b2**2+h1**2)*m2/12
        i3 = b1*h2*(b1**2+h2**2)*m3/12
        i4 = b2*h2*(b2**2+h2**2)*m4/12
        self.inertia = float(i1+i2+i3+i4)/self.mass
        print i1,i2,i3,i4,self.inertia

    def cheakRest(self,maxx,maxy):
        can = False
        point = False
        points = self.points
        
        for k in range(len(points)):
            p1 = points[k]
            cheak1 = vectorMath.cheakOver(p1,maxx,maxy)
            if cheak1[0] == True:
                end = (k+1)%len(points)
                p2 = points[end]
                
                cheak2 = vectorMath.cheakOver(p2,maxx,maxy)
                if cheak2[0]==True and cheak1[1]==cheak2[1]:
                    #print(cheak1,'{S*AD YAS*ND }')
                    point = cheak1[1]
                    can = True
                    break
                else: pass
            else: pass

        return(can,point)

    def getRegion2(self,chunkx,chunky):
        #x1 = int((self.pt1[0]//chunkx)*chunkx)
        #y1 = int((self.pt1[1]//chunky)*chunky)
        #x2 = int((self.pt2[0]//chunkx)*chunkx)
        #y2 = int((self.pt2[1]//chunky)*chunky)
        #x3 = int((self.pt3[0]//chunkx)*chunkx)
        #y3 = int((self.pt3[1]//chunky)*chunky)
        #x4 = int((self.pt4[0]//chunkx)*chunkx)
        #y4 = int((self.pt4[1]//chunky)*chunky)
        #coords = ((x1,y1),(x2,y2),(x3,y3),(x4,y4))
        """
        do note that bounding regions must be taken
        into account for line segments BETWEEN points,
        rather than just the points themselves

        furthermore, as the line coordinates must be
        incremented from min as max, hence the sorting
        """
        final = []
        
        for k in range(len(self.points)):
            end = (k+1)%(len(self.points))
            x1 = int((self.points[k][0]//chunkx)*chunkx)
            y1 = int((self.points[k][1]//chunky)*chunky)
            x2 = int((self.points[end][0]//chunkx)*chunkx)
            y2 = int((self.points[end][1]//chunky)*chunky)
            minx = min((x1,x2))
            miny = min((y1,y2))
            maxx = max((x1,x2))
            maxy = max((y1,y2))

            if (minx,miny) not in final:
                final.append((minx,miny))
            elif (maxx,maxy) not in final:
                final.append((maxx,maxy))

            startx = minx//chunkx
            for i in range(0,(maxx-minx)//chunkx+1):
                ans = vectorMath.gradCrossIn(
                    self.points[k],self.points[end]
                    ,((startx+i)*chunkx,0)
                    ,((startx+i)*chunkx,float('inf'))
                    )
                if ans != False:
                    modx = int((ans[0]//chunkx)*chunkx)
                    mody = int((ans[1]//chunky)*chunky)
                    if (modx,mody) not in final:
                        final.append((modx,mody))

            starty = miny//chunky
            for i in range(0,(maxy-miny)//chunky+1):
                ans = vectorMath.gradCrossIn(
                    self.points[k],self.points[end]
                    ,(0,(starty+i)*chunky)
                    ,(float('inf'),(starty+i)*chunky)
                    )
                if ans != False:
                    modx = int((ans[0]//chunkx)*chunkx)
                    mody = int((ans[1]//chunky)*chunky)
                    if (modx,mody) not in final:
                        final.append((modx,mody))

        return(final)
        
    def makePoints(self
        ,chunkx,chunky,boundary,timey
        ,maxx,maxy,interval=10
        ,kill=False,cheak=[]
        ):
        #self.pt1 
        #print 'asdasd',[self.length]
        """
        x1 = int((self.pt1[0]//chunkx)*chunkx)
        y1 = int((self.pt1[1]//chunky)*chunky)
        x2 = int((self.pt2[0]//chunkx)*chunkx)
        y2 = int((self.pt2[1]//chunky)*chunky)
        x3 = int((self.pt3[0]//chunkx)*chunkx)
        y3 = int((self.pt3[1]//chunky)*chunky)
        x4 = int((self.pt4[0]//chunkx)*chunkx)
        y4 = int((self.pt4[1]//chunky)*chunky)
        """
        """
        cx,cy = chunkx,chunky
        for thing in boundary[(x1,y1,x1+cx,y1+cy)]:
            if thing[0] == self.name
        """
        coords = self.getRegion2(chunkx,chunky)

        cx,cy = chunkx,chunky
        pt1,pt2,pt3,pt4 = self.getPoints(
            self.x,self.y,self.a
            ,self.length,self.breath
            )
        past,point = vectorMath.cheakData(
            (pt1,pt2,pt3,pt4),maxx,maxy
            )

        #coords = ((x1,y1),(x2,y2),(x3,y3),(x4,y4))
        for k in range(len(coords)):
            x,y = coords[k]
            if x<0: x=0
            if y<0: y=0
            if self in boundary[(x,y,x+cx,y+cy)]:
                #del boundary[(x,y,x+cx,y+cy)][self.name]
                boundary[(x,y,x+cx,y+cy)].remove(self)
                
        #print cheak[0]
        xneg = None
        yneg = None
        cheakRest = self.cheakRest(maxx,maxy)
        if cheakRest[0] == True:
            #print('PYTHON TESTING')
            cheakRest = cheakRest[1]
            if cheakRest == 1:
                self.vx = max([self.vx,0])
                xneg = False
            elif cheakRest == 2:
                self.vx = min([self.vx,0])
                xneg = True
            elif cheakRest == 3:
                self.vy = min([self.vy,0])
                yneg = False
            elif cheakRest == 4:
                self.vy = max([self.vy,0])
                yneg = True
        
        if past == False:
            self.points = (pt1,pt2,pt3,pt4)
            self.boundFix(boundary,cheak,chunkx,chunky)

        elif past == True:
            tell = False
            #if self.name == 'blob':
                #print 'FARKING BLOB'
                #tell = True
                
            self.unUpdate(maxx,maxy,timey)
            """
            #print 'SJOKD ASLH NDUOISABDF'
            self.x,self.vx = vectorMath.revSemiEuler(
                self.x,self.vx,self.fx
                ,timey,runs=1 #interval
                )[0]
            self.y,self.vy  = vectorMath.revSemiEuler(
                self.y,self.vy,self.fy
                ,timey,runs=1 #interval
                )[0]
            self.a,self.va  = vectorMath.revSemiEuler(
                self.a,self.va,self.fa
                ,timey,runs=1 #interval
                )[0]
            """
            points = (pt1,pt2,pt3,pt4)
            past,point = vectorMath.cheakData(
                points,maxx,maxy
                )

            if point[1] == 1:
                normal = [1,0]
            elif point[1] == 2:
                normal = [-1,0]
            elif point[1] == 3:
                normal = [0,-1]
            elif point[1] == 4:
                normal = [0,1]

            pt1,pt2,pt3,pt4 = self.getPoints(
                self.x,self.y,self.a
                ,self.length,self.breath
                )
            #points = (pt1,pt2,pt3,pt4)
            part = points[point[0]-1]
            rap = vectorMath.toVector(
                self.x,self.y,part[0],part[1]
                )
            vcm = (self.vx,self.vy)
            vab = vectorMath.addVector(
                vcm,vectorMath.scale(
                math.radians(self.va),vectorMath.perp(rap)
                ))
            #print vab
            j = vectorMath.collide(
                self.e,vab,rap,(1,1)
                ,self.inertia,float('inf')
                ,normal,self.mass,float('inf')
                )
            
            #print self.vx,self.vy,self.va,'PRE DAT'
            x = self.x
            y = self.y
            a = self.a
            nvx = (j/self.mass)*normal[0]
            nvy = (j/self.mass)*normal[1]
            nva = math.degrees(
                vectorMath.dotProduct(
                vectorMath.perp(rap)
                ,vectorMath.scale(j,normal)
                )/self.inertia
                )

            if tell == True:
                print('NORMAL',normal)
                print('ARGHHH ADD',nvx,nvy,nva)
                print('ARGHHH BFT',self.vx,self.vy,self.va)
            
            self.vx = self.vx+nvx
            self.vy = self.vy+nvy
            self.va = self.va+nva
            #print self.vx,self.vy,self.va,'AFT DAT'
            #self.update()

            if tell == True:
                print('ARGHHH AFT',self.vx,self.vy,self.va)

            self.update(maxx,maxy,timey)
            pt1,pt2,pt3,pt4 = self.getPoints(
                self.x,self.y,self.a
                ,self.length,self.breath
                )
            self.points = (pt1,pt2,pt3,pt4)
            self.boundFix(boundary,cheak,chunkx,chunky)

            if kill == False:
                kill = True
                ######################################
                #self.update(maxx,maxy,timey)
                ######################################
                # UPDATING REMOVED to fix boundary
                # bugs. everything updated already above
                ######################################
                self.makePoints(
                chunkx,chunky,boundary,timey
                ,maxx,maxy,interval,kill
                )

        self.points = (pt1,pt2,pt3,pt4)
        self.boundFix(boundary,cheak,chunkx,chunky)
        
    def boundFix(self,boundary,cheak,chunkx,chunky):
        """
        cx,cy = chunkx,chunky
        x1 = int((self.pt1[0]//chunkx)*chunkx)
        y1 = int((self.pt1[1]//chunky)*chunky)
        x2 = int((self.pt2[0]//chunkx)*chunkx)
        y2 = int((self.pt2[1]//chunky)*chunky)
        x3 = int((self.pt3[0]//chunkx)*chunkx)
        y3 = int((self.pt3[1]//chunky)*chunky)
        x4 = int((self.pt4[0]//chunkx)*chunkx)
        y4 = int((self.pt4[1]//chunky)*chunky)
        
        coords = ((x1,y1),(x2,y2),(x3,y3),(x4,y4))
        """
        cx,cy = chunkx,chunky
        coords = self.getRegion2(chunkx,chunky)
        
        for k in range(len(coords)):
            x,y = coords[k]
            if x<0: x=0
            if y<0: y=0
            if k == 0:
                m = 4
            else:
                m = k

            try:
                if self in boundary[(x,y,x+cx,y+cy)]:
                    break
                else:
                    boundary[(x,y,x+cx,y+cy)].append(self)
                    if (x,y,x+cx,y+cy) not in cheak:
                        cheak.append((x,y,x+cx,y+cy))
                    else: pass

            except KeyError:
                pass
            
            """
            if self.name in boundary[(x,y,x+cx,y+cy)]:
                listy = boundary[(x,y,x+cx,y+cy)][self.name]
                    
                if m not in listy:
                    listy.append(m)
                    listy.append(k)
                if (k+1) not in listy:
                    listy.append(k+1)
                if (k+2)%4+1 not in listy:
                    listy.append((k+2)%4+1)
                
            else:
                boundary[(x,y,x+cx,y+cy)][self.name] = [
                m,k+1,(k+2)%4+1
                ]
            """

    def getPoints(self,x,y,a,length,breath):
        pt1 = vectorMath.rotate3(
            x,y,x-length[0],y-breath[0],a
            )
        pt2 = vectorMath.rotate3(
            x,y,x+length[1],y-breath[0],a
            )
        pt3 = vectorMath.rotate3(
            x,y,x+length[1],y+breath[1],a
            )
        pt4 = vectorMath.rotate3(
            x,y,x-length[0],y+breath[1],a
            )
        return(pt1,pt2,pt3,pt4)
        
    def update(self,maxx,maxy,timey=[0,60**-1]):
        cheak = self.cheakRest(maxx,maxy)
        vx = self.vx
        vy = self.vy
        fx = self.fx
        fy = self.fy
        xneg = None
        yneg = None
        if cheak[0] == True:
            #print('PYTHON TESTING')
            cheak = cheak[1]
            if cheak == 1:
                self.vx = max([self.vx,0])
                xneg = False
            elif cheak == 2:
                self.vx = min([self.vx,0])
                xneg = True
            elif cheak == 3:
                self.vy = min([self.vy,0])
                yneg = False
            elif cheak == 4:
                self.vy = max([self.vy,0])
                yneg = True
        
        self.x,self.vx = vectorMath.semiEuler2(
            self.x,vx,fx,timey,
            runs=1 #,neg=xneg
            )
        #if yneg != None: print yneg
        self.y,self.vy = vectorMath.semiEuler2(
            self.y,vy,fy,timey,
            runs=1 #,neg=yneg
            )
        self.a,self.va = vectorMath.semiEuler2(
            self.a,self.va,self.fa,timey,
            runs=1
            )

    def unUpdate(self,maxx,maxy,timey=[0,60**-1]):
        cheak = self.cheakRest(maxx,maxy)
        vx = self.vx
        vy = self.vy
        fx = self.fx
        fy = self.fy

        self.x,self.vx = vectorMath.revSemiEuler(
            self.x,vx,fx,timey,runs=1
            )[-1]
        self.y,self.vy = vectorMath.revSemiEuler(
            self.y,vy,fy,timey,runs=1
            )[-1]
        self.a,self.va = vectorMath.revSemiEuler(
            self.a,self.va,self.fa,timey,runs=1
            )[-1]
