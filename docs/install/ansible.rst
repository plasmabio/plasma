.. _install/ansible:

Deploying with Ansible
======================

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

        conda create -n plasmasbio -c conda-forge python nodejs
        conda activate plasmabio


Make sure `Ansible <https://docs.ansible.com/ansible/latest/index.html>`_ is installed:

.. code-block:: bash

    python -m pip install ansible


To verify the installation, run:

.. code-block:: bash

    which ansible

This should return the path to the ansible CLI tool in the virtual environment.
For example: ``/home/myuser/miniconda/envs/plasmabio/bin/ansible``

Check out the repository, and go to the ``plasmabio/ansible/`` directory:

.. code-block:: bash

    git clone https://github.com/plasmabio/plasmabio
    cd plasmabio/ansible

Make sure the ``hosts`` file contains the correct IP and hostname for the server. For example:

.. code-block:: text

    [servers]
    51.178.95.237

Then run the following command after replacing ``<user>`` by your user on the remote machine:

.. code-block:: bash

    ansible-playbook all.yml -i hosts -u <user>

Many Ubuntu systems running on cloud virtual machines have the default ``ubuntu`` user. In this case, the command becomes:

.. code-block:: bash

    ansible-playbook all.yml -i hosts -u ubuntu

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


Running individual playbooks
............................

The ``all.yml`` Ansible playbook includes all the playbooks and will process them in order.

It is however possible to run the playbooks individually. For example to run the ``tljh.yml`` playbook only (to install
and update The Littlest JupyterHub):

.. code-block:: bash

    ansible-playbook tljh.yml -i hosts -u ubuntu

For more in-depth details about the Ansible playbook, check out the
`official documentation <https://docs.ansible.com/ansible/latest/user_guide/playbooks.html>`_.
