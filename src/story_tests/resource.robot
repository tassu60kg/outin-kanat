*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${SERVER}    localhost:5001
${DELAY}     0.5 seconds
${HOME_URL}  http://${SERVER}
${BROWSER}   chrome
${HEADLESS}  false

*** Keywords ***
Open And Configure Browser
    IF  $BROWSER == 'chrome'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys
        Call Method  ${options}  add_argument  --incognito
    ELSE IF  $BROWSER == 'firefox'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys
        Call Method  ${options}  add_argument  --private-window
    END
    IF  $HEADLESS == 'true'
        Set Selenium Speed  0.05 seconds
        Call Method  ${options}  add_argument  --headless
    ELSE
        Set Selenium Speed  ${DELAY}
    END
    Open Browser  browser=${BROWSER}  options=${options}

Add Book Reference
    Click Link  Add reference
    Title Should Be  Add a reference
    Page Should Contain  Add a reference
    Fill Reference With Book Test
    Click Button  send

Fill Reference With Book Test
    Select From List By Value    name=type    book
    Input Text    name=cite_key      kesakirja
    Input Text    name=author        Tove Jansson
    Input Text    name=title         Kesäkirja
    Input Text    name=year          1972
    Input Text    name=publisher     WSOY
    Input Text    name=ISBN          9789510434383

Add Article Reference
    Click Link  Add reference
    Page Should Contain  Add a reference
    Fill Reference With Article Test
    Click Button  send

Fill Reference With Article Test
    Select From List By Value    name=type    article
    Input Text    name=cite_key    CBH91 
    Input Text    name=author      Allan Collins and John Seely Brown and Ann Holum
    Input Text    name=title       Cognitive apprenticeship: making thinking visible
    Input Text    name=journal     American Educator
    Input Text    name=year        1991
    Input Text    name=volume      3
    Input Text    name=pages       38–46

Add Inproceedings Reference
    Click Link  Add reference
    Page Should Contain  Add a reference
    Fill Reference With Inproceedings Test
    Click Button  send

Fill Reference With Inproceedings Test
    Select From List By Value    name=type    inproceedings
    Input Text    name=cite_key    VPL11
    Input Text    name=author      Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti
    Input Text    name=title       Extreme Apprenticeship Method in Teaching Programming for Beginners.
    Input Text    name=year        2011
    Input Text    name=booktitle   SIGCSE '11: Proceedings of the 42nd SIGCSE technical symposium on Computer science education

Check Table Exists
    Page Should Contain Element  xpath=//table
    Page Should Contain  Type
    Page Should Contain  Cite key
    Page Should Contain  Title
    Page Should Contain  Author
    Page Should Contain  Year
    Page Should Contain  Publisher
    Page Should Contain  Journal
    Page Should Contain  Booktitle
    Page Should Contain  Volume
    Page Should Contain  Volume
    Page Should Contain  Pages
    Page Should Contain  ISBN

Delete Reference
    Click Link  Delete
    Title Should Be  Delete reference
    Page Should Contain  Kesäkirja –– Tove Jansson
    Click Button  Delete reference

Check Reference is Deleted
    Page Should Not Contain Element  xpath=//table[cite_key="kesakirja"]

Delete Any Reference
    Click Link    Delete
    Click Button    Delete reference

