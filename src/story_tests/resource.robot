*** Settings ***
Library   OperatingSystem
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
    Page Should Contain  Select a reference type:
    Select From List By Label  name=type      Book
    Click Button  Continue
    Page Should Contain  Add book reference
    Fill Reference With Book Test
    Click Button  send
    Go To  ${HOME_URL}

Fill Reference With Book Test
    Input Text    name=cite_key      kesakirja
    Input Text    name=author        Tove Jansson
    Input Text    name=title         Kesäkirja
    Input Text    name=year          1972
    Input Text    name=publisher     WSOY
    Input Text    name=isbn          9789510434383

Check Book Reference In Table
    Page Should Contain   book
    Page Should Contain   kesakirja
    Page Should Contain   Tove Jansson
    Page Should Contain   Kesäkirja
    Page Should Contain   1972
    Page Should Contain   WSOY
    Page Should Contain   9789510434383

Add Article Reference
    Click Link  Add reference
    Title Should Be  Add a reference
    Page Should Contain  Select a reference type:
    Select From List By Label  name=type      Article
    Click Button  Continue
    Fill Reference With Article Test
    Click Button  send
    Go To  ${HOME_URL}

Fill Reference With Article Test
    Input Text    name=cite_key    CBH91
    Input Text    name=author      Allan Collins and John Seely Brown and Ann Holum
    Input Text    name=title       Cognitive apprenticeship: making thinking visible
    Input Text    name=year        1991
    Input Text    name=journal     American Educator
    Input Text    name=volume      3
    Input Text    name=pages       38–46

Check Article Reference In Table
    Page Should Contain   article
    Page Should Contain   CBH91
    Page Should Contain   Allan Collins and John Seely Brown and Ann Holum
    Page Should Contain   Cognitive apprenticeship: making thinking visible
    Page Should Contain   1991
    Page Should Contain   American Educator
    Page Should Contain   3
    Page Should Contain   38–46

Add Inproceedings Reference
    Click Link  Add reference
    Title Should Be  Add a reference
    Page Should Contain  Select a reference type:
    Select From List By Label  name=type      Inproceedings
    Click Button  Continue
    Fill Reference With Inproceedings Test
    Click Button  send
    Go To  ${HOME_URL}

Fill Reference With Inproceedings Test
    Input Text    name=cite_key    VPL11
    Input Text    name=author      Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti
    Input Text    name=title       Extreme Apprenticeship Method in Teaching Programming for Beginners
    Input Text    name=year        2011
    Input Text    name=booktitle   SIGCSE '11: Proceedings of the 42nd SIGCSE technical symposium on Computer science education

Check Inproceeding Reference In Table
    Page Should Contain   inproceedings
    Page Should Contain   VPL11
    Page Should Contain   Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti
    Page Should Contain   Extreme Apprenticeship Method in Teaching Programming for Beginners
    Page Should Contain   2011
    Page Should Contain   SIGCSE '11: Proceedings of the 42nd SIGCSE technical symposium on Computer science education

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

Delete Most Recent Reference
    Click Link  Delete
    Title Should Be  Delete reference
    Page Should Contain  Extreme Apprenticeship Method in Teaching Programming for Beginners –– Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti
    Page should contain  Are you sure you want to delete this reference?
    Click Button  Delete reference

Check Reference is Deleted
    Page Should Not Contain Element  [cite_key="Extreme Apprenticeship Method in Teaching Programming for Beginners"]

Delete Any Reference
    Click Link    Delete
    Click Button  Delete reference

Edit Most Recent Reference
    Click Link  Update
    Title Should Be  Edit reference
    Page Should Contain  Edit reference
    Input Text    name=title     Sommarboken
    Input Text    name=author    Jansson Tove
    Click Button  Update reference

Edit Tags Of Most Recent Reference
    Click Link  Update tags
    Title Should Be  Edit tags
    Page Should Contain  Edit tags of
    Input Text    name=tag    test_tag
    Click Button  Send

Check Tag Is Visible In Table
    Page Should Contain   test_tag


Open BibTeX Page
    Click Link    Create BibTeX
    Title Should Be    BibTeX
    Page Should Contain    Copy your BibTeX references here

Check Book Reference In BibTeX
    Page Should Contain    @book{kesakirja
    Page Should Contain    author = {Tove Jansson}
    Page Should Contain    title = {Kesäkirja}
    Page Should Contain    year = {1972}
    Page Should Contain    publisher = {WSOY}
    Page Should Contain    ISBN = {9789510434383}

Check Article Reference In BibTeX
    Page Should Contain    @article{CBH91
    Page Should Contain    author = {Allan Collins and John Seely Brown and Ann Holum}
    Page Should Contain    title = {Cognitive apprenticeship: making thinking visible}
    Page Should Contain    year = {1991}
    Page Should Contain    journal = {American Educator}
    Page Should Contain    volume = {3}
    Page Should Contain    pages = {38–46}

Check Inproceedings Reference In BibTeX
    Page Should Contain    @inproceedings{VPL11
    Page Should Contain    author = {Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti}
    Page Should Contain    title = {Extreme Apprenticeship Method in Teaching Programming for Beginners}
    Page Should Contain    year = {2011}
    Page Should Contain    booktitle = {SIGCSE '11: Proceedings of the 42nd SIGCSE technical symposium on Computer science education}