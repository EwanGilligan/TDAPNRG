#Fields

**test** [see test section](#test)

___

**reference_rng** 

String link to where to download the reference rng.
```metadata json
"reference_rng": "https://drive.google.com/uc?id=<FILE ID>"
```
Can be generated from google drive by right clicking the file, and creating shareable link.
This may have ```open``` instead of ```uc```, but you can just replace it.
___

**runs**

Number of times to run the experiment per generator, represented as an integer.
```metadata json
"runs": 10
```
___

**n_points**

Number of points to generate for the test, represented as an integer.. For the Hypercube Test, around 12000 is recommended.
For the matrix rank, at least 100 is recommended.
```metadata json
"n_points": 12000
```
___
**homology_dimension**

The dimension of the homology to calculate for the test. By default, this is 0 for both the Hypercube and Matrix Rank test.
```metadata json
"homology_dimension": 0
```
___
**filtration_size**

The size of filtration to use when calculating the homology distribution. This isn't used for the Matrix Rank test,
but at least 20 is recommended for the Hypercube Test.
```metadata json
"filtration_size": 10
```
___
**verbose**\[optional]

Whether or not the program will print out intermediate results, such as the result of individual tests, or the current scale.
This field is a boolean, and is true by default.
```metadata json
"verbose": false
```
___
**recalculate_distribution**\[optional]

Whether or not to recalculate the reference distribution with each generator, represented as a boolean.
If set to true, then a new reference distribution will be calculated per generator.
If false, then the same distribution will be used for all generators.
```metadata json
"recalculate_distribution": false
```
___
**store_data**\[optional]

Whether or not to store all data generated during running. So this is the entire point clouds for the Hypercube test,
and the matrices and distance matrix for the Matrix Rank test. It will also include the distribution for each run.
This is false by default.
```metadata json
"store_data": true
```
___
**gpu**\[optional]

Whether or not to use CUDA optimisations, represented as a boolean. This is false by default.
```metadata json
"gpu": false
```

# test

## generator