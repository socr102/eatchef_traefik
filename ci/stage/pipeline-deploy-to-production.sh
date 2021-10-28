#!/bin/bash
set -e
#echo "$DOCKER_HUB_PASSWORD" | docker login --username $DOCKER_HUB_USERNAME --password-stdin
export BITBUCKET_USERNAME=$PIPE_BITBUCKET_USERNAME
export BITBUCKET_PASSWORD=$PIPE_BITBUCKET_PASSWORD
export BITBUCKET_BRANCH=$BITBUCKET_BRANCH
export DOMAIN=$DOMAIN
export MAIN_DIR="traefik"
export REPO_URL="https://$BITBUCKET_USERNAME:$BITBUCKET_PASSWORD@bitbucket.org/mikkl/lottery-traefik.git"
if [ -d "$MAIN_DIR" ]; then rm -rf $MAIN_DIR; fi
git clone --single-branch --branch $BITBUCKET_BRANCH $REPO_URL $MAIN_DIR

cd $MAIN_DIR/ci/production/

python3 scripts.py create_env
python3 scripts.py load_env
python3 scripts.py up_traefik

cd ~ && rm -rf $MAIN_DIR

exec "$@"
