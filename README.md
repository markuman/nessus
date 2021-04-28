# markuman.nessus Ansible Collection

This Ansible Collection brings back Nessus Task Automation ✊  

## How does it work

Since `post` and `put` api requests result in status code `412` using nessus on-premise, the ansible collection uses simple selenium and firefox to create or update tasks.  
[See it in action](https://home.osuv.de/apps/sharingpath/m/pub/ansible_nessus.gif).

## Status

Only the targets of an existing task (scan) can be modified!  
The intention is, that you throw your dynamic inventories into nessus tasks/scans.


```yaml
    - name: update nessus task
      markuman.nessus.task:
        targets:
            - 10.0.0.1
            - 10.0.0.32
        task: task_name
        host: nessus.mydomain.tld
        username: nessus_user
        password: nessus_password
```

## install

* `ansible-galaxy collection install markuman.nessus`
* `pip3 install selenium --user`
  * Gecko Driver https://github.com/mozilla/geckodriver/releases install to `~/.local/bin/`

## Auth

Just use your nessus username and password.

| **Ansible Parameter** | **ENV Variable** |
| --- | --- |
| `username` | `NESSUS_USERNAME` |
| `password` | `NESSUS_PASSWORD` |

# Usage

## task

| parameters | default | comment |
| --- | --- | --- |
| `name` | - | name of the nessus task |
| `purge` | `true` | Wether a existing targets should be replaced (`true`) or appended (`false`). Alias parameter are: `replace`, `overwrite`, `solo`. |
| `headless` | `true` | If set to (`false`), firefox will spawned. Good for debugging. |
| `host` | - | Host of your nessus installation (_without https://_) |
| `targets` | - | List of targets that should be present in the nessus task |
| `username` | - | Nessus Username. Environment `NESSUS_USERNAME` can be also used. |
| `password` | - | Nessus Password, Environment `NESSUS_PASSWIRD` can be also used. |

# SCM

| **host** | **category** |
| --- | --- |
| https://git.osuv.de/m/nessus | origin |
| https://gitlab.com/markuman/nessus | pull mirror, issues, MR |
| https://github.com/markuman/nessus | push mirror, issues, PR |


#### License

GNU General Public License v3.0+ 