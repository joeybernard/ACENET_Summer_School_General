---
title: "Independent tasks and job schedulers"
teaching: 5
exercises: 5
objectives:
- Be able to identify a problem of independent tasks
- Use a scheduler like SGE or SLURM to submit an array job 
---

- Some problems are easy to parallelize
- as long as the sub-problems don't need information from each other,
- e.g. counting blobs in 10,000 image files.
- Other tests: Do the sub-tasks have to be done at the same time, 
 or in order? Or could they all start and end at random times?
- Computer scientists sometimes call these "embarrassingly parallel" problems.
- We call them "perfectly parallel". They're extremely efficient.
- "Parameter sweep" is another type of this problem.

> ## Independent tasks in your field?
>
> Can you think of a problem in your field that can be formulated
> as a set of independent tasks?
{: .challenge}

- Don't need fancy parallel programming interfaces to handle these problems.
- Can use a simple task scheduler like [GNU Parallel](https://docs.computecanada.ca/wiki/GNU_Parallel)
- or dynamic resource managers like PBS, Torque, SLURM, SGE, *etc.*
- Most DRMs support "job arrays" or "task arrays" or "array jobs".
- SLURM: [Job Arrays](https://docs.computecanada.ca/wiki/Job_arrays) 


An example of a submission script for an array job with the slurm schedular. 

~~~ {.shell}
#!/bin/bash
#SBATCH --account=YOUR_ACCOUNT
#SBATCH --array=10-100:10
#SBATCH --time=0-00:01:00

echo "This is task $SLURM_ARRAY_TASK_ID on $(hostname) at $(date)"
~~~

If the above is saved into a script called `array_job_submit.sh` and `YOUR_ACCOUNT` with your CC account it can be submitted to the SLURM schedular with:
~~~ {.shell}
$ sbatch array_job_submit.sh
~~~

