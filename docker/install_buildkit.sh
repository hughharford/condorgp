
#!/bin/bash
#
# https://docs.docker.com/build/buildkit/
# https://github.com/docker/buildx/releases/
# https://github.com/docker/buildx

## docker builder prune --all
## docker buildx du --verbose

## For Ubuntu 24.04 try: sudo apt install docker-buildx
## Or run the commands below.

#VERSION=v0.14.1
VERSION=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/docker/buildx/releases/latest)
VERSION=${VERSION##*/}

mkdir -p $HOME/.docker/cli-plugins
wget https://github.com/docker/buildx/releases/download/$VERSION/buildx-$VERSION.linux-amd64 -O $HOME/.docker/cli-plugins/docker-buildx
chmod +x $HOME/.docker/cli-plugins/docker-buildx

export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

echo 'export DOCKER_BUILDKIT=1' >> $HOME/.profile
echo 'export COMPOSE_DOCKER_CLI_BUILD=1' >> $HOME/.profile
