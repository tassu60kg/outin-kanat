*** Settings ***
Resource  resource.robot
Suite Setup  Setup Suite
Suite Teardown  Close Browser


*** Test Cases ***


User Can Add Article Reference With DOI
    Go To  ${HOME_URL}
    Add Article Reference With DOI
    Go To  ${HOME_URL}
    Check DOI article In Table

User Can Add Inproceedings Reference With DOI
    Go To  ${HOME_URL}
    Add Inproceedings Reference With DOI
    Go To  ${HOME_URL}
    Check DOI Inproceedings In Table

User Can Add Book Reference With DOI
    Go To  ${HOME_URL}
    Add Book Reference With DOI
    Go To  ${HOME_URL}
    Check DOI Book In Table

User Cannot Add Reference With Invalid DOI
    Go To  ${HOME_URL}
    Click Link  Add reference with DOI
    Title Should Be  Add reference with DOI
    Fill Book Reference With Invalid DOI
    Click Button   Add Reference
    Page Should Contain   No Data was found with this DOI. Please check it and try again.

User can see BibTeX of all DOI references
    Go To  ${HOME_URL}
    Open BibTeX Page
    Page Should Contain    Copy your BibTeX references here
    Check DOI Book Reference In BibTeX
    Check DOI Article Reference In BibTeX
    Check DOI Inproceedings Reference In BibTeX
    Click Button    Back
    Title Should Be    References









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
    ${db_url}=    Get Environment Variable    DATABASE_URL
    ${result}=    Run Process    psql    ${db_url}    -c    TRUNCATE TABLE bib_references RESTART IDENTITY CASCADE;    stdout=YES    stderr=YES
    Log    ${result.stdout}
    Log    ${result.stderr}