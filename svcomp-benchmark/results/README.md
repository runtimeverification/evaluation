Data collected from running [RV-Match](https://runtimeverification.com/match) on the [SV-COMP Benchmark Verification Tasks](https://github.com/sosy-lab/sv-benchmarks). These results were collected on April 13th, 2016. More details about the verification tasks, and the structure of the benchmarks can be found at [SV-COMP's website](http://sv-comp.sosy-lab.org/2016/index.php).

#### Naming Convention

C files in The SV-COMP verification benchmarks are organized under [folders](https://github.com/sosy-lab/sv-benchmarks/tree/master/c) named after categories of verification tasks. The error reports follow the naming convention "\<folder-name\>-results.txt", where \<folder-name\> is the name of a folder in the benchmarks. For instance, the file "array-examples-results.txt" contains the results of running RV-Match on the correct examples in the ["array-examples"](https://github.com/sosy-lab/sv-benchmarks/tree/master/c/array-examples) folder.


#### Directory Structure

RV-Match was run on 1346 correct programs from the benchmark. 

Correct files in the following folders were analyzed RV-Match -

* array-examples
* reducercommutativity
* bitvector
* bitvector-regression
* signedintegeroverflow-regression
* heap-manipulation
* list-properties
* ldv-regression
* memsafety
* memsafety-ext
* list-ext-properties
* ldv-memsafety
* floats-cdfpl
* float-benchs
* floats-cbmc-regression
* ssh-simplified
* locks
* loops
* loop-invgen
* loop-acceleration
* loop-new
* loop-lit
* recursive
* recursive-simple
* product-lines
* systemc
* termination-crafted
* termination-crafted-lit
* termination-restricted-15
* pthread-ext
* pthread-wmm
* pthread-lit
* ldv-races


Files in the following folders had been preprocessed, and were not analyzed with RV-Match. 

* ldv-linux-3.0
* ldv-linux-3.4-simple
* ldv-linux-3.7.3
* ldv-commit-tester
* ldv-consumption
* ldv-linux-3.12-rc1
* ldv-linux-3.16-rc1
* ldv-validator-v0.6
* ldv-validator-v0.8
* ldv-linux-4.2-rc1
* ldv-challenges

It must be noted here that C11 sec. 7.1.4:2 states, "Provided that a library function can be declared without reference to any type defined in a header, it is also permissible to declare the function and use it without including its associated header". Files in the above mentioned folders however declare functions that have refer to types defined in headers, without including the headers themselves. This, according to the standard is not permissible, and thus files in the above mentioned folders do not qualify as valid standalone C programs. 

Correct files in the following folders were not analyzed due to miscellaneous reasons, such as limitation of RV-Match, and syntax errors in files.

* ddv-maczwd
* ntdrivers-simplified
* ntdrivers
* ssh
* array-memsafety
* memory-alloca
* termination-libowfat
* termination-15
* seq-mthread
* seq-pthread
* termination-numeric
* pthread
* pthread-atomic


 For more information on how the files were run with RV-Match, please see [scripts](../scripts) directory.
