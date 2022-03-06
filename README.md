# Optimization Algorithms

## Task
Code **Simulated annealing**, **Particle Swarm Optimization**, and **Artificial Bee Colony** for two 2D test functions. The **2D Rosenbrock function** and the function $(2x)^2+y^2+ (x-3)y$.

## Algorithms
### Particle Swarm Optimization
Assume we have $P$ particles, individually exhibiting position $i$ at iteration $t$ as $X^i(t)$. They will have the coordinates:

$$
    X^i(t) = (x^i(t),y^i(t))
$$

The particle will also have a velocity $V^i(t)$ denoted by:

$$
    V^i(t) = (v_x^i(t),v^i_y(t))
$$

At every iteration, each particle would be updated using the following:

$$
    X^i(t+1) = X^i(t) + V^i(t+1)
$$

Velocities are updated using the following rule:

$$
    V^i(t+1) = wV^i(t) + c_1r_1(pbest^i - X^i(t)) + c_2r_2(gbest - X^i(t))
$$

Where $r_1$ and $r_2$ are randomly generated numbers $r_1,r_2 \in [0,1]$. $w,c_1,c_2$ are parameter constants, $pbest^i$ is the best position currently explored by particle $i$, and $gbest$ is the best position current explored by all particles in the swarm.

$w$ is the inertia weight constant, $w \in [0,1]$. It determines how much the particle should keep on with its current velocity. Parameters $c_1$ and $c_2$ are called cognitive and social coeffients repectively. They controls how much weight should be given between refining the search result of the particle itself and recognizing the search result of the swarm. These parameters are the trade off between **exploration** and **exploitation**.

Positions $pbest^i$ and $gbest$ are updated in each iteration to reflect the best position ever found thus far.

### Artificial Bee Colony

### Simulated Annealling
