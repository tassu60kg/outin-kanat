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

User can see BibTeX of all references
    Go To  ${HOME_URL}
    Add Book Reference
    Add Article Reference
    Add Inproceedings Reference
    Go To  ${HOME_URL}
    Open BibTeX Page
    Page Should Contain    Copy your BibTeX references here
    Check Book Reference In BibTeX
    Check Article Reference In BibTeX
    Check Inproceedings Reference In BibTeX
    Click Button    Back
    Title Should Be    temp


*** Keywords ***
Setup Suite
    Open And Configure Browser
    ${test_env}=    Get Environment Variable    TEST_ENV    false
    Run Keyword If    '${test_env}' == 'false'    Empty References
    Run Keyword If    '${test_env}' == 'true'     Reset Database

Empty References
    Go To    ${HOME_URL}
    FOR    ${i}    IN RANGE    100
        ${has_delete}=    Run Keyword And Return Status    Page Should Contain Link    Delete
        IF    not ${has_delete}
            Exit For Loop
        END
        Delete Any Reference
    END

Reset Database
    Run Process    psql    -c    TRUNCATE TABLE bib_references RESTART IDENTITY CASCADE;