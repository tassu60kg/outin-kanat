*** Settings ***
Resource  resource.robot
Suite Setup  Setup Suite
Suite Teardown  Close Browser

*** Comments ***
User Story: Käyttäjänä pystyn luomaan lähteestä BibTeX-muodon.

Hyväksymiskriteerit:
- Käyttäjä pystyy luomaan kaikista lisätyistä viitteistä BibTeX-muodon.
- Etusivulla "Luo BibTeX" -nappi.
- BibTeX-nappia painamalla avautuu erillinen sivu.
- Sivu näyttää kaikki viitteet BibTeX-muodossa tekstinä.

User Story: Käyttäjänä pystyn suodattamaan viitteitä tageilla.

Hyväksymiskriteerit:
- Lista tägeistä, jotka on lisätty viitteille
- Pystyy valitsemaan listasta haluaman tägin/tägit
- Painamalla "Näytä viitteet" -nappia, sivu päivittyy näyttämään vain valitulla tagilla merkityt viitteet
- Suodattimet voi tyhjentää

User Story: Käyttäjänä pystyn suodattamaan tageja BibTeX näkymään.

Hyväksymiskriteerit:
- Lista tägeistä, jota voi suodattaa.
- Pystyy valitsemaan listasta haluamansa tägin/tägit.
- Lista checklist muodossa.
- BibTeX-sivu näyttää vain tägeillä suodatetut viitteet.

User Story: Käyttäjänä haluan, että sivu on Outin väreissä ja on selkeä + siisti

Hyväksymiskriteerit:
- Nettisivu vastaa tiettyä värimaailmaa
- Nettisivu on selkeä ja helppokäyttöinen
- Sivuston ulkoasu on yhtenäinen

User story: Käyttäjänä pystyn kopioimaan kaikki viitteet BibTex muodossa

Hyväksymiskriteerit:
 - "Copy text"-nappi BibTeX sivulla.
 - BibTexit kopioituu asiakkaan leikepöydälle.
 - Viesti "References copied".



*** Test Cases ***
Homepage has a link to form
    Go To  ${HOME_URL}
    Title Should Be  References
    Page Should Contain Link  Add reference
    Click Link  Add reference
    Title Should Be  Add a reference

Homepage has a link to BibTeX page
    Go To  ${HOME_URL}
    Title Should Be  References
    Page Should Contain Link  Create BibTeX
    Click Link  Create BibTeX
    Title Should Be  BibTeX
    Page Should Contain    Copy your BibTeX references here

Homepage has a link to add reference with DOI
    Go To  ${HOME_URL}
    Title Should Be  References
    Page Should Contain Link  Add reference with DOI
    Click Link  Add reference with DOI
    Title Should Be  Add reference with DOI

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
    Title Should Be    References

User can filter references by tag
    Go To  ${HOME_URL}
    Edit Tags Of Most Recent Reference
    Go To  ${HOME_URL}
    Check Tag Is Visible In Table
    Edit Tags of Second Most Recent Reference
    Go To  ${HOME_URL}
    Click Element  xpath://form/details/summary["Filter references by tags"]
    Select Checkbox  test_tag
    Click Button  Show
    Page Should Contain  test_tag

User can clear filters
    Go To  ${HOME_URL}
    Click Element  xpath://form/details/summary["Filter references by tags"]
    Select Checkbox  test_tag
    Click Button  Show
    Page Should Contain  test_tag
    Click Element  xpath://form/details/summary["Filter references by tags"]
    Click Button  Clear filters
    Page Should Contain  test_tag
    Page Should Contain  tag_test

User can see BibTeX of filtered references
    Go To  ${HOME_URL}
    Edit Tags of Inproceedings
    Go To  ${HOME_URL}
    Click Element  xpath://form/details/summary["Filter references by tags"]
    Select Checkbox  tag_filter
    Open BibTeX Page
    Check Book Reference Not In BibTeX
    Check Article Reference Not In BibTeX
    Check Inproceedings Reference In BibTeX

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