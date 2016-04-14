The [SV-benhmark](https://github.com/sosy-lab/sv-benchmarks/tree/master/c) consists of a large number of C programs that are used as verification tasks during the [SV-COMP](http://sv-comp.sosy-lab.org/2016/benchmarks.php). We took 1346 programs classified as correct from the benchmark, and ran them after compiling with [RV-Match](http://runtimeverification.com/match). For more information on how we compiled the programs with RV-Match, please see the [scripts](scipts/) directory. 

We observed that 188 programs (14 %) of the programs exhibited undefined behaviors. Upon further analysis, we found that a large number of them exhibited undefined behaviors arising from very subtle and seemingly innocuous mistakes. For instance, every correct program in the floats-cdfpl, when after compilation with RV-Match, spat out the following error - "Indeterminate value used in an expression". This error occured since the main function in every program in ```floats-cdfpl``` declared a variable ```float IN```, and used the variable without initiazing it. 

The presence of undefined behavior in these correct programs also render them unusable in their application as verification tasks for SV-COMP, as correctly verified programs cannot exhibit undefined behavior along any execution paths. SV-COMP participants may also be able to use the results of this analysis to improve their effectiveness and accuracy. For more information on the undefined behaviors we discovered with all the correct programs, please see the [results](results/) directory.



