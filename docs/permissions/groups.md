# Managing UNIX groups

(permissions-groups)=

## The group include list

By default Plasma users don't have access to any environments.

Users must be assigned to UNIX groups, and included groups be defined in the Plasma configuration.

Unix groups are defined in the config file `users-config.yml` already used for users creation (see {ref}`install-users-playbook`).

```yaml
plasma_groups:
    - python-course
    - bash-intro
```

To add these groups into allowed groups to access environments, execute the `ansible/include-groups.yml` playbook:

```bash
cd ansible/
ansible-playbook include-groups.yml -i hosts -u ubuntu -e @users-config.yml
```

The playbook creates the groups on the host machine if they don't already exist, and defines the list
of included groups in the TLJH config.

## Managing user groups via the command line

To create a new group `test`:

```bash
groupadd test
```

To add a user `alice` to the `test` group:

```bash
usermod -a -G test alice
```

To remove the user `alice` from the `test` group:

```bash
deluser alice test
```

Groups can be listed using the following command:

```bash
$ cat /etc/group
root:x:0:
daemon:x:1:
bin:x:2:
sys:x:3:
adm:x:4:syslog,ubuntu
tty:x:5:
disk:x:6:
lp:x:7:
mail:x:8:
...
```

There are also plenty of good resources online to learn more about UNIX user and groups management.
