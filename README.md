# Slack-Eve-Killmail

## Requirements
* Slack
* Python 2 (w/ sqlite 3)
* [EVE Static Data Export (SDE)](https://developers.eveonline.com/resource/static-data-export)
	* Only universeDataDx.db is a requirement

## Install Instructions
* In Slack, go to /services/new, select Incoming WebHooks. 
	* Fill in channel/name
	* Copy URL in config.py in the config\_slack\_url
* After Github clone, place universeDataDx.db in the cloned folder (or where ever you installed the script)
* In config.py configure which alliances to track
	* Format is dictionary in array
	* Each dictionary in the array is a separate corporation or alliance to track
	* Key is allianceID or corporationID
	* Value is the ID
		* Go to [zkillboard](https://zkillboard.com/)
		* Search your corp/alliance
		* ID is in URL behind /corporation/ or /alliance/
* If you haven't already, bind corporation API key to zkillboard to get all kills listed
* Run using _python killboard.py_

## Configurable fields
* config\_header = 'Slack-Eve-Killboard/1.0a https://github.com/dimurgos/Slack-Eve-Killmail' # header
* config\_owner = [{'': 0}] # Format of: 'corporationID': <id> or 'allianceID': <id> (can be multiple)
* config\_check = '86400' # Check for the last day (maximal retrieval amount)
* config\_sleep\_time = 1200 # Delay between checks (20 minutes default)
* config\_slack\_url = 'https://hooks.slack.com/services/' # Slack integration code

## Result
* Every 20 minutes the list of kills over the last day will be posted in the configured Slack channel
* Posts if it is a loss or a kill (green for kill, red for loss)
* Includes damage dealt, pilots involved, ship, value, system and most damage done

## Example
![example](docs/killmails.png?raw=true)