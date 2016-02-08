__author__ = 'manasvi'

import sys
import yaml
import utils.external_info
import math
import os
from tools.itc_benchmark.valgrind import Valgrind
from tools.itc_benchmark.comcert import Compcert
from tools.itc_benchmark.ub_san import UBSan
from tools.itc_benchmark.tsan import TSan
from tools.itc_benchmark.a_san import ASan
from tools.itc_benchmark.m_san import MSan
from tools.itc_benchmark.frama_c import FramaC
from tools.itc_benchmark.helgrind import Helgrind
from tools.itc_benchmark.rv_match import RVMatch
from tabulate import tabulate
from utils.external_info import Info

info = Info()
error_info = info.get_spec_dict()
ignore_list = info.get_ignore_list()
ignore_dict = info.get_ignore_dict()


def merge(dict1, dict2):
    retdict = {}
    for key in dict1.keys():
        if key not in retdict:
            retdict[key] = {"TP": set([]), "FP": set([])}

        retdict[key]["TP"] = retdict[key]["TP"] | dict1[key]["TP"]
        retdict[key]["FP"] = retdict[key]["FP"] | dict1[key]["FP"]

        if key in dict2:
            retdict[key]["TP"] = retdict[key]["TP"] | dict2[key]["TP"]
            retdict[key]["FP"] = retdict[key]["FP"] | dict2[key]["FP"]

    for key in dict2:
        if key not in retdict:
            retdict[key] = {"TP": dict2[key]["TP"],
                            "FP": dict2[key]["FP"]}

    return retdict


def crunch_data(output_dict):
    return_dict = {}
    for key in output_dict:
        return_key = error_info[key]["type"]
        if return_key not in return_dict:
            return_dict[return_key] = {"count": 0, "TP": 0,
                                       "FP": 0}

        return_dict[return_key]["count"] += output_dict[key]["count"]
        return_dict[return_key]["TP"] += output_dict[key]["TP"]
        return_dict[return_key]["FP"] += output_dict[key]["FP"]

    for error_key in return_dict:
        return_dict[error_key]["count"] = return_dict[error_key]["count"] / 2
    return return_dict


def merge_data(tp_tuple_set, fp_tuple_set):
    return_dict = {}
    spec_dict = info.get_spec_dict()

    for key in spec_dict:
        error_type = error_info[key]["type"]
        if error_type not in return_dict:
            return_dict[error_type] = {"count": 0, "TP": 0,
                                       "FP": 0}
        return_dict[error_type]["count"] += spec_dict[key]["actual_count"]
        for testnum in range(1, spec_dict[key]["count"] + 1):
            if (key, testnum) in tp_tuple_set:
                return_dict[error_type]["TP"] += 1
            if (key, testnum) in fp_tuple_set:
                return_dict[error_type]["FP"] += 1
    return return_dict


