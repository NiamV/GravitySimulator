import random
import math
import sys
from PIL import Image, ImageDraw

from Collisions import *

class Particle:
    #Position and velocity are lists of length 2
    def __init__(self, mass, position, velocity):
        self.m = mass
        self.x = position[0]
        self.y = position[1]
        self.vx = velocity[0]
        self.vy = velocity[1]

particles = [Particle(1,[random.randint(250,750),random.randint(250,750)],[0,0]) for i in range(300)]

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

dt = float(1)/float(50)
e = 1

print(" ")

for i in range(1,100000):
    drawImage.rectangle([(0, 0), (1001, 1001)], fill = "#000000")

    for j in range(1, len(particles)):
        accn = [0,0]
        for k in range(1,len(particles)):
            if j != k:                
                delta_x = particles[k].x - particles[j].x
                delta_y = particles[k].y - particles[j].y
                delta_r = math.sqrt( delta_x ** 2 + delta_y ** 2 )

                if delta_r < 3 and delta_r > 0:
                    xj = Vector(particles[j].x, particles[j].y)
                    xk = Vector(particles[k].x, particles[k].y)
                    vj = Vector(particles[j].vx, particles[j].vy)
                    vk = Vector(particles[k].vx, particles[k].vy)

                    resultant_velocity = Collision(xj, xk, vj, vk, e)
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
        particles[j].x = newLocation(particles[j].x, particles[j].vx, x_accn, dt)
        particles[j].vx = newVelocity(particles[j].vx, x_accn, dt)
        
        y_accn = accn[1]
        particles[j].y = newLocation(particles[j].y, particles[j].vy, y_accn, dt)
        particles[j].vy = newVelocity(particles[j].vy, y_accn, dt)
        
        drawImage.ellipse([(particles[j].x - 1, particles[j].y - 1),(particles[j].x + 1, particles[j].y + 1)], fill = "#FFFFFF", outline = "#FFFFFF")
        # drawImage.point((particles[j].x, particles[j].y), fill = "#FFFFFF")
        
        if abs(particles[j].x - 500) > 600 or abs(particles[j].y - 500) > 600:
            # particles[j].x = random.randint(250,750)
            # particles[j].y = random.randint(250,750)
            # particles[j].vx = random.randint(-500,500)
            # particles[j].vy = random.randint(-500,500)
            continue

        # if j == 1:
        #     print(delta_x, x_accn, y_accn)

    
    frames.append(currentImage)
    currentImage.save("D:/GravitySimulatorImages/CollisionsSimulation3/" + "{:03d}".format(i) + ".png", format = "PNG")
    sys.stdout.write("\033[F")
    print(i)
    
# frames[0].save('Gravity.gif', format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)