# GravitySimulator

This is a python program that simulates gravity between many particles. It outputs a folder of images which can be combined into a video.

## Specifying the Particles

There are two ways of specifying the initial mass, position and velocity of the particles in the simulation:

### Defined Particles

Using ` DefinedParticles.py ` you can decide exactly the mass, position and velocity of the particles you want to simulate. This works well when you have a small number of particles or the particles are nicely arranged.

``` python
particles = [
    Particle( mass, [x_pos, y_pos], [x_vel, y_vel]),
    # Repeat for all of the particles
]
```


