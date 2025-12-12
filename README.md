# Python webapp with Streamlit to run Axe-Core accessibility tests

this is a simple app to run Axe-Core accessibility tests using the share.streamlit.io cloud for learning purposes.

## How to use it
Access the link: https://axe-core.streamlit.app/ inform the url that you want to test, 
select the mode (desktop or mobile) and theirs options then click on run Axe-Core.

## Results
The results will be displayed in two dataframes:
- The first show the total of violations found.
- The second show all the elements with issues.

## Features
For now this app only support scan a url and display the results in a dataframe. 
No actions inside the webpage are supported (and we don´t have plans to do it).

# Streamlit Cloud
To work with share.streamlit.io we need to have the `packages.txt` file with the packages that the app is using,
and we need to have a `requirements.txt` file with the python packages that are needed.

## Browser
Because the streamlit.io is running in a debian server and have support for these packages: 
https://packages.debian.org/bullseye/web/ we need to use the chromium headless browser.