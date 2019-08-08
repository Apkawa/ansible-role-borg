# flake8: noqa
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_cron_generated(host):
    cmd = host.run('crontab -l')
    assert cmd.rc == 0
    assert cmd.stdout.strip() == (
        r'#Ansible: borg__minimal' '\n'
        r"0 1 * * * cd $HOME && {  /usr/bin/borg create --compression=lz4 "
        r"'/tmp/borg_remote/default/::{hostname}_minimal' /path/to/from_folder "
        r"--stdin-name=stdout; } 2>&1 >>/var/log/borg__minimal.log" '\n'
        r'#Ansible: borg__with_stdin_and_cleanup' '\n'
        r'30 2 * * * cd /etc/ && { out=$(echo "Backup to stdout") '
        r'&& echo $out |  /usr/bin/borg create --compression=lz4 '
        r"'/tmp/borg_remote/db/::{hostname}_db_{now:\%Y-\%m-\%dT\%H:\%M:\%S}' - "
        r"--stdin-name=dump.sql; } 2>&1 >>/var/log/borg__with_stdin_and_cleanup.log" '\n'
        r'#Ansible: borg__prune__with_stdin_and_cleanup' '\n'
        
        r'0 2 * * * /usr/bin/borg prune '
        r'--keep-hourly=24 --keep-daily=14 --keep-weekly=8 --keep-monthly=-1 '
        r'/tmp/borg_remote/db/' '\n'
    ).strip()


def test_borg_version(host):
    cmd = host.run('borg --version')
    assert cmd.rc == 0

def test_borg_remote(host):
    cmd = host.run('borg info /tmp/borg_remote/default/')
    assert cmd.rc == 0

