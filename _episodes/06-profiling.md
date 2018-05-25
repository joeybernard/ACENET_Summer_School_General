---
title: "Analyzing Performance using a Profiler"
teaching: 30
exercises: 10
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

We will analyze an example program, which simulates the spread of a forest 
fire, with the GNU profiler [Gprof](http://sourceware.org/binutils/docs/gprof/).
There are different profilers for many different languages available and some
of them can display the results graphically. Many Integrated Development 
Environments (IDEs) also include a profiler. A wide selection of profilers is 
[listed on Wikipedia](https://en.wikipedia.org/wiki/List_of_performance_analysis_tools).

## Molecular Dynamics Simulation
<!-- 
## Forest Fire Simulation

The example program performs a probabilistic simulation of a forest fire.
The program is available as [C][fire_serial_c], [C++][fire_serial_cpp],
[FORTRAN77][fire_serial_f77], [Fortran 90][fire_serial_f90] and [Python][fire_serial_py]
version from [John Burkhardt's website][jburkardt] released under the GNU LGPL license.

[fire_serial_c]:   http://people.sc.fsu.edu/~jburkardt/c_src/fire_serial/fire_serial.html
[fire_serial_cpp]: http://people.sc.fsu.edu/~jburkardt/cpp_src/fire_serial/fire_serial.html
[fire_serial_f77]: http://people.sc.fsu.edu/~jburkardt/f77_src/fire_serial/fire_serial.html
[fire_serial_f90]: http://people.sc.fsu.edu/~jburkardt/f_src/fire_serial/fire_serial.html
[fire_serial_py]:  http://people.sc.fsu.edu/~jburkardt/py_src/fire_serial/fire_serial.html
[jburkardt]: http://people.sc.fsu.edu/~jburkardt

The program creates a square forest of 20x20 trees and randomly ignites a
single tree.  In each simulation step a burning tree progresses one step from
*SMOLDERING* to *BURNING* to *BURNT*. Also each tree in the *BURNING* state
has a 50% chance to ignite each *UNBURNT* tree to the North, East, South and
West.  The simulation stops once no trees in the *SMOLDERING* or *BURNING*
state are left. 
-->

### Functions in `md_gprof.f90`
* ...

<!-- 
### Functions in `fire_serial.f90`

* **MAIN** is the main program for FIRE_SERIAL.
* **FIRE_SPREADS** determines whether the fire spreads.
* **FOREST_BURNS** models a single time step of the burning forest.
* **FOREST_INITIALIZE** initializes the forest values.
* **FOREST_IS_BURNING** reports whether any trees in the forest are burning.
* **FOREST_PRINT** prints the state of the trees in the forest.
* **GET_PERCENT_BURNED** computes the percentage of the forest that burned.
* **GET_SEED** returns a seed for the random number generator.
* **I4_UNIFORM_AB** returns a scaled pseudorandom I4 between A and B.
* **R8_UNIFORM_01** returns a unit pseudorandom R8.
* **TIMESTAMP** prints the current YMDHMS date as a time stamp.
* **TREE_IGNITE** sets a given tree to the SMOLDERING state.

This list was taken from the web-page for the [Fortran 90][fire_serial_f90]
version of `fire_serial`.
 -->

### Regular invocation:

For the demonstration we are using the [Fortran 90 version]({{ site.url }}/code/profiling/md_gprof.f90).

```console
# Download the source code file:
$ wget {{ site.url }}/code/profiling/md_gprof.f90

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

![Call Graph]({{ site.url }}/fig/profiling/md_gprof_graph.png)
