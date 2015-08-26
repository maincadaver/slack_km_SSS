import urllib2
import urllib
import hashlib
import json
import sys
import exceptions
import locale
import config
from datetime import datetime
import time

def run_killboard(config_type, config_id):
    kills = 'https://zkillboard.com/api/{0}/{1}/pastSeconds/{2}/'.format(config_type, config_id, config.config_check)

    locale.setlocale(locale.LC_ALL,'en_US')

    request = urllib2.Request(kills)
    request.add_header('User-Agent', config.config_header)
    opener = urllib2.build_opener()
    data = opener.open(request)
    root = json.load(data)

    handled_kills = []
    f = open('handled_kills.dat', 'r+')
    for line in f:
        handled_kills.append(line.rstrip('\n'))

    for record in root:
        try:
            kill_id = record['killID']
            if str(kill_id) in handled_kills:
                continue
            
            killer = {}
            attackerCount = 0
            highestDmg = 0
            for attacker in record['attackers']:
                if attacker['finalBlow'] == 1:
                    killer = attacker
                if attacker['factionID'] == 0:
                    attackerCount += 1
                else:
                    continue
                if attacker['damageDone'] > highestDmg:
                    highestDmg = attacker['damageDone']
                    highestDealer = attacker

            victim = record['victim']

            attachment = {}
            damageTaken = {}
            kill = {}
            if killer['characterID'] == 0:
                kill['fallback'] = 'POS killed {0} ({1})'.format(victim['characterName'], victim['corporationName'])
                kill['color'] = 'good'
                damageTaken['title'] = "Damage dealt"
            elif victim[config_type] == config_id:
                kill['fallback'] = '{0} got killed by {1} ({2})'.format(victim['characterName'], killer['characterName'], killer['corporationName'])
                kill['color'] = 'danger'
                damageTaken['title'] = "Damage taken"
            else:
                kill['fallback'] = '{0} killed {1} ({2})'.format(killer['characterName'], victim['characterName'], victim['corporationName'])
                kill['color'] = 'good'
                damageTaken['title'] = "Damage dealt"

            kill['title'] = kill['fallback']
            kill['title_link'] = 'https://zkillboard.com/kill/{0}/'.format(kill_id)
            kill['thumb_url'] = 'https://imageserver.eveonline.com/Render/{0}_64.png'.format(victim['shipTypeID'])
            
            damageTaken['value'] = locale.format('%d', victim['damageTaken'], grouping=True)
            damageTaken['short'] = "true"
            
            value = {'title': 'Value', 'value': locale.format('%d', record['zkb']['totalValue'], grouping=True) + ' ISK', 'short': 'true'}
            totalAttackers = {'title': 'Pilots involved', 'value': str(attackerCount), 'short': 'true'}

            mostDmg = {}
            if highestDealer and highestDealer['characterID'] != 0:
                mostDmg['title'] = 'Most Damage'
                mostDmg['value'] = '<https://zkillboard.com/character/{0}|{1}> ({2})'.format(highestDealer['characterID'], highestDealer['characterName'], locale.format('%d', highestDmg, grouping=True))
                mostDmg['short'] = "true"
            
            kill['fields'] = [damageTaken, value, totalAttackers, mostDmg]
            
            attachment['attachments'] = [kill]
            
            payload = json.dumps(attachment)
            
            data = urllib.urlencode({'payload': payload})
            
            request_slack = urllib2.Request(config.config_slack_url, data)
            urllib2.urlopen(request_slack)

            time.sleep(2)
            f.write('{0}\n'.format(kill_id))
        except urllib2.HTTPError as e:
            print "Exception in processing record: " + e.reason
        except exceptions.KeyError as e:
            print "Exception in processing record: " + str(e)
        except:
            print "Exception in processing record" + str(sys.exc_info()[0])
        
    f.close()
    
    time.sleep(config.config_sleep_time)

while True:
    try:
        for key,val in config.config_owner.items():
            run_killboard(key, val)
    except urllib2.HTTPError as e:
        print "Exception in processing killboard data: " + e.reason
        time.sleep(60)
