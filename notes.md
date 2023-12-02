Login page: `https://panel.zdrowycatering.pl/pl/auth/login?from=/my-account/my-orders`

Tutorial how to `https://realpython.com/python-web-scraping-practical-introduction/#use-an-html-parser-for-web-scraping-in-python`


Beautiful Soup: https://beautiful-soup-4.readthedocs.io/en/latest/
MechanicalSoup: https://mechanicalsoup.readthedocs.io/en/stable/

Docker tutorial: https://www.docker.com/blog/containerized-python-development-part-1/


Marcin (#88285) nr zamówienia (#97141)

//*[@id="react-select-5-option-2"]



# Scraper
## TODO
1. Add headless mode
2. Get username and password from keyvault or env file
3. Clanup code


# Telegram BOT
BotName: @ZdrowyCatering_bot
https://web.telegram.org/a/#6304583297
API Token in KeePass in Zdrowy Catering entry

## TODO
1. Send message to my private account


## Sending Message
Method: sendMessage
https://core.telegram.org/bots/api#sendmessage

https://api.telegram.org/bot6304583297:AAFHNBFFt78tSXzfHlP9xnQtaJddc7duUUk/sendMessage

# Docker
Download Chrome: `wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb`

apt --fix-broken install
apt-get install chromium -y

https://github.com/password123456/setup-selenium-with-chrome-driver-on-ubuntu_debian

Run Docker with Browser Engine
https://github.com/SeleniumHQ/docker-selenium/tree/trunk#dynamic-grid
https://www.selenium.dev/documentation/grid/getting_started/#standalone
https://www.selenium.dev/documentation/webdriver/drivers/remote_webdriver/

https://stackoverflow.com/questions/45323271/how-to-run-selenium-with-chrome-in-docker




## Network
`docker network create --driver bridge selenium`
`docker run -d --shm-size=2g --hostname browser --network selenium -p 4444:4444 selenium/standalone-chrome`
`docker build -t myimage .; docker run --network selenium  myimage`
`docker run --network selenium  myimage`


# Terraform
`terraform apply -auto-approve -var-file="secrets.tfvars"`
## Container APP
**Container App has limitation of the size of Share Memory**
https://datawookie.dev/blog/2021/11/shared-memory-docker/
Blog about Shared Memory. Thanks @datawookie
`chrome_options.add_argument("--disable-dev-shm-usage")` - can tell chrome to not use shared memory

### Container App creation timeout out
Bug knows since February 2023. Timeout because of the luck of "latestRevision": true
https://github.com/hashicorp/terraform-provider-azurerm/issues/20435