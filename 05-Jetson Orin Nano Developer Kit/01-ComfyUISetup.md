## Running uncensored models on the NVIDIA Jetson Orin Nano Super Developer Kit

This guide is aimed at helping you set up uncensored models seamlessly on your Jetson Orin Nano, ensuring you can run powerful image generation models on this compact, yet powerful device.

This tutorial will walk you through each step of the process. Even if you're starting from a fresh installation, following along should ensure everything is set up correctly. And if anything doesn’t work as expected, feel free to reach out—I'll keep this guide updated to keep it running smoothly.

---

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
Preconfigured on JetPack 6.1!
```

Next, confirm that CUDA is installed correctly by checking the `nvcc` version.

```bash
nvcc --version
```

### Step 3: Installing PyTorch, TorchVision, and TorchAudio

Now let's install the essential libraries for image generation: PyTorch, TorchVision, and Torchaudio from here [devpi - cu12.6](http://jetson.webredirect.org/jp6/cu126)

```bash
pip install https://pypi.jetson-ai-lab.dev/jp6/cu126/+f/5cf/9ed17e35cb752/torch-2.5.0-cp310-cp310-linux_aarch64.whl
pip install https://pypi.jetson-ai-lab.dev/jp6/cu126/+f/9d2/6fac77a4e832a/torchvision-0.19.1a0+6194369-cp310-cp310-linux_aarch64.whl
pip install https://pypi.jetson-ai-lab.dev/jp6/cu126/+f/812/4fbc4ba6df0a3/torchaudio-2.5.0-cp310-cp310-linux_aarch64.whl
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

Go to the [ControlNet reference demo](https://civitai.com/posts/3943573), download image, import it in comfyUI.

And hit the "Queue Prompt" button, and watch the magic unfold!

Happy generating! 🎉
