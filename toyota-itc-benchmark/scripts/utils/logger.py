import os

class Logger:

    def __init__(self, log_file_path, tool_name):
        self.log_file_path = log_file_path
        self.tool_name = tool_name
        if not os.path.exists(log_file_path):
            os.mkdir(os.path.expanduser(log_file_path))
        self.log_file = open(os.path.expanduser(os.path.join(log_file_path, tool_name + "-log.txt")), 'w+')


    def sanitize_paths(self, output):
        output_new = ""
        for line in output.split('\n'):
            for word in line.split(' '):
                path = word.split('/')
                if len(path) > 1:
                    output_new += (word[-1]) + " "
                else:
                    output_new += (path[0]) + " "
            output_new += "\n"
        return output_new




    def log_output(self, output, file, folder, test_num, result):
         output_new = self.sanitize_paths(output)
         self.log_file.write(self.tool_name + " being tested on " + folder + " " + str(file) + " " + str(test_num) + "\n\n")
         self.log_file.write(output_new + "\n")
         if(result == "TP"):
             self.log_file.write("Confirmed as True Positive \n\n")
         elif(result == "FP"):
             self.log_file.write("Confirmed as False Positive \n\n")

         elif(result == "TO"):
             self.log_file.write("Operation Timed Out Considered a negative \n\n")

         else:
             self.log_file.write("Confirmed Negative \n\n")



    def close_log(self):
        self.log_file.close()