#### Requirements
* python-2.7
* (RV-Match)[https://runtimeverification.com/match/)

#### Running the Scripts

1. Install Python Dependencies
	* `pip install subprocess32`

2. Run `python svcomp-runner.py <SV-Comp benchmarks path> <Log file path>`. The results of running the RV-Match on the benchmarks are stored at the location specified by the `log file path` argument to the python process. So, for instance, if the sv-benchmarks reside at "/home/rvmatch/sv-benchmarks/c", and I want the result files to be stored at "/home/rvmatch/results", the call to the python script would look like `python svcomp-runner.py /home/rvmatch/sv-benchmarks/c /home/rvmatch/results`.

3. In order to make the programs in the benchmarks executable, we had to provide concrete definitions for functions modelling symbolic values in the benchmarks. The definitions reside in the [implementations.c](implementations.c) file. If you'd like to use your definitions instead of the ones provided, you may do so by replacing the contents of the implementations.c file.

4. Additionally, to choose the folders to be run, modify the tests.txt file. By default, all folders known to work well with rv-match are enabled.
