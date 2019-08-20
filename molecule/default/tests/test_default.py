# flake8: noqa
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_cron_generated(host):
    cmd = host.run('crontab -l')
    assert cmd.rc == 0
    print(cmd.stdout)
    assert cmd.stdout.strip() == (
        """
#Ansible: borg__minimal
0 1 * * * set -ex && cd $HOME && {  /usr/bin/borg create --compression=lz4 '/tmp/borg_remote/default/::{hostname}_minimal' /path/to/from_folder --stdin-name=stdout; } 2>&1 >>/var/log/borg__minimal.log
#Ansible: borg__with_stdin_and_cleanup
30 2 * * * set -ex && cd /etc/ && { echo "Backup to stdout" |  /usr/bin/borg create --compression=lz4 '/tmp/borg_remote/db/::{hostname}_db_{now:\%Y-\%m-\%dT\%H:\%M:\%S}' - --stdin-name=dump.sql; } 2>&1 >>/var/log/borg__with_stdin_and_cleanup.log
#Ansible: borg__prune__minimal
0 2 * * * /usr/bin/borg prune --keep-hourly=24 --keep-daily=14 --keep-weekly=8 --keep-monthly=-1 /tmp/borg_remote/default/
#Ansible: borg__prune__with_stdin_and_cleanup
0 2 * * * /usr/bin/borg prune --keep-hourly=24 --keep-daily=14 --keep-weekly=8 --keep-monthly=-1 /tmp/borg_remote/db/
        """
    ).strip()


def test_borg_version(host):
    cmd = host.run('borg --version')
    assert cmd.rc == 0


def test_borg_remote(host):
    cmd = host.run('borg info /tmp/borg_remote/default/')
    assert cmd.rc == 0
