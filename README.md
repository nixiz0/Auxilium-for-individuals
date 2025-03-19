# **Auxilium**

## **Project Overview**

Auxilium is designed to make optimizing and managing Large Language Models (LLMs) locally more accessible and adaptable for everyone, everywhere. This project provides a powerful system that includes:

- **Automatic Translation**: Currently supports French to English but can be adapted for other languages.
- **Reflection Chain**: A feature that can be activated or deactivated to enhance model thinking processes.
- **Advanced Document Profile Management**: Use an advanced Retrieval-Augmented Generation (RAG) system to interact with your own documents effectively.
- **Custom Model Creation**: Through a guided menu, users can create their own instruction-tuned models.
- **Self-Contained System**: Everything operates seamlessly within a Docker container with an internal network.


### **For Nvidia graphics card**

For systems with NVIDIA GPUs:
- Ensure drivers are installed.
- Install CUDA 11.8 (if compatible).

---


## **Docker Commands**

**For Windows & Linux with Nvidia CUDA (11.8) compatible:**

- ```docker-compose -f docker-compose-common.yml -f docker-compose-gpu.yml build``` to build the container

- ```docker-compose -f docker-compose-common.yml -f docker-compose-gpu.yml up -d``` to start the container

**For Mac:**

- ```docker-compose -f docker-compose-common.yml -f docker-compose-cpu.yml build``` to build the container

- ```docker-compose -f docker-compose-common.yml -f docker-compose-cpu.yml up -d``` to start the container


## **Project Architecture**

![Auxilium Architecture](auxilium_architecture.png)


## Models LLM Advice

- For Global Discussion Recommended Model : ```llama3.1:latest```

- For Reflexion Recommended Model : ```wizardlm2:latest```


## Author

- [@nixiz0](https://github.com/nixiz0)