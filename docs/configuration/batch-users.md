(batch-users)=

# Creating users in batches

The {ref}`install-users` section details how to create the initial list of users.

However in some cases it is useful to have a more automated way to create (and delete) users
in batches. For example when preparing and cleaning up a group of students at the beginning and end of a semester.

This section details how to create users defined in a CSV file using Ansible Playbooks.

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

## Running the playbooks

To create the users, go to the `ansible/` folder and run the `student-create.yml` playbook with:

```sh
ansible-playbook student-create.yml -u ubuntu -e "studentdef=students.csv"
```

It is also possible to delete the users from the same CSV definition, using the `student-remove.yml` playbook:

```sh
ansible-playbook student-remove.yml -u ubuntu -e "studentdef=students.csv"
```
