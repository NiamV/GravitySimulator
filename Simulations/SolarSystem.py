import random
import math
import sys
from PIL import Image, ImageDraw

from Collisions import *

from progress.bar import Bar

class Particle:
    #Position and velocity are lists of length 2
    def __init__(self, mass, position, velocity, colour):
        self.m = mass
        self.x = position[0]
        self.y = position[1]
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.colour = colour

particles = [
    Particle(333030, [500,500], [0,0], "rgb(255, 191, 0)"),
    Particle(0.055, [504, 500], [0, 9124.555], "rgb(181, 181, 181)"),
    Particle(0.815, [507, 500], [0, 6897.515], "rgb(255, 148, 0)"),
    Particle(1.000, [510, 500], [0, 5770.875], "rgb(0, 255, 246)"),
    Particle(0.107, [515, 500], [0, 4711.900], "rgb(255, 29, 0)"),
    Particle(318.0, [552, 500], [0, 2530.696], "rgb(255, 165, 0)"),
    Particle(95.00, [595, 500], [0, 1872.319], "rgb(246, 255, 0)"),
    Particle(15.00, [692, 500], [0, 1317.016], "rgb(0, 182, 255)"),
    Particle(17.00, [800, 500], [0, 1053.613], "rgb(0, 127, 255)")
]

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

frames = []

currentImage = Image.new("RGBA", (1000,1000), color="#000000")
drawImage = ImageDraw.Draw(currentImage)

dt = float(1)/float(10000)
e = 0.8

NoOfFrames = 20000

bar = Bar("Simulating", max = NoOfFrames)

for i in range(1,NoOfFrames + 1):
    drawImage.rectangle([(0, 0), (1001, 1001)], fill = "#000000")

    newParticles = []

    for j in range(0, len(particles)):
        accn = [0,0]
        for k in range(0,len(particles)):
            if j != k:                
                delta_x = particles[k].x - particles[j].x
                delta_y = particles[k].y - particles[j].y
                delta_r = math.sqrt( delta_x ** 2 + delta_y ** 2 )

                if delta_r < 2 and delta_r > 0:
                    xj = Vector(particles[j].x, particles[j].y)
                    xk = Vector(particles[k].x, particles[k].y)
                    vj = Vector(particles[j].vx, particles[j].vy)
                    vk = Vector(particles[k].vx, particles[k].vy)

                    resultant_velocity = Collision(1, 1, xj, xk, vj, vk, e)
                    particles[j].vx = resultant_velocity.x
                    particles[j].vy = resultant_velocity.y

                else:
                    try:
                        accn[0] += float(1000 * (particles[k].m) * delta_x) / float(delta_r ** 3)
                    except:
                        accn[0] += 0

                    try:
                        accn[1] += float(1000 * (particles[k].m) * delta_y) / float(delta_r ** 3)
                    except:
                        accn[1] += 0

        
        x_accn = accn[0]
        particleNew_x = newLocation(particles[j].x, particles[j].vx, x_accn, dt)
        particleNew_vx = newVelocity(particles[j].vx, x_accn, dt)
        
        y_accn = accn[1]
        particleNew_y = newLocation(particles[j].y, particles[j].vy, y_accn, dt)
        particleNew_vy = newVelocity(particles[j].vy, y_accn, dt)

        newParticles.append(Particle(
            particles[j].m, 
            [particleNew_x, particleNew_y],
            [particleNew_vx, particleNew_vy],
            particles[j].colour,
        ))
        
        drawImage.ellipse([(particles[j].x - 1, particles[j].y - 1),(particles[j].x + 1, particles[j].y + 1)], fill = particles[j].colour, outline = particles[j].colour)
        # drawImage.point((particles[j].x, particles[j].y), fill = particles[j].colour)
        
        if abs(particles[j].x - 500) > 600 or abs(particles[j].y - 500) > 600:
            # particles[j].x = random.randint(250,750)
            # particles[j].y = random.randint(250,750)
            # particles[j].vx = random.randint(-500,500)
            # particles[j].vy = random.randint(-500,500)
            continue

        # if j == 1:
        #     print(delta_x, x_accn, y_accn)

    
    # frames.append(currentImage)
    currentImage.save("D:/GravitySimulatorImages/SolarSystem/" + "{:03d}".format(i) + ".png", format = "PNG")
    sys.stdout.write("\033[F")
    
    particles = []

    for p in newParticles:
        particles.append(p)
    
    bar.next()
    
bar.finish()
# frames[0].save('Gravity.gif', format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)