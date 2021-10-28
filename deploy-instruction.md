Server pre-configuration

- Connect to server
- Install latest Docker and Docker Compose

```shell

# docker install
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# docker-compose install
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

```

- Create docker network
  - `docker network create --internal=false --attachable "proxy"`
- Add a new pipeline in bitbucket-pipeline.yml if you want to deploy to another server with a new environment.
    ```shell
      - step:
          <<: *Build-Deploy-Step
          deployment: {new-env}
          trigger: manual |< Optional
    ```
- Add all required env to deployment environment in bitbucket
- Add ssh key to host in .ssh/authorized_keys and get ssh fingerprint key from bitbucket
