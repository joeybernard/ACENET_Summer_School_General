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


### Regular invocation:

For the demonstration we are using the [Fortran 90 version]({{ site.url }}/code/profiling/fire_serial.f90).
If you prefer, you can follow along using the [C version]({{ site.url }}/code/profiling/fire_serial.c),
replacing the `gfortran` commands with `gcc`.

```console
# Download the source code file:
$ wget {{ site.url }}/code/profiling/fire_serial.f90
$ wget {{ site.url }}/code/profiling/fire_serial.c

# Compile with gfortran:
$ gfortran fire_serial.f90  -o fire_serial

# OR with GCC:
$ gcc fire_serial.c  -o fire_serial

$ ./fire_serial 
```
{: .bash}

```
22 May 2018   5:14:10.418 PM

FIRE_SERIAL
  FORTRAN90 version
  A probabilistic simulation of a forest fire.
  The probability of tree-to-tree spread is   0.500000    
  The random number generator is seeded by    940585266

  Fire starts at tree( 8, 9)

  Map of fire damage.
  Fire started at "*".
  Burned trees are indicated by ".".
  Unburned trees are indicated by "X".

  XXXXXXXXXXXXXXXXXXXX
  XXXXXXXXXXXXXXXXXXXX
  XXXXXXXXXXXXXXXXXXXX
  XXXXXXXXXXXXXXXXXXXX
  XXXXXXXXXXXXXXXXXXXX
  XXXXXXXXXX..XXXXXXXX
  XXXXXXXXX...X.XXXXXX
  XXXXXXXX*.......XXXX
  XXXXXX.X.........XXX
  XXXXXX............XX
  XXXXXXXX..X........X
  XXXXXXXX.........XXX
  XXXXXXXX........XXXX
  XXXXXXXXX.......XXXX
  XXXXXXXXXXXX...XXXXX
  XXXXXXXXXXXXXXXXXXXX
  XXXXXXXXXXXXXXXXXXXX
  XXXXXXXXXXXXXXXXXXXX
  XXXXXXXXXXXXXXXXXXXX
  XXXXXXXXXXXXXXXXXXXX

  Percentage of forest burned =   0.182500    

FIRE_SERIAL:
  Normal end of execution.

22 May 2018   5:14:10.420 PM
```
{: .output}


### Compiling with enabled profiling



