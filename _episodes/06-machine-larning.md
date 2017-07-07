---
title: "Machine Learning with Spark"
teaching: 30
exercises: 60
questions:
- "How to get started using Spark?"
- "How can I model data with Spark's MLlib?"
- "How can I asses the models I create to compare them?"
objectives:
- "Load and visualize a subset of the housing data."
- "Create a linear regression model to predict house prices."
- "Evaluate how well the model predicts house prices."
keypoints:
- "The **SparkSession** object provides the entry point for creating and working with DataFrames."
- "A **DataFrame** is a container for working with collimated data."
- "A **Pipeline** can be used to combine tasks into one."
- "A **RegressionEvaluator** can be used to evaluate regression models."
---
> ## Prerequisites
> There is very strong requirements on:
>
> * Python programing language (version 3)
> * Unix Shell
> 
> The following are related and will make the learning curve shallower but aren't required:
> * pandas
> * matplotlib
{: .prereq}

## Setup
In this episode we will use housing sales data from Seattle Washington to explore [Apache Spark](http://spark.apache.org/) and its machine learning library [MLlib](http://spark.apache.org/mllib/). The data set was originally posted on [kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction) but I have done some cleaning of the data (e.g. removing quotes) and we will use the cleaned data set as the starting point to save some time. A question that might be asked of this data set is, based on the features of a house can we predict the price of a house?

Lets get started. First, connect to an ACENET cluster

~~~
$ ssh -X glooscap.ace-net.ca
~~~
{: .bash}

The `-X` enables X11 forwarding, we will be using that to display plots we make in X11 windows. In some cases you may need to use `-Y` option if the `-X` option doesn't work. Test that your X11 forwarding is working by running a small graphical application on the remote computer.

~~~
$ xclock
~~~

you should see a window like that shown below open on your laptop.

![xclock window](../fig/machine_learning/xclock-window.png)

If you do not see a window as shown above, check that you have an X11 server running and or try the `-Y` options when connecting via ssh to the server. Once you have an xclock window open, we can move on.

Next on the server we just connected to, create a new folder to work in.

~~~
$ mkdir ml_spark
$ cd ml_spark
~~~
{: .bash}

Now download the cleaned data set with
~~~
wget https://github.com/joeybernard/ACENET_Summer_School_General/raw/gh-pages/data/machine_learning/houses_clean.csv
~~~
{: .bash}
and check that it is there
~~~
$ ls
~~~
{: .bash}
~~~
houses_clean.csv
~~~
{: .output}
Lets take a look at the first few lines of house data to see what it contains
~~~
$ head houses_clean.csv
~~~
{: .bash}
~~~
id,date,price,bedrooms,bathrooms,sqft_living,sqft_lot,floors,waterfront,view,condition,grade,sqft_above,sqft_basement,yr_built,yr_renovated,zipcode,lat,long,sqft_living15,sqft_lot15,
7129300520,20141013T000000,221900.0,3.0,1.0,1180.0,5650.0,1.0,0.0,0.0,3.0,7.0,1180.0,0.0,1955.0,0.0,98178.0,47.5112,-122.257,1340.0,5650.0
6414100192,20141209T000000,538000.0,3.0,2.25,2570.0,7242.0,2.0,0.0,0.0,3.0,7.0,2170.0,400.0,1951.0,1991.0,98125.0,47.721,-122.319,1690.0,7639.0
5631500400,20150225T000000,180000.0,2.0,1.0,770.0,10000.0,1.0,0.0,0.0,3.0,6.0,770.0,0.0,1933.0,0.0,98028.0,47.7379,-122.233,2720.0,8062.0
2487200875,20141209T000000,604000.0,4.0,3.0,1960.0,5000.0,1.0,0.0,0.0,5.0,7.0,1050.0,910.0,1965.0,0.0,98136.0,47.5208,-122.393,1360.0,5000.0
1954400510,20150218T000000,510000.0,3.0,2.0,1680.0,8080.0,1.0,0.0,0.0,3.0,8.0,1680.0,0.0,1987.0,0.0,98074.0,47.6168,-122.045,1800.0,7503.0
7237550310,20140512T000000,1225000.0,4.0,4.5,5420.0,101930.0,1.0,0.0,0.0,3.0,11.0,3890.0,1530.0,2001.0,0.0,98053.0,47.6561,-122.005,4760.0,101930.0
1321400060,20140627T000000,257500.0,3.0,2.25,1715.0,6819.0,2.0,0.0,0.0,3.0,7.0,1715.0,0.0,1995.0,0.0,98003.0,47.3097,-122.327,2238.0,6819.0
2008000270,20150115T000000,291850.0,3.0,1.5,1060.0,9711.0,1.0,0.0,0.0,3.0,7.0,1060.0,0.0,1963.0,0.0,98198.0,47.4095,-122.315,1650.0,9711.0
2414600126,20150415T000000,229500.0,3.0,1.0,1780.0,7470.0,1.0,0.0,0.0,3.0,7.0,1050.0,730.0,1960.0,0.0,98146.0,47.5123,-122.337,1780.0,8113.0
~~~
{: .output}

Here you can see various "features" of each house listing. Some features may influence the price of the house, for example the amount of livable space (`sqft_living`) or the location (`lat`,`long`).

To start working with Spark lets load the Spark module and dependencies. We are going to be working with something known as a **DataFrame** which requires Spark version 2.0.0 or greater.

> ## Check Spark versions when reading documentation
> There were a large number of changes to Spark in version 2.0.0 from previous versions. While browsing for documentation or tutorials always make sure the documentation is current to the version of Spark you are using. Spark is still in a very active development phase and large changes are frequent.
{: .callout}

To prepare our ACENET environment to work with spark run the following commands:

~~~
$ module purge
~~~
{: .bash}
to give us a clean slate so we are all starting from the same point, then
~~~
$ module load java/8u45 gcc python/3.4.1 spark/2.0.0
~~~
{: .bash}
to load the spark module and dependencies. Next we will start up the python spark shell, `pyspark`, by running the command

~~~
$ pyspark
~~~
{:.bash}

~~~
Python 3.4.1 (default, Jun  8 2016, 16:01:04)
[GCC 4.4.7 20120313 (Red Hat 4.4.7-17)] on linux
Type "help", "copyright", "credits" or "license" for more information.
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel).
17/04/10 14:44:06 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 2.0.0
      /_/

