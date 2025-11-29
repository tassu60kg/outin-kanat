*** Settings ***
Resource  resource.robot
Suite Setup  Setup Suite
Suite Teardown  Close Browser

*** Test Cases ***
Homepage has a link to form
    Go To  ${HOME_URL}
    Title Should Be  temp
    Page Should Contain Link  Add reference
    Click Link  Add reference
    Title Should Be  Add a reference

User can add Book Reference
    Go To  ${HOME_URL}
    Add Book Reference
    Go To  ${HOME_URL}
    Check Table Exists
    Check Book Reference In Table

User can add Article Reference
    Go To  ${HOME_URL}
    Add Article Reference
    Go To  ${HOME_URL}
    Check Table Exists
    Check Article Reference In Table

User can add Inproceedings Reference
    Go To  ${HOME_URL}
    Add Inproceedings Reference
    Go To  ${HOME_URL}
    Check Table Exists
    Check Inproceeding Reference In Table

User can delete reference
    Go To  ${HOME_URL}
    Check Table Exists
    Delete Most Recent Reference
    Check Reference is Deleted

*** Keywords ***
Setup Suite
    Open And Configure Browser
    ${test_env}=    Get Environment Variable    TEST_ENV    false
    Run Keyword If    '${test_env}' == 'false'    Empty References

Empty References
    Go To    ${HOME_URL}
    FOR    ${i}    IN RANGE    100
        ${has_delete}=    Run Keyword And Return Status    Page Should Contain Link    Delete
        IF    not ${has_delete}
            Exit For Loop
        END
        Delete Any Reference
    END