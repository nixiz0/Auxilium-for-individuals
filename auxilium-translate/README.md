## Docker commands

**For CUDA 11.8 Image (using Nvidia GPU)**

```docker build -f Dockerfile.cuda -t translate_api_cuda .```

```docker run --network="host" --gpus all translate_api_cuda```


**For No Cuda Image (using CPU)**

```docker build -f Dockerfile.nocuda -t translate_api_nocuda .```

```docker run --network="host" translate_api_nocuda```