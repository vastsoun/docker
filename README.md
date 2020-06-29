# Docker 19.03 on Ubuntu 18.04 LTS

## Installation

The following instructions originate from the following [link](https://docs.docker.com/install/linux/docker-ce/ubuntu/).

```bash
sudo apt update
```

```bash
sudo apt install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
```

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

```bash
sudo apt-key fingerprint 0EBFCD88
```

```bash
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```

```bash
sudo apt update
```

```bash
sudo apt install docker-ce docker-ce-cli containerd.io
```

```bash
sudo groupadd docker
```

## Nvidia GPUs

In addition to the previous steps, when wanting to run with an Nvidia GPU, the following must also be installed:
```bash
$ distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
$ curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
$ curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
$ sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
$ sudo systemctl restart docker

```

## Shell Commands

### Execution

Testing the base docker installation:
```bash
docker run hello-world
```

Starting bash terminal using a temporary user:
```bash
docker run -u $(id -u):$(id -g) --gpus all -it <DOCKER-IMAGE>
```

Starting bash terminal as the default `docker` sudoer user:
```bash
docker run -u docker --gpus all -it <DOCKER-CONTAINER>
```

Create new terminal session in already running container:
```bash
docker exec -it <CONTAINER> bash
```

### Management

Listing containers currently running on the host system:
```bash
docker ps
```

Listing images currently available on the host system:
```bash
docker image ls
```

Remove unused images:
```bash
docker image prune
```

## License

[Apache License 2.0](LICENSE)
