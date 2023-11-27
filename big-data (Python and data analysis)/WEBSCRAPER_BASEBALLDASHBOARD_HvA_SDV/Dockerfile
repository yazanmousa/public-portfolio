FROM python:3

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# Updating apt to see and install Google Chrome
RUN apt-get -y update
# Magic happens
RUN apt-get install -y google-chrome-stable

# Installing Unzip
RUN apt-get install -yqq unzip
# Download the Chrome Driver
# Download and install Chromedriver
# RUN wget -q --continue -P $C:/Users/37046/Downloads "http://chromedriver.storage.googleapis.com/2.0/chromedriver_win32.zip"
RUN wget -q --continue -P $C:/Users/37046/Downloads "http://chromedriver.storage.googleapis.com/2.0/chromedriver_linux64.zip"
RUN unzip $C:/Users/37046/Downloads/chromedriver* -d $C:/Users/37046/Downloads
# Unzip the Chrome Driver into /usr/local/bin directory
# RUN unzip Users/tmp/chromedriver.zip chromedriver -d /usr/local/bin/
# Set display port as an environment variable
ENV DISPLAY=:99

WORKDIR /application

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "MASTER_SCRIPT.py" ]