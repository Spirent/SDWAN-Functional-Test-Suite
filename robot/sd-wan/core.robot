*** Settings ***
Resource        ${EXECDIR}/script/resources.robot

Test Setup      TestInit    TESTCASE_FILE=${TESTCASE_FILES}[${TEST NAME}]
Test Teardown   TestFinish

*** Variables ***
&{TESTCASE_FILES}   sd-wan.path_selection.001=sd-wan${/}Path_Selection_L2_to_L4_Steering.yaml
...                 sd-wan.path_selection.002=sd-wan${/}Path_Selection_Application_Aware_Steering.yaml
...                 sd-wan.resiliency_link_blackout.002=sd-wan${/}Resiliency_Link_Blackout_Remote_no_Congestion.yaml

*** Test Cases ***
sd-wan.path_selection.001
    [Tags]      priority=1
    TestRun

sd-wan.path_selection.002
    [Tags]      priority=1
    TestRun

sd-wan.resiliency_link_blackout.002
    [Tags]          priority=2
    TestRun