Using Python version 3.4.1 (default, Jun  8 2016 16:01:04)
SparkSession available as 'spark'.
>>>
~~~
{: .output}

we are now in the python spark shell. The `>>>` is a prompt for us to enter python code lines in the python spark shell. We will use a `>>>` to denote commands run in the pyspark shell.

> ## Running a script
> We are working in the pyspark shell for this episode as it works well for quickly trying things out. However it is often nicer to work with python scripts to avoid re-type many lines when mistakes are made and as a way to save the work you have done for reuse and future reference. You can run python scripts you write with spark using the `spark-submit` command passing it the path and name of your python script.
{: .callout}

## Visualizing the data
One of the first steps to exploring data is visualizing it to get an overall impression of the data. Start by loading the data into a **DataFrame**. Two of the leading languages for data analysis Python (using the [Pandas](http://pandas.pydata.org/) library) and R have similar data frame constructs and were likely part of the inspiration for Spark to adopt a similar construct. A **DataFrame** organizes data into named columns and as such is a natural fit to load our CSV file into. The data within a Spark dataframe is divided across the memory of multiple nodes, tasks performed on the dataframes are done in parallel by the processors on the various nodes. In this way Spark can scale to larger datasets by running on more compute nodes.

The entry point for working with Spark's dataframes is the **SparkSession**. A SparkSession is used to set and get configuration options in your spark environment and is used to create dataframes in a variety of ways, such as reading from a file.

~~~
>>> import pyspark.sql.session as pys
>>> spark = pys.SparkSession.builder.getOrCreate()
~~~
{: .python}
Now we can use the **SparkSession** we just created, `spark`, to load our data into a new **DataFrame**.
~~~
>>> houseSDF = spark.read.csv("file:///home/cgeroux/ml_spark/houses_clean.csv", header=True, inferSchema=True)
~~~
{:.python}
Here we have read in the csv file 'houses_clean.csv' and stored the data in the spark dataframe `houseSDF`. 

When you run the above command you will see a couple warning messages something like:
~~~
WARN ObjectStore: Version information not found in metastore. hive.metastore.schema.verification is not enabled so recording the schema version 1.2.0
WARN ObjectStore: Failed to get database default, returning NoSuchObjectException
~~~
{: .output}

These warnings result because we don't have a database configured for our SparkSession. In this case it creates a new database for us. If you look in the `ml_spark` directory we are working in you will see an additional file `derby.log` which contains information about the creation of the database and the directory `metastore_db` which contains the database files.

To see a list of all columns available in a Spark dataframe look at the `columns` attribute of the dataframe, which is a list of column names.
~~~
>>> houseSDF.columns
~~~
{: .python}
~~~
['id', 'date', 'price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view', 'condition', 'grade', 'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated', 'zipcode', 'lat', 'long', 'sqft_living15', 'sqft_lot15']
~~~
{: .output}

To start to get a "feel" for the data look at the description of a few columns in our **DataFrame** using the `describe` function which takes a list of column names as an argument and returns a new **DataFrame** containing the some statistics. To view the contents of a **DataFrame** we use the `show()` function.
~~~
>>> houseSDF.describe(["price","sqft_living"]).show()
~~~
{: .python}
~~~
+-------+------------------+------------------+
|summary|             price|       sqft_living|
+-------+------------------+------------------+
|  count|             21613|             21613|
|   mean| 540088.1417665294|2079.8997362698374|
| stddev|367127.19648270035| 918.4408970468096|
|    min|           75000.0|             290.0|
|    max|         7700000.0|           13540.0|
+-------+------------------+------------------+
~~~
{: .output}

We can create a smaller sample from the total data which will allow us to plot a subset of the data. If your data is very large this is important to do because the data will need to fit onto one machine in order to plot it. In this case however we are actually only using one machine and the data set isn't that large but in theory that data set could be very large and distributed across many machines. The first parameter of the `sample` function is `False` indicating that it should sample "without replacement" which means that once a particular house's data is chosen it can not be picked again. If `True` individual data elements can be chosen multiple times. The second parameter `0.1` indicates that we want a sample that is 10% the size of the original data set. The final parameter provides a `seed` to use for the random sampling. Choosing the same seed from one execution to another ensures the same random sample is chosen. This is helpful if reproducibility is needed (e.g. for debugging, testing, or comparison).
~~~
>>> houseSDFSmall = houseSDF.sample(False, 0.1, seed=10)
~~~
{: .python}

Spark dataframes are very similar to Pandas dataframes, in fact you can convert a spark dataframe into a Pandas dataframe, which is what we will do to plot our data.
~~~
>>> housePDFSmall = houseSDFSmall.toPandas()
>>> housePDFSmall.plot(x="sqft_living",y="price",kind="scatter")
~~~
{: .python}
~~~
<matplotlib.axes._subplots.AxesSubplot object at 0x7f7ad5411cf8>
~~~
{: .output}

These function calls have created a Pandas dataframe `housePDFSmall` and created a plot. In order to see the plot we must tell it to show us the plot. Pandas uses matplotlib to do its plotting so we can use the matplotlib function `show` to show the plot created for the dataframe. First, import the matplotlib python model with
~~~
>>> import matplotlib.pyplot as plt
~~~
{: .python}

Then we can use the `plt` object to show the plot with
~~~
>>> plt.show()
~~~
{: .python}

![sqft_living vs. price](../fig/machine_learning/sqft_living_vs_price.png)

> ## Do other features show a relation to price?
> Try plotting some of the other feature columns against the price to see if there are other potential relationships between house features and their prices.
> > ## Solution
> > to plot another feature do something like:
> > ~~~
> > >>> housePDFSmall.plot(x="grade",y="price",kind="scatter")
> > >>> plt.show()
> > ~~~
> > {: .python}
> {: .solution}
{: .challenge}

# Modelling the data
To create a model of how house prices depend on their features we will split the data into two groups, a training set used to build our model and a testing set to test our model. The testing set allows us to assess how well our model works for data not included in our training set and gives us some indication of how well it works for predicting house prices from the chosen features.
~~~
>>> testingSetSDF, trainingSetSDF=houseSDF.randomSplit([0.3,0.7], seed=10)
~~~
{: .python}

To model how the price depends on house features we will use linear regression.

~~~
>>> from pyspark.ml.regression import LinearRegression
>>> lr = LinearRegression(predictionCol="predicted_price", labelCol="price", featuresCol="features",regParam=0.1)
~~~
{: .python}

This creates a new **LinearRegression** object which will be fit to a DataFrame with a `features` and `price` column to create a new linear regression model. This  linear regression model can then be applied to other dataframes with a `features` column creating a `predicted_price` column. The `regParam` indicates how much regularization should be included in the linear regression model. Regularization is an extra term added to the minimization function which adds a penalty on overly complex fits helping reduce the likelihood of over fitting to the data.

The "features" column should be a vector containing all the features for that house we wish to use to predict the price. To add such a column to our DataFrame we will use a **VectorAssembler**

~~~
>>> from pyspark.ml.feature import VectorAssembler
>>> colsToVecColFeatures = VectorAssembler(inputCols = ["sqft_living"], outputCol = "features")
~~~
{: .python}
The **VectorAssembler** object we just created takes the input columns and creates a new output column `features` which is a vector containing all the values in the input columns. We can use this to create a new `Dataframe` with a "features" column.

At this point we could just apply the `transform()` function of our new **VectorAssembler** to create a new DataFrame with the features column we need. However, we could combine both the **VectorAssembler** and the **LinearRegression** steps into a single pipeline. This has the advantage of being able to easily apply our pipeline to different DataFrames to create multiple new models allowing us to compare them. As the number of steps in processing data become larger, pipelines become increasingly beneficial.

~~~
>>> from pyspark.ml import Pipeline
>>> lrPipe=Pipeline(stages=[colsToVecColFeatures,lr])
~~~
{: .python}

Now we can create our linear regression model with the `fit(DataFrame)` function of the `lrPipe` Pipeline. This will first transform the DataFrame we give to the `fit` function, then call the `fit` function on our linear regression object, `lr`, to create a linear regression model. It should be noted, that until we execute the `fit()` function, we haven't done any heavy lifting yet, we have only defined the stepsto create the linear model. Executing the below command will do all the processing of our DataFrame through the entire pipeline creating our model.

~~~
>>> lrModel=lrPipe.fit(trainingSetSDF)
~~~
{: .python}
~~~
WARN BLAS: Failed to load implementation from: com.github.fommil.netlib.NativeSystemBLAS
WARN BLAS: Failed to load implementation from: com.github.fommil.netlib.NativeRefBLAS
WARN LAPACK: Failed to load implementation from: com.github.fommil.netlib.NativeSystemLAPACK
WARN LAPACK: Failed to load implementation from: com.github.fommil.netlib.NativeRefLAPACK
~~~
{: .output}

These warnings indicate that the native implementations of BLAS and LAPACK are not being used (these are libraries to perform linear algebra operations), instead versions implemented in java are being used. While this version should work perfectly fine it will have poorer performance than native systems libraries.

We can take a look at the intercepts and coefficients of our model
~~~
>>> lrModel.stages[1].intercept
~~~
{: .python}
~~~
-39762.06580688563
~~~
{: .output}
~~~
>>> lrModel.stages[1].coefficients
~~~
{: .python}
~~~
DenseVector([278.7955])
~~~
{: .output}

To visualize our new model, lets apply it to our small Dataframe `houseSDFSmall` which creates a new DataFrame `predictions` which has a column `predicted_price` generated from our model.
~~~
>>> predictionsSDF = lrModel.transform(houseSDFSmall)
~~~
{: .python}
Next convert it to a Pandas DataFrame so we can plot it, as before
~~~
>>> predictionsPDF = predictionsSDF.toPandas()
~~~
{: .python}
This time however we want to plot two separate sets of data, the `price` and the `predicted` price. In this case instead of using the `plot` function on the Pandas DataFrame we are calling the `matplotlib` plot function directly, which is easier to customize
~~~
>>> plt.plot(predictionsPDF["sqft_living"],predictionsPDF["price"],'ro')
>>> plt.plot(predictionsPDF["sqft_living"],predictionsPDF["predicted_price"],'bo')
~~~
{: .python}
In this case the `price` will be red circles, `ro`, and the `predicted_price` will be blue circles, `bo`. Next lets add some axis labels so we know what we are looking at
~~~
>>> plt.xlabel("sqft_living")
>>> plt.ylabel("price")
~~~
{: .python}
Finally create a legend to remind us which symbols are `price` and `predicted_price` and show the plot.
~~~
>>> handles,labels=plt.gca().get_legend_handles_labels()
>>> plt.legend(handles,labels,loc=2)
>>> plt.show()
~~~
{: .python}

![sqft_living vs. price with linear fit](../fig/machine_learning/sqft_living_vs_price_fit.png)

> ## Include more features in the model
> To include more features you will need to start by creating a new *VectorAssembler* and follow the lesson down from there. Does your fit still look completely linear?
> > ## Solution
> > Make a new `VectorAssembler` including another feature
> > ~~~
> > >>> vectorizerGR = VectorAssembler(inputCols = ["sqft_living","grade"], outputCol = "features")
> > ~~~
> > {: .python}
> >
> > Create a new model pipeline with the new vectorizer
> > ~~~
> > >>> lrGRPipe=Pipeline(stages=[vectorizerGR,lr])
> > ~~~
> > {: .python}
> >
> > Make a new model with the new model pipeline
> > ~~~
> > >>> lrModelGR = lrGRPipe.fit(trainingSetSDF)
> > ~~~
> > {: .python}
> > Then apply the new model
> > ~~~
> > >>> predictionsGRSDF=lrModelGR.transform(houseSDFSmall)
> > ~~~
> > {: .python}
> >
> > then convert the new predictions to a Pandas DataFrame and plot the new predictions to see how it changed
> > ~~~
> > >>> predictionsGRPDF=predictionsGRSDF.toPandas()
> > >>> plt.plot(predictionsGRPDF["sqft_living"],predictionsGRPDF["price"],"ro")
> > >>> plt.plot(predictionsGRPDF["sqft_living"],predictionsGRPDF["predicted_price"],"bo")
> > >>> plt.xlabel("sqft_living")
> > >>> plt.ylabel("price")
> > >>> handles,labels=plt.gca().get_legend_handles_labels()
> > >>> plt.legend(handles,labels,loc=2)
> > >>> plt.show()
> > ~~~
> > {: .python}
> {: .solution}
{: .challenge}

## Assessing the model
Now that we have a model and visualized it we will want to be able to discriminate quantitatively between different models. One of the simplest ways to measure the quality of a model is the root mean square error between the model and observations. For this we will use the `testingSetSDF` created previously. Thus far all our work has been with `trainingSetSDF` used to create our model. The first step in assessing our model is to create some predictions based on `testingSetSDF`
~~~
>>> predictionsSDF = lrModel.transform(testingSetSDF)
~~~
{: .python}
Next we create an evaluator for our regression model. We indicate we want the root mean squared error ("rmse") as our metric and use it to compare the "predicted_price" and "price" columns in our DataFrame.
~~~
>>> from pyspark.ml.evaluation import RegressionEvaluator
>>> regEval = RegressionEvaluator(predictionCol="predicted_price",labelCol="price",metricName="rmse")
~~~
{: .python}

Then we can evaluate our predictions and print out the root mean squared error
~~~
>>> rmse = regEval.evaluate(predictionsSDF)
>>> print(rmse)
~~~
{: .python}
~~~
261951.22
~~~
{: .output}
which represents a "characteristic" error of our model. In this case it is quite large, for comparison lets take a look at the average house price
~~~
>>> testingSetSDF.describe(["price"]).show()
~~~
{: .python}
~~~
+-------+------------------+
|summary|             price|
+-------+------------------+
|  count|              6544|
|   mean| 540804.2923288508|
| stddev|370962.05890724383|
|    min|           78000.0|
|    max|         7700000.0|
+-------+------------------+
~~~
{: .output}
we see that it is about half the average house price. Would you want to buy a house based on these predicted prices?

> ## Can you get a better linear model?
> Try various combinations of features to see what the lowest value for rmse you can get.
{: .challenge}


