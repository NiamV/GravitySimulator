import random
import math

class Particle:
    #Position and velocity are lists of length 2
    def __init__(self, mass, position, velocity):
        self.m = mass
        self.x = position[0]
        self.y = position[1]
        self.vx = velocity[0]
        self.vy = velocity[1]

particles = [Particle(random.randint(1,10),[random.randint(250,750),random.randint(250,750)],[random.randint(-500,500),random.randint(-500,500)]) for i in range(100)]

def TotalMass(objects):
    totalMass = 0
    for i in objects:
        totalMass += i.m
    return totalMass

M_T = TotalMass(particles)

def CentreOfMass(objects, index): #Objects is a list of particles
    totalMass = TotalMass(objects)
    totalX = 0
    totalY = 0
    for i in objects:
        if i != index:
            totalX += i.m * i.x
            totalY += i.m * i.y
    return [float(totalX) / float(totalMass), float(totalY) / float(totalMass)]

def newVelocity(u, a, t):
    v = u + a*t
    return v

def newLocation(x, u, a, t):
    x_1 = x + u*t + float(a * t * t) / float(2)
    return x_1
    

def setup():
    frameRate(30)
    size(1000,1000)
    stroke('#FFFFFF')
    strokeWeight(3)

def draw():
    stroke('#FFFFFF')
    background('#000000')
    dt = float(1)/float(1000)
    for j in range(1, len(particles)):
        try:
            xToCOM = CentreOfMass(particles, j)[0] - particles[j].x
            yToCOM = CentreOfMass(particles, j)[1] - particles[j].y
            
            rToCOM = math.sqrt(xToCOM ** 2 + yToCOM ** 2)
            
            accn = float(100000 * (M_T - particles[j].m)) / float(rToCOM ** 2)
            
            x_accn = accn * float(xToCOM) / float(rToCOM)
            particles[j].x = newLocation(particles[j].x, particles[j].vx, x_accn, dt)
            particles[j].vx = newVelocity(particles[j].vx, x_accn, dt)
            
            y_accn = accn * float(yToCOM) / float(rToCOM)
            particles[j].y = newLocation(particles[j].y, particles[j].vy, y_accn, dt)
            particles[j].vy = newVelocity(particles[j].vy, y_accn, dt)
            
            circle(particles[j].x, particles[j].y, float(particles[j].m))
            
            if abs(particles[j].x - 500) > 600 or abs(particles[j].y - 500) > 600:
                particles[j].x = random.randint(250,750)
                particles[j].y = random.randint(250,750)
                particles[j].vx = random.randint(-500,500)
                particles[j].vy = random.randint(-500,500)
        except:
            continue
    stroke('#FC0000')
    point(CentreOfMass(particles, -1)[0], CentreOfMass(particles, -1)[1])
    
        
    
