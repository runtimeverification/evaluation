import os
import subprocess32 as subprocess
from utils.logger import Logger
from utils.make_pipeline import MakePipeline

class UBSan:
    def get_name(self):
        return self.name


    def __init__(self, benchmark_path, log_file_path):
        self.pipeline = MakePipeline(benchmark_path)
        self.name = "UBSan"
        self.logger = Logger(log_file_path, self.name)
        self.output_dict = {}
        self.tp_set = set([])
        self.fp_set = set([])
        self.neg_count = 0
        os.chdir(os.path.expanduser(benchmark_path))

    def run(self):
        self.pipeline.build_benchmark(CC="clang", CFLAGS="-g -fsanitize=undefined -fsanitize=integer", LD="clang")
        self.pipeline.run_bechmark(self, [], 2)
        return self.output_dict

    def get_output_dict(self):
        return self.output_dict

    def get_tp_set(self):
        print len(self.tp_set)
        return self.tp_set

    def get_fp_set(self):
        print len(self.fp_set)
        return self.fp_set

    def analyze_output(self, exit_code, stdout, stderr, cur_dir, i, j):
        if len(stderr) > 0:
            print(stderr)
        if i not in self.output_dict:
            self.output_dict[i] = {"count": 0, "TP": 0, "FP": 0}
        self.output_dict[i]["count"] += 1
        if "runtime error" in (stdout + stderr).lower():
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
            self.neg_count += 1

    def analyze_timeout(self, cur_dir, i, j):
        if i not in self.output_dict:
            self.output_dict[i] = {"count": 0, "TP": 0, "FP": 0}
        self.output_dict[i]["count"] += 1
        self.logger.log_output("", i, cur_dir, j, "NEG")
        self.neg_count += 1

    def cleanup(self):

        Tool.cleanup(self)
        self.logger.close_log()
