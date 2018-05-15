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
- Can use a simple task scheduler like https://www.gnu.org/software/parallel/
- or dynamic resource managers like PBS, Torque, SLURM, SGE, *etc.*
- Most DRMs support "job arrays" or "task arrays" or "array jobs".
- SLURM: https://slurm.schedmd.com/job_array.html
- SGE: http://wiki.gridengine.info/wiki/index.php/Simple-Job-Array-Howto

An example for the Slurm scheduler:

~~~ {.shell}
#SBATCH --time=0-00:01:00
#SBATCH --array=10-100:10
echo "This is task $SLURM_ARRAY_TASK_ID on $(hostname) at $(date)"
~~~

An example for the SGE scheduler:

~~~ {.shell}
#$ -cwd
#$ -j yes
#$ -l h_rt=0:1:0
#$ -t 10-100:10
echo "This is task $SGE_TASK_ID on $(hostname) at $(date)"
~~~
