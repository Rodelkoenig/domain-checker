# Domain Checker

Simple Python Script to check if a given list of domains is available.\
Sends a Telegram Message via Bot to a list of Telegram IDs for each available domain

## Setup

1. Create properties: `cp config.properties.dist config.properties`
2. Setup a Telegram Bot: <https://core.telegram.org/bots/>
3. Get your Telegram Chat Id e.g. with RawDataBot
4. Register for free at: <https://jsonwhoisapi.com/> (1000 free requests / month)
5. Fill config.properties
6. Call script via cron e.g. `0 3 * * * /usr/bin/python3 ~/scripts/domain_checker.py >> ~/scripts/domain_checker.log`
