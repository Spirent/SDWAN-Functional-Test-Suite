SD-WAN Functional Test Suite [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
=====================

This repository contains the source code and other files for SD-WAN Testpack.
SD-WAN Testpack is bundle of automation-oriented test capabilities aimed to provide an end-to-end SD-WAN solution relying on feature rich Spirent products. Testpack development is based on open source projects including Python, PyATS, and the Robot Framework. Users will be able to easily configure and execute SD-WAN Test Cases using Testpack. Declarative configuration of test equipment parameters eliminates costly development and setup times. Reliable and easy-to-interpret results are produced.

## Table of Contents
- [Installation](#Installation)
- [Test Case Library](#Test-Case-Library)
- [Test Configuration](#Test-Configuration)
- [Test Execution](#Test-Execution)
- [Test Results](#Test-Results)
- [Folder Structure and Naming](#Folder-Structure-and-Naming)

## Installation
Follow these instructions to obtain a copy of the project and get it up and running on your local machine for development and testing purposes. The TestPack is designed to run on a Linux environment and is based on Python.

1. Requirement: Python3.4 or higher must be installed on your system. On Ubuntu systems make, python3-venv, python3-dev, curl, and git must also be installed.

    Run the following command to install the packages:
    ```
    sudo apt-get install make python3-dev python3-venv curl git
    ```
2. Clone the SD-WAN TestPack repository from Git and cd to that directory:

    ```
    git clone https://github.com/SpirentOrion/SDWAN-Testpack.git
    cd SDWAN-Testpack
    ```
3. Run `make` from the repository root. This installs the Python virtual environment in pkg/atsenv, along with required packages such as pyats, unicon, genie, jinja2, stcrestclient, and robotframework.  
    Example：
    ```
    make  
    ```  

    If there are errors when you run `make`, resolve the errors, and run `make clean` to clean up the previous environment and then run `make` again.  
    ```
    make clean
    make
    ```

## Test Case Library
This table includes a list of the test scripts and a brief description of their function.

| Test Case Name | Test Case ID | Test Objective |
| :---           | ---          | :---           |
| Path_Selection_L2_to_L4_Steering | sd-wan.path_selection.001 | Validate DUT can steer traffic among WAN links by using traditional L2/L3/L4 traffic classification method |
| Path_Selection_Application_Aware_Steering | sd-wan.path_selection.002 | Validate DUT can steer traffic among WAN links by using application aware traffic classification method |
| Resiliency_Link_Blackout_Local_No_Congestion | sd-wan.resiliency_link.001 | Validate DUT can steer traffic from Internet link to MPLS link if link blackout was detected on local side of internet link and vice versa |
| Resiliency_Link_Blackout_Remote_No_Congestion | sd-wan.resiliency_link.002 | Validate DUT can steer traffic from Internet link to MPLS link if link blackout was detected on remote side of internet link and vice versa |
| Resiliency_Link_Brownout_Packet_Loss | sd-wan.resiliency_link.003 | Validate DUT can steer traffic from Internet link to MPLS link if packet loss ratio on Internet link exceeds threshold and vice versa |
| Resiliency_Link_Brownout_Packet_Delay | sd-wan.resiliency_link.004 | Validate DUT can steer traffic from Internet link to MPLS link if two-way delay (from DUT1 to DUT2) on Internet link exceeds threshold and vice versa |
| Resiliency_Link_Brownout_Jitter | sd-wan.resiliency_link.005 | Validate DUT can steer traffic from Internet link to MPLS link if jitter on Internet link exceeds threshold and vice versa |
| Resiliency_Link_Brownout_Out_Of_Order | sd-wan.resiliency_link.006 | Validate DUT can steer traffic from Internet link to MPLS link if packet out-of-order ratio on Internet link exceeds threshold and vice versa |
| Resiliency_Link_Brownout_Duplication | sd-wan.resiliency_link.007 | Validate DUT can steer traffic from Internet link to MPLS link if packet duplication ratio on Internet link exceeds threshold and vice versa |


## Test Configuration
Before test execution, follow these steps.

1. Identify the test case name and id that you want to execute from the table in the previous section.

2. A mapping file is provided that maps individual test cases to specific topology within the physical testbed configuration file. Find the appropriate physical testbed section that maps to the test case Id from the mapping file `testbeds_lab/sd-wan_testbed_map.py`.

3. You must modify the physical testbed information within your lab. This is a single configuration file to be supplied by the user that contains the complete details of their lab equipments. For example, refer to `testbeds_lab/sd-wan_configuration.yaml`. Several other Spirent TestCenter configuration parameters are also exposed, if you need to override the defaults.

4. For SD-WAN scripts there is no DUT configuration in the test script. You must configure the DUT manually before running the test. The gateway address of the emulated devices is the same as with DUT interface IP address.

    **Example:**

    > **Step1:** This example uses SD-WAN_Path_Selection_Application_Aware_Steering, which is identified by its test case id sd-wan.path_selection.002.

    > **Step2:** In the testbeds_lab/sd-wan_testbed_map.py file, you will find that for test case id sd-wan.path_selection.002, the physical testbed information being used is 3stc_1dut_type01_testbed02.

    > **Step3:** In testbeds_lab/sd-wan_configuration.yaml file, find the section referenced in Step#2 ("3stc_1dut_type01_testbed02") and note that it uses chassis_1, chassis_2, chassis_3, ls_1. You must modify the IPv4 address under stc1, stc2, stc3, spirent_lab_server_1, and the slot/port number under chassis_1, chassis_2 and chassis_3.

    > **Step4:** Check the gateway address of emulated_devices under 3stc_1dut_type01_testbed02, which should be the same as the interfaces ip address on the DUT. If they are different, modify the gateway or change the DUT interface ip.

For additional details about each test case, please refer to the [TestPack Specification Document](https://github.com/SpirentOrion/SDWAN-Testpack/blob/master/testpacks/sd-wan/Spirent%20SD-WAN%20TestPack%20Specification.pdf). All test cases are explained under their unique Test Case ID in the document.


## Test Execution
1. Activate Python 3 venv. From the repository root folder:
    ```
    . pkg/atsenv/bin/activate
    ```
2. Add your root folder to the Python path:
    ```
    export PYTHONPATH=/home/spirent/SDWAN-Testpack
    ```

3. Run tests from the root folder. You can run tests using robot commands, as follows:
    ```
    robot -v testbed_config:testbeds_lab/sd-wan_configuration.yaml -V testbeds_lab/sd-wan_testbed_map.py -t sd-wan.path_selection.002 -d testrun robot/sd-wan/core.robot
    ```  

    Refer to section [Test Results](#Test-Results) to check the test results.

    Refer to *Robot Framework User Guide* for a complete syntax of robot commands, including pattern matching for selecting test cases to be executed based on test case ids or tags.

    The -v validate:1 argument is supported for validating testbed files without running tests.
    ```
    robot -v testbed_config:testbeds_lab/sd-wan_configuration.yaml -V testbeds_lab/sd-wan_testbed_map.py -t sd-wan.path_selection.002 -v validate:1 -d testrun testpacks/sd-wan/core.robot
    ```

## Test Results
Output files are configured using robot command line options.

In section:[Test Execution](#Test-Execution), `-d testrun` specifies the results directory as `testrun`.

Several reports/logs are generated, for example Robot report files, test script logs, and Spirent TestCenter logs.

1. Robot report files:   
   `report.html`, `log.html` and `output.xml` files are typically generated.  
   `report.html` contains an overview of the test execution results in HTML format.  
   `log.html` contains details about the executed test cases in HTML format.  
   `output.xml` contains the test execution results in XML format.  
   You can use any browser to open the result.  
    ```
    firefox report.html
    ```

2. Test script logs:  
   `test.log.json` under `testrun/sd-wan.path_selection.002` contains the test script execution logs.

3. Spirent TestCenter logs:  
   There are Spirent TestCenter BLL/IL and configuration logs under `testrun/sd-wan.path_selection.002`.  


## Folder Structure and Naming
1. Robot files are organized into testpacks folders, for example: `testpacks/sd-wan`.

    Robot automation framework is the test runner. Test cases are defined in robot files that accompany Python test scripts. These robot files, such as `testpacks/sd-wan/core.robot` are the wrappers for Robot framework. They seamlessly call test functions in Python scripts. A set of related test cases can be defined in a single `.robot` script.

    Every test case must have a unique, immutable identifier. This will identify the test case in the metadata file and in the Robot file. Test case ids follow the format **\<testpack>.\<area>.###**, that is the unique testpack name along with a 3 digit testcase number relative to a testpack. For example, `sd-wan.path_selection.002`.

2. Test scripts are organized into testpacks folders, see example: `testpacks/sd-wan/`. They are Python based.  

    Every test case should be accompanied by metadata, see example `testpacks/sd-wan/path_selection_application_aware_steering.yaml`.

    Each testpack has a specification to describe the test cases. See example:`testpacks/sd-wan/"Spirent SD-WAN TestPack Specification.pdf"`.  

3. The `testbed_templates` folder is for the logical testbed template. See example: `testpacks/sd-wan/testbed_templates/3stc_1dut_type01.yaml`, which gets the information from the physical lab configuration and generates the final configuration file used by the test script.

4. The `testbeds_lab` folder is used for the physical configuration and the mapping file. See example: `testbeds_lab/sd-wan_testbed_map.py`, which defines the mapping for each test case id to a section in physical configuration file `testbeds_lab/sd-wan_configuration.yaml`


## License
This Test pack is distributed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0), see [LICENSE](./LICENSE) and [NOTICE](./NOTICE) for more information.
