#Kategorian valinta muokkaa näkymää viitteen muokkaamislomakkeessa.
#Viitteeseen voi lisätä tägin.
#Viitteen tägejä voi muokata.
#Tägit näkyvät taulukossa.

*** Settings ***
Resource  resource.robot
Suite Setup  Setup Suite
Suite Teardown  Close Browser

*** Test Cases ***
User can edit a reference
    Go To  ${HOME_URL}
    Add Book Reference
    Go To  ${HOME_URL}
    Check Table Exists
    Page Should Contain  kesakirja
    Edit Most Recent Reference
    Go To  ${HOME_URL}
    Page Should Contain  Sommarboken
    Page Should Contain  Jansson Tove

User can edit tags of a reference
    Go To  ${HOME_URL}
    Add Book Reference
    Go To  ${HOME_URL}
    Check Table Exists
    Edit Tags Of Most Recent Reference
    Go To  ${HOME_URL}
    Check Tag Is Visible In Table

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