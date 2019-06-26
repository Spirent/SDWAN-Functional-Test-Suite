SD-WAN Functional Test Suite [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
=====================

SD-WAN Functional Test Suite is bundle of automation-oriented test capabilities aimed at providing an end-to-end SD-WAN solution relying on feature rich Spirent products. Test Suite development is based on open source projects including PyATS, Genie, and the Robot Framework allowing users to easily configure and execute SD-WAN test capabilities using this suite. Declarative configuration of testbed topology and test equipment parameters in YAML files models testbed objects such as devices and their interfaces intuitively as Python objects. This eliminates costly development and setup times as well as enables reliable and easy-to-interpret results to be produced.

## Table of Contents
- [Installation](#Installation)
- [Test Case Library](#Test-Case-Library)
- [Test Configuration](#Test-Configuration)
- [Test Execution](#Test-Execution)
- [Test Results](#Test-Results)
- [Folder Structure and Naming](#Folder-Structure-and-Naming)
- [Support](#Support)
- [License](#License)

## Installation
Follow these instructions to obtain a copy of the project source and get it up and running on your local machine for development and testing purposes. The Test suite is based on Python and is designed work on Linux, MacOS, and Windows Subsystem for Linux.

The steps below are specific to setup on an Ubuntu 18.04 LTS or Windows Subsystem Linux (WSL) running Ubuntu 18.04 LTS. Any differences in setup instructions between the two operating systems are specifically highlighted.

1. Requirement: Python3.6 or higher must be installed on your system.

    On Ubuntu run the following command to install additional packages:
    ```
    sudo apt install python3-pip python3-dev python3-venv git
    ```

    On WSL an update to apt-get as well an additional package is needed to satisfy gcc dependencies:
    ```
    sudo apt-get update
    sudo apt install python3-pip python3-dev python3-venv lib32ncurses5-dev git
    ```

2. Clone the SD-WAN Test Suite repository from Git and cd to that repository root folder.

    ```
    git clone https://github.com/SpirentOrion/SDWAN-Functional-Test-Suite.git

    cd ~/SDWAN-Functional-Test-Suite
    ```

3. Setup your Python virtual environment in the repository root folder.

    Create the virtual environment in folder **testenv**
    ```
    python3 -m venv testenv
    ```

    Activate the virtual environment
    ```
    . testenv/bin/activate
    ```

    Add your root folder to the Python path
    ```
    export PYTHONPATH=~/SDWAN-Functional-Test-Suite/
    ```

4. Install the Spirent Testpack framework, SD-WAN Test Suite, and additional dependencies that are needed to execute the tests.

    Install wheel as required for pip package installations
    ```
    pip install wheel
    ```

    Install the Spirent Testpack Framework source
    ```
    pip install -t test_framework spirent-testpack-framework
    ```

    Install the Spirent SD-WAN Test Suite
    ```
    pip install -t testpacks spirent-sdwan-test-suite
    ```

    Install additional required dependencies such as pyATS, Unicon, Genie, Jinja2, Stcrestclient, and Robotframework.  
    ```
    pip install -r requirements.txt
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

2. A mapping file `testpacks/sd-wan/testbed_lab/testbed_map.py` is provided that maps individual test case id's to specific testbed sections within the physical testbed configuration file in Step 3. Find the appropriate testbed section that maps to the test case Id from within the mapping file.

3. Once you have identified the physical testbed section that maps to your test case, you must edit that section with configuration details specific to your lab. This section can be found in a single configuration file `testpacks/sd-wan/testbed_lab/configuration.yaml` which houses configuration for all testbeds. Several other Spirent TestCenter configuration parameters are also exposed, if you need to override the defaults.

4. For SD-WAN scripts there is no DUT configuration in the test script. You must configure the DUT manually before running the test. The gateway address of the emulated devices is the same as with DUT interface IP address.

    **Example:**

    > **Step1:** This example uses SD-WAN_Path_Selection_Application_Aware_Steering, which is identified by its test case id sd-wan.path_selection.002.

    > **Step2:** In the testpacks/sd-wan/testbed_lab/testbed_map.py file, you will find that for test case id sd-wan.path_selection.002, the physical testbed information being used is 3stc_1dut_type01_testbed02.

    > **Step3:** Find the physical testbed section referenced in Step#2 ("3stc_1dut_type01_testbed02") in the following file testpacks/sd-wan/testbed_lab/configuration.yaml and update it with appropriate values for your lab. Note that it uses chassis_1, chassis_2, chassis_3, ls_1. You must modify the IPv4 address under stc1, stc2, stc3, spirent_lab_server_1, and the slot/port number under chassis_1, chassis_2 and chassis_3.

    > **Step4:** Check the gateway address of emulated_devices under 3stc_1dut_type01_testbed02, which should be the same as the interfaces ip address on the DUT. If they are different, modify the gateway or change the DUT interface ip.

For additional details about each test case, please refer to the [TestPack Specification Document](Spirent%20SD-WAN%20Functional%20Test%20Suite%20Specification.pdf). All test cases are explained under their unique Test Case ID in the document.


## Test Execution
1. Before you execute the tests it is required to activate Python 3 virtual environment and set your Python path.

Note: This setup is only required one time per shell instance.

If you have already done this as part of installation, then proceed to Step 2. Otherwise run the commands below.
    ```
    . testenv/bin/activate

    export PYTHONPATH=~/SDWAN-Functional-Test-Suite/
    ```

2. Run tests from the root folder. You can run tests using robot commands, as follows:
    ```
    robot -v testbed_config:testpacks/sd-wan/testbed_lab/configuration.yaml -V testpacks/sd-wan/testbed_lab/testbed_map.py -t sd-wan.path_selection.002 -K off -d testrun testpacks/sd-wan/
    ```

    **Parameters**   
    `testbed_config`: Physical lab Configuration  
    `.../testbed_map.py`: This file maps testcases to specific testbeds in lab configuration file  
    `-t sd-wan.path_selection.002`: Testcase selector  
    `-d testrun`: Output directory for logs/reports  
    `testpacks/sd-wan/`: Folder path where Robot will look for testcase files  

    Refer to section [Test Results](#Test-Results) to check the test results.

    Refer to **Robot Framework User Guide** for a complete syntax of robot commands, including pattern matching for selecting test cases to be executed based on test case ids or tags.

    The -v validate:1 argument is supported for validating testbed files without running tests.
    ```
    robot -v testbed_config:testpacks/sd-wan/testbed_lab/configuration.yaml -V testpacks/sd-wan/testbed_lab/testbed_map.py -t sd-wan.path_selection.002 -v validate:1 -d testrun -L INFO testpacks/sd-wan/core.robot
    ```

## Test Results
Output files are configured using robot command line options.

In section:[Test Execution](#Test-Execution), `-d testrun` specifies the results directory as **testrun**.

Test execution will generate several reports/logs, for example Robot report files, test script logs, and Spirent TestCenter logs.

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

    Every test case has a unique, immutable identifier. This will identify the test case in the metadata file and in the Robot file. Test case ids follow the format **\<testpack>.\<area>.###**, that is the unique testpack name along with a 3 digit testcase number relative to a testpack. For example, `sd-wan.path_selection.002`.

2. Test scripts are organized into testpacks folders **testpacks/sd-wan/**. They are Python based.  

    Every test case is accompanied by metadata, see example `testpacks/sd-wan/path_selection_application_aware_steering.yaml`.

    Each testpack has a specification to describe the test cases. See example in the [TestPack Specification](Spirent%20SD-WAN%20Functional%20Test%20Suite%20Specification.pdf) document.

3. The **testbed_templates** folder is for the logical testbed template. See example: `testpacks/sd-wan/testbed_templates/3stc_1dut_type01.yaml`, which gets the information from the physical lab configuration and generates the final configuration file used by the test script.

4. The **testbed_lab** folder is used for the physical configuration and the mapping file. See example: `testpacks/sd-wan/testbed_lab/testbed_map.py`, which defines the mapping for each test case id to a specific testbed section in physical configuration file `testpacks/sd-wan/testbed_lab/configuration.yaml`. The physical configuration is a single file to be supplied by the end user that contains complete details of their lab equipment, along with how they are interconnected into testbeds.

5. The script **test_framework/script/check_stc_param.py** is used to get the Spirent TestCenter port parameters values(phy and speed). When you edit the port 'phy' and 'speed' in physical lab configuration, you can find their values via this script:
`python script/check_stc_param.py -l <lab server ip> -c <chassis ip> -s <slot number> -p <port number>`


## Support
If you encounter any issues during installation or test execution, have general questions, or feedback around new features, please open an issue on our Github repository. You can also reach the development team via email testpack@spirent.com.


## License
This Test pack is distributed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0), see [LICENSE](./LICENSE) and [NOTICES](./NOTICES) for more information.
