import os
import subprocess32 as subprocess
from utils.logger import Logger
from utils.make_pipeline import MakePipeline

class Helgrind:
    def get_name(self):
        return self.name

    def build(self):
        if "Makefile" in os.listdir(os.getcwd()):
            subprocess.check_call(["make", "clean"])
        subprocess.check_call(["autoreconf", "--install"])
        subprocess.check_call(["automake"])
        subprocess.check_call(["./configure", "CFLAGS=-g"])
        subprocess.check_call(["make"], stderr=subprocess.STDOUT)

    def __init__(self, benchmark_path, log_file_path):
        self.pipeline = MakePipeline(benchmark_path)
        self.name = "Helgrind"
        self.logger = Logger(log_file_path, self.name)
        self.output_dict = {}
        self.tp_set = set([])
        self.fp_set = set([])
        os.chdir(os.path.expanduser(benchmark_path))

    def run(self):
        self.pipeline.build_benchmark(CC="gcc", CFLAGS="-g", LD="gcc")
        self.pipeline.run_bechmark(self, ["valgrind", "--tool=helgrind", "--error-exitcode=10"], 6)
        return self.output_dict

    def get_output_dict(self):
        return self.output_dict

    def get_tp_set(self):
        return self.tp_set

    def get_fp_set(self):
        return self.fp_set

    def analyze_output(self, exit_code, stdout, stderr, cur_dir, i, j):
        print(stderr)
        if i not in self.output_dict:
            self.output_dict[i] = {"count": 0, "TP": 0, "FP": 0}
        self.output_dict[i]["count"] += 1
        if exit_code != 0:
            if "w_Defects" in cur_dir:
                self.output_dict[i]["TP"] += 1
                self.logger.log_output(stderr, i, cur_dir, j, "TP")
                self.tp_set.add((i, j))
            else:
                self.output_dict[i]["FP"] += 1
                self.logger.log_output(stderr, i, cur_dir, j, "FP")
                self.fp_set.add((i, j))
        else:
            self.logger.log_output(stdout, i, cur_dir, j, "NEG")

    def analyze_timeout(self, cur_dir, i, j):
        if i not in self.output_dict:
            self.output_dict[i] = {"count": 0, "TP": 0, "FP": 0}
        self.output_dict[i]["count"] += 1
        self.logger.log_output("", i, cur_dir, j, "NEG")

    def cleanup(self):
        Tool.cleanup(self)
        self.logger.close_log()
