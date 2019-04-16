*** Settings ***
Library     Process
Library     OperatingSystem

*** Variables ***
${TESTBED_FILE}      testbed.yaml
${validate}         0

*** Keywords ***
TestInit
    [Arguments]         ${TESTBED_TOPO}
    Set Environment Variable    SPIRENT_TESTCASE_ID     ${TEST NAME}
    Set Test Variable   ${TEST_DIR}     ${OUTPUT DIR}${/}${TEST NAME}
    Create Directory    ${TEST_DIR}

    ${result} =         run process  ${EXECDIR}/script/generate-config.py  -t  ${EXECDIR}/testbed_templates/${TESTBED_TOPO}  -c  ${testbed_config}  -i  ${TESTCASE_TESTBEDS}[${TEST NAME}]  -f  ${TEST_DIR}/${TESTBED_FILE}
    Should Be Empty     ${result.stderr}
    Run Keyword If      ${validate}==1      ValidateTestbed
    Pass Execution If   ${validate}==1      Done

ValidateTestbed
    ${result} =         run process  ${EXECDIR}/script/validate-config.py  -f  ${TEST_DIR}/${TESTBED_FILE}
    Should Be Empty     ${result.stderr}
