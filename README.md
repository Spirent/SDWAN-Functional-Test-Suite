SD-WAN TestPack
=====================

This repository contains the source code and other files for SD-WAN Testpack. 
SD-WAN Testpack is bundle of automation-oriented test capabilities aimed to provide an end to end SD-WAN solution relying on feature rich Spirent products. Testpack development is based on open source projects including Python, PyATS, and the Robot Framework. Users will be able to easily configure and execute SD-WAN Test Cases using Testpack. Declarative configuration of test equipment parameters eliminates costly development and setup times. Reliable and easy-to-interpret results are produced.

## Table of Contents
- [Installation](https://github.com/SpirentOrion/SDWAN-Testpack#Installation)
- [Testcase Library](https://github.com/SpirentOrion/SDWAN-Testpack#Testcase-Library)
- [Test Configuration](https://github.com/SpirentOrion/SDWAN-Testpack#Test-Configuration)
- [Test Execution](https://github.com/SpirentOrion/SDWAN-Testpack#Test-Execution)
- [Test Results](https://github.com/SpirentOrion/SDWAN-Testpack#Test-Results)
- [Folder Structure and Naming](https://github.com/SpirentOrion/SDWAN-Testpack#Folder-Structure-and-Naming)

## Installation
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. The TestPack is designed to run on a Linux environment and based on python.

1. Requirement: Make sure Python3.4 or higher are installed on your system. On Ubuntu systems make, python3-venv, python3-dev, curl, and git also need to be installed.  

    Run the following command to install the packages:
    ```
    sudo apt-get install make python3-dev python3-venv curl git
    ```
2. Clone the SD-WAN TestPack repository from Git and cd into that directory:

    ```
    git clone https://github.com/SpirentOrion/SDWAN-Testpack.git
    cd SDWAN-Testpack
    ```
3. Run `make` from repository root. This will install the Python virtual environment in pkg/atsenv, along with required packages such as pyats, unicon, genie, jinja2, stcrestclient, and robotframework.  
    Example：
    ```
    make  
    ```  

    If there is anything wrong with 'make', after solving the errors, run `make clean` to clean up the previous environment and `make` again.  
    ```
    make clean
    make
    ```

## Testcase Library
The table below shows a list of all test scripts provided and a brief description of what each one does.

| Test Case Name | Test Case ID | Test Area | Test Objective |
| --- | --- | ----- | ---------- |
| Path_Selection_L2_to_L4_Steering | sd-wan.path_selection.001 | Path Selection | Validate DUT can steer traffic among WAN links by using traditional L2/L3/L4 traffic classification method |
| Path_Selection_Application_Aware_Steering | sd-wan.path_selection.002 | Path Selection | Validate DUT can steer traffic among WAN links by using application aware traffic classification method |
| Resiliency_Link_Blackout_Local_No_Congestion | sd-wan.resiliency_link_blackout.001 | Resiliency Link Blackout | Validate DUT can steer traffic from Internet link to MPLS link if link blackout was detected on internet link and vice versa |
| Resiliency_Link_Blackout_Remote_No_Congestion | sd-wan.resiliency_link_blackout.002 | Resiliency Link Blackout | Validate DUT can steer traffic from Internet link to MPLS link if link blackout was detected on internet link and vice versa |
| Resiliency_Link_Brownout_Packet_Loss | sd-wan.resiliency_link_brownout.001 | Resiliency Link Brownout | Validate DUT can steer traffic from Internet link to MPLS link if packet loss ratio on Internet link exceeds threshold and vice versa |
| Resiliency_Link_Brownout_Packet_Delay | sd-wan.resiliency_link_brownout.002 | Resiliency Link Brownout | Validate DUT can steer traffic from Internet link to MPLS link if two-way delay (from DUT1 to DUT2) on Internet link exceeds threshold and vice versa |
| Resiliency_Link_Brownout_Jitter | sd-wan.resiliency_link_brownout.003 | Resiliency Link Brownout | Validate DUT can steer traffic from Internet link to MPLS link if jitter on Internet link exceeds threshold and vice versa |
| Resiliency_Link_Brownout_Out_Of_Order | sd-wan.resiliency_link_brownout.004 | Resiliency Link Brownout | Validate DUT can steer traffic from Internet link to MPLS link if packet out-of-order ratio on Internet link exceeds threshold and vice versa |
| Resiliency_Link_Brownout_Duplication | sd-wan.resiliency_link_brownout.005 | Resiliency Link Brownout | Validate DUT can steer traffic from Internet link to MPLS link if packet duplication ratio on Internet link exceeds threshold and vice versa |

## Test Configuration
Before test Test execution, you need to know the following information.
1. Identify the test case name and id you need to execute from the table in above section.

2. A mapping file is provided that maps individual test cases to specific topology within the physical testbed configuration file. Find the appropriate physical testbed section that maps to the Test case Id from the mapping file `testbeds_lab/sd-wan_testbedMap.py`.

3. Next you will need to modify the physical testbed information within your lab. This is a single configuration file to be supplied by the user that contains the complete details of their lab equipments. See for example `testbeds_lab/sd-wan.yaml`. Several other STC configuration paramaters are also exposed if you need to override the defaults.

4. For SD-WAN scripts there is no DUT configuration in the test script. You have to configure the DUT manually before running the test. The Gateway of EmulatedDevices are the same as with DUT interface IP.

    Example:
    ```
    Step1. For this example we will use SD-WAN_Path_Selection_Application_Aware_Steering, which is identified by its Test Case Id sd-wan.path_selection.002.

    Step2. In the testbeds_lab/sd-wan_testbedMap.py file you will find that for test case id sd-wan.path_selection.002, the physical testbed information being used is 3Stc1Dut_Type01_Testbed02.

    Step3. In testbeds_lab/sd-wan.yaml file find the section referenced in Step#2 (3Stc1Dut_Type01_Testbed02) and see that it uses chassis_1, chassis_2, chassis_3, ls_1. You will need modify the ipv4 under stc1, stc2, stc3, spirent_lab_server_1, and slot/port number under chassis_1, chassis_2 and chassis_3.

    Step4. Check the Gateway of EmulatedDevices under 3Stc1Dut_Type01_Testbed02, which should be the same as the interfaces' ip on DUT. If they are different, modify the Gateway or change the DUT interface Ip.
    ```

For additional details around each test cases please refer to the [TestPack Specification Document](https://github.com/SpirentOrion/SDWAN-Testpack/blob/master/testpacks/sd-wan/Spirent%20SD-WAN%20TestPack%20Specification.pdf). All test cases are laid out by their unique Test Case ID in the document.

## Test Execution
1. Activate Python 3 venv. From the repository root folder:
    ```
    . pkg/atsenv/bin/activate
    ```
2. Add your root folder to Python path:
    ```
    export PYTHONPATH=/home/spirent/SDWAN-Testpack
    ```

3. Run tests from the root folder. Tests can be run using robot command, as follows:
    ```
    robot -v testbed_config:testbeds_lab/sd-wan.yaml -V testbeds_lab/sd-wan_testbedMap.py -t sd-wan.path_selection.002 -d testrun robot/sd-wan/core.robot
    ```  

    Refer to section [Test Results](https://github.com/SpirentOrion/SDWAN-Testpack#Test-Results) to check test result.

    Refer to Robot framework user guide for complete syntax of robot command, including pattern matching for selecting testcases to be executed based on testcase ids or tags.

    We support -v validate:1 argument for just validating testbed files without running tests.
    ```
    robot -v testbed_config:testbeds_lab/sd-wan.yaml -V testbeds_lab/sd-wan_testbedMap.py -t sd-wan.path_selection.002 -v validate:1 -d testrun robot/sd-wan/core.robot
    ```

## Test results
Output files are configured using robot command line options.

In section:[Test Execution](https://github.com/SpirentOrion/SDWAN-Testpack#Test-Execution), `-d testrun` specifies the results directory as `testrun`.

There are several reports/logs that are generated (Robot report files, test script logs, and STC logs).

1. Robot report files:   
   `report.html`, `log.html` and `output.xml` files are typically generated.  
   `report.html` contains an overview of the test execution results in HTML format.  
   `log.html` contains details about the executed test cases in HTML format.  
   `output.xml` contains the test execution results in XML format.  
   You can use any browser to open the result.  
    ```
    firefox report.html
    ```

2. test script logs:  
   `test.log.json` under `testrun/sd-wan.path_selection.002` contains the test script execution logs.

3. STC logs:  
   There are STC BLL/IL logs and STC configuration under `testrun/sd-wan.path_selection.002`.  

## Folder Structure and Naming
1. Robot files are organized into testpacks folders, see example: `testpacks/sd-wan`.

Robot automation framework is used as our test runner. Test cases are defined in robot files that accompany Python test scripts. These robot files, such as `testpacks/sd-wan/core.robot` are the wrappers for Robot framework. They seamlessly call test functions in Python scripts. A set of related test cases can be defined in a single `.robot` script.

    Every testcase must have a unique, immutable identifier. This will identify the testcase in the metadata file and in the Robot file. Testcase ids will follow the format **\<testpack>.\<area>.###**, that is the unique testpack name along with a 3 digit testcase number relative to a testpack. For example, `sd-wan.path_selection.002`.

2. Test scripts are organized into testpacks folders, see example: `testpacks/sd-wan/`. They are python based.  

    Every test case should be accompanied by metadata, see example `testpacks/sd-wan/Path_Selection_Application_Aware_Steering.yaml`.

    Each testpack has a specification to describe the test cases. See example:`testpacks/sd-wan/"Spirent SD-WAN TestPack Specification.pdf"`.  

3. `testbed_templates` folder is for the logical testbed template. See example: `testpacks/sd-wan/testbed_templates/3Stc1Dut_Type01.yaml`, which get the information from the Physical lab configuration and generate the final configuration file used by the test script.

4. `testbeds_lab` folder is used for the physical configuration and the mapping file. See example: `testbeds_lab/sd-wan_testbedMap.py`, which defines the mapping for each test case id to section in physical configuration file `testbeds_lab/sd-wan.yaml`
