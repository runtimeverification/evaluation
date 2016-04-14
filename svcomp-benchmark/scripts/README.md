#### Requirements
* python-2.7

#### Running the Scripts

1. Install Python Dependencies
	* `pip install subprocess32`

2. Run `python svcomp-runner.py <SV-Comp benchmark path> <Log file path>`. The results of running the scripts are stored at the location specified by the `log file path` argument to the python process.

3. Additionally, to choose the folders to be run, modify the tests.txt file. By default, all folders known to work well with rv-match are enabled.
