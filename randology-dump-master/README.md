# How random is random?


This repository contains artifacts related to the "How random is random?" project. I do not store the random numbers obtained from [RANDOM.ORG](https://random.org) as they take up over 300 megabytes. I will provide a link once they find a permanent home.

## Thesis

The [`thesis/`](thesis/) directory contains all the Java code used to generate the results in my honors thesis, along with Java implementations of many common and exotic PRNG algorithms.

**Usage: **
Make sure that OpenJDK 8 is the default JVM (use the `openjdk-8-jdk` package on Debian-based Linux distributions).
Extract [`thesis/lib.tar.gz`](thesis/lib.tar.gz), which contains all the library dependencies.
Import the project into your favorite IDE, making sure to include all the dependencies in the search path. 
The reference data provided by [RANDOM.ORG](https://random.org) cannot be stored in this repository (it takes up over 300 megabytes of space), but if you have them, you can place them under `thesis/res`. 
If you do not have the reference data, edit [`Generators.java`](thesis/src/uk/ac/stir/randology/Generators.java) and disable all `FromBinaryFile` generators.
Refer to [`XRunExperiment.java`](thesis/src/uk/ac/stir/randology/XRunExperiment.java) on invoking the experiments.

## Reimpl

The [`reimpl/`](reimpl/) directory contains an unfinished Scala reimplementation of the persisent homology computations and the experimental framework  used in my honors thesis.
The original intention was to make all the experiments reproducible (the JavaPlex library used in the original code was far from deterministic).
The homology calculation part works, and includes a complete validation suite, but I never got around to reimplementing the actual experiments

**Usage: **
Make sure that OpenJDK 8 is the default JVM (use the `openjdk-8-jdk` package on Debian-based Linux distributions).
All the dependencies of this project are handled automatically by the build tool `sbt`: execute `sbt test` for the test suite or `sbt run` for an example calculation.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request.

