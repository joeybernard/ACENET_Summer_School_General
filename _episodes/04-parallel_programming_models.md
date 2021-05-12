---
title: "Parallel Programming Models"
teaching: 15
exercises: 10
questions:
- "What levels of parallelism are available in modern computer systems?"
- "How can a parallel program access different levels of parallelization?"
objectives:
- "Explain parallelism in modern computer systems"
- "Introduce parallel programming models"

keypoints:
- "There are many layers of parallelism in modern computer systems"
- "An application can implement vectorization, multithreading and message passing"
---

### Parallel Programming Models

Developing a parallel application requires an understanding of the potential amount of parallelism in your application and the best ways to expose this parallelism to the underlying computer architecture. Current hardware and programming languages give many different options to parallelize your application. Some of these options can be combined to yield even greater efficiency and speedup.

### Levels of Parallelism
There are several layers of parallel computing:
1. Vectorization (processing several data units at a time)
2. Multithreading  (a way to spawn multiple cooperating threads sharing the same memory and working together on a larger task). Multithreading provides a relatively simple opportunity to achieve improved application performance with multi-core processors.
3. Process-based parallelism

Available hardware features influence parallel strategies.

### Example workflow of a parallel application in the 2D domain.

- Discretize the problem into smaller cells or elements
- Define operations to conduct on each element of the computational mesh
- Stencil operation involves a pattern of adjacent cells to calculate the new value for each cell.

![](../fig/parallel_app_1.svg)

Blur operation:

$$x_{i,j}^{new}=x_{i-1,j}+x_{i,j-1}+x_{i,j}^{old}+x_{i+1,j}+x_{i,j+1}$$
- Repeat computations for each element of the mesh

#### Vectorization
Vectorization can be used to work on more than one unit of data at a time.

![](../fig/parallel_app_2.svg)

- Most processors today have vector units that allow processors to operate on more than one piece of data (int, float, double) at a time.  For example, a vector operation shown in the figure is conducted on eight floats. This operation can be executed in a single clock cycle, with little overhead costs to the serial operation.

##### Example AVX2 program
avx2_example.c
~~~
#include <immintrin.h>
#include <stdio.h>

int main() {

  /* Initialize the two argument vectors */
  __m256 evens = _mm256_set_ps(2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0);
  __m256 odds = _mm256_set_ps(1.0, 3.0, 5.0, 7.0, 9.0, 11.0, 13.0, 15.0);

  /* Compute the difference between the two vectors */
  __m256 result = _mm256_sub_ps(evens, odds);

  /* Display the elements of the result vector */
  float *f = (float *)&result;
  printf("%f %f %f %f %f %f %f %f\n",
    f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7]);

  return 0;
}
~~~
{: .source}
Compiling: gcc -mavx


#### Threads
Most of today’s CPUs have several processing cores. So, we can use threading to engage several cores to operate simultaneously on four rows at a time as shown in Figure.

![](../fig/parallel_app_3.svg)

Technically, a thread is defined as an independent stream of instructions that can be scheduled to run by the operating system.  From a developer point of view, thread is a "procedure" that runs independently from its main program.

Imagine the main program that contains a number of procedures. In a "multi-threaded" program all of these procedures can be scheduled to run simultaneously and/or independently by the operating system.

Threads operate in shared-memory multiprocessor architectures.

POSIX Threads (Pthreads) and OpenMP represent the two most popular implementations of multiprocessing models. Pthreads library is a low-level API providing extensive control over threading operations. It is very flexible and provides very fine-grained control over multi-threading operations. Being low-level it requires multiple steps to perform simple threading tasks.

On the other hand, OpenMP is a much higher level and much simpler to use.

##### Example OpenMP program
omp_example.c
~~~
#include <omp.h>
#include <stdio.h>

int main()
{

int i;
int n=10;
float a[n];
float b[n];

for (i = 0; i < n; i++)
    a[i] = i;

#pragma omp parallel for
/* i is private by default */
for (i = 1; i < n; i++)
    {
     b[i] = (a[i] + a[i-1]) / 2.0;
    }

for (i = 1; i < n; i++)
    printf("%f ", b[i]);
printf("\n");
return(0);
}
~~~
{: .source}
- Compiling: gcc -fopenmp
- Running: OMP_NUM_THREADS


#### Distributed memory / Message Passing

Further parallelization can be achieved by spreading out computations to a set of processes (tasks) that use their own local memory during computation.

Multiple tasks can reside on the same physical machine and/or across an arbitrary number of machines.

Tasks exchange data through communications by sending and receiving messages.

OpenMPI and Intel MPI are two of the most popular implementations of message passing multiprocessing models installed on Compute Canada systems.

![](../fig/parallel_app_4.svg)

##### MPI example
mpi_example.c
~~~
#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    // Initialize the MPI environment
    MPI_Init(NULL, NULL);

    // Get the number of processes
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    // Get the rank of the process
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    // Print off a hello world message
    printf("Hello world from rank %d out of %d Processors\n", world_rank, world_size);

    // Finalize the MPI environment.
    MPI_Finalize();
}
~~~
- Compiling: gcc mpi_example.c -lmpi
- Running: srun -n 4 -A def-sponsor0 ./a.out

- Passing messages takes time


#### Resources:

1. [Crunching numbers with AVX and AVX2.](
https://www.codeproject.com/Articles/874396/Crunching-Numbers-with-AVX-and-AVX)
2. [Threading Models for High-Performance Computing: Pthreads or OpenMP](https://software.intel.com/en-us/articles/threading-models-for-high-performance-computing-pthreads-or-openmp)
3. [Getting Started with OpenMP](https://software.intel.com/en-us/articles/getting-started-with-openmp)
4. [More OpenMP Books](https://www.openmp.org/resources/openmp-books)


{% include links.md %}
