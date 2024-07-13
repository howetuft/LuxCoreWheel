export CIBW_DEBUG_KEEP_CONTAINER=TRUE
act --action-offline-mode --matrix os:ubuntu-latest --matrix python-minor:'7'
