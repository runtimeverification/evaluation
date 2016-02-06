Data collected from running static and dynamic analysis tools on the Toyota ITC Benchmark (http://github.com/regehr/itc-benchmarks/).

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

Every folder has a name representative of a tool, or a set of related tools, and contains data obtained from running the aforementioned tool or set of tools on the benchmark. For instance, the folder Compcert contains data collected from  running Compcert on the ITC benchmark, while the folder Valgrind+Helgrind (GCC) contains data from running multiple separate, but complementary tools on the benchmark. The folder in this case also has three subfolders - GCC, Valgrind and Helgrind each containing data obtained from running the tool individually on the benchmark. Since the tools in this case are complementary, we combine the data, and place it under the main Valgrind+Helgrind (GCC) folder.

### Format of Results
Each result consists of 2 tables. Three parameters have been mentioned in the table: DR, FPR, and P.
* **DR** (Detect Rate) is the percentage of tests with defects where the tool correctly detected the defect.
* **FPR** (False Positive Rate) is the percentage of tests without defects where the tool incorrectly detected a defect.
* **P** (Productivity) evaluates both DR and FPR at the same time. It's the square root of the product of DR and 100 - FPR. 

The second table lists numbers obtained while running the tool on the tests. Parameters used in the table:
* **# w Defects Detected** is the number of tests with defects where the tool correctly found the defect.
* **# w/o Defects Detected** is the number of tests w/o defects where the tool incorrectly reported an defect.
* **# of Variations in total** is the total number of tests, or variations in the benchmark. Note that the number of tests we run differs from the number mentioned in the paper. Refer to the Ignored Tests section for details.  


### Ignored Tests

The Toyota ITC benchmark, described in this [ISSRE'15](https://www.researchgate.net/publication/283548090_Test_Suites_for_Benchmarks_of_Static_Analysis_Tools) paper consists of a total of 1276 tests. Half of the tests have defects, while the other half are without any defects. We were able to detect, using RV-Match, bugs in many tests in the benchmark itself. We corrected several of the them, and made a pull request into the original repository with the fixes. However, at the time of writing, there were still 38 tests with non-trivial bugs. We ignore these 38 tests, and the corresponding with or without defects versions.



