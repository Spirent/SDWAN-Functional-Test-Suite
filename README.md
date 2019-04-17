README for TestPack.
=====================

This archive contains the source code and other files for Testpack.

## Topics
- [Installation](https://github.com/SpirentOrion/SDWAN-Testpack#Installation)
- [Testbed information](https://github.com/SpirentOrion/SDWAN-Testpack#Testbed-information)
- [Test execution](https://github.com/SpirentOrion/SDWAN-Testpack#Test-execution)
- [Repository Files](https://github.com/SpirentOrion/SDWAN-Testpack#Repository-Folders)

## Installation
1. Make sure Python3.4 or higher is installed on your system, On Debian/Ubuntu systems, build-essential and python3-venv also need installed. For running RIDE, Robot framework's free GUI, Python 3.6 or higher is required.

2. Run 'make" from repository root. This will install the Python virtual environment in pkg/atsenv, along with required packages such as pyats, unicon, genie, jinja2, stcrestclient, and robotframework.

## Testbed information
Before test Test execution, the following configuraiton need modified.
1. Physical lab configuration: This is a single template file to be supplied by the user that contains the complete details of their lab equipment, along with how they are interconnected into testbeds. See for exmaple testbeds_lab/sd-wan.yaml, at least, the STC Chassis IP(ipv4 under Stc1, Stc2, Stc3,Stc4,Stc5), Lab Sever IP(ipv4 under spirent_lab_server_1) , SNE IP(ipv4 under sne1) need modified by users. Other STC configuration only need modified if user has any different values or add any new configurations.
2. A mapping file that maps individual test cases to specific physical testbeds identified in the lab configuration file - see for example testbeds_lab/sd-wan_testbedMap.py,which aleady hasall the default mappings. User need to modify this mapping file when a new case is added or change the existing mapping.

## Test execution
1. Activate Python 3 venv. From the repository root folder: . pkg/atsenv/bin/activate
2. Add your own root folder to Python path, example: export PYTHONPATH=/home/spirent/vincent6/SDWAN-Testpack.
3. Run tests. Tests can be run using robot command, as follows:
robot -v testbed_config:testbeds_lab/sd-wan.yaml -V testbeds_lab/sd-wan_testbedMap.py -t sd-wan.path_selection.002 -d testrun test_cases/sd-wan/core.robot

Refer to Robot framework user guide for complete syntax of robot command, including pattern matching for selecting testcases to be executed based on testcase ids or tags. Refer to Section 4.1.4 for reporting test status.

We support -v validate:1 argument for just validating testbed files without running tests.
robot -v testbed_config:testbeds_lab/sd-wan.yaml -V testbeds_lab/sd-wan_testbedMap.py -t sd-wan.path_selection.002 -v validate:1 -d testrun test_cases/sd-wan/core.robot
## Repository Folders
1. Testcases are organized into test_cases folders, see example:test_cases/sd-wan/.We use Robot automation framework as our test runner. Test cases are defined in robot files that accompany Python test scripts. These robot files, such as test_cases/sd-wan/core.robot are the wrappers for Robot framework. They seamlessly call test functions in Python scripts. A set of related test cases can be defined in a single .robot script. Every testcase must have a unique, immutable identifier. This will identify the testcase in the metadata file and in the Robot file. Testcase ids will follow the format <testpack>.<area>.###, that is the unique testpack name along with a 3 digit testcase number relative to a testpack. For example, sd-wan.path_selection.001.
Every test case should be accompanied by metadata, see example test_cases/sd-wan/metadata/sd-wan.path_selection.001.yaml.
Each testpack has a document to discribe the test cases. See example: /home/spirent/vincent5/SDWAN-Testpack/testpacks/sd-wan/"Spirent SD-WAN TestPack Specification.pdf".
2. Test scripts are organized into testpacks folders, see example:testpacks/sd-wan/. They are python based.
3. testbed_templates folder is for the logic testbed template. See example: testbed_templates/sd-wan/3Stc1Dut_Type01.yaml, which get the information from the Physical lab configuration and generate the final configuraiotn file used by the test script.
