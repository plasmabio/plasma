# Removing an environment

To remove an environment, click on the `Remove` button. This will bring the following confirmation dialog:

```{image} ../images/environments/remove-dialog.png
:align: center
:alt: Removing an environment
:width: 100%
```

After clicking on `Remove`, a spinner will be shown and the page will reload shortly after:

```{image} ../images/environments/remove-spinner.png
:align: center
:alt: Removing an environment - spinner
:width: 100%
```

(remove-error)=

## Removing an environment returns an error

It is possible that removing an environment returns an error such as the following:

```{image} ../images/environments/remove-image-error.png
:align: center
:alt: Removing an environment - error
:width: 100%
```

This is most likely because the environment is currently being used. We recommend asking the users to stop their server
before attempting to remove the environment one more time.

The environment (image) that a user is currently using is also displayed in the Admin panel:

```{image} ../images/environments/admin-panel-images.png
:align: center
:alt: Admin panel with the image name
:width: 100%
```
