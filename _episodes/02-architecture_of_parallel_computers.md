---
title:  "Parallel Computer Architecture"
teaching: 15
exercises: 0
questions:
- How is a typical CPU organized?
- How are parallel computers organized?
objectives:

keypoints:
- Serial computers, including modern CPU cores, resemble very well von Neumann's 1945 design.
- Parallel computers can be characterized as collections of von Neumann CPUs.
- Parallel computers may be shared-memory, distributed-memory, or both.
---

To make full use of computing resources the programmer needs to have a working knowledge of the parallel programming concepts and tools available for writing parallel applications. To build a basic understanding of how parallel computing works, let's start with an explanation of the components that comprise computers and their function.

### Von Neumann's Architecture

John von Neumann published a general description of a computer architecture in 1945. It describes the stored-program principle where computer memory is used to store both instructions and data. The **von Neumann architecture** is still an excellent model for the computer processors we use today.

![](../fig/von_Neumann.svg)

- Central Processing Unit (**CPU**):
    - The electronic circuit responsible for executing the instructions of a computer program.
    - The CPU contains:
    - Control unit:
        - Reads and interprets instructions from the memory unit.
        - Controls the operation of the ALU, memory and input/output devices, telling them how to respond to the program instructions.
    - Arithmetic Logic Unit (ALU):
        - Carries out arithmetic (add, subtract etc) and logic (AND, OR, NOT etc) operations.
    - Registers
        - Registers are high-speed storage areas in the CPU.  All data must be stored in registers before they can be processed by the ALU.
- Memory Unit:
    - Consists of random access memory (**RAM**) modules. RAM is slower than registers but much faster than a hard drive (secondary memory), and directly addressable by the CPU.
- Input/Output Devices:
    - The interface to the outside world, e.g. hard drives, network, keyboard, mouse, monitor, etc.

Parallel computers still follow this basic design, just multiplied in units.  A
*physical* CPU chip in the 2020s may contain several von Neumann CPUs, which we
usually call **cores** when we need to make the distinction.  An individual
computer might also contain more than one of these multi-core CPU chips.  But
essential layout of a modern core is the same as the von Neumann architecture
shown above.

For the remainder of this course we may sometimes say "CPU" when we should more
precisely say "core", because the physical CPU chip is not the important
component when thinking about parallel programming.  The core executes
instructions in serial order, not in parallel.  The core is the basic building
block of parallel computing hardware.

> ## Classifications of parallel computers
> There are various academic classifications of parallel computer architectures.
> Here are two you can look up later if you're interested:
> 
> 1. [Flynn's taxonomy](https://en.wikipedia.org/wiki/Flynn%27s_taxonomy) (1966) is based on whether there are one or more instruction streams and one or more data streams.
> 2. [Feng’s classification](https://en.wikipedia.org/wiki/Feng%27s_classification) (1972) is based on the number of bits than can be processed at one time.
>
> Flynn's taxonomy is probably the most widely known. It gives rise to terms like "Single-Instruction, Multiple-Data" (SIMD) and "Multiple-Instruction, Multiple-Data" (MIMD).
{: .callout}

## Memory organization

We can see from the von Neumann architecture that a processing core needs to
get both data and instructions from memory, and write data back to that same
memory.  Engineering constraints mean that the processor can typically carry
out instructions far faster than data can be read and written to main memory,
so how memory is organized has important consequences for the design and
execution of parallel programs.

There are currently two main ways to organize memory for parallel computing:
- Shared memory
- Distributed memory
A hybrid of these two could be considered a third way.

### Shared memory

- Multiple processors can operate independently but share the same memory resources.
- All processors have equal access to data and instructions in this memory
- Changes in a memory done by one processor are visible to all other processors.

Shared memory computers can be further sub-divided into two categories:

- Uniform Memory Access (UMA)
- Non-Uniform Memory Access (NUMA)

![](../fig/shared_memory_UMA.svg)
- All processors share memory uniformly, i.e. access time to a memory location is independent on which of the processors.
![](../fig/shared_memory_NUMA.svg)
- Used in multiprocessor systems.
- When many CPUs are trying to access the same memory they can be "starved" of data because only one processor can access the computer's memory at a time.
- NUMA attempts to address this problem by providing separate memory for each processor.
- CPUs are physically linked using a fast interconnect.
- A CPU can access its local memory faster than non-local memory (memory local to another processor or memory shared between processors).

In a shared memory system it is only necessary to build a data structure in memory and pass references to the data structure to parallel subroutines. For example, a matrix multiplication routine that breaks matrices into a set of blocks only needs to pass the indices of each block to the parallel subroutines.

#### Advantages
- User-friendly programming.
- Fast data sharing due to a close connection between CPUs and memory

#### Disadvantages
- Not highly scalable. Adding more CPUs increases traffic on the shared memory-CPU path.
- Lack of data coherence. The change in the memory made by one CPU needs to be reflected to the other processors, otherwise, the different processors will be working with inconsistent data.
- The programmer is responsible for synchronization.

### Distributed memory

![](../fig/distributed_memory.svg)

- In a distributed memory system each processor has a local memory that is not accessible from any other processor
- Programs on each processor interact with each other using some form of a network interconnect (Ethernet, Infiniband, Omni-Path, etc.).
- A distributed memory program must create copies of shared data in each local memory. These copies are created by sending a message containing the data to another processor.

#### Advantages

- Each processor can use its local memory without interference from other processors.
- There is no inherent limit to the number of processors; the size of the system is constrained only by the network used to connect processors.

#### Disadvantages

- Complexity of programming: The programmer is responsible for many of the details associated with data communication between processors.
- It may be difficult to map complex data structures from global memory, to distributed memory organization.
- Longer data access times, if the data is not local to the process.

### Hybrid Distributed-Shared Memory
![](../fig/hybrid_distributed_memory.svg)
Practically all HPC computer systems today employ both shared and distributed memory architectures.

- The shared memory component can be a shared memory machine and/or graphics processing units (GPU).
- The distributed memory component is the networking of multiple shared memory/GPU machines.

The important advantage is increased scalability. Increased complexity of programming is an important disadvantage.

### Programming models are memory models

When designing a parallel solution to your problem, the major decision is
usually "which memory model should we follow?"

- A shared-memory solution can only be scaled up as far as the largest
  shared-memory machine available to you.

- In a distributed-memory solution, data must be copied from one node to another
  via messages, and this communication overhead can reduce efficiency to the
  point where scaling-up produces no benefit.


{% include links.md %}
