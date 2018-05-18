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

## .
