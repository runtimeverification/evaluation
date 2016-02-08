import os
import subprocess32 as subprocess
import utils.external_info
from utils.external_info import Info
from utils.logger import Logger


class FramaC:


    def analyze_output(self, output, file_name):
        print output
        for line in output.split('\n'):
            if file_name in line and "WARNING" in line.upper():
                if "Neither code nor specification" in line:
                    continue
                # Simple condition for an alarm in the file
                return True
        return False

    def get_framac_command(self, cur_dir, file_prefix, temp_dir_name, vflag):
        cur_path = os.path.join(self.benchmark_path, cur_dir)
        temp_path = os.path.join(cur_path, temp_dir_name)
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)

        relevant_file_path = os.path.join(cur_path, file_prefix + ".c")
        bootstrap_file_path = os.path.join(temp_path, file_prefix + "-temp.c")
        utils.external_info.bootstrap_file(relevant_file_path, bootstrap_file_path, vflag, "SH")
        return ["frama-c", "-val", "-machdep", "gcc_x86_64", bootstrap_file_path]

    def run(self):
        relevant_dirs = ["01.w_Defects", "02.wo_Defects"]
        output_dict = {}

        for cur_dir in relevant_dirs:
            spec_dict = self.info.get_spec_dict()
            mapping_dict = self.info.get_file_mapping()
            for i in range(1, len(spec_dict.keys()) + 1):
                if i not in output_dict:
                    output_dict[i] = {"count": 0, "TP": 0, "FP": 0}
                if (i, -1) in self.info.get_ignore_list():
                    continue
                file_prefix = mapping_dict[i]
                verdict = False
                output = ""
                for j in range(1, spec_dict[i]["count"] + 1):
                    if (i, j) in self.info.get_ignore_list():
                        continue
                    output_dict[i]["count"] += 1
                    vflag = str('%03d' % j)
                    framac_command = self.get_framac_command(cur_dir, file_prefix, "framac_dir", vflag)
                    print self.name + " ** " + " ".join(framac_command)
                    try:
                        if len(framac_command) != 0:
                            process = subprocess.Popen(framac_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            process.wait(timeout=8)
                            output = process.stdout.read() + process.stderr.read()
                            verdict = self.analyze_output(output, file_prefix)
                            if verdict:
                                if "w_Defects" in cur_dir:
                                    output_dict[i]["TP"] += 1
                                    self.tp_set.add((i, j))
                                else:
                                    output_dict[i]["FP"] += 1
                                    self.fp_set.add((i, j))

                    except subprocess.TimeoutExpired:
                        self.logger.log_output(output, i, cur_dir, j, "TO")
                    finally:
                        process.kill()
                        if verdict:
                            if "w_Defects" in cur_dir:
                                self.logger.log_output(output, i, cur_dir, j, "TP")
                            else:
                                self.logger.log_output(output, i, cur_dir, j, "FP")
                        else:
                            self.logger.log_output(output, file_prefix + ".c", cur_dir, str(j), "NEG")
        return output_dict

    def get_name(self):
        return self.name

    def __init__(self, benchmark_path, log_path):
        self.info = Info()
        self.benchmark_path = benchmark_path
        self.name = "framac"
        self.logger = Logger(log_path, self.name)
        self.fp_set = set()
        self.tp_set = set()

    def analyze(self):
        Tool.analyze(self)

    def cleanup(self):
        Tool.cleanup(self)
        self.logger.close_log()

    def get_tp_set(self):
        return self.tp_set

    def get_fp_set(self):
        return self.fp_set