README for TestPack.
=====================

This archive contains the source code and other files for Testpack.

## Topics
- [Installation](https://github.com/SpirentOrion/SDWAN-Testpack#Installation)
- [Testbed information](https://github.com/SpirentOrion/SDWAN-Testpack#Testbed-information)
- [Test execution](https://github.com/SpirentOrion/SDWAN-Testpack#Test-execution)
- [Test result](https://github.com/SpirentOrion/SDWAN-Testpack#Test-result)
- [Repository Files](https://github.com/SpirentOrion/SDWAN-Testpack#Repository-Folders)

## Installation
TestPack is designed to run on a Linux environment and based on python.
1. Requirement: Make sure Python3.4 or higher/make/git are installed on your system, On Debian/Ubuntu systems, build-essential (installs make), python3-venv, python3-dev, and curl also need installed.  

    Example how to install these softwares on Ubuntu 18.04, which already includes the Python3.6 and git.
    ```
    sudo apt-get install build-essential python3-venv
    sudo apt-get install python3-dev
    sudo apt-get install curl
    ```
2. Download testpack from Git

    You might need to install Git if not already installed.
    ```
    sudo apt install git
    ```
    Example：
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

## Testbed information
Before test Test execution, you need to know the following information.
1. Read the test case specification. In this specification, there is a Test Case Id for each test case, see the example for sd-wan testpack: [testpacks/sd-wan/Spirent SD-WAN TestPack Specification.pdf](https://github.com/SpirentOrion/SDWAN-Testpack/blob/master/testpacks/sd-wan/Spirent%20SD-WAN%20TestPack%20Specification.pdf).
2. A mapping file that maps individual test cases to specific physical testbeds identified in the lab configuration file. Find the testbed template according to the Test case Id from the testbedMap.py, see the example for sd-wan testpack: `testbeds_lab/sd-wan_testbedMap.py`.
3. You need to modify the physical testbeds informaiton in the lab configuraion.This is a single template file to be supplied by the user that contains the complete details of their lab equipments. See for example `testbeds_lab/sd-wan.yaml`, at least, some ipv4 addresses (ipv4 under Stc1, Stc2, Stc3,Stc4,Stc5,spirent_lab_server_1,sne1) need modified. Other STC configuration only need modified if you requires the different values.
4. For sd-wan, there is no DUT configuration in the test script, you have to configure the DUT manually before running the test.The Gateway of EmulatedDevices are the same as with DUT interface Ip.

    Example:
    ```
    Step1. To run the test case SD-WAN_Path_Selection_Application_Aware_Steering, in testpacks/sd-wan/Spirent SD-WAN TestPack   Specification.pdf, find its Test Case Id is sd-wan.path_selection.002.
    Step2. Find sd-wan.path_selection.002's physical testbed is 3Stc1Dut_Type01_Testbed02 in testbeds_lab/sd-wan_testbedMap.py.
    Step3. In testbeds_lab/sd-wan.yaml, find 3Stc1Dut_Type01_Testbed02 uses chassis_1,chassis_2,chassis_3,ls_1. You need modify the ipv4  under stc1,stc2 , stc3, spirent_lab_server_1, and slot/port number under chassis_1, chassis_2 and chassis_3.
    Step4. Check the Gateway of EmulatedDevices under 3Stc1Dut_Type01_Testbed02, which should be the same as the interfaces' ip on DUT. If they are different, modify the Gateway or change the DUT interface Ip.
    ```

## Test execution
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
    robot -v testbed_config:testbeds_lab/sd-wan.yaml -V testbeds_lab/sd-wan_testbedMap.py -t sd-wan.path_selection.002 -d testrun  test_cases/sd-wan/core.robot
    ```  

    Refer to section [Test result](https://github.com/SpirentOrion/SDWAN-Testpack#Test-result) to check test result.

    Refer to Robot framework user guide for complete syntax of robot command, including pattern matching for selecting testcases to be executed based on testcase ids or tags.

    We support -v validate:1 argument for just validating testbed files without running tests.
    ```
    robot -v testbed_config:testbeds_lab/sd-wan.yaml -V testbeds_lab/sd-wan_testbedMap.py -t sd-wan.path_selection.002 -v validate:1 -d testrun test_cases/sd-wan/core.robot
    ```
## Test result
Output files are configured using robot command line options. In section:[Test execution](https://github.com/SpirentOrion/SDWAN-Testpack#Test-execution), `-d testrun` specifies the result directory is `testrun`. There are robot report files, STC and test script logs.
1. Robot report files: `report.html`, `log.html` and `output.xml` files are typically generated.
   `report.html` contains an overview of the test execution results in HTML format.
   `log.html` contains details about the executed test cases in HTML format.
   `output.xml` contains the test execution results in machine readable XML format.
   You can use any brower to open the result.
    ```
    firefox report.html
    ```

2. test script logs:  
   `test.log.json` under `testrun/sd-wan.resiliency_link.002` contains the test scriopt execution logs.  

3. STC logs:  
   There are STC BLL/IL logs and STC configuraiton under `testrun/sd-wan.resiliency_link.002`.  

## Repository Folders
1. Testcases are organized into test_cases folders, see example: `test_cases/sd-wan`.
We use Robot automation framework as our test runner. Test cases are defined in robot files that accompany Python test scripts. These robot files, such as test_cases/sd-wan/core.robot are the wrappers for Robot framework. They seamlessly call test functions in Python scripts. A set of related test cases can be defined in a single .robot script.  

    Every testcase must have a unique, immutable identifier. This will identify the testcase in the metadata file and in the Robot file. Testcase ids will follow the format **\<testpack>.\<area>.###**, that is the unique testpack name along with a 3 digit testcase number relative to a testpack. For example, `sd-wan.path_selection.001`.

    Every test case should be accompanied by metadata, see example `test_cases/sd-wan/metadata/sd-wan.path_selection.001.yaml`.

    Each testpack has a specification to describe the test cases. See example:`testpacks/sd-wan/"Spirent SD-WAN TestPack Specification.pdf"`.

2. Test scripts are organized into testpacks folders, see example: `testpacks/sd-wan/`. They are python based.

3. `testbed_templates` folder is for the logic testbed template. See example: `testbed_templates/sd-wan/3Stc1Dut_Type01.yaml`, which get the information from the Physical lab configuration and generate the final configuraiotn file used by the test script.
