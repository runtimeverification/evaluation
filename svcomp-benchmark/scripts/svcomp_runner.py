import sys
import os
import subprocess32 as subprocess
import re

total_tests = 0
total_undefined = 0
location = sys.argv[1]
log_location = sys.argv[2]
includes_location = os.path.join(location, "decls.h")
implementation_location = os.path.join(location, "implementations.o")

def check_result(output):
    error_regex = re.compile('(UB|CV|USP)\-([A-Z]+[0-9]*)')
    if re.search(error_regex, output):
        return True, output
    return False, ""


def log_result(file, executable, result, output):
    file.write("File " + executable + "\n")
    if result:
        sys.stdout.write("UNDEFINED!\n")
        file.write("Found Undefined Behavior! \n")
        file.write(output + "\n")
    else:
        sys.stdout.write("OK!\n")
        file.write("File was well defined \n")
    file.write("\n")


def run_command(command, timeout):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait(timeout=timeout)
        output = process.stderr.read()
        process.kill()
        return check_result(output)
    except subprocess.TimeoutExpired:
        process.kill()
        if command[0] == "kcc":
            return False, "Timeout"
        return False, ""


def run_example(example_folder):
    tests_run = 0
    undefined = 0
    global total_tests
    global total_undefined
    os.chdir(os.path.join(location, example_folder))
    print("In Directory - " + os.getcwd())
    output_file = open(os.path.join(log_location, example_folder + "-results.txt"), "w+")
    for file in os.listdir(os.getcwd()):
        if "true" in file and file.endswith(".c"):
            tests_run += 1
            simple_name = file.rsplit(".", 1)[0]
            executable_name = simple_name + ".out"
            object_name = simple_name + ".o"
            if not os.path.exists(executable_name):
                sys.stdout.write("[Compile] " + file + " -- ")
                sys.stdout.flush()
                # compile the file
                result, output = run_command(
                        ["kcc", "-c", "-Wno-implementation-defined", "-Wno-unspecified", "-include", includes_location,
                         file, "-o", object_name], 10)

                if output == "Timeout":
                    sys.stdout.write("TIMEOUT!\n")
                    sys.stdout.flush()
                    continue

                if not result:
                    sys.stdout.write("OK!\n")
                    sys.stdout.flush()

                    sys.stdout.write("[Link] " + object_name + " -- ")
                    sys.stdout.flush()
                    command = ["kcc", object_name, implementation_location, "-o", executable_name]
                    result, output = run_command(command,
                                                 20)

                if output == "Timeout":
                    sys.stdout.write("TIMEOUT!\n")
                    sys.stdout.flush()
                    continue

                if not result:
                    sys.stdout.write("OK!\n")
                    sys.stdout.flush()

            else:
                print "[Cache] ",
                result = False
            if result:
                log_result(output_file, file, result, output)
                undefined += 1
                continue
            else:
                # run the executable
                sys.stdout.write("[Run] " + executable_name + " -- ")
                sys.stdout.flush()
                result, output = run_command(["./" + executable_name], 1)
                log_result(output_file, file, result, output)
                if result:
                    undefined += 1

    output_file.write("Total Executables - " + str(tests_run) + "\n")
    output_file.write("Undefined - " + str(undefined) + "\n")
    output_file.close()
    total_tests += tests_run
    total_undefined += undefined


def init_implementations():
    sys.stdout.write("Initializing kcc -- ")
    sys.stdout.flush
    subprocess.check_call(["kcc", "-c", "implementations.c", "-o", os.path.join(location, "implementations.o")])
    sys.stdout.write("ok\n")
    sys.stdout.flush()


def main():
    test_file = open("tests.txt", 'r').read()
    init_implementations()
    map(lambda y: run_example(y), filter(lambda x: x.split(), test_file.split("\n")))
    print("Total Undefined - " + str(total_undefined))
    print("Total Run - " + str(total_tests))


if __name__ == '__main__':
    main()
