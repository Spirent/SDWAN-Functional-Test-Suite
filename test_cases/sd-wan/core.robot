*** Settings ***
Resource        ${EXECDIR}/script/resources.robot

Test Setup      TestInit        TESTBED_TOPO=${TESTCASE_TEMPLATE}[${TEST NAME}]
Test Teardown   Run Keyword     ${TEST_CLASS}.cleanup

*** Variables ***
&{TESTCASE_TEMPLATE}    sd-wan.path_selection.001=sd-wan${/}3Stc1Dut_Type01.yaml    sd-wan.resiliency_link.002=sd-wan${/}3Stc1Sne2Dut_Type01.yaml

*** Test Cases ***
sd-wan.path_selection.001
    [Tags]      priority=1
    [Timeout]   600
    Set Test Variable   ${TEST_CLASS}   path_selection_L2_L4_steering
    Import Library  testpacks.sd-wan.path_selection_L2_L4_steering   ${TEST_DIR}     ${TESTBED_FILE}  WITH NAME  ${TEST_CLASS}
    Run Keyword     ${TEST_CLASS}.setup
    ${RC} =     Run Keyword     ${TEST_CLASS}.run
    Set Test Message    ${RC}

sd-wan.resiliency_link.002
    [Tags]          priority=2
    [Timeout]       1200
    Set Test Variable  ${TEST_CLASS}  sd_wan_resiliency_link_002
    Import Library  testpacks.sd-wan.SD-WAN_Resiliency_Link_Blackout_Remote_no_Congestion.sd_wan_resiliency_link_002  ${TEST_DIR}   ${TESTBED_FILE}  WITH NAME  ${TEST_CLASS}
    Run Keyword  ${TEST_CLASS}.setup
    ${RC} =  Run Keyword  ${TEST_CLASS}.run
    Set Test Message  ${RC}