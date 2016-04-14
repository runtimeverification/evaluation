import sys
import os
import signal
import subprocess32 as subprocess
import re


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
    process = None
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
        process.wait(timeout=timeout)
        output = process.stderr.read()
        return check_result(output)
    except subprocess.TimeoutExpired:
        if command[0] == "kcc":
            return False, "Timeout"
        return False, ""
    finally:
        try:
            if process is not None:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except OSError:
            pass


def run_example(example_folder):
    tests_run = 0
    undefined = 0
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


def init_implementations():
    sys.stdout.write("Initializing kcc -- ")
    sys.stdout.flush
    os.chdir(location)
    subprocess.check_call(["kcc", "-c", "implementations.c", "-o", "implementations.o"])
    sys.stdout.write("ok\n")
    sys.stdout.flush()

def tabulate_results(test_folders):
    print "length" + str(len(test_folders))
    undef_regex = re.compile('Undefined\s\-\s([0-9]+)')
    run_regex = re.compile('Executables\s\-\s([0-9]+)')
    total_undef = 0
    total_run = 0
    for folder in test_folders:
        try:
            file = open(os.path.join(log_location, folder + "-results.txt"))
            content = file.read()
            undef = undef_regex.search(content)
            run = run_regex.search(content)
            if undef is not None and run is not None:
                total_undef += int(undef.group(1))
                total_run += int(run.group(1))
        except IOError as e:
            print e.message
    print "Number of Correct Files Run (with kcc) - " + str(total_run)
    print "Total Number of Correct Files with undefined behavior - " + str(total_undef)






def main():
    test_file = open("tests.txt", 'r').read()
    # init_implementations()
    test_folders = filter(lambda x: x.split(), test_file.split("\n"))
    # map(lambda y: run_example(y), test_folders)
    tabulate_results(test_folders)


if __name__ == '__main__':
    main()