def tabulate_itc_criteria(tool_list, crunched_data):
    header = [" "]
    for tool in tool_list:
        header.append(tool + " (DR)")
        header.append(tool + " (FRP)")
        header.append(tool + " 100 - (FPR)")
        header.append(tool + " (P)")

    table = []
    print_table = []
    raw_table = []
    for error in crunched_data[0].keys():
        row = []
        print_row = []
        row.append(error)
        print_row.append(error)
        for i in range(0, len(tool_list)):
            dr = round(float(crunched_data[i][error]["TP"]) / float(crunched_data[i][error]["count"]) * 100, 3)
            fpr = round(float(crunched_data[i][error]["FP"]) / crunched_data[i][error]["count"] * 100, 3)
            prod = round(math.sqrt(dr * (100 - fpr)), 3)
            row = row + [(dr, (crunched_data[i][error]["TP"], crunched_data[i][error]["count"])),
                         (fpr, (crunched_data[i][error]["FP"], crunched_data[i][error]["count"])), 100 - fpr, prod]
            print_row = print_row + [
                str(dr) + " (" + str(crunched_data[i][error]["TP"]) + "/" + str(crunched_data[i][error]["count"]) + ")",
                str(fpr) + " (" + str(crunched_data[i][error]["FP"]) + "/" + str(
                        crunched_data[i][error]["count"]) + ")", 100 - fpr, prod]
        table.append(row)
        print_table.append(print_row)
    for error in crunched_data[0].keys():
        row = [error]
        total_tp = 0
        total_fp = 0
        for i in range(0, len(tool_list)):
            raw_tp = crunched_data[i][error]["TP"]
            raw_fp = crunched_data[i][error]["FP"]
            total_tp += raw_tp
            total_fp += raw_fp
            row = row + [raw_tp, raw_fp, crunched_data[i][error]["count"]]
        raw_table.append(row)

    count_dict = info.get_count_dict()
    test_total = info.get_total()
    average = ["Average (weighted)"]
    uaverage = ["Average (unweighted)"]
    for column in range(1, len(table[0])):
        if column % 4 == 0:
            prod = round(math.sqrt(average[-1] * average[-3]), 3)
            average.append(prod)
            prod = round(math.sqrt(uaverage[-1] * uaverage[-3]), 3)
            uaverage.append(prod)
            continue

        sum = 0
        usum = 0
        for row in range(0, len(table)):
            error = table[row][0]
            if column % 3 == 0:
                sum += float(table[row][column]) * (float(count_dict[error]) / test_total)
                usum += float(table[row][column])
                continue
            sum += float(table[row][column][0]) * (float(count_dict[error]) / test_total)
            usum += float(table[row][column][0])
        average.append(round(sum, 3))
        uaverage.append(round((usum / float(9)), 3))

    table.append(average)
    table.append(uaverage)
    print_table.append(average)
    print_table.append(uaverage)
    print tabulate(print_table, headers=header, tablefmt="simple")

    print tabulate(raw_table, headers=["Error", "True Positive Count", "False Positive Count", "Tests Run"])


def run_single_tool(name, output_dict):
    tabulate_itc_criteria([name], map(lambda x: crunch_data(x), [output_dict]))


def run_itc_benchmark(path, log_location, tool):
    global tools
    if tool == "RVMatch":
        tools = [RVMatch(path, log_location)]
    elif tool == "GCC":
        tools = [Valgrind(path, log_location), Helgrind(path, log_location)]
    elif tool == "Clang":
        tools = [UBSan(path, log_location), TSan(path, log_location), ASan(path, log_location),
                 MSan(path, log_location)]
    elif tool == "Compcert":
        tools = [Compcert(path, log_location)]
    elif tool == "FramaC":
        tools = [FramaC(path, log_location)]
    else:
        print "Tool " + tool + " not available"
        return
    output_dicts = map(lambda x: x.run(), tools)
    names_list = map(lambda x: x.get_name(), tools)
    map(lambda x: run_single_tool(names_list[x], output_dicts[x]), xrange(0, len(output_dicts)))
    tp_tuple_set = reduce(lambda a, b: a | b, map(lambda x: x.get_tp_set(), tools), set([]))
    fp_tuple_set = reduce(lambda a, b: a | b, map(lambda x: x.get_fp_set(), tools), set([]))
    if tool == "GCC":
        tp_tuple_set = tp_tuple_set | utils.external_info.get_gcc_warnings_set()
    if tool == "Clang":
        tp_tuple_set = tp_tuple_set | utils.external_info.get_clang_warnings_set()
    data_list = [merge_data(tp_tuple_set, fp_tuple_set)]
    tabulate_itc_criteria(["+".join(names_list)], data_list)
    map(lambda x: x.cleanup(), tools)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Needed: Path to yaml configuration file as argument"
    else:
        yaml_path = sys.argv[1]
        try:
            with open(os.path.expanduser(yaml_path)) as yaml_file:
                parsed_dict = yaml.load(yaml_file.read())
                path = os.path.expanduser(parsed_dict["benchmark_path"])
                log_location = os.path.expanduser(parsed_dict["log_path"])
                tool = parsed_dict["tool"]

                run_itc_benchmark(path, log_location, tool)
        except yaml.error.YAMLError as e:
            print "Error in Parsing Yaml File" + e.output
