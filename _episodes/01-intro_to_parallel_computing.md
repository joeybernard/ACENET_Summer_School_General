---
title:  "Introduction"
start: true
teaching: 10
exercises: 5
questions:
- "What parallel computing is and why it is important?"
- "How does a parallel program work?"
objectives:
- "Explain differences between a serial and a parallel program"
- "Introduce types of parallelism available in modern computers"

keypoints:
- "Parallel computing is much better suited for modelling, simulating and understanding complex, real-world phenomena."
- "Modern computers have several levels of parallelism"
---

### Why to learn parallel computing?
- Building faster serial computers became constrained due to both physical and practical reasons.

- The increase in serial performance slowed down because processor designs approached limits of miniaturization, clock frequency, power consumption, data transmission speed.

- It is increasingly expensive to make a single processor faster. Using a larger number of moderately fast commodity processors to achieve the same (or better) performance is more practical.


### Parallel Computing Applications

Here are just a few examples of how parallel computing is helping to accelerate research and solve the previously unsolvable problems.

1. Numeric Weather prediction
    - Taking current observations uses mathematical models  to forecast the future state of the weather
2. Computational Astrophysics
    -  Numerical relativity, magnetohydrodynamics, stellar and galactic magnetohydrodynamics
3. Seismic Data Processing
    - Analyze seismic data to find oil and gas-bearing layers
4. Commercial world
    - Nearly every major aspect of today’s banking, from credit scoring to risk modelling to fraud detection, is GPU-accelerated.
5. Pharmaceutical design
    - Uses parallel computing for running simulations of molecular dynamics

<figure class="video_container">
  <video width="360" controls="true" autoplay loop style="display:block; margin:0 auto;" allowfullscreen="true">
    <source src="../fig/calmodulin.mp4" type="video/mp4">
  </video>
</figure>
6. Computational fluid dynamics, tidal wave simulations

<figure class="video_container">
  <video width="360" controls="true" autoplay loop style="display:block; margin:0 auto;" allowfullscreen="true">
    <source src="../fig/Grand_Passage_curl_int4_PTSx2.mp4" type="video/mp4">
  </video>
</figure>

### Benefits of Parallel Computing:
 - It allows us to solve problems in a shorter time.
 - Allows solving larger, more detailed problems compared to serial execution.
 - Overall parallel computing is much better suited for modelling, simulating and understanding complex, real-world phenomena.

### Limitations and Disadvantages:

- Some problems can not be broken into pieces of work that can be done independently
- Not every problem can be solved in less time with multiple compute resources than with a single computing resource. Some problems may not have enough inherent parallelism to exploit.
- Could be more costly in equipment (expensive interconnect)
- Coding expertise
- Require time and effort

#### Before you start your parallel computing project

- Select the most appropriate parallelization options for your problem.
- Estimate the effort and potential benefits.

In this lesson, we hope to give you knowledge and skills to make the right decisions on parallel computing projects.

### How does a Parallel Program Work?

 Parallelism is the future of computing. Parallel programming allows us to increase the amount of processing power in a system. How does a parallel program work?


### Traditional serial program
![](../fig/Serial_program.svg)

- A problem is broken into a set of instructions
- Instructions are executed sequentially on a single CPU
- Only one instruction can be executed at a time

###  Parallel program

- Parallel computing is breaking a problem into smaller chunks and executing them concurrently on a set of different CPUs and/or computers.

![](../fig/Parallel_program.svg)

- A problem is broken into parts that can be done concurrently
- Each part is further broken down into a set of instructions
- Instructions from each part execute simultaneously on different processors
- Requires an overall execution control & coordination mechanism.

- Modern desktop/laptop computers come equipped with multiple central processing units (cores) that can process many sets of instructions simultaneously.

- Each core is equipped with a vector unit that can process multiple data at one time. Vector units are described by the number of the bits that the vector unit can process at one time. For example, a 256 bit-wide vector unit can process four double-precision floating point numbers simultaneously.

- Networks connect multiple stand-alone computers (nodes) to make larger parallel computer clusters.

For example, a typical Compute Canada cluster has thousands of computers (network nodes):
- Each compute node is a multi-processor parallel computer
- Each processor is equipped with AVX-2 or AVX-512 vector units
- Multiple compute nodes are interconnected with an Infiniband network
- Special purpose nodes (login, storage, scheduling, etc.)

> ## What fraction of the total processing power can a serial program use?
> Let’s consider an 8 core CPU with AVX-512 vector unit, commonly found in home desktops.
- What percentage of the theoretical processing capability of this processor can a double-precision serial program without vectorization use?
- What about a serial program with vectorization?
>
>>## Solution
>> 1. 8 cores x (512 bit-wide vector unit)/(64-bit double) = 64-way parallelism. 1 serial path/64 parallel paths = .016 or 1.6%
>> 2. Full use of 1 of 8 cores = 25%
>>
> {: .solution}
{: .challenge}

> ## [TOP 500](https://www.top500.org) publishes current details of the fastest computer systems.
> - [The fastest supercomputer: IBM Summit](https://www.top500.org/system/179397)
> ![](../fig/IBM_Summit.jpg)
> - [Summit System Overview](https://www.olcf.ornl.gov/wp-content/uploads/2019/05/Summit_System_Overview_20190520.pdf)
> - [Performance Development](https://www.top500.org/statistics/perfdevel)
> - In the application area statistics "Not Specified" is by far the largest category - probably means multiple applications.
>
{: .callout}


{% include links.md %}
