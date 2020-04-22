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

PlasmaBio comes with several `Ansible Playbooks` to automatically provision the machine with
the system requirements, as well as installing PlasmaBio and starting up the services.

.. note::

    We recommend creating a new virtual environment to install Python packages.

    Using the built-in ``venv`` module:

    .. code-block:: bash

        python -m venv .
        source bin/activate

    Using ``conda``:

    .. code-block:: bash

        conda create -n plasmabio -c conda-forge python nodejs
        conda activate plasmabio


Make sure `Ansible <https://docs.ansible.com/ansible/latest/index.html>`_ is installed:

.. code-block:: bash

    python -m pip install ansible


To verify the installation, run:

.. code-block:: bash

    which ansible

This should return the path to the ansible CLI tool in the virtual environment.
For example: ``/home/myuser/miniconda/envs/plasmabio/bin/ansible``

Running the Playbooks
---------------------

Check out the repository, and go to the ``plasmabio/ansible/`` directory:

.. code-block:: bash

    git clone https://github.com/plasmabio/plasmabio
    cd plasmabio/ansible

Create a ``hosts`` file with the following content:

.. code-block:: text

    [servers]
    51.178.95.237

    [servers:vars]
    ansible_python_interpreter=/usr/bin/python3

Replace the IP corresponds to your server. If you already defined the hostname (see :ref:`install/https`),
you can also specify the domain name:

.. code-block:: text

    [servers]
    dev.plasmabio.org

    [servers:vars]
    ansible_python_interpreter=/usr/bin/python3

Then run the following command after replacing ``<user>`` by your user on the remote machine:

.. code-block:: bash

    ansible-playbook site.yml -i hosts -u <user>

Many Ubuntu systems running on cloud virtual machines have the default ``ubuntu`` user. In this case, the command becomes:

.. code-block:: bash

    ansible-playbook site.yml -i hosts -u ubuntu

Ansible will log the progress in the terminal, and will indicate which components have changed in the process of running the playbook:

.. code-block:: text

    PLAY [all] **********************************************************************************************************************************

    TASK [Gathering Facts] **********************************************************************************************************************
    ok: [51.178.95.237]

    TASK [Install aptitude using apt] ***********************************************************************************************************
    ok: [51.178.95.237]

    TASK [Install required system packages] *****************************************************************************************************
    ok: [51.178.95.237] => (item=apt-transport-https)
    ok: [51.178.95.237] => (item=ca-certificates)
    ok: [51.178.95.237] => (item=curl)
    ok: [51.178.95.237] => (item=software-properties-common)
    ok: [51.178.95.237] => (item=python3-pip)
    ok: [51.178.95.237] => (item=virtualenv)
    ok: [51.178.95.237] => (item=python3-setuptools)

    TASK [Add Docker GPG apt Key] ***************************************************************************************************************
    ok: [51.178.95.237]

    TASK [Add Docker Repository] ****************************************************************************************************************
    ok: [51.178.95.237]

    TASK [Update apt and install docker-ce] *****************************************************************************************************
    ok: [51.178.95.237]

    PLAY [all] **********************************************************************************************************************************

    TASK [Gathering Facts] **********************************************************************************************************************
    ok: [51.178.95.237]

    TASK [Add Test User] ************************************************************************************************************************
    ok: [51.178.95.237]

    PLAY [all] **********************************************************************************************************************************

    TASK [Gathering Facts] **********************************************************************************************************************
    ok: [51.178.95.237]

    TASK [Install aptitude using apt] ***********************************************************************************************************
    ok: [51.178.95.237]

    TASK [Install required system packages] *****************************************************************************************************
    ok: [51.178.95.237] => (item=curl)
    ok: [51.178.95.237] => (item=python3)
    ok: [51.178.95.237] => (item=python3-dev)
    ok: [51.178.95.237] => (item=python3-pip)

    TASK [Download the TLJH installer] **********************************************************************************************************
    ok: [51.178.95.237]

    TASK [Run the TLJH installer] ***************************************************************************************************************
    changed: [51.178.95.237]

    TASK [Upgrade the tljh-plasmabio plugin] ****************************************************************************************************
    changed: [51.178.95.237]

    TASK [Restart JupyterHub] *******************************************************************************************************************
    changed: [51.178.95.237]

    PLAY RECAP **********************************************************************************************************************************
    51.178.95.237              : ok=15   changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


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

List of available playbooks
---------------------------

The Ansible playbooks are located in the ``ansible/`` directory:

- ``docker.yml``: install Docker CE on the host
- ``utils.yml``: install extra system packages useful for debugging and system administration
- ``users.yml``: create the tests users on the host
- ``quotas.yml``: enable quotas on the host to limit disk usage
- ``cockpit.yml``: install Cockpit on the host as a monitoring tool
- ``tljh.yml``: install TLJH and the PlasmaBio TLJH plugin
- ``admins.yml``: add admin users to JupyterHub
- ``https.yml``: enable HTTPS for TLJH
- ``uninstall.yml``: uninstall TLJH only
- ``site.yml``: the main playbook that references some of the other playbooks