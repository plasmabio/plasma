# Changelog

## [Unreleased]

- Show a loading spinner when navigating from the JupyterLab launcher (e.g. RStudio) inside the iframe

## [0.4]

- Side panel toggle button now displays the PLASMA logo rotated vertically

## [0.3]

- Upgrade tljh-repo2docker

## [0.2]

### User Interface

- JupyterLab is now embedded in a full-screen iframe on the hub home page
- A retractable side panel provides access to Stop and Home buttons without leaving JupyterLab
- The side panel toggle button shows the PLASMA logo and auto-expands for 2 seconds on page load
- A loading overlay with spinner is shown while JupyterLab loads; after 15 seconds without response a Reload button is displayed
- Links and `window.open` calls from inside the iframe are intercepted to stay in the same tab

### Permissions page

- Added a filter input to search environments by name
- Compacted the layout to show more environments on screen
- Fixed appearance in Firefox dark mode

### Ansible

- Improved upgrade reliability: plugins are now force-reinstalled on each run
- Simplified service restart (single `restart` instead of stop/kill/start sequence)

### Other

- tljh-repo2docker upgraded to 3.0
- The database URL can now be set via the `TLJH_PLASMA_DB_URL` environment variable
- Fixed non-unique UID handling in the container entrypoint

## [0.1] 2020-05-11

First public announcement of the Plasma project.

Check out the following links to learn more:

- Blog post: https://blog.jupyter.org/plasma-a-learning-platform-powered-by-jupyter-1b850fcd8624
- Plasma website: https://plasmabio.org
- GitHub organization: https://github.com/plasmabio
