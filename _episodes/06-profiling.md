---
title: "Analyzing Performance using a Profiler"
teaching: 30
exercises: 15
questions:
- How do I identify the computationally expensive parts of my code?
objectives:
- Using a profiler too analyze the runtime-behavior of a program.
- Identifying areas of the code with a potential for optimization and/or
  parallelization.
keypoints:
- Don't start to parallelize or optimize your code without having used
  a profiler first.
- A programmer can easily spend many hours of work "optimizing" a part
  of the code which eventually speeds up the program by only a minuscule
  amount.
- When viewing the profiler report, look for areas where the largest amounts
  of CPU time are spent, working your way down.
- Pay special attention to areas that you didn't expect to be slow.
- In some cases one can achieve a 10x (or more) speedup by understanding
  the intrinsics of the language of choice.
---

Programmers often tend to over-think design and might spend a lot of their
time optimizing parts of the code that only contributes a small amount to
the total runtime.  It is easy to misjudge the runtime behavior of a program.

> In order to make an informed decision what parts of the code to optimize,
> one can use a performance analysis tool, or short "*profiler*", to analyze 
> the runtime behavior of a program and measure how much CPU-time is used 
> by each function.
{: .callout}

We will analyze an example program, for simple Molecular Dynamics (MD)
simulations, with the GNU profiler [Gprof](http://sourceware.org/binutils/docs/gprof/).
There are different profilers for many different languages available and some
of them can display the results graphically. Many Integrated Development 
Environments (IDEs) also include a profiler. A wide selection of profilers is 
[listed on Wikipedia](https://en.wikipedia.org/wiki/List_of_performance_analysis_tools).

## Molecular Dynamics Simulation

The example program performs simple Molecular Dynamics (MD) simulations
of particles interacting with a simple harmonic potential of the form:

```
v(x) = ( sin ( min ( x, PI/2 ) ) )^2
```

It is a modified version of an MD example written in [Fortran 90][md_f90]
by [John Burkardt][jburkardt] and released under the GNU LGPL license.

Every time step, the MD algorithm essentially calculates the distance, 
potential energy and force for each pair of particles as well as the kinetic 
energy for the system.  Then it updates the velocities based on the acting 
forces and updates the coordinates of the particles based on their velocities.

[md_f90]: http://people.sc.fsu.edu/~jburkardt/f_src/md/md.html
[jburkardt]: http://people.sc.fsu.edu/~jburkardt


### Functions in `md_gprof.f90`

The MD code `md_gprof.f90` has been modified from [John Burkardt's version][md_f90]
by splitting out the computation of the distance, force, potential- and 
kinetic energies into separate functions, to make for a more interesting
and instructive example to analyze with a profiler.

| Name of Subroutine    | Description                                       |
| :-------------------- | :------------------------------------------------ |
| **MAIN**              | is the main program for MD.                       |
| **INITIALIZE**        | initializes the positions, velocities, and accelerations. |
| **COMPUTE**           | computes the forces and energies.                 |
| **CALC_DISTANCE**     | computes the distance of a pair of particles.     |
| **CALC_POT**          | computes the potential energy for a pair of particles. |
| **CALC_FORCE**        | computes the force for a pair of particles.       |
| **CALC_KIN**          | computes the kinetic energy for the system.       |
| **UPDATE**            | updates positions, velocities and accelerations.  |
| **R8MAT_UNIFORM_AB**  | returns a scaled pseudorandom R8MAT.              |
| **S_TO_I4**           | reads an integer value from a string.             |
| **S_TO_R8**           | reads an R8 value from a string.                  |
| **TIMESTAMP**         | prints the current YMDHMS date as a time stamp.   |


### Regular invocation:

For the demonstration we are using the [Fortran 90 version](../code/profiling/md_gprof.f90).

```console
# Download the source code file:
$ wget https://acenet-arc.github.io/ACENET_Summer_School_General/code/profiling/md_gprof.f90

# Compile with gfortran:
$ gfortran md_gprof.f90  -o md_gprof

$ ./md_gprof 2 200 500 0.1
```
{: .bash}

```
25 May 2018   4:45:23.786 PM
 
MD
  FORTRAN90 version
  A molecular dynamics program.
 
  ND, the spatial dimension, is        2
  NP, the number of particles in the simulation is      200
  STEP_NUM, the number of time steps, is      500
  DT, the size of each time step, is   0.100000    
 
  At each step, we report the potential and kinetic energies.
  The sum of these energies should be a constant.
  As an accuracy check, we also print the relative error
  in the total energy.
 
      Step      Potential       Kinetic        (P+K-E0)/E0
                Energy P        Energy K       Relative Energy Error
 
         0     19461.9         0.00000         0.00000    
        50     19823.8         1010.33        0.705112E-01
       100     19881.0         1013.88        0.736325E-01
       150     19895.1         1012.81        0.743022E-01
       200     19899.6         1011.14        0.744472E-01
       250     19899.0         1013.06        0.745112E-01
       300     19899.1         1015.26        0.746298E-01
       350     19900.0         1014.37        0.746316E-01
       400     19900.0         1014.86        0.746569E-01
       450     19900.0         1014.86        0.746569E-01
       500     19900.0         1014.86        0.746569E-01
 
  Elapsed cpu time for main computation:
     19.3320     seconds
 
MD:
  Normal end of execution.
 
25 May 2018   4:45:43.119 PM

```
{: .output}


### Compiling with enabled profiling

To enable profiling with the compilers of the GNU Compiler Collection, we 
just need to add the `-pg` option to the `gfortran`, `gcc` or `g++` command.
When running the resulting executable, the profiling data will be stored
in the file `gmon.out`.

```console
# Compile with GFortran with -pg option:
$ gfortran md_gprof.f90 -o md_gprof -pg

$ ./md_gprof 2 500 1000 0.1
# ... skipping over output ...

$ /bin/ls -F
gmon.out  md_gprof*  md_gprof.f90
# Now the file gmon.out has been created.

# Run gprof to view the output:
$ gprof ./md_gprof | less
```
{: .bash}


#### Flat Profile:
```
Flat profile:

Each sample counts as 0.01 seconds.
  %   cumulative   self              self     total           
 time   seconds   seconds    calls   s/call   s/call  name    
 39.82      1.19     1.19 19939800     0.00     0.00  calc_force_
 37.48      2.31     1.12 19939800     0.00     0.00  calc_pot_
 17.07      2.82     0.51 19939800     0.00     0.00  calc_distance_
  4.68      2.96     0.14      501     0.00     0.01  compute_
  1.00      2.99     0.03      501     0.00     0.00  calc_kin_
  0.00      2.99     0.00      500     0.00     0.00  update_
  0.00      2.99     0.00        3     0.00     0.00  s_to_i4_
  0.00      2.99     0.00        2     0.00     0.00  timestamp_
  0.00      2.99     0.00        1     0.00     2.99  MAIN__
  0.00      2.99     0.00        1     0.00     0.00  initialize_
  0.00      2.99     0.00        1     0.00     0.00  r8mat_uniform_ab_
  0.00      2.99     0.00        1     0.00     0.00  s_to_r8_
```
{: .output}

#### Call Graph:
```
			Call graph


granularity: each sample hit covers 2 byte(s) for 0.33% of 2.99 seconds

index % time    self  children    called     name
                0.14    2.85     501/501         MAIN__ [2]
[1]    100.0    0.14    2.85     501         compute_ [1]
                1.19    0.00 19939800/19939800     calc_force_ [4]
                1.12    0.00 19939800/19939800     calc_pot_ [5]
                0.51    0.00 19939800/19939800     calc_distance_ [6]
                0.03    0.00     501/501         calc_kin_ [7]
-----------------------------------------------
                0.00    2.99       1/1           main [3]
[2]    100.0    0.00    2.99       1         MAIN__ [2]
                0.14    2.85     501/501         compute_ [1]
                0.00    0.00     500/500         update_ [8]
                0.00    0.00       3/3           s_to_i4_ [9]
                0.00    0.00       2/2           timestamp_ [10]
                0.00    0.00       1/1           s_to_r8_ [13]
                0.00    0.00       1/1           initialize_ [11]
-----------------------------------------------
                                                 <spontaneous>
[3]    100.0    0.00    2.99                 main [3]
                0.00    2.99       1/1           MAIN__ [2]
-----------------------------------------------
                1.19    0.00 19939800/19939800     compute_ [1]
[4]     39.8    1.19    0.00 19939800         calc_force_ [4]
-----------------------------------------------
                1.12    0.00 19939800/19939800     compute_ [1]
[5]     37.5    1.12    0.00 19939800         calc_pot_ [5]
-----------------------------------------------
                0.51    0.00 19939800/19939800     compute_ [1]
[6]     17.1    0.51    0.00 19939800         calc_distance_ [6]
-----------------------------------------------
                0.03    0.00     501/501         compute_ [1]
[7]      1.0    0.03    0.00     501         calc_kin_ [7]
-----------------------------------------------
                0.00    0.00     500/500         MAIN__ [2]
[8]      0.0    0.00    0.00     500         update_ [8]
-----------------------------------------------
                0.00    0.00       3/3           MAIN__ [2]
[9]      0.0    0.00    0.00       3         s_to_i4_ [9]
-----------------------------------------------
                0.00    0.00       2/2           MAIN__ [2]
[10]     0.0    0.00    0.00       2         timestamp_ [10]
-----------------------------------------------
                0.00    0.00       1/1           MAIN__ [2]
[11]     0.0    0.00    0.00       1         initialize_ [11]
                0.00    0.00       1/1           r8mat_uniform_ab_ [12]
-----------------------------------------------
                0.00    0.00       1/1           initialize_ [11]
[12]     0.0    0.00    0.00       1         r8mat_uniform_ab_ [12]
-----------------------------------------------
                0.00    0.00       1/1           MAIN__ [2]
[13]     0.0    0.00    0.00       1         s_to_r8_ [13]
-----------------------------------------------
```
{: .output}

#### Index by function name:
```
Index by function name

   [2] MAIN__                  [5] calc_pot_               [9] s_to_i4_
   [6] calc_distance_          [1] compute_               [13] s_to_r8_
   [4] calc_force_            [11] initialize_            [10] timestamp_
   [7] calc_kin_              [12] r8mat_uniform_ab_       [8] update_
```
{: .output}



### Plotting the Call Graph
#### Install GraphViz and Gprof2Dot
```bash
$ module load python
$ pip install --user graphviz gprof2dot
```

#### Generate the plot
```bash
$ gprof ./md_gprof  | gprof2dot -n0 -e0 | dot -Tpng -o md_gprof_graph.png
$ display output.png
```

![Call Graph](../fig/profiling/md_gprof_graph.png)
