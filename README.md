## Docker-Commands

**For Windows & Linux with Nvidia CUDA (11.8) compatible:**

- ```docker-compose -f docker-compose-common.yml -f docker-compose-gpu.yml build``` to build the container

- ```docker-compose -f docker-compose-common.yml -f docker-compose-gpu.yml up -d``` to start the container

**For Mac:**

- ```docker-compose -f docker-compose-common.yml -f docker-compose-cpu.yml build``` to build the container

- ```docker-compose -f docker-compose-common.yml -f docker-compose-cpu.yml up -d``` to start the container


## Installation (on your hosted computer)

- Install driver for NVIDIA

- Install Cuda 11.8


## Models LLM Advice

- For Global Discussion best Model : ```llama3.1:latest```

- For Reflexion best Model : ```wizardlm2:latest```
