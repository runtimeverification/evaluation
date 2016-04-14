#### Requirements
* python-2.7

#### Running the Scripts

1. Install Python Dependencies
	* `pip install subprocess32`

2. Run `python svcomp-runner.py \<SV-Comp benchmarks path\> \<Log file path\>`. The results of running the RV-Match on the benchmarks are stored at the location specified by the `log file path` argument to the python process.

4. In order to make the programs in the benchmarks executable, we had to provide concrete definitions for functions modelling symbolic values in the benchmarks. The definitions reside in the [implementations.c](implementations.c) file. If you'd like to use your definitions instead of the ones provided, you may do so by replacing the contents of the implementations.c file.

3. Additionally, to choose the folders to be run, modify the tests.txt file. By default, all folders known to work well with rv-match are enabled.
