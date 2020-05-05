#!/bin/bash -l

set -e

# ${HOME} is set by SystemUserSpawner:
# https://github.com/jupyterhub/dockerspawner/blob/6f7e04ce9f989e98cf99bb2a6dfa1cff96466135/dockerspawner/systemuserspawner.py#L113

# handle user override
NB_GID=${NB_UID}
PATH=${PATH//jovyan/$NB_USER}
IMAGE_DIR=${HOME}/${USER_IMAGE}

# add a new group for the user
groupadd -g $NB_GID -o ${NB_GROUP:-${NB_USER}}

# add the user and set their home directory
useradd --home ${HOME} -u $NB_UID -g $NB_GID -G 100 -l $NB_USER

# copy the content from the default docker image to the user home directory
shopt -s dotglob
cp -r --no-clobber /home/jovyan/* ${IMAGE_DIR}

# remove the .cache if it exists, as it can be a couple hundreds MB big
if [ -d ${IMAGE_DIR}/.cache ]
then
  rm -r ${IMAGE_DIR}/.cache
fi

# set the name of the environment as the topbar text indicator
TOPBAR_TEXT_SETTINGS_DIR=${IMAGE_DIR}/.jupyter/lab/user-settings/jupyterlab-topbar-text
mkdir -p ${TOPBAR_TEXT_SETTINGS_DIR}
echo "{\"editable\": false, \"text\":\"${USER_IMAGE}\"}" > ${TOPBAR_TEXT_SETTINGS_DIR}/plugin.jupyterlab-settings

# set the correct permissions for the user home subdirectory
chown -R ${NB_USER}:${NB_USER} ${IMAGE_DIR}

# set the Jupyter paths environment variables to find potential configuration
# and data files from the user environment base images home directories
export JUPYTER_CONFIG_DIR=${IMAGE_DIR}/.jupyter
export JUPYTER_PATH=${IMAGE_DIR}/.local/share/jupyter

# start the notebook server from the environment directory
cd ${IMAGE_DIR}

# execute the notebook process as the given user
exec su - $NB_USER -m -c '"$0" "$@"' -- "$@"
