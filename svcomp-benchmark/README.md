The [SV-benhmark](https://github.com/sosy-lab/sv-benchmarks/tree/master/c) consists of a large number of C programs that are used as verification tasks during the [SV-COMP](http://sv-comp.sosy-lab.org/2016/benchmarks.php). We took 1346 correct (programs that sastisfied their specification) programs from the sv-benchmark, and ran them with [RV-Match](http://runtimeverification.com/match/). We found that out the 1346 correct programs we tested, 188 contained undefined behavior. 

For more information on the results, please see the [results](results/) directory. 

To re-run any of the tests on the benchmark, please follow these [instructions](scripts/README.md).


