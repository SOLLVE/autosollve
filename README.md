
# autoSOLLVEvv

autoSOLLVEvv is an automation command line tool for SOLLVE V&V


This project aims to bridge the gap between the SOLLVE V&V testsuite and the Application Developers/Vendors/Facilities by making the testsuite more accessible by building an interactive and easy to use command line interface tool. This CLI tool seeks to inform its users of the compiler/runtime failures that have already been declared as bugs by the testsuite.

The current version of this tool is built for use on the pre-exascale system Crusher


## Installation

The installation media is located in the UMS012 space on crusher at /sw/crusher/ums/ums012/SOLLVE/autosollvevv/


The installation requires Python3 and pip3 dependencies
```bash
pip3 install -e /sw/crusher/ums/ums012/SOLLVE/autosollvevv/ -t .
```
The -e installation option is for --editable, by which the user wouldn't have to install newer versions as the current version will autmatically be updaed without the need for reinstallation

The -t installation option is for --targert, which helps specify the location of the installation. The '.' at the end is to install in the current working directory


## Usage

```bash
python3 autosollvevv file
```


```bash
positional arguments:
  file                  This is to input the program file

optional arguments:
  -h, --help            show this help message and exit
  -c {llvm,rocm,cce}, --compiler {llvm,rocm,cce}
                        This is to specify the compiler to show all versions
  -cv {llvm_14,llvm_15,llvm_16,rocm_4.5,rocm_5.0,rocm_5.2,cce_14.0.0,cce_14.0.1}, --compilerversion {llvm_14,llvm_15,llvm_16,rocm_4.5,rocm_5.0,rocm_5.2,cce_14.0.0,cce_14.0.1}
                        This is to specify the compiler with it's version
  -omp {4.5,5.0,5.1,5.2}, --openmp {4.5,5.0,5.1,5.2}
                        This is to specify the OpenMP Version

```
