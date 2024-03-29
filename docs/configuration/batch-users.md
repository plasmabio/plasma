(batch-users)=

# Creating and deleting users in batches

The {ref}`install-users` section details how to create the initial list of users.

However in some cases it is useful to have a more automated way to create (and delete) users
in batches. For example when preparing and cleaning up a group of students at the beginning and end of a semester.

This section details how to create and delete users defined in a CSV file using Ansible Playbooks.

## Creating the CSV File

Create the `student.csv` file which should contain the `username`, `password` and `group` columns.

Here is an example of such file:

```text
username,password,group
stu-megm1-01,bn3r7RjtOyg15X,megm1
stu-megm1-02,2shgP3xK7aTuMN,megm1
stu-megm1-03,Kh5jn4GuEIFIzY,megm1
stu-megm1-04,g9gBHQjJ4VqQG1,megm1
stu-megm1-05,73O88oFb6B1TB0,megm1
stu-megm1-06,laZubrmgKBNg1x,megm1
stu-megm1-07,gAONEMsgdz28si,megm1
stu-megm1-08,tjlGadyELWj59M,megm1
stu-megm1-09,soIb4txJDPjo1d,megm1
stu-megm1-10,QjhalcW9Uq5wxo,megm1
```

````{warning}
Since the fields in the CSV file are delimited by commas, passwords should not contain any `,` character.
````

## Running the playbook to create users

To create the users, go to the `ansible/` folder and run the `student-create.yml` playbook with:

```sh
ansible-playbook student-create.yml -u ubuntu -e "studentdef=students.csv"
```


````{note}
It is possible to pass additional parameters when creating users in batches.

For example if you have a file `students-config.yml` defining disk quotas for a group of students:

```yaml
# default quotas for students
quota:
  soft: 200G
  hard: 250G
```

You can run the playbook and reference that extra file:

```sh
ansible-playbook student-create.yml -u ubuntu -e "studentdef=students.csv" -e @students-config.yml
```
````


## Running the playbook to delete users

To delete users, go to the `ansible/` folder and run the `student-remove.yml` playbook with:

```sh
ansible-playbook student-remove.yml -u ubuntu -e "studentdef=students.csv"
```

````{warning}
You need to provide the exact same CSV file you used to create users in the first place.
````

````{warning}
Please note that user home directories are deleted.
````