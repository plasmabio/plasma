Culling idle servers
====================

PlasmaBio uses the `same defaults as The Littlest JupyterHub <http://tljh.jupyter.org/en/latest/topic/idle-culler.html#default-settings>`_
for culling idle servers.

It overrides the ``timeout`` value to ``3600``, which means that the user servers will be shut down if they have
been idle for more than one hour.
