---
title: "Input and Output"
teaching: 12
exercises: 3
objectives:
- Sketch the storage structure of a generic, typical cluster
- Understand the terms "metadata"
---

## Cluster storage

- Cluster architecture refresher:
- Login node, compute nodes
- May also be a data transfer node (DTN)
- Compute nodes may or may not have local disk
- Most I/O goes to a storage array (SAN)

- Many architectural choices for SAN.
- What technology? Lustre popular these days, ACENET & Compute Canada
- How many servers? How many MDS? Switches? Network structure? Fibre or ethernet? Redundancy?
- MDS = MetaData Server. Depends on architecture, but things like 'ls' only require *metadata*
- This is all the domain of the sysadmins, but what should you as the user do about it?

- Local disk suffers little or no contention, but is inconvenient

- File-per-process is reliable, portable and simple
- ...but lousy for checkpointing and restarting
- Many small files leads to metadata bottlenecks
- Most HPC filesystems assume no more than 1,000 files per directory

- Parallel I/O (e.g. MPI-IO) -> many processes, one file
- Solves restart problems, but requires s/w infrastructure and programming

- High-level interfaces like NetCDF and HDF5 are highly recommended

- I/O bottlenecks:
- Disk read-write rate. Alleviated by striping.
- Fibre bandwidth (or Ethernet or ...)
- Switch capacity.
- Metadata accesses (especially if only one MDS)

> ## Measuring I/O rates
>
> - Look into IOR: https://github.com/LLNL/ior or https://sourceforge.net/projects/ior-sio/
{: .challenge}
 

## Moving data on and off a cluster

- "Internet" cabling varies a lot. 100Mbit/s widespread, 1Gbit becoming common, 10Gbit or more between *most* CC sites
- http://weathermap.canarie.ca/index.html
- Firewalls sometimes the problem - security versus speed

- Filesystem at sending or receiving end often the bottleneck (SAN or simple disk)
- What are typical disk I/O rates? Highly variable! 
- See e.g. https://serverfault.com/questions/190451/what-is-the-throughput-of-15k-rpm-sas-drive
- Throughput 16MB/s to 200MB/s depending on how you do it
- IOPS (IO operations per second) 150-200

> ## Estimating transfer times
> 1. How long to move a gigabyte at 100Mbit/s?
> 2. How long to move a terabyte at 1Gbit/s? 
>
> > ## Solution
> > Remember a byte is 8 bits, a megabyte is 8 megabits, etc.
> > 1. 1024MByte/GByte * 8Mbit/MByte / 100Mbit/sec = 81 sec
> > 2. 8192 sec = 2 hours and 20 minutes
> >
> {: .solution}
{: .challenge}

- These are "theoretical maximums"! There is almost always some other bottleneck or contention that reduces this!
- Disk I/O limit? https://serverfault.com/questions/190451/what-is-the-throughput-of-15k-rpm-sas-drive

- Restartable downloads (wget? rsync? Globus!)
- checksumming (md5sum) to verify integrity of large transfers
- 

