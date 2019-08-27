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

particles = [
    Particle(
        1,
        [random.randint(250,750),random.randint(250,750)],
        [random.randint(-100,100),random.randint(-100,100)]) 
    for i in range(500)]

def newLocation(x, u, t):
    x_1 = x + u*t
    return x_1

frames = []

currentImage = Image.new("RGBA", (1000,1000), color="#000000")
drawImage = ImageDraw.Draw(currentImage)

dt = float(1)/float(50)
e = 1

print(" ")

for i in range(1,100000):
    drawImage.rectangle([(0, 0), (1001, 1001)], fill = "#000000")
    drawImage.rectangle([(250, 250), (750, 750)], fill = "#000000", outline = "#FFFFFF")

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

                    resultant_velocity = Collision(1,1,xj, xk, vj, vk, e)
                    particles[j].vx = resultant_velocity.x
                    particles[j].vy = resultant_velocity.y
           
        x_accn = accn[0]
        particleNew_x = newLocation(particles[j].x, particles[j].vx, dt)
        particleNew_vx = particles[j].vx
        
        y_accn = accn[1]
        particleNew_y = newLocation(particles[j].y, particles[j].vy, dt)
        particleNew_vy = particles[j].vy

        if abs(particleNew_x - 500) > 250:
            particles[j].vx *= -1
            particleNew_x = newLocation(particles[j].x, particles[j].vx, dt)
            particleNew_vx = particles[j].vx

        if abs(particleNew_y - 500) > 250:
            particles[j].vy *= -1
            particleNew_y = newLocation(particles[j].y, particles[j].vy, dt)
            particleNew_vy = particles[j].vy
            

        newParticles.append(Particle(
            particles[j].m, 
            [particleNew_x, particleNew_y],
            [particleNew_vx, particleNew_vy]
        ))
        
        # drawImage.ellipse([(particles[j].x - 1, particles[j].y - 1),(particles[j].x + 1, particles[j].y + 1)], fill = "#FFFFFF", outline = "#FFFFFF")
        drawImage.point((particles[j].x, particles[j].y), fill = "#FFFFFF")
        
    frames.append(currentImage)
    currentImage.save("D:/GravitySimulatorImages/GasSimulation2/" + "{:03d}".format(i) + ".png", format = "PNG")
    sys.stdout.write("\033[F")
    
    particles = []

    for p in newParticles:
        particles.append(p)
    
    print(i)
    
# frames[0].save('Gravity.gif', format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)