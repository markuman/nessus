#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
module: markuman.nessus.task
short_description: create or modify nessus tasks
'''

EXAMPLES = '''
    - name: update nessus task
      markuman.nessus.task:
        targets:
            - 10.0.0.1
            - 10.0.0.32
        task: "183"
        host: nessus.mydomain.tld
        username: nessus_user
        password: nessus_password
'''

from ansible.module_utils.basic import *
from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
from pathlib import Path


def wer_braucht_schon_eine_api(task, targets, username, password, host):

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(str(Path.home()) + '/.local/bin/', options=options)
    print ("Headless Firefox Initialized")
    driver.get('https://' + host)

    time.sleep(3)

    username_input = "/html/body/div/form/div[1]/input"
    password_input = "/html/body/div/form/div[2]/input" 
    login_submit = "/html/body/div/form/button"

    driver.find_element_by_xpath(username_input).send_keys(username)
    driver.find_element_by_xpath(password_input).send_keys(password)
    driver.find_element_by_xpath(login_submit).click()

    time.sleep(5)

    driver.get('https://{HOST}/#/scans/reports/{TASK}/config/settings/basic/general'.format(TASK=task, HOST=host))

    time.sleep(5)
    targets_element = "/html/body/section[3]/section[3]/section/form/div/div/div/div[1]/section/div[1]/div[1]/div[1]/div[5]/div/textarea"

    change = False
    existing = driver.find_element_by_xpath(targets_element).text
    for item in targets:
        if item not in existing:
            change = True
            break

    if change:
        driver.find_element_by_xpath(targets_element).clear()
        driver.find_element_by_xpath(targets_element).send_keys(','.join(targets))
        save = "/html/body/section[3]/section[3]/section/form/button"
        driver.find_element_by_xpath(save).click()

    time.sleep(5)

    driver.quit()
    return change

def main():
    module = AnsibleModule(
        argument_spec = dict(
            targets = dict(required=False, type='list', elements='str'),
            password = dict(required=False, type='str', no_log=True),
            username = dict(required=False, type='str'),
            task = dict(required=True, type='str'),
            host = dict(required=True, type='str')
        )
    )


    raw_targets = module.params.get("targets")
    password = module.params.get("password")
    username = module.params.get("username")
    task = module.params.get("task")
    host = module.params.get("host")

    change = wer_braucht_schon_eine_api(task, ips, username, password, host)
    module.exit_json(changed=change)
    

if __name__ == '__main__':
    main()