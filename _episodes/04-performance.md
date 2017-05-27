---
title: "Performance and its measurement"
teaching: 20
exercises: 0
questions:
- "What affects performance?"
- "How do you measure it?"
- "How can you improve it?"
objectives:
- "Measure performance"
- "Measure efficiency"
keypoints:
- "Early optimization is the source of all evil"
---

One of the key reasons for learning to write parallel programs is to getting better performance for your particular problem. But, how best can you apply these new skills? There is a very famous quote from Donald Knuth:

> ## Evil
> The real problem is that programmers have spent far too much time worrying about efficiency in the wrong places and at the wrong times; premature optimization is the root of all evil (or at least most of it) in programming.
{: .callout}

So, the first order of business is to have an algorithm that solves the problem you are trying to solve correctly. Then, you need to look at how to optimize it. There are two general areas where you can optimize your program: first in the amount of space it uses, and second in the amount of time in takes. These two elements form a kind of Heisenberg uncertainty principle for code, where you can decrease one at the cost of increasing the other. So the first step is to decide which side of the equation you wish to optimize for before starting anything.

Human beings are notoriously bad at trying to figure out where a program is spending most of its time or memory. This where science needs to step in and you need make actual measurements with actual numbers. The class of utilities that you can use for this are called profilers. These programs wrap your own code and give you a profile of where your code is spending its time and how memory is being used. This will help you focus in one those specific functions, or even specific individual lines, that will give you the biggest bang for your time spent trying to do optimization.

Most programming languages, such as C/C++, Java, Python, R, all have associated profiling utilities. They all specialize in particular areas, so you will need to do a bit of research to find the most appropriate tool. For writing C/C++ programs, time profiling can be measured using gprof. Gprof is a statistical profiler, which means that it samples your program as it runs to build up statistics. If you want to profile memory usage, a very popular tool is valgrind, which can track all of the memory usage and find issues such as memory leaks.

Let's say that you now have a single-threaded program that has had as much performance as possible squeezed out of it, but that is still not enough. What is the next step? This is where you need to consider ping your code. This brings to mind a second famous quote, this one by Brian Kernighan.

> ## Debugging
> Everyone knows that debugging is twice as hard as writing a program in the first place. So if you're as clever as you can be when you write it, how will you ever debug it?
{: .callout}

This maxim goes doubly so for parallel programs. The rule of thumb is to move slowly and carefully, with as much forethought as possible. Trying to debug issues after that fact is very difficult, so try your absolute best to avoid them in the first place.

So, how do you measure your newly parallelized codes performance? The vast majority of people are most concerned with time performance, so that will be our focus here, as well. You should see the time taken for your code decreasing with each additional CPU that you can add to the problem. The exact amount of time decrease is called the speedup ratio, given by

~~~
speedup = sequential_time / parallel_time
~~~
{: .source}

This doesn't really tell you how well your code is using each of the CPUs given to it, however. To measure this, you need to look at efficiency, given by

~~~
efficiency = speedup / num_cpus
~~~
{: .source}

You will almost never reach 100% efficiency because not 100% of your program can be done in parallel. There will always be parts that need to be done in a sequential order. For example, if you need to calculate the following function

~~~
z = sin(x) * sin(y)
~~~
{: .source}

you can do the two sine functions in parallel, but you need to wait for them to be done before you can do the multiplication, and then you can do the assignment to the variable z. Because of the necessity of having some proportion of your code single-threaded, there is a maximum speedup that you can achieve, no matter how many CPUs you through at it. This maximum is defined by Amdahl's Law.

~~~
max speedup <= (f + (1-f)/p)^-1
~~~
{: .source}

where 'f' is the percentage of your code that must be sequential, and 'p' is the number of processors being used. Looking at this equation, if we let 'p'go off to infinity, we get the absolute maximum possible for your code as 1/f. So, if half of your code needs to run sequentially, the absolute largest sppedup you will ever get is a factor of 2.

These are just thoughts to keep in mind as we progress through the rest of the summer school.