```console
# Compile with GFortran with -pg option:
$ gfortran fire_serial.f90  -o fire_serial -pg

# OR with GCC with -pg option:
$ gcc fire_serial.c  -o fire_serial -pg

$ ./fire_serial 
# ... skipping over output ...

$ /bin/ls -F
fire_serial*  fire_serial.c  fire_serial.f90  gmon.out
# Now the file gmon.out has been created.

# Run gprof to view the output:
$ gprof ./fire_serial | less
```
{: .bash}
```
Flat profile:

Each sample counts as 0.01 seconds.
 no time accumulated

  %   cumulative   self              self     total           
 time   seconds   seconds    calls  Ts/call  Ts/call  name    
  0.00      0.00     0.00      581     0.00     0.00  fire_spreads_
  0.00      0.00     0.00      581     0.00     0.00  r8_uniform_01_
  0.00      0.00     0.00       27     0.00     0.00  forest_is_burning_
  0.00      0.00     0.00       26     0.00     0.00  forest_burns_
  0.00      0.00     0.00        2     0.00     0.00  i4_uniform_ab_
  0.00      0.00     0.00        2     0.00     0.00  timestamp_
  0.00      0.00     0.00        1     0.00     0.00  MAIN__
  0.00      0.00     0.00        1     0.00     0.00  forest_initialize_
  0.00      0.00     0.00        1     0.00     0.00  forest_print_
  0.00      0.00     0.00        1     0.00     0.00  get_percent_burned_
  0.00      0.00     0.00        1     0.00     0.00  get_seed_
  0.00      0.00     0.00        1     0.00     0.00  tree_ignite_

 %         the percentage of the total running time of the
time       program used by this function.

cumulative a running sum of the number of seconds accounted
 seconds   for by this function and those listed above it.

 self      the number of seconds accounted for by this
seconds    function alone.  This is the major sort for this
           listing.

calls      the number of times this function was invoked, if
           this function is profiled, else blank.

 self      the average number of milliseconds spent in this
ms/call    function per call, if this function is profiled,
       else blank.

 total     the average number of milliseconds spent in this
ms/call    function and its descendents per call, if this
       function is profiled, else blank.

name       the name of the function.  This is the minor sort
           for this listing. The index shows the location of
       the function in the gprof listing. If the index is
       in parenthesis it shows where it would appear in
       the gprof listing if it were to be printed.

Copyright (C) 2012-2015 Free Software Foundation, Inc.

Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.

         Call graph (explanation follows)


granularity: each sample hit covers 2 byte(s) no time propagated

index % time    self  children    called     name
                0.00    0.00     581/581         forest_burns_ [4]
[1]      0.0    0.00    0.00     581         fire_spreads_ [1]
                0.00    0.00     581/581         r8_uniform_01_ [2]
-----------------------------------------------
                0.00    0.00     581/581         fire_spreads_ [1]
[2]      0.0    0.00    0.00     581         r8_uniform_01_ [2]
-----------------------------------------------
                0.00    0.00      27/27          MAIN__ [7]
[3]      0.0    0.00    0.00      27         forest_is_burning_ [3]
-----------------------------------------------
                0.00    0.00      26/26          MAIN__ [7]
[4]      0.0    0.00    0.00      26         forest_burns_ [4]
                0.00    0.00     581/581         fire_spreads_ [1]
-----------------------------------------------
                0.00    0.00       2/2           MAIN__ [7]
[5]      0.0    0.00    0.00       2         i4_uniform_ab_ [5]
-----------------------------------------------
                0.00    0.00       2/2           MAIN__ [7]
[6]      0.0    0.00    0.00       2         timestamp_ [6]
-----------------------------------------------
                0.00    0.00       1/1           main [18]
[7]      0.0    0.00    0.00       1         MAIN__ [7]
                0.00    0.00      27/27          forest_is_burning_ [3]
                0.00    0.00      26/26          forest_burns_ [4]
                0.00    0.00       2/2           timestamp_ [6]
                0.00    0.00       2/2           i4_uniform_ab_ [5]
                0.00    0.00       1/1           get_seed_ [11]
                0.00    0.00       1/1           forest_initialize_ [8]
                0.00    0.00       1/1           tree_ignite_ [12]
                0.00    0.00       1/1           forest_print_ [9]
                0.00    0.00       1/1           get_percent_burned_ [10]
-----------------------------------------------
                0.00    0.00       1/1           MAIN__ [7]
[8]      0.0    0.00    0.00       1         forest_initialize_ [8]
-----------------------------------------------
                0.00    0.00       1/1           MAIN__ [7]
[9]      0.0    0.00    0.00       1         forest_print_ [9]
-----------------------------------------------
                0.00    0.00       1/1           MAIN__ [7]
[10]     0.0    0.00    0.00       1         get_percent_burned_ [10]
-----------------------------------------------
                0.00    0.00       1/1           MAIN__ [7]
[11]     0.0    0.00    0.00       1         get_seed_ [11]
-----------------------------------------------
                0.00    0.00       1/1           MAIN__ [7]
[12]     0.0    0.00    0.00       1         tree_ignite_ [12]
-----------------------------------------------

 This table describes the call tree of the program, and was sorted by
 the total amount of time spent in each function and its children.

 Each entry in this table consists of several lines.  The line with the
 index number at the left hand margin lists the current function.
 The lines above it list the functions that called this function,
 and the lines below it list the functions this one called.
 This line lists:
     index	A unique number given to each element of the table.
    Index numbers are sorted numerically.
    The index number is printed next to every function name so
    it is easier to look up where the function is in the table.

     % time	This is the percentage of the `total' time that was spent
    in this function and its children.  Note that due to
    different viewpoints, functions excluded by options, etc,
    these numbers will NOT add up to 100%.

     self	This is the total amount of time spent in this function.

     children	This is the total amount of time propagated into this
    function by its children.

     called	This is the number of times the function was called.
    If the function called itself recursively, the number
    only includes non-recursive calls, and is followed by
    a `+' and the number of recursive calls.

     name	The name of the current function.  The index number is
    printed after it.  If the function is a member of a
    cycle, the cycle number is printed between the
    function's name and the index number.


 For the function's parents, the fields have the following meanings:

     self	This is the amount of time that was propagated directly
    from the function into this parent.

     children	This is the amount of time that was propagated from
    the function's children into this parent.

     called	This is the number of times this parent called the
    function `/' the total number of times the function
    was called.  Recursive calls to the function are not
    included in the number after the `/'.

     name	This is the name of the parent.  The parent's index
    number is printed after it.  If the parent is a
    member of a cycle, the cycle number is printed between
    the name and the index number.

 If the parents of the function cannot be determined, the word
 `<spontaneous>' is printed in the `name' field, and all the other
 fields are blank.

 For the function's children, the fields have the following meanings:

     self	This is the amount of time that was propagated directly
    from the child into the function.

     children	This is the amount of time that was propagated from the
    child's children to the function.

     called	This is the number of times the function called
    this child `/' the total number of times the child
    was called.  Recursive calls by the child are not
    listed in the number after the `/'.

     name	This is the name of the child.  The child's index
    number is printed after it.  If the child is a
    member of a cycle, the cycle number is printed
    between the name and the index number.

 If there are any cycles (circles) in the call graph, there is an
 entry for the cycle-as-a-whole.  This entry shows who called the
 cycle (as parents) and the members of the cycle (as children.)
 The `+' recursive calls entry shows the number of function calls that
 were internal to the cycle, and the calls entry for each member shows,
 for that member, how many times it was called from other members of
 the cycle.

Copyright (C) 2012-2015 Free Software Foundation, Inc.

Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.

Index by function name

   [7] MAIN__                  [3] forest_is_burning_      [5] i4_uniform_ab_
   [1] fire_spreads_           [9] forest_print_           [2] r8_uniform_01_
   [4] forest_burns_          [10] get_percent_burned_     [6] timestamp_
   [8] forest_initialize_     [11] get_seed_              [12] tree_ignite_
```
{: .output}
