# Fields

These are the fields in the top level of the json.

**test** 

[see test section](#test)
```metadata json
"test": {
    ...
}
```
___

**generators**

[see generators section](#generators)
```metadata json
"generators":{
    ...
}
```

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

## test
This object contains information specific to each individual test. Each object must contain a ```name```
field to specify which test.
### Hypercube Test
```metadata json
"name": "hypercube"
```
___
**dimension**

The dimension of the hypercube to sample points from within, represented as an integer.
```metadata json
"dimension": 3
```
___
**scales**

List of floats to use as different side lengths of hypercube to sample from within. 
These are in (0,1]. The generators will be tested in the order given, and the output will specify
the last scale at which the generator passes, or -1 if it passes at no scales.
```metadata json
"scales": [0.15, 0.3, 0.45, 1]
```
___
**failure_threshold**

This is the number of passes a generator must exceed in order to be deemed to pass the test.
If the number of passes is less than or equal to the failure threshold, then it is considered a failure.
```metadata json
"failure_threshold": 5
```
___
**delayed_coordinates**\[optional]

Whether or not to use the alternate method of point generator, called delayed coordinates.
This is false by default.
```metadata json
"delayed_coordinates": false
```
___
**visualisations**\[optional]

This determines when visualisations will be produced. If `fail`, then visualisations will be produced when
a generator fails the test. If 'all', then visualisations will be produced for every generator at all scales.
By default, no visualisations are produced. Note that visualisations are only supported for 3D.
```metadata json
"visualisations": "all"
```
### Matrix Rank Test
```metadata json
"name": "matrix rank"
```
___
**matrix_size**

Size of matrix to use for the matrix rank test, represented as an integer in \[1, 64].
```metadata json
"matrix_size": 64
```
## generators
This object specifies which generators will be used in the test. 
There are three modes, which fall into two categories of pre-generated and runtime generated.
### Runtime Generated.
This mode generates the values at runtime.

The two modes for selecting generators are `group` or `list`. Only one is required.

___

**group**

Specify a premade group of generators to test, such as linear congruential generators.
These lists can be found in the `generators.py` file.
```metadata json
"group": "LFSRs"
```
___
**list**

Specify a list of specific generators to test. The full list of generators currently supported can be 
found in the `generators.py` file.
```metadata json
"list": ["Randu", "MWC", "XorShift32"]
```
___
**seeds**\[optional]

A list of 4 integers to use as seeds for the random number generators. 
If this isn't provided, then they will be generated using python's `random` module.
```metadata json
"seeds": [
      23525325,
      125325325,
      373592855,
      212601099710477
    ]
```
___
**salt**\[optional]

A string salt to use for the generators that use hashing algorithms. If not provided, then hashing generators won't be included.
```metadata json
"salt": "salty"
```
### Pre-generated.
This mode involves downloading binary files to use for the generators.
___
**directory**

Link to a zipped file containing the binary files, stored on google drive. 
Note that the files should be zipped together, not a zipped folder.
```metadata json
"directory": "https://drive.google.com/uc?id=<FILE ID>"
```
Can be generated from google drive by right clicking the file, and creating shareable link.
This may have ```open``` instead of ```uc```, but you can just replace it.
___
**loop_file**\[optional]

Whether or not to loop back to the start of a binary file, if the end is reached. 
This is represented by a boolean. True by default.
```metadata json
"loop_file": true
```
___
## Example
```metadata json
{
  "test": {
    "name": "hypercube",
    "dimension": 3,
    "scales": [
      0.15,
      0.45,
      1
    ],
    "failure_threshold": 3,
    "delayed_coordinates": false,
    "visualisations": "none"
  },
  "reference_rng": "https://drive.google.com/uc?id=<FILE ID>",
  "runs": 10,
  "n_points": 12000,
  "homology_dimension": 0,
  "filtration_size": 20,
  "generators": {
    "list": ["Randu", "MWC", "XorShift32"],
    "seeds": [
      23525325,
      125325325,
      373592855,
      212601099710477
    ],
    "salt": "salt"
  },
  "verbose": true,
  "recalculate_distribution": false,
  "store_data": true,
  "gpu": false
}
```
