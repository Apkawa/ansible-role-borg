# Ansible role: borg

[![Build Status](https://travis-ci.org/apkawa/ansible-role-borg.svg?branch=master)](https://travis-ci.org/apkawa/ansible-role-borg)

[![Ansible role](https://img.shields.io/ansible/role/42608.svg)](https://galaxy.ansible.com/apkawa/borg)
[![Ansible role downloads](https://img.shields.io/ansible/role/d/42608.svg)](https://galaxy.ansible.com/apkawa/borg)
[![Ansible role quality](https://img.shields.io/ansible/quality/42608.svg)](https://galaxy.ansible.com/apkawa/borg)

Ansible role for [borgbackup](https://borgbackup.readthedocs.io/en/stable/)

Requirements
------------

None

Role Variables
--------------

Available variables are listed below, along with default values (see `defaults/main.yml`):
```yaml
# borg help compression
borg_compression: lz4
# partialy implemented
# https://borgbackup.readthedocs.io/en/stable/usage/init.html
# borg help init
borg_encryption: none

# https://borgbackup.readthedocs.io/en/stable/usage/general.html
borg_remotes:
  default:
    # required
    path: 'ssh://example.org'
    # optional
    compression: "{{ borg_compression }}"
    # Todo handle it
    encryption: "{{ borg_encryption }}"
  # may be string
  db: /path/to/folder

borg_backups:
  -
    # require
    name: minimal
    from:
      - /path/to/from_folder #
    dest: "{hostname}_minimal"
  -
    # require
    name: example
    from:
      - "-" # for stdin
      - /path/to/from_folder # also can add file
    dest: "{hostname}_db_{now:%Y-%m-%dT%H:%M:%S}"
    #optional
    stdin_name: dump.sql
    # By default - true
    before_command: >- # Must be no line!
      /usr/local/bin/command_to_stout_backup

    # defaults
    workdir: '$HOME' # For add to archive by relative path
    remote: db
    user: "{{ ansible_ssh_user }}"

    cron:
      # By default every day 
      minute: "0"
      hour: "1"

      day: "*"
      month: "*"
      weekday: "*"

    prune: true
        cron:
          # https://crontab.guru/
          # By default every day
          minute: "0"
          hour: "0"
          day: "*"
          month: "*"
          weekday: "*"
        # https://borgbackup.readthedocs.io/en/stable/usage/prune.html
        prefix: null
        glob: null
        keep:
            # https://crontab.guru/
            secondly: null
            minutely: null
            hourly: 24
            daily: 14
            weekly: 8
            monthly: -1
    #
    delete: false
```


Dependencies
------------

- [apkawa.cron](https://galaxy.ansible.com/apkawa/cron)

Example Playbook
----------------

```yaml
- hosts: all
  roles:
    - role: apkawa.borg

```

License
-------

MIT 

Author Information
------------------

Apkawa 


Contributing
------------

1. [Install docker](https://docs.docker.com/install/linux/docker-ce/debian/)
2. [Install pipenv](https://docs.pipenv.org/en/latest/install/#installing-pipenv)
3. Initialize pipenv:
    ```
    pipenv install --dev
    ```
4. Run tests
    ``` 
    pipenv run -- tox -e centos7
    ```

###  Low level run part of test

1. pipenv shell
2. `molecule converge` 
3. `molecule idempotence`
4. `molecule verify` for run Testinfra