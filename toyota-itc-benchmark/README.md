Data collected from running static and dynamic analysis tools on the [Toyota ITC Benchmark](https://github.com/Toyota-ITC-SSD/Software-Analysis-Benchmark). These results were collected on February 6th, 2016. 


### Directory Structure
```
├── Compcert
│   └── Compcert .pdf
├── Frama C Value Analysis
│   └── Frama C Value Analysis.pdf
├── README
├── RV-Match
│   └── RV-Match.pdf
├── UBSan+TSan+ASan+MSan (Clang)
│   ├── ASan
│   │   └── ASan.pdf
│   ├── Clang
│   │   └── Clang.pdf
│   ├── MSan
│   │   └── MSan.pdf
│   ├── TSan
│   │   └── TSan.pdf
│   ├── UBSan
│   │   └── UBSan.pdf
│   └── UBSan+TSan+ASan+MSan (Clang).pdf
└── Valgrind+Helgrind (GCC)
    ├── GCC
    │   └── GCC.pdf
    ├── Helgrind
    │   └── Helgrind.pdf
    ├── Valgrind
    │   └── Valgrind.pdf
    └── Valgrind+Helgrind (GCC).pdf

```
### Naming Convention

Every folder has a name representative of a tool, or a set of related tools, and contains data obtained from running the aforementioned tool or set of tools on the benchmark. For instance, the folder Compcert contains data collected from  running Compcert on the ITC benchmark, while the folder Valgrind+Helgrind (GCC) contains data from running multiple separate, but complementary tools on the benchmark. The folder in this case also has three subfolders - GCC, Valgrind and Helgrind each containing data obtained from running the tool individually on the benchmark. Since the tools in this case are complementary, we combine the data, and place it under the main Valgrind+Helgrind (GCC) folder. We run two such suites, containing multiple tools each, on the benchmark. The first suite consists of Valgrind and Helgrind. GCC is used as the C compiler to build the benchmark in this suite. The second suite consists of Memory Sanitizer (MSan), Undefined Behavior Sanitizer (UBSan), Thread Sanitizer (TSan), and Address Sanitizer (ASan). The suite uses Clang C compiler to build the benchmark. We choose to group together these tools under suites as developers often use them together 


### Format of Results
Three parameters have been mentioned in the table used to present results: DR, FPR, and P.
* **DR** (Detect Rate) is the percentage of tests with defects where the tool correctly detected the defect.
* **FPR** (False Positive Rate) is the percentage of tests without defects where the tool incorrectly detected a defect.
* **P** (Productivity) evaluates both DR and FPR at the same time. It's the square root of the product of DR and 100 - FPR. 

### Ignored Tests

The Toyota ITC benchmark used in the ISSRE'15 paper consists of a total of 1276 tests. Half of the tests have defects, while the other half are without any defects. During the experiments we found that a few of these tests had unintended undefinedness bugs, which we reported to the Toyota ITC authors. However, at the time of writing (February  2016), there are still 42 non-trivial unintended bugs in the benchmark, which will need to be fixed. For a fair evaluation, we ignore the 84 corresponding tests (42 with defects and 42 without defects).



