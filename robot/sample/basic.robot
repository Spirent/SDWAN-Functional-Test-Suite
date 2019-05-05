*** Settings ***
Resource        ${EXECDIR}/script/resources.robot

Test Setup      TestInit    TESTCASE_FILE=${TESTCASE_FILES}[${TEST NAME}]
Test Teardown   TestFinish

*** Variables ***
&{TESTCASE_FILES}   sample.basic.001=sample${/}basic_forwarding.yaml
...                 sample.basic.002=sample${/}basic_bgp.yaml

*** Test Cases ***
sample.basic.001
    [Tags]      priority=1
    TestRun

sample.basic.002
    [Tags]      priority=2
    TestRun
