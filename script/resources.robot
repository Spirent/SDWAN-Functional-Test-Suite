*** Settings ***
Library     Process
Library     OperatingSystem

*** Variables ***
${TESTBED_FILE}      testbed.yaml
${validate}         0

*** Keywords ***
TestInit
    [Arguments]         ${TESTCASE_FILE}
    Set Test Variable   ${TEST_DIR}     ${OUTPUT DIR}${/}${TEST NAME}
    Create Directory    ${TEST_DIR}
    Import Variables    ${EXECDIR}/testpacks/${TESTCASE_FILE}
    Should Be Equal     ${TEST NAME}    ${testcase.id}  Testcase id mismatch, mapping incorrect!
    ${result} =         run process     ${EXECDIR}/script/generate-config.py  -t  ${EXECDIR}/testbed_templates/${testcase.run_info.testbed}  -c  ${testbed_config}  -i  ${TESTCASE_TESTBEDS}[${TEST NAME}]  -f  ${TEST_DIR}/${TESTBED_FILE}
    Should Be Empty     ${result.stderr}
    Set Test Variable   &{TEST_INP}     &{testcase.run_info}    testbed=${TESTBED_FILE}     outdir=${TEST_DIR}  testcase_id=${TEST NAME}
    Run Keyword If      ${validate}==1  ValidateTestbed

TestRun
    [Timeout]           ${TEST_INP.timeout}
    Pass Execution If   ${validate}==1      Done
    Set Test Variable   ${TEST_CLASS}   ${TEST_INP.script_class}
    Import Library      ${TEST_INP.script_module}    ${TEST_INP}    WITH NAME   ${TEST_CLASS}
    Run Keyword         ${TEST_CLASS}.setup
    ${RC} =     Run Keyword     ${TEST_CLASS}.run
    Set Test Message    ${RC}

TestFinish
    Pass Execution If   ${validate}==1      Done
    Run Keyword         ${TEST_CLASS}.cleanup

ValidateTestbed
    ${result} =         run process  ${EXECDIR}/script/validate-config.py  -f  ${TEST_DIR}/${TESTBED_FILE}
    Should Be Empty     ${result.stderr}
