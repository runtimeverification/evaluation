#### Requirements
* python-2.7

#### Running the Scripts

1. Install Python Dependencies
	* `pip install subprocess32`
	* `pip install pyyaml`
	* `pip install tabulate`

2. Create a Yaml config file following the format:
	```
	benchmark_path: <Location of the Toyota ITC benchmark directory>

	tool: <Can be one of RVMatch, GCC, Clang, Compcert, FramaC>

	log_path: <Path to the directory where you want the log files to be stored>
	```

3. Run `python benchmark.py <Path to Yaml File>`


