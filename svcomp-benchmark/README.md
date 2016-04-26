## Checking For Undefined Behavior In Programs Classified As Correct In The SV-COMP Benchmark Suite Using RV-Match

Data presented here was collected on April 13th, 2016.

The [SV-COMP Benchmark Suite](https://github.com/sosy-lab/sv-benchmarks/tree/master/c) consist of a large number of C programs that are used as verification tasks during the [SV-COMP](http://sv-comp.sosy-lab.org/2016/benchmarks.php). We analyzed 1346 programs classified as correct from the benchmarks, and ran them after compiling with [RV-Match](http://runtimeverification.com/match). For more information on how the programs were chosen, please see the [results](results/) directory. For information on how we compiled and ran the programs with RV-Match, please see the [scripts](scripts/) directory. If you'd like to run RV-Match on the benchmarks yourself, or use RV-Match to run more experiments, then you can obtain the latest version of the tool (Academic/Evaluation licenses available) from [RV Inc.'s website](https://runtimeverification.com/match/download/).


We observed that 188 programs (14 %) of the programs exhibited undefined behaviors. Upon further analysis, we found that a large number of them exhibited undefined behaviors arising from subtle and seemingly innocuous mistakes. For instance, every correct program in the [floats-cdfpl](https://github.com/sosy-lab/sv-benchmarks/tree/master/c/floats-cdfpl) folder, when run after compilation with RV-Match, reported error code ["UB-CEE2"](https://github.com/kframework/c-semantics/blob/master/examples/error-codes/Error_Codes.csv) having description - "Indeterminate value used in an expression". This error occured since the main function in every program in floats-cdfpl declares a variable ```float IN```, and uses the variable in expressions without initializing it. One may choose to ignore this error, since these programs don't crash when run after compilation with gcc. A C11 compliant compiler may  however, choose to terminate the programs upon encountering undefined behavior represented by "UB-CEE2", and we'd end up with supposedly correct programs that may crash on completely valid inputs. Thus, it's imperative for programs classified to be correct to not exhibit undefined behavior. 

For more information on all the undefined behaviors we discovered, please see the [results](results/) directory.



