---
title: "Parallel Architecture"
teaching: 10
exercises: 0
questions:
objectives:
- Explain the difference between Shared Memory, Distributed Memory,
  and Hybrid systems
keypoints:
- Multiple processors installed in the same host can share a common memory.
- Multiple hosts with a single processor an some memory can communicate via 
  an interconnect.
- Contemporary clusters consist of multi-core nodes that are connected with
  a fast interconnect.
---

Parallel Computers can be built using one of three diffent parallel layouts:
Shared Memory, Distributed Memory or a hybrid of shared and distributed Memory.

## Shared Memory

![figure of Shared Memory Layout](../fig/parallel_architecture/shared_memory.png)

With the advent of multi-core processors, virtually all consumer-grade computers
sold in since about 2008 are shared memory computers which have 2, 4 or 8 CPU cores
in the same machine that have access to the installed memory (RAM).  Even
modern smart-phones are using multi-core processors.

As of 2018 there are server grade processors available whith up to 28 cores
in the same processor (package) which then can be intalled on single-socket
mainboards or on ones that can take up to 8 processors.

## Distributed Memory

![figure of Distributed Memory Layout](../fig/parallel_architecture/distributed_memory.png)

Each processor has it's own amount of memory that it can access and multiple
processors communicate with each other over an interconnect.
The interconnnect can be Ethernet (copper cables) or optical fibre (e.g. 
Infiniband, Myrinet or OmniPath).  Optical interconnect is significantly 
more expensive but has much higher bandwidth and lower latency than Ethernet.

## Hybrid Memory

![figure of Hybrid Memory Layout](../fig/parallel_architecture/hybrid_memory.png)

Contemporary clusters usually built using this hybrid model: hundreds of 
multi-core computers (called "nodes") are connected with a fast interconnect.
