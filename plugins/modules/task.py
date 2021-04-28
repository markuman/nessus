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
import requests
import yaml


def diff_handler(before=[], after=[]):
    before = "".join(before.split()).split(',')
    before.sort()
    after.sort()

    return dict(
        before=yaml.safe_dump(before),
        after=yaml.safe_dump(after)
    )


def wer_braucht_schon_eine_api(task, targets, username, password, host, headless, fail_json, check_mode):

    post_data = {
        'username': username,
        'password': password
    }
    response = requests.post(f'https://{host}/session', data=post_data)
    if response.status_code == 200:
        token = response.json().get('token')
        header = {
            "X-Cookie":f"token={token}",
            "Content-Type":"application/json"
        }
        response = requests.get(f'https://{host}/scans', headers=header)

        if response.status_code == 200:
            scans = response.json().get('scans')

            for scan in scans:
                if task == scan.get('name'):
                    task_id = scan.get('id')

        else:
            fail_json(msg=f'List Scans Failed. Status Code {response.status_code}')
    else:
        fail_json(msg=f'Login Failed. Status Code {response.status_code}')


    options = Options()
    options.headless = headless

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

    driver.get(f'https://{host}/#/scans/reports/{task_id}/config/settings/basic/general')

    time.sleep(5)
    targets_element = "/html/body/section[3]/section[3]/section/form/div/div/div/div[1]/section/div[1]/div[1]/div[1]/div[5]/div/textarea"

    change = False
    existing = driver.find_element_by_xpath(targets_element).text
    diff = diff_handler(existing, targets)
    for item in targets:
        if item not in existing:
            change = True
            break

    if not change:
        for item in "".join(existing.split()).split(','):
            if item not in targets:
                change = True
                break

    if change and not check_mode:
        driver.find_element_by_xpath(targets_element).clear()
        driver.find_element_by_xpath(targets_element).send_keys(','.join(targets))
        save = "/html/body/section[3]/section[3]/section/form/button"
        driver.find_element_by_xpath(save).click()

    time.sleep(5)

    driver.quit()
    return change, diff

def main():
    module = AnsibleModule(
        argument_spec = dict(
            targets = dict(required=False, type='list', elements='str'),
            password = dict(required=False, type='str', no_log=True),
            username = dict(required=False, type='str'),
            task = dict(required=True, type='str'),
            host = dict(required=True, type='str'),
            headless = dict(required=False, type='bool', default=False)
        ),
        supports_check_mode=True
    )


    targets = module.params.get("targets")
    password = module.params.get("password") or os.environ.get('NESSUS_PASSWORD')
    username = module.params.get("username") or os.environ.get('NESSUS_USERNAME')
    task = module.params.get("task")
    host = module.params.get("host")
    headless = module.params.get("headless")

    change, diff = wer_braucht_schon_eine_api(task, targets, username, password, host, headless, module.fail_json, module.check_mode)
    module.exit_json(changed=change, diff=diff)
    

if __name__ == '__main__':
    main()