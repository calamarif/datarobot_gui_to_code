# "GUI PI" - DataRobot GUI to Code (API)

The purpose of this script is to provide a programatic way to specify "Optional Features" within the call to "make predictions" which the API currently does not support.

The way this is facilitated is through the python Selenium library, using the gecko Chrome driver (which needs to be put into the PATH). Download from here: https://github.com/mozilla/geckodriver/releases

## Instructions to use this script

#### 1) Download and Copy Gecko Driver to PATH:
- Download Gecko driver from here: https://github.com/mozilla/geckodriver/releases
- Put geckodriver into the PATH of your operating system

#### 2) Edit the _.env (example)_ file with the required variables:
- Rename the file (ie remove the "(example)" part of it
- Update the .env file

#### 3) Install the python libraries (listed in the requirements.txt file):
- (optional) Create a virtualenv 
- Install the python required libraries : ```pip install -r requirements.txt ```

#### 4) Run the script:
- ```python gui_pi.py ```


##### Known Limitations
- You must log into DataRobot with a username and password (ie not SSO)
- The first model of each project will run by default (it would be simple to customise this)
- It is likely a number of time.sleep(n) calls could be more efficiently tuned (reduced)
- Occassionally the script will fail, only to run successfully the next run (a combination of network latency issues and time.sleep calls that are potentially too short)
- It is possible different environments may need to alter the amount of waiting on each step
- It is recommended to keep CLEANUP flag set to True (as there isn't currently robust logic to handle multiple same named files)


##### Disclaimer
This is sample code, use at your own discretion. While I have endeavoured to make this script safe, it does make use of tags and XPATHS that may (and probably will) change, which will lead to unexpected results (and at worst case, things being deleted). Additionally there are likely be situations I have not catered for, hence use at your own risk.