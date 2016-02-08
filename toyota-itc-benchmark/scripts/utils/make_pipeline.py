import subprocess32 as subprocess
import os
from utils import external_info


class MakePipeline:
    def __init__(self, benchmark_path):
        self.benchmark_path = benchmark_path
        self.info = external_info.Info()

    def build_benchmark(self, CC, CFLAGS, LD):
        os.chdir(self.benchmark_path)
        if "Makefile" in os.listdir(os.getcwd()):
            subprocess.check_call(["make", "clean"])
            pass
        subprocess.check_call(["./bootstrap"])
        subprocess.check_call(["automake"])
        subprocess.check_call(["./configure", "CC=" + CC, "LD=" + LD, "CFLAGS=" + CFLAGS])
        subprocess.check_call(["make"], stderr=subprocess.STDOUT)

    def run_bechmark(self, tool_self, pre_condition_array=[], timeout=3):
        os.chdir(self.benchmark_path)
        spec_dict = self.info.get_spec_dict()
        ignore_list = self.info.get_ignore_list()
        mapping_dict = self.info.get_file_mapping()
        for cur_dir in ["01.w_Defects", "02.wo_Defects"]:
            benchmark = 0
            executable_name = cur_dir.split('.')[0] + "_" + cur_dir.split('.')[-1]
            for i in spec_dict:
                if (i, -1) in ignore_list:
                    continue
                for j in xrange(1, spec_dict[i]["count"] + 1):
                    if (i, j) in ignore_list:
                        continue
                    benchmark += 1
                    file_prefix = mapping_dict[i]
                    arg = str('%03d' % i) + str('%03d' % j)
                    command = pre_condition_array + [os.path.join(self.benchmark_path, cur_dir, executable_name), arg]
                    print tool_self.get_name() + " ** " + " ".join(command)
                    try:
                        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        exit_code = process.wait(timeout=timeout)
                        tool_self.analyze_output(exit_code, process.stdout.read(), process.stderr.read(), cur_dir, i, j)
                    except subprocess.TimeoutExpired:
                        tool_self.analyze_timeout(cur_dir, i, j)
                    finally:
                        process.kill()
            print benchmark
