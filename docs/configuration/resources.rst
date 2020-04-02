Resources
=========

Memory
------

By default PlasmaBio sets a limit of ``2GB`` for each user server.

This limit is enforced by the operating system, which kills the process if the memory consumption goes aboved this threshold.

Users can monitor their memory usage using the indicator in the top bar area:

.. image:: ../images/configuration/memory-usage.png
   :alt: Memory indicator in the top bar area
   :width: 50%
   :align: center

CPU
---

By default PlasmaBio sets a limit of ``2 cpus`` for each user server.

This limit is enforced by the operating system, which throttles access to the CPU by the processes running in the
Docker container.
