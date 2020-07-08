.. _install/ansible:

Deploying with Ansible
======================

What is Ansible?
----------------

Ansible is an open-source tool to automate the provisioning of servers, configuration management,
and application deployment.

Playbooks can be used to define the list of tasks that should be executed and to declare the desired
state of the server.

Check out the `How Ansible Works <https://www.ansible.com/overview/how-ansible-works>`_ guide on the Ansible
official documentation website for more information.

Installing Ansible
------------------

Plasma comes with several `Ansible Playbooks` to automatically provision the machine with
the system requirements, as well as installing Plasma and starting up the services.

.. note::

    We recommend creating a new virtual environment to install Python packages.

    Using the built-in ``venv`` module:

    .. code-block:: bash

        python -m venv .
        source bin/activate

    Using ``conda``:

    .. code-block:: bash

        conda create -n plasma -c conda-forge python nodejs
        conda activate plasma


Make sure `Ansible <https://docs.ansible.com/ansible/latest/index.html>`_ is installed:

.. code-block:: bash

    python -m pip install ansible>=2.9

.. note::

    We recommend ``ansible>=2.9`` to discard the warning messages
    regarding the use of ``aptitude``.


To verify the installation, run:

.. code-block:: bash

    which ansible

This should return the path to the ansible CLI tool in the virtual environment.
For example: ``/home/myuser/miniconda/envs/plasma/bin/ansible``

Running the Playbooks
---------------------

Check out the repository, and go to the ``plasma/ansible/`` directory:

.. code-block:: bash

    git clone https://github.com/plasmabio/plasma
    cd plasma/ansible

Create a ``hosts`` file with the following content:

.. code-block:: text

    [server]
    51.178.95.237

    [server:vars]
    ansible_python_interpreter=/usr/bin/python3

Replace the IP corresponds to your server. If you already defined the hostname (see :ref:`install/https`),
you can also specify the domain name:

.. code-block:: text

    [server]
    dev.plasmabio.org

    [server:vars]
    ansible_python_interpreter=/usr/bin/python3

If you have multiple servers, the ``hosts`` file will look like the following:

.. code-block:: text

    [server1]
    51.178.95.237 

    [server2]
    51.178.95.238

    [server1:vars]
    ansible_python_interpreter=/usr/bin/python3

    [server2:vars]
    ansible_python_interpreter=/usr/bin/python3

Then run the following command after replacing ``<user>`` by your user on the remote machine:

.. code-block:: bash

    ansible-playbook site.yml -i hosts -u <user>

Many Ubuntu systems running on cloud virtual machines have the default ``ubuntu`` user. In this case, the command becomes:

.. code-block:: bash

    ansible-playbook site.yml -i hosts -u ubuntu

Ansible will log the progress in the terminal, and will indicate which components have changed in the process of running the playbook:

