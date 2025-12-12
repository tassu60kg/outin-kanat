*** Settings ***
Resource  resource.robot
Suite Setup  Setup Suite
Suite Teardown  Close Browser

*** Comments ***
User Story: Käyttäjänä pystyn lisäämään kirjan, inproceedings ja artikkelin.

Hyväksymiskriteerit:
- Käyttäjä voi valita lomakkeesta haluamansa viitteen kategorian (kirja, inproceedings, artikkeli).
- Kategorian valinta muokkaa näkymää viitteen muokkaamislomakkeessa.
- Kun viite lisätään, sen kategoria tallentuu.
- Lisätty viite ja viitteen kategoria näkyvät taulukossa.

User Story: Käyttäjänä pystyn katsomaan listan viitteistä

Hyväksymiskriteerit:
- Viitteet näkyvät taulukkona
- Taulukossa näkyy viitteen kategoria ja siihen laaditut tiedot

*** Test Cases ***
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