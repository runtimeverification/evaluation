import os
import subprocess32 as subprocess
import utils.external_info
from utils.external_info import Info
import utils.logger


class Compcert:
    def get_compcert_command(self, cur_dir, file_prefix, temp_dir_name, vflag):
        cur_path = os.path.join(self.benchmark_path, cur_dir)
        temp_path = os.path.join(cur_path, temp_dir_name)
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)

        relevant_file_path = os.path.join(cur_path, file_prefix + ".c")
        bootstrap_file_path = os.path.join(temp_path, file_prefix + "-temp.c")
        utils.external_info.bootstrap_file(relevant_file_path, bootstrap_file_path, vflag)
        return ["ccomp", "-interp", "-fbitfields", "-fstruct-passing",
                "-I" + os.path.join(self.benchmark_path, "include"),
                bootstrap_file_path]

    def check_output(self, output):
        if "ERROR" not in output.upper() and "UNDEFINED" not in output.upper():
            return False
        if "Stuck state: calling" in output:
            return False
        return True

    def run(self):
        relevant_dirs = ["01.w_Defects", "02.wo_Defects"]
        output_dict = {}
        ignore_list = self.info.get_ignore_list()
        for cur_dir in relevant_dirs:
            spec_dict = self.info.get_spec_dict()
            mapping_dict = self.info.get_file_mapping()
            for i in range(1, len(spec_dict.keys()) + 1):
                if i not in output_dict:
                    output_dict[i] = {"count": 0, "TP": 0, "FP": 0}
                if (i, -1) in ignore_list:
                    continue
                file_prefix = mapping_dict[i]
                print self.name + " being tested on folder " + cur_dir + " and file " + file_prefix + ".c"
                output = ""
                for j in range(1, spec_dict[i]["count"] + 1):
                    if (i, j) in ignore_list:
                        continue
                    output_dict[i]["count"] += 1
                    vflag = str('%03d' % j)
                    compcert_command = self.get_compcert_command(cur_dir, file_prefix, "bootstrap_dir", vflag)
                    print " ".join(compcert_command)
                    verdict = "NEG"
                    try:
                        if len(compcert_command) != 0:
                            process = subprocess.Popen(compcert_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            exit_code = process.wait(timeout=5)
                            output = process.stdout.read() + process.stderr.read()
                            print output
                            if exit_code != 0:
                                if self.check_output(output):
                                    if "w_Defects" in cur_dir:
                                        output_dict[i]["TP"] += 1
                                        verdict = "TP"
                                        self.tp_set.add((i, j))
                                    else:
                                        output_dict[i]["FP"] += 1
                                        verdict = "FP"
                                        self.fp_set.add((i, j))

                    except subprocess.TimeoutExpired:
                        verdict = "TO"

                    finally:
                        if len(compcert_command) > 0:
                            process.kill()
                        self.logger.log_output(output, i, cur_dir, j, verdict)

        return output_dict

    def get_name(self):
        return self.name

    def __init__(self, benchmark_path, log_file_path):
        self.info = Info()
        self.benchmark_path = benchmark_path
        self.name = "Compcert"
        self.logger = utils.logger.Logger(log_file_path, self.name)
        self.tp_set = set([])
        self.fp_set = set([])

    def cleanup(self):
        self.logger.close_log()
