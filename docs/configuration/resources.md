# Resources

Plasma provides default values to limit the memory and CPU usage.

## Memory

By default Plasma sets a limit of `2GB` for each user server.

This limit is enforced by the operating system, which kills the process if the memory consumption goes aboved this threshold.

Users can monitor their memory usage using the indicator in the top bar area if the environment has these dependencies
(see the {ref}`resources-display` section below).

```{image} ../images/configuration/memory-usage.png
:align: center
:alt: Memory indicator in the top bar area
:width: 50%
```

## CPU

By default Plasma sets a limit of `2 CPUs` for each user server.

This limit is enforced by the operating system, which throttles access to the CPU by the processes running in the
Docker container.

Users can monitor their CPU usage using the indicator in the top bar area if the environment has these dependencies
(see the {ref}`resources-display` section below).

```{image} ../images/configuration/cpu-usage.png
:align: center
:alt: CPU indicator in the top bar area
:width: 50%
```

(resources-display)=

## Displaying the indicators

To enable the memory and CPU indicators as shown above, the following dependencies must be added to the user environment:

- `jupyter-resource-usage`
- `jupyterlab-topbar`
- `jupyterlab-topbar-text`
- `jupyterlab-system-monitor`

As an example, checkout this [template](https://github.com/plasmabio/template-python/blob/master/binder/environment.yml) for a Python environment.
