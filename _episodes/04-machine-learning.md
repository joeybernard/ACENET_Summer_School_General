---
title: "Machine Learning with Spark "
teaching: 0
exercises: 0
questions:
- "Key question"
objectives:
- "First objective."
keypoints:
- "First key point."
---

## Getting started
The first thing we need to do is connect to an ACENET cluster. Then we need to 
load the Spark module and its dependencies. We are going to be working with a
class in Spark known as a `Dataframe` which requires Spark version 2.0.0 or 
greater. Run

~~~
$ module purge
~~~
{: .bash}
to give us a clean slate so we are all starting from the same point, then
~~~
$ module load java/8u45 gcc python/3.4.1 spark/2.0.0
~~~
{: .bash}

Next we will start up the python spark shell `pyspark` by running the command

~~~
$ pyspark
~~~
{:.bash}

~~~
Python 2.6.6 (r266:84292, Aug  9 2016, 06:11:56)
[GCC 4.4.7 20120313 (Red Hat 4.4.7-17)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
/usr/local/spark-2.0.0/python/pyspark/sql/context.py:477: DeprecationWarning: HiveContext is deprecated in Spark 2.0.0. Please use SparkSession.builder.enableHiveSupport().getOrCreate() instead.
  DeprecationWarning)
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel).
17/03/29 13:24:11 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 2.0.0
      /_/

Using Python version 2.6.6 (r266:84292, Aug  9 2016 06:11:56)
SparkSession available as 'spark'.
>>>
~~~
{: .output}

> ## Running a script
> We are working in the pyspark shell for this episode as it works well for quickly trying things out. However it is often nicer to work with python scripts to avoid re-type many lines when mistakes are made and as a way to save work you have done for reuse and future reference. You can run python scripts you write with spark using the `spark-submit` command passing it the path and name of your python script.
{: .callout}

## Dataframes