from math import *
import math

"""
double integrator given force equation
given as lambda expression
swapped order of x and v being incremented
as it's more accurate that way
"""

class mathy(object):
    def linesToCenter(self,a,b):
        aInv = self.perp(a)
        bInv = self.perp(b)
        # to be added
        return(aInv,bInv)

    def getAngle2(self,a,b,clockwise=True,degrees=True):
        # measures angle of b from a
        # the original function might very well be wrong
        # make apropriate edits for polygon 0-10
        a = self.normalise(a)
        b = self.normalise(b)
        angle = -math.atan2(a[0]*b[1]-a[1]*b[0],a[0]*b[0]+a[1]*b[1])

        while angle<0: angle+=2*math.pi
        if clockwise == False:
            angle = 2*math.pi-angle
        if degrees == True:
            angle = math.degrees(angle)
            
        return(angle)
    
    def cross(self,a,b):
        return(a[0]*b[1]-a[1]*b[0])
    
    def getLines(self,a,b,c,d):
        pt1 = self.ptInvLine(a,b,c,clip=True)
        pt2 = self.ptInvLine(a,b,d,clip=True)
        return((pt1,c),(pt1,d),(pt2,c),(pt2,d))

    def acMinLines(self,a,b,c,d):
        """
        test.minLine((5,5),(8,6),(6,9),(4,8))
        test.minLine((0,1),(8,6),(6,9),(4,1))
        not currently used for anything
        nor planned to
        """
        pt1 = self.ptInvLine(a,b,c,clip=True)
        pt2 = self.ptInvLine(a,b,d,clip=True)
        
        if self.ptInLine(a,b,pt1) == False:
            ac = self.toVector(a[0],a[1],c[0],c[1])
            bc = self.toVector(b[0],b[1],c[0],c[1])
            lenAc = self.getLength(ac)
            lenBc = self.getLength(bc)
            
            if lenAc > lenBc: pt1 = b
            else: pt1 = a

        if self.ptInLine(a,b,pt2) == False:
            ad = self.toVector(a[0],a[1],d[0],d[1])
            bd = self.toVector(b[0],b[1],d[0],d[1])
            lenAd = self.getLength(ad)
            lenBd = self.getLength(bd)
            
            if lenAd > lenBd: pt2 = b
            else: pt2 = a

        return((pt1,c),(pt2,d))

    def minLine(self,a,b,c,d):
        """
        test.minLine((5,5),(8,6),(6,9),(4,8))
        test.minLine((0,1),(8,6),(6,9),(4,1))
        not currently used for anything
        nor planned to
        """
        pt1 = self.ptInvLine(a,b,c,clip=True)
        pt2 = self.ptInvLine(a,b,d,clip=True)
        
        if self.ptInLine(a,b,pt1) == False:
            ac = self.toVector(a[0],a[1],c[0],c[1])
            bc = self.toVector(b[0],b[1],c[0],c[1])
            lenAc = self.getLength(ac)
            lenBc = self.getLength(bc)
            
            if lenAc > lenBc: pt1 = b
            else: pt1 = a

        if self.ptInLine(a,b,pt2) == False:
            ad = self.toVector(a[0],a[1],d[0],d[1])
            bd = self.toVector(b[0],b[1],d[0],d[1])
            lenAd = self.getLength(ad)
            lenBd = self.getLength(bd)
            
            if lenAd > lenBd: pt2 = b
            else: pt2 = a

        line1 = self.toVector(
            pt1[0],pt1[1],c[0],c[1]
            )
        line2 = self.toVector(
            pt2[0],pt2[1],d[0],d[1]
            )
        length1 = self.getLength(line1)
        length2 = self.getLength(line2)

        if length1 > length2: ans = (pt1,c)
        else: ans = (pt2,d)

        return(ans)

    def ptInLine(self,a,b,pt):
        cond1 = (a[0]>=pt[0]>=b[0])
        cond2 = (b[0]>=pt[0]>=a[0])
        cond3 = (a[1]>=pt[1]>=b[1])
        cond4 = (b[1]>=pt[1]>=a[1])
        if not(cond1 or cond2) == True:
            can = False
        elif not(cond3 or cond4) == True:
            can = False
        else:
            cross = self.ptInvLine(a,b,pt)
            if cross == pt:
                can = True
            else:
                can = False

        return(can)

    def vecDrct(self,a,b):
        a = self.normalise(a)
        b = self.normalise(b)
        if self.dotProduct(a,b) < 0:
            drct = False
        else:
            drct = True

        return(drct)
    
    def toVector(self,x1,y1,x2,y2):
        return(x2-x1,y2-y1)

    def flip(self,vector):
        assert(len(vector)==2)
        return(vector[1],vector[0])

    def cheak(self,length,breath,m1,m2,m3,m4,m):
        h1,h2 = breath
        b1,b2 = length
        h1 = float(h1)
        h2 = float(h2)
        b1 = float(b1)
        b2 = float(b2)
        
        print((m1+m3)*b1,(m2+m4)*b2)
        print((m1+m2)*h1,(m3+m4)*h2)
        print(m1*b1*h1+m2*b2*h1+m3*b1*h2+m4*b2*h2)
        print(m*(b1+b2)*(h1+h2))

    def ifParallel(self,a,b,c,d,thres=0.5):
        #print(a,b,c,d,'BBABABABABABP')
        line1 = self.toVector(a[0],a[1],b[0],b[1])
        line2 = self.toVector(c[0],c[1],d[0],d[1])
        #print line1,line2,'QWERTYUIOP'
        angle = self.getAngle(line1,line2)
        while angle>=90: angle-=180
        #print 'ANGULARTION',angle
        #if abs(angle%90)<thres:
        #    print 'PRALLELSIUMS'#,random.choice(range(100))
        if abs(angle)<thres: return(True)
        else: return(False)

    def ptInvLine(self,a,b,x,clip=False):
        """
        gets the equation of line perpendicular to ab
        and cutting through c
        test.ptInvLine((5,5),(10,11),(17,15))
        test.ptInvLine((5,5),(10,11),(17,15),True)
        """
        try:
            m,c = self.getGrad(a,b)
            if m == 0:
                coords = (x[0],c)
            else:
                #print 'DERP DERP',m
                m2 = -m**-1
                c2 = x[1]-m2*x[0]
                coords = self.gradCrossGrad(m,c,m2,c2)
                
        except ZeroDivisionError:
            #print 'MONSCRIPT'
            m = 0
            c = x[1]
            assert(a[0]==b[0])
            coords = (a[0],c)

        if clip == True:
            if self.ptInLine(a,b,coords) == False:
                len1 = self.getLength(
                    (a[0]-coords[0],a[1]-coords[1])
                    )
                len2 = self.getLength(
                    (b[0]-coords[0],b[1]-coords[1])
                    )
                if len1 > len2: coords = b
                else: coords = a
            
        return(coords)
            
    def chopMass(self,length,breath,mass):
        """
        test.chopMass([100,20],[100,20],20)
        test.chopMass([80,50],[90,25],20)
        """
        h1,h2 = breath
        b1,b2 = length
        h1 = float(h1)
        h2 = float(h2)
        b1 = float(b1)
        b2 = float(b2)
        m = float(mass)

        mx1 = m*(b1+b2)/(2*b1)
        mx2 = m*(b1+b2)/(2*b2)
        m1 = mx1*(h1+h2)/(2*h1)
        m3 = mx1*(h1+h2)/(2*h2)
        m2 = mx2*(h1+h2)/(2*h1)
        m4 = mx2*(h1+h2)/(2*h2)

        #print(self.cheak(length,breath,m1,m2,m3,m4,m))
        return(m1,m2,m3,m4)
        
    def cheakData(self,data,maxx,maxy):
        past = False
        point = None
        for k in range(len(data)):
            part = data[k]
            if part[0]<0.5:
                point = (k+1,1)
                past = True
                break
            elif part[0]>maxx-0.5:
                point = (k+1,2)
                past = True
                break
            elif part[1]<0.5:
                point = (k+1,3)
                past = True
                break
            elif part[1]>maxy-0.5:
                point = (k+1,4)
                past = True
                break
                
        return(past,point)

    def cheakOver(self,part,maxx,maxy):
        past = False
        point = None
        if part[0]<=1:
            point = 1
            past = True
            #break
        elif part[0]>=maxx-1:
            point = 2
            past = True
            #break
        elif part[1]<=1:
            point = 3
            past = True
            #break
        elif part[1]>=maxy-1:
            point = 4
            past = True
            #break

        return(past,point)
    
    def datSemiEuler(self,x,v,func,limit,runs=60,neg=None):
        """
        test.datSemiEuler(0,0,lambda x:10*x ,[0,1])
        test.datSemiEuler(0,0,lambda x:2*x**2 ,[0,1])
        """
        data = []
        a,b = float(limit[0]),float(limit[1])
        step = (b-a)/float(runs)

        data.append((x,v))
        for k in range(1,runs+1):
            #step = (b-a)/float(runs)
            #print a+k*step
            fdv = func(a+k*step)
            if fdv>0 and neg==True:
                fdv = 0
            elif fdv<0 and neg==False:
                fdv = 0
            elif neg == bool:
                fdv = 0
            
            #print a+k*step,fdv
            x += step*v
            v += step*fdv
            data.append((x,v))
                        
        return(data)
    
    def revSemiEuler(self,x,v,func,limit,runs=60,neg=None):
        """
        reverse semi euler
        test.revSemiEuler(
            test.semiEuler2(10,12,lambda x:10*x ,[0,1])[0]
            ,test.semiEuler2(10,12,lambda x:10*x ,[0,1])[1]
            ,lambda x:10*x ,[0,1]
            )
        """
        data = []
        a,b = float(limit[0]),float(limit[1])
        step = (b-a)/float(runs)
        
        for k in range(0,runs):
            #step = (b-a)/float(runs)
            #print a+k*step
            fdv = func(b-k*step)
            if fdv>0 and neg==True:
                fdv = 0
            elif fdv<0 and neg==False:
                fdv = 0
            elif neg == bool:
                fdv = 0
            
            #print a+k*step,fdv
            v -= step*fdv
            x -= step*v

            data.append((x,v))

        return(data)
    
    def semiEuler2(self,x,v,func,limit,runs=60,neg=None):
        """
        test.semiEuler2(0,0,lambda x:10*x ,[0,1])
        test.semiEuler2(0,0,lambda x:2*x**2 ,[0,1])
        """
        x0,v0 = x,v
        a,b = float(limit[0]),float(limit[1])
        step = (b-a)/float(runs)

        for k in range(1,runs+1):
            #step = (b-a)/float(runs)
            #print a+k*step
            fdv = func(a+k*step)
            if fdv>0 and neg==True:
                fdv = 0
            elif fdv<0 and neg==False:
                fdv = 0
            elif neg == bool:
                fdv = 0
                
            #print a+k*step,fdv
            #v += step*fdv
            x += step*v
            v += step*fdv

        #if abs(x0-x)<0.1: x=x0
        return(x,v)
    
    def semiEuler(self,x,v,f,var,limit,runs=60):
        """
        test.semiEuler(0,0,'10*(t)','t',[0,1])
        test.semiEuler(0,0,'2*(t**2)','t',[0,1])
        """
        a,b = float(limit[0]),float(limit[1])
        for k in range(1,runs+1):
            step = (b-a)/float(runs)
            #print a+k*step
            fdv = eval(f.replace(var,str(a+k*step)))
            #print a+k*step,fdv
            x += step*v
            v += step*fdv
            
        return(x,v)

    def getGrad(self,v1,v2):
        """
        test.getGrad([1,2],[5,3])
        test.getGrad([5,5],[5,110])
        """
        m = (v2[1]-v1[1])/float(v2[0]-v1[0])
        c = v1[1]-v1[0]*m
        return(m,c)

    def gradCross(self,a,b,c,d):
        """
        test.gradCross([0,0],[10,10],[5,5],[10,0])
        test.gradCross([0,0],[10,100],[0,10],[10,110])
        test.gradCross([972,0],[00,33],[0,0],[10,110])
        """
        cond1,cond2 = True,True
        try:
            m1,c1 = self.getGrad(a,b)
        except ZeroDivisionError:
            cond1 = False
        try:
            m2,c2 = self.getGrad(c,d)
        except ZeroDivisionError:
            cond2 = False
            
        can = True

        if cond1 and cond2 == True:
            #print 'STRAFTING[1]'
            try:
                x = (c2-c1)/float(m1-m2)
                y = m1*x+c1
            except ZeroDivisionError:
                x = float('inf')
                y = m1*x+c1
                can = False
                
        elif cond1 == False:
            #print 'STRAFTING[2]'
            if cond2 == True:
                x = a[0]
                y = m2*x+c2
            else:
                x = float('inf')
                y = float('inf')

        elif cond2 == False:
            #print 'STRAFTING[3]'
            if cond1 == True:
                x = c[0]
                y = m1*x+c1
            else:
                x = float('inf')
                y = float('inf')
        
        return(x,y)

    def gradCrossGrad(self,m1,c1,m2,c2):
        """
        test.gradCrossGrad([0,0],[10,10],[5,5],[10,0])
        test.gradCrossGrad([0,0],[10,100],[0,10],[10,110])
        test.gradCrossGrad([972,0],[00,33],[0,0],[10,110])
        """
            
        try:
            x = (c2-c1)/float(m1-m2)
            y = m1*x+c1
        except ZeroDivisionError:
            x = float('inf')
            y = m1*x+c1
            can = False

        return(x,y)

    def gradCrossIn(self,a,b,c,d):
        """
        test.gradCrossIn([0,0],[10,10],[5,5],[10,0])
        test.gradCrossIn([0,0],[10,100],[0,10],[10,110])
        test.gradCrossIn([972,0],[00,33],[0,0],[10,110])
        test.gradCrossIn([0,0],[17,234],[10,0],[10,110])
        test.gradCrossIn([0,0],[17,234],[0,10],[float('inf'),10])
        test.gradCrossIn([0,0],[17,234],[10,10],[float('inf'),10])
        """
        ans = False
        cond1,cond2 = True,True
        try:
            m1,c1 = self.getGrad(a,b)
            #print('GET GRAD ONE')
        except ZeroDivisionError:
            cond1 = False
        try:
            m2,c2 = self.getGrad(c,d)
            #print('GET GRAD TWO')
        except ZeroDivisionError:
            cond2 = False
        
        try:
            if cond1 and cond2 == True:
                try:
                    x = (c2-c1)/float(m1-m2)
                    y = m1*x+c1
                    ans = (x,y)
                except ZeroDivisionError:
                    #x = float('inf')
                    #y = m1*x+c1
                    ans = False
                    
            elif cond1 == False:
                if cond2 == True:
                    x = a[0]
                    y = m2*x+c2
                    ans = (x,y)
                else:
                    ans = False

            elif cond2 == False:
                if cond1 == True:
                    x = c[0]
                    y = m1*x+c1
                    ans = (x,y)
                else:
                    ans = False
                    
        except ZeroDivisionError:
            #print 'ZERRO DIV ERROR'
            ans = False

        if ans != False:
            #print 'ANS IS NOT FALSE'
            cond = (
            ((a[0]<=x<=b[0]) or (a[0]>=x>=b[0]))
            and ((a[1]<=y<=b[1]) or (a[1]>=y>=b[1]))
            and ((c[0]<=x<=d[0]) or (c[0]>=x>=d[0]))
            and ((c[1]<=y<=d[1]) or (c[1]>=y>=d[1]))
            )
            if cond == False:
                ans = False

        """
        if ans == False:
            assert(self.ifPast3(a,b,c,d)==False)
        """ 
        return(ans)

    def ifContains(self,a,b):
        """
        cheak if a contains b
        test.ifContains((0,10),(2,4))
        """
        a = (min(a),max(a)) #should use sorted
        b = (min(b),max(b))
        ####################################
        # data must be sorted first b4 comparism
        # e.g. (2,4),(4,2)
        ####################################
        cond = ((b[0]>a[0]) and (b[1]<a[1])) 
        return(cond)

    def getOverlap(self,a,b):
        """
        test.getOverlap((0,3),(2,30)) 1 
        test.getOverlap((4,20),(-1,7)) 3
        test.getOverlap((1,10),(2,4)) 2
        test.getOverlap((0,3),(3,5)) 0
        test.getOverlap((-2,6),(-1,10)) 7
        """
        ans = min(max(a),max(b))-max(min(a),min(b))
        return(ans)

    def overlap(self,a,b):
        """
        test.overlap((0,10),(11,22))
        """
        aMax = max(a)
        aMin = min(a)
        bMax = max(b)
        bMin = min(b)
        if ((aMax < bMin) or (bMax < aMin)):
            return(False)
        else:
            return(True)
    
    def ccw(self,A,B,C):
        return((C[1]-A[1])*(B[0]-A[0])>=(B[1]-A[1])*(C[0]-A[0]))
    
    # Return true if line segments AB and CD intersect
    def ifPast(self,A,B,C,D):
        """
        test.ifPast([0,0],[10,10],[5,5],[10,0])
        """
        #print A,B,C,D
        return(
        (self.ccw(A,C,D) != self.ccw(B,C,D))
        and (self.ccw(A,B,C) != self.ccw(A,B,D))
        )

    def ifPast2(self,a,b,c,d):
        """
        test.ifPast2([0,0],[10,10],[5,5],[10,0])
        test.ifPast2([972,0],[00,33],[0,0],[10,110])
        test.ifPast2([972,0],[00,33],[20,20],[10,110])
        test.ifPast2([972,0],[00,33],[220,220],[10,110])
        """
        x,y = self.gradCross(a,b,c,d)
        minx = min(a[0],b[0])
        miny = min(a[1],b[1])
        maxx = max(a[0],b[0])
        maxy = max(a[1],b[1])

        cond1 = (maxx>x>minx)
        cond2 = (maxy>y>miny)
        minx = min(c[0],d[0])
        miny = min(c[1],d[1])
        maxx = max(c[0],d[0])
        maxy = max(c[1],d[1])

        cond3 = (maxx>x>minx)
        cond4 = (maxy>y>miny)
        return(cond1 and cond2 and cond3 and cond4)

    def ifPast3(self,a,b,c,d):
        """
        test.ifPast3([0,0],[10,10],[5,5],[10,0])
        test.ifPast3([972,0],[00,33],[0,0],[10,110])
        test.ifPast3([972,0],[00,33],[20,20],[10,110])
        test.ifPast3([972,0],[00,33],[220,220],[10,110])
        """
        
        x,y = self.gradCross(a,b,c,d)
        cond = (
            ((a[0]<=x<=b[0]) or (a[0]>=x>=b[0]))
            and ((a[1]<=y<=b[1]) or (a[1]>=y>=b[1]))
            and ((c[0]<=x<=d[0]) or (c[0]>=x>=d[0]))
            and ((c[1]<=y<=d[1]) or (c[1]>=y>=d[1]))
            )
        return(cond)
        
    def dotProduct(self,a,b):
        """
        test.dotProduct([1,3],[5,2])
        """
        assert(len(a)==len(b))

        ans = 0
        for k in range(len(a)):
            ans += a[k]*b[k]
        return(ans)

    def dot(self,a,b):
        return(self.dotProduct(a,b))

    def addVector(self,a,b):
        return((a[0]+b[0],a[1]+b[1]))

    def minVector(self,a,b):
        return(a[0]-b[0],a[1]-b[1])

    def midVector(self,a,b):
        return((a[0]+b[0])/2.0,(a[1]+b[1])/2.0)

    def scale(self,mul,vector):
        """
        new list needs to be created otherwise original
        data gets overwritten
        """
        new = []
        for k in range(len(vector)):
            new.append(vector[k]*mul)
        return(new)

    def normalise(self,vector):
        """
        test.normalise([4,9])
        test.normalise([7,6])
        """
        div = vector[0]**2+vector[1]**2
        if div != 0:
            new = self.scale(div**-0.5,vector)
        else:
            new = (0,0)
            
        return(new)
        
    def perp(self,vector):
        """
        test.perp([1.5,4])
        """
        assert(len(vector)==2)
        new = [-vector[1],vector[0]]
        return(new)

    def collide(self,e,vab,rap,rbp,ia,ib,normal,aMass,bMass):
        """
        test.collide(
        0.1,[3,4],[5,9],[6,3],
        12312,45212,[-0.5,7],19,21
        )
        test.collide(
        0.1,[3,4],[0,0],[1,0],
        12312,45212,[-0.5,7],19,float('inf')
        )
        """
        top = -(1+e)*self.dotProduct(vab,normal)
        rap = self.perp(rap)
        rbp = self.perp(rbp)
        
        pt1 = self.dotProduct(normal,normal)
        pt1 = pt1*(1.0/aMass+1.0/bMass)
        pt2 = (self.dotProduct(rap,normal)**2)/ia
        pt3 = (self.dotProduct(rbp,normal)**2)/ib
        j = top/(pt1+pt2+pt3)
        return(j)

    def getLength(self,vector):
        return((vector[0]**2+vector[1]**2)**0.5)

    def project(self,a,b):
        #ans = self.para(a,self.projection(a,b))
        ans = []
        dp = self.dotProduct(a,b)
        ans.append(float(dp)/(b[0]**2+b[1]**2)*b[0])
        ans.append(float(dp)/(b[0]**2+b[1]**2)*b[1])
        return(ans)

    def projectold(self,a,b):
        ans = self.para(a,self.projection(a,b))
        return(ans)

    def projection(self,a,b):
        lengtha = self.getLength(a)
        lengthb = self.getLength(b)
        proj = (a[0]*b[0]+a[1]*b[1])/lengthb
        return(proj)

    def para(self,vector,u=1):
        length = self.getLength(vector)
        vector = self.scale(u/length,vector)
        return(vector)

    def atan2(self,y,x):
        y = math.radians(y)
        x = math.radians(x)
        
        ans = 0
        if x>0:
            ans = math.atan(y/x)
        elif y>=0 and x<0:
            ans = math.atan(y/x)+math.pi
        elif y<0 and x<0:
            ans = math.atan(y/x)-math.pi
        elif y>0 and x==0:
            ans = math.pi/2
        elif y<0 and x==0:
            ans = -math.pi/2
        elif x==0 and y==0:
            ans = float('inf')
        else:
            raise ValueError

        return(math.degrees(ans))

    def isLeft(self,b,c,ref=None):
        if ref == None: ref = (0,0)
        pt1 = (b[0]-ref[0])*(c[1]-ref[1])
        pt2 = (b[1]-ref[1])*(c[0]-ref[0])
        if pt1-pt2 > 0: return(True)
        else: return(False)
        
    def getAngle(self,a,b,clockwise=None):
        """
        calculates the angle of vector b FROM
        vector a
        test.getAngle([0,1],[1,1],clockwise=True)
        -> 45
        """
        try:
            a = self.normalise(a)
        except ZeroDivisionError:
            a = (0,0)
        try:
            b = self.normalise(b)
        except ZeroDivisionError:
            b = (0,0)
            
        angle = math.acos(self.dotProduct(a,b))
        angle = math.degrees(angle)
        lefty = self.isLeft(a,b)
        
        if clockwise == None: pass
        elif (lefty and clockwise) == True:
            angle = angle-360
        elif (lefty or clockwise) == False:
            angle = angle-360
            
        return(angle)
    
    def rotate2(self,x0,y0,x1,y1,angle):
        # test.rotate2(440,150,480,155,0)
        # test.rotate2(440,150,460,1465,0)
        angle = -angle-90
        radius = ((y1-y0)**2+(x1-x0)**2)**0.5
        alpha = acos((x1-x0)/radius)
        angle = radians(angle)

        r = 1
        cond2 = (y0>y1)
        #print(cond1,cond2)
        if (cond2): r = -1
        
        x2 = radius*cos(r*alpha-angle)+x0
        y2 = radius*sin(r*alpha-angle)+y0
        return(x2,y2)

    def rotate3(self,x0,y0,x1,y1,angle):
        # rotate (x1,y1) around (x0,y0)
        # test.rotate3(440,150,480,155,0)
        # test.rotate3(440,150,460,1465,0)
        angle = radians(angle)
        cosAngle = cos(angle)
        sinAngle = sin(angle)

        x2 = cosAngle*(x1-x0) - sinAngle*(y1-y0) + x0
        y2 = sinAngle*(x1-x0) + cosAngle*(y1-y0) + y0
        #print x2,y2,sinAngle,cosAngle
        return(x2,y2)

    def splitVector(self,vector):
        #vector = list(vector)
        #vector[0] = vector[0]**2
        #vector[1] = vector[1]**2
        return(
            (vector[0]/2.0,-vector[0]/2.0)
            ,(vector[1]/2.0,-vector[1]/2.0)
            )

    def getBestEdge(self,normal,center,points):
        """
        test.getBestEdge(
        (0,-1),(11,17),((8,20),(14,20),(14,4),(8,4)))
        )
        ((8,4),(8,4),(14,4))
        test.getBestEdge(
        (0,1),(8,2),[(4,5),(12,5),(12,-1),(4,-1)])
        )
        ((12, 5), (12, 5), (4, 5))
        test.getBestEdge(
        (0,-1),(9,11),[(2, 8), (12, 18),(16, 14), (6, 4)])
        )
        ((6, 4), (6, 4), (16, 14))
        test.getBestEdge(
        (0,-1),(9,11),[(2, 8), (12, 18),(16, 14), (6, 4)])
        )
        ((6,4),(2,8),(6,4))
        """
        index = 0
        normal = self.normalise(normal)
        maxNum = -float('inf')

        """
        note ambiguity towards definition of "v"
        (implemented as vector) in tutorial code

        01
        // step 1
        02
        // find the farthest vertex in
        03
        // the polygon along the separation normal

        """

        #print '-'*50
        #print 'INIT EDGE',pen.name,normal
        x,y = center
        
        for i in range(len(points)):
            endi = (i+1)%len(points)
            """
            vector = self.toVector(
                points[i][0]
                ,points[i][1]
                ,points[endi][0]
                ,points[endi][1]
                )
            vector = self.minVector((0,0),vector)
            """
            
            vector = self.toVector(
                x,y
                ,points[i][0]
                ,points[i][1]
                )
            
            """
            note the "???" modifications made
            to compensate for downwards y axis
            and winding direction 
            """
            #vector = list(points[i]) #WARNING
            #vector[1] = self.canvasBreath-vector[1]
            #vector = self.minVector((0,0),vector)
            vector = self.normalise(vector)
            projection = self.dotProduct(
                normal,(vector[0],vector[1]) #??? #*-1
                )
            if (projection > maxNum):
                maxNum = projection
                index = i

        v = points[index]
        v1 = points[(index+1)%len(points)]
        v0 = points[index-1]
        v0,v1 = v1,v0 #???

        """
        cmLine = self.toVector(
            x,y,v[0],v[1]
            )
        cmLine = self.normalise(cmLine)
        """
        """
        if self.dotProduct(cmLine,normal) < 0:
            normal[0] *= -1
            normal[1] *= -1
        """ 
        #print v0,v,v1
        
        lVector = list(self.minVector(v,v1))
        rVector = list(self.minVector(v,v0))
        #lVector[1] *= -1
        #rVector[1] *= -1
        lVector = self.normalise(lVector)
        rVector = self.normalise(rVector)

        rDot = self.dotProduct(normal,rVector)
        lDot = self.dotProduct(normal,lVector)
        #print 'PREP RDOT LDOT RVEC LVEC'
        #print rDot,lDot,rVector,lVector
        
        #rDot = abs(rDot)
        #lDot = abs(lDot)
        #assert(rDot>=0)
        #assert(lDot>=0)
        
        if (rDot <= lDot):
            return(v,v0,v)
        else:
            return(v,v,v1)

if __name__ == '__main__':
    test = mathy()
