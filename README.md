# [WIP] markuman.nessus Ansible Collection

This Ansible Collection brings back Nessus Task Automation ✊  

## How does it work

Since `post` and `put` api requests result in status code `412` using nessus on-premise, the ansible collection uses simple selenium and firefox to create or update tasks.

## Status

Currently only update target list of existing tasks is working.  
This is helpfull, because you can throw your (dynamic) inventory files on an existing nessus task now.


```yaml
    - name: update nessus task
      markuman.nessus.task:
        targets:
            - 10.0.0.1
            - 10.0.0.32
        task: "183"
        host: nessus.mydomain.tld
        username: nessus_user
        password: nessus_password
```

