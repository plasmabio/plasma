(environments-rebuild)=

# Rebuilding an environment

To rebuild an environment, click the **Rebuild** button (circular arrow icon) on the right of the
environment row. A dialog will open, pre-filled with the existing settings:

```{note}
The **Rebuild** button is only available if the environment belongs to the current user and is not
currently being built.
```

```{image} ../images/environments/rebuild-dialog.png
:align: center
:alt: Rebuild environment dialog
:width: 100%
```

Click **Rebuild Environment** to start the build.

```{warning}
Users whose server is currently running on this environment will keep using the old image until they
stop and restart their server.
```
