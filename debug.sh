#export CIBW_DEBUG_KEEP_CONTAINER=TRUE
act --action-offline-mode -s GITHUB_TOKEN="$(gh auth token)" --matrix os:ubuntu-latest --matrix python-minor:'7'
