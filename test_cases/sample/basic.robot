*** Settings ***
Resource        ${EXECDIR}/script/resources.robot

Test Setup      TestInit        TESTBED_TOPO=${TESTCASE_TEMPLATE}[${TEST NAME}]
Test Teardown   Run Keyword     ${TEST_CLASS}.cleanup

*** Variables ***
&{TESTCASE_TEMPLATE}    sample.basic.001=common${/}2Stc1Router_Type01.yaml  sample.basic.002=common${/}2Stc1Router_Type01.yaml

*** Test Cases ***
sample.basic.001
    [Tags]      priority=1
    [Timeout]   600
    Set Test Variable   ${TEST_CLASS}   basic_forwarding
    Import Library  testpacks.sample.basic_forwarding   ${TEST_DIR}     ${TESTBED_FILE}  WITH NAME  ${TEST_CLASS}
    Run Keyword     ${TEST_CLASS}.setup
    ${RC} =     Run Keyword     ${TEST_CLASS}.run
    Set Test Message    ${RC}

sample.basic.002
    [Tags]      priority=2
    [Timeout]   600
    Set Test Variable   ${TEST_CLASS}   basic_bgp
    Import Library  testpacks.sample.basic_bgp   ${TEST_DIR}     ${TESTBED_FILE}  WITH NAME  ${TEST_CLASS}
    Run Keyword     ${TEST_CLASS}.setup
    ${RC} =     Run Keyword     ${TEST_CLASS}.run
    Set Test Message    ${RC}
