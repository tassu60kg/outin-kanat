*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Test Cases ***
Homepage has a link to form
    Go To  ${HOME_URL}
    Title Should Be  temp
    Page Should Contain Link  lomake
    Click Link  lomake
    Page Should Contain  Lomake ja sillee
