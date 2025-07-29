## Running uncensored models on the NVIDIA Jetson Orin Nano Super Developer Kit

This guide is aimed at helping you set up uncensored models seamlessly on your Jetson Orin Nano, ensuring you can run powerful image generation models on this compact, yet powerful device.

This tutorial will walk you through each step of the process. Even if you're starting from a fresh installation, following along should ensure everything is set up correctly. And if anything doesn’t work as expected, feel free to reach out—I'll keep this guide updated to keep it running smoothly.

---
## Preparation
* Ubuntu 22.04 JetPack 6.2.x
* nvidia-jetson package - require TorchAudio, TorchVision build
* cmake 4.x.x or higher - require ComfyUI build
* Up-to-date all packages - require pytorch build

Require this package from build TorchAudio, TorchVision
```bash
sudo apt install ffmpeg libavformat-dev libavcodec-dev libavutil-dev libavdevice-dev libavfilter-dev
```

If your `cmake` version is below 3.5.x, you need update cmake version.
`pip install cmake` isn't work because build process isn't using python cmake package.
```bash
git clone https://github.com/Kitware/CMake --depth 1
./bootstrap && make && sudo make install
```

## Let’s Dive In

### Step 1: Installing Miniconda and Setting Up a Python Environment

First, we need to install Miniconda on your Jetson Nano. This will allow us to create an isolated Python environment for managing dependencies. Let's set up our project environment.

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
chmod +x Miniconda3-latest-Linux-aarch64.sh
./Miniconda3-latest-Linux-aarch64.sh

conda update conda
```

Now, we create and activate a Python 3.10 environment for our project.

```bash
conda create -n comfyui python=3.10
conda activate comfyui
```

### Step 2: Installing CUDA, cuDNN, TensorRT, and Verifying nvcc

```bash
Preconfigured on JetPack 6.2!
```

Next, confirm that CUDA is installed correctly by checking the `nvcc` version.

```bash
nvcc --version
```

### Step 3: Installing PyTorch, TorchVision, and TorchAudio

Now let's install the essential libraries for image generation: PyTorch, TorchVision, and Torchaudio from here [devpi - cu12.6](http://jetson.webredirect.org/jp6/cu126)

```bash
pip install https://developer.download.nvidia.com/compute/redist/jp/v61/pytorch/torch-2.5.0a0+872d972e41.nv24.08.17622132-cp310-cp310-linux_aarch64.whl
```

You need build TorchVision.
```bash
git clone https://github.com/pytorch/vision torchvision
cd torchvison
git checkout v0.19.1
USE_CUDA=1 pip install -v -e . --no-use-pep517
python setup.py install --user
```

If you're using audio generation, build TorchAudio (Optional)
```bash
git clone https://github.com/pytorch/audio torchaudio
cd torchaudio
git checkout v2.5.0
USE_CUDA=1 pip install -v -e . --no-use-pep517
python setup.py install --user
```

### Step 4: Cloning the Project Repository

Now, we clone the necessary source code for the project from GitHub. This will include the files for running uncensored models from civtai.com.

```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
```

### Step 5: Installing Project Dependencies

Next, install the required dependencies for the project by running the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### Step 6: Resolving Issues with NumPy (if necessary)

If you encounter issues with NumPy, such as compatibility problems, you can fix it by downgrading to a version below 2.0.

```bash
pip install "numpy<2"
```

### Step 7: Running ComfyUI

Finally, we can run ComfyUI to check if everything is set up properly. Start the app with the following command:

```bash
python main.py --listen 0.0.0.0
```

---

## Great! Now that you've got ComfyUI up and running, it’s time to load your first uncensored model.

1. Navigate to [civitai.com](https://civitai.com) and select a model. For example, you can choose the following model:

   [RealVisionBabes v1.0](https://civitai.com/models/543456?modelVersionId=604282)

2. Download the model file: [realvisionbabes_v10.safetensors](https://civitai.com/api/download/models/604282?type=Model&format=SafeTensor&size=pruned&fp=fp16)

3. Place it inside the `models/checkpoints` folder.

4. Download the VAE file: [ClearVAE_V2.3_fp16.pt](https://civitai.com/api/download/models/604282?type=VAE)

5. Place it inside the `models/vae` folder.



---

## You're all set to launch your first run! 

Visit the provided URL by ComfyUI (`http://jetson:8188`) on your Jetson Nano.

Go to the [ControlNet reference demo](https://civitai.com/posts/3943573), download the workflow (also available in the repo as workflow-api.json) and, import it in comfyUI.

And hit the "Queue Prompt" button, and watch the magic unfold!

Happy generating! 🎉