.. code-block:: text

    PLAY [all] **********************************************************************************************

    TASK [Gathering Facts] **********************************************************************************
    Tuesday 07 July 2020  11:34:43 +0200 (0:00:00.043)       0:00:00.043 ********** 
    ok: [51.83.15.159]

    TASK [Install required system packages] *****************************************************************
    Tuesday 07 July 2020  11:34:44 +0200 (0:00:01.428)       0:00:01.472 ********** 
    changed: [51.83.15.159] => (item=apt-transport-https)
    changed: [51.83.15.159] => (item=ca-certificates)
    changed: [51.83.15.159] => (item=curl)
    changed: [51.83.15.159] => (item=software-properties-common)
    changed: [51.83.15.159] => (item=python3-pip)
    changed: [51.83.15.159] => (item=virtualenv)
    ok: [51.83.15.159] => (item=python3-setuptools)

    TASK [Add Docker GPG apt Key] ***************************************************************************
    Tuesday 07 July 2020  11:37:36 +0200 (0:02:51.590)       0:02:53.062 ********** 
    changed: [51.83.15.159]

    TASK [Add Docker Repository] ****************************************************************************
    Tuesday 07 July 2020  11:37:38 +0200 (0:00:02.577)       0:02:55.640 ********** 
    changed: [51.83.15.159]

    TASK [Update apt and install docker-ce] *****************************************************************
    Tuesday 07 July 2020  11:37:45 +0200 (0:00:06.394)       0:03:02.035 ********** 
    changed: [51.83.15.159]

    TASK [Install Docker Module for Python] *****************************************************************
    Tuesday 07 July 2020  11:38:13 +0200 (0:00:27.878)       0:03:29.914 ********** 
    changed: [51.83.15.159]

    PLAY [all] **********************************************************************************************

    TASK [Gathering Facts] **********************************************************************************
    Tuesday 07 July 2020  11:38:16 +0200 (0:00:03.123)       0:03:33.038 ********** 
    ok: [51.83.15.159]

    TASK [Install extra system packages] ********************************************************************
    Tuesday 07 July 2020  11:38:17 +0200 (0:00:01.295)       0:03:34.333 ********** 
    changed: [51.83.15.159] => (item=jq)
    changed: [51.83.15.159] => (item=tree)

    TASK [Install ctop] *************************************************************************************
    Tuesday 07 July 2020  11:38:31 +0200 (0:00:13.419)       0:03:47.752 ********** 
    changed: [51.83.15.159]

    PLAY [all] **********************************************************************************************

    TASK [Gathering Facts] **********************************************************************************
    Tuesday 07 July 2020  11:38:33 +0200 (0:00:02.825)       0:03:50.578 ********** 
    ok: [51.83.15.159]

    TASK [Install required system packages] *****************************************************************
    Tuesday 07 July 2020  11:38:35 +0200 (0:00:01.304)       0:03:51.883 ********** 
    ok: [51.83.15.159] => (item=curl)
    ok: [51.83.15.159] => (item=python3)
    ok: [51.83.15.159] => (item=python3-dev)
    ok: [51.83.15.159] => (item=python3-pip)

    TASK [Download the TLJH installer] **********************************************************************
    Tuesday 07 July 2020  11:38:48 +0200 (0:00:13.532)       0:04:05.415 ********** 
    changed: [51.83.15.159]

    TASK [Check if the tljh-plasma is already installed] ****************************************************
    Tuesday 07 July 2020  11:38:49 +0200 (0:00:00.999)       0:04:06.414 ********** 
    ok: [51.83.15.159]

    TASK [Upgrade the tljh-plasma plugin first if it is already installed] **********************************
    Tuesday 07 July 2020  11:38:50 +0200 (0:00:00.728)       0:04:07.143 ********** 
    skipping: [51.83.15.159]

    TASK [Run the TLJH installer] ***************************************************************************
    Tuesday 07 July 2020  11:38:50 +0200 (0:00:00.040)       0:04:07.183 ********** 
    changed: [51.83.15.159]

    TASK [Set the idle culler timeout to 1 hour] ************************************************************
    Tuesday 07 July 2020  11:40:00 +0200 (0:01:09.668)       0:05:16.852 ********** 
    changed: [51.83.15.159]

    TASK [Set the default memory and cpu limits] ************************************************************
    Tuesday 07 July 2020  11:40:01 +0200 (0:00:01.053)       0:05:17.905 ********** 
    changed: [51.83.15.159]

    TASK [Reload the hub] ***********************************************************************************
    Tuesday 07 July 2020  11:40:02 +0200 (0:00:01.555)       0:05:19.461 ********** 
    changed: [51.83.15.159]

    TASK [Pull jupyter/repo2docker] *************************************************************************
    Tuesday 07 July 2020  11:40:06 +0200 (0:00:03.571)       0:05:23.032 ********** 
    changed: [51.83.15.159]

    PLAY RECAP **********************************************************************************************
    51.83.15.159               : ok=18   changed=13   unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   

    Tuesday 07 July 2020  11:40:16 +0200 (0:00:10.626)       0:05:33.658 ********** 
    =============================================================================== 
    Install required system packages --------------------------------------------------------------- 171.59s
    Run the TLJH installer -------------------------------------------------------------------------- 69.67s
    Update apt and install docker-ce ---------------------------------------------------------------- 27.88s
    Install required system packages ---------------------------------------------------------------- 13.53s
    Install extra system packages ------------------------------------------------------------------- 13.42s
    Pull jupyter/repo2docker ------------------------------------------------------------------------ 10.63s
    Add Docker Repository ---------------------------------------------------------------------------- 6.40s
    Reload the hub ----------------------------------------------------------------------------------- 3.57s
    Install Docker Module for Python ----------------------------------------------------------------- 3.12s
    Install ctop ------------------------------------------------------------------------------------- 2.83s
    Add Docker GPG apt Key --------------------------------------------------------------------------- 2.58s
    Set the default memory and cpu limits ------------------------------------------------------------ 1.56s
    Gathering Facts ---------------------------------------------------------------------------------- 1.43s
    Gathering Facts ---------------------------------------------------------------------------------- 1.30s
    Gathering Facts ---------------------------------------------------------------------------------- 1.30s
    Set the idle culler timeout to 1 hour ------------------------------------------------------------ 1.05s
    Download the TLJH installer ---------------------------------------------------------------------- 1.00s
    Check if the tljh-plasma is already installed ---------------------------------------------------- 0.73s
    Upgrade the tljh-plasma plugin first if it is already installed ---------------------------------- 0.04s

.. _install/individual-playbook:


Running individual playbooks
----------------------------

The ``site.yml`` Ansible playbook includes all the playbooks and will process them in order.

It is however possible to run the playbooks individually. For example to run the ``tljh.yml`` playbook only (to install
and update The Littlest JupyterHub):

.. code-block:: bash

    ansible-playbook tljh.yml -i hosts -u ubuntu

For more in-depth details about the Ansible playbook, check out the
`official documentation <https://docs.ansible.com/ansible/latest/user_guide/playbooks.html>`_.


Using a specific version of Plasma
----------------------------------

By default the Ansible playbooks use the latest version from the ``master`` branch.

This is specified in the ``ansible/vars/default.yml`` file:

.. code-block:: yaml

    tljh_plasma: git+https://github.com/plasmabio/plasma@master#"egg=tljh-plasma&subdirectory=tljh-plasma"

But it is also possible to use a specific git commit hash, branch or tag. For example to use the version of Plasma
tagged as ``v0.1``:

.. code-block:: yaml

    tljh_plasma: git+https://github.com/plasmabio/plasma@v0.1#"egg=tljh-plasma&subdirectory=tljh-plasma"


List of available playbooks
---------------------------

The Ansible playbooks are located in the ``ansible/`` directory:

- ``docker.yml``: install Docker CE on the host
- ``utils.yml``: install extra system packages useful for debugging and system administration
- ``users.yml``: create the tests users on the host
- ``quotas.yml``: enable quotas on the host to limit disk usage
- ``include-groups.yml``: add user groups to JupyterHub
- ``cockpit.yml``: install Cockpit on the host as a monitoring tool
- ``tljh.yml``: install TLJH and the Plasma TLJH plugin
- ``https.yml``: enable HTTPS for TLJH
- ``uninstall.yml``: uninstall TLJH only
- ``site.yml``: the main playbook that references some of the other playbooks


Running playbook on a given server
----------------------------------

If you have multiple servers defined in the ``hosts`` file, you can run a playbook on a single server with the ``--limit`` option:

.. code-block:: bash

    ansible-playbook site.yml -i hosts -u ubuntu --limit server1
