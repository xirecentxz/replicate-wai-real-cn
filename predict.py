import os
import time
import torch
from typing import List
from cog import BasePredictor, Input, Path
from diffusers import (
    StableDiffusionXLPipeline,
    EulerAncestralDiscreteScheduler,
    AutoencoderKL
)

MODEL_URL = "https://huggingface.co/LyliaEngine/waiREALCN_v50/resolve/main/waiREALCN_v50.safetensors"
WEIGHTS_CACHE = "./weights/waiREALCN_v50.safetensors"

class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory to make running multiple predictions efficient"""
        print("--> Initializing WAI Real Asian v5.0 (Pony SDXL)...")
        
        # Download weights if not baked into the image
        if not os.path.exists(WEIGHTS_CACHE):
            os.makedirs(os.path.dirname(WEIGHTS_CACHE), exist_ok=True)
            print(f"--> Weights not found locally. Downloading from {MODEL_URL}...")
            # Use pget or wget for high speed
            exit_code = os.system(f"wget -c -O {WEIGHTS_CACHE} '{MODEL_URL}'")
            if exit_code != 0 or not os.path.exists(WEIGHTS_CACHE):
                raise RuntimeError(f"Failed to download model weights from {MODEL_URL}")
        
        print(f"--> Loading pipeline from single file: {WEIGHTS_CACHE}...")
        self.pipe = StableDiffusionXLPipeline.from_single_file(
            WEIGHTS_CACHE,
            torch_dtype=torch.float16,
            use_safetensors=True
        )
        
        # Set Euler A scheduler (optimal for Pony / SDXL Realism)
        self.pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(self.pipe.scheduler.config)
        self.pipe.to("cuda")
        self.pipe.enable_vae_tiling()
        print("--> WAI Real Asian v5.0 setup complete and ready for inference!")

    def predict(
        self,
        prompt: str = Input(
            description="Prompt tags (Pony format: score_9, score_8_up, 1girl, ...)",
            default="score_9, score_8_up, score_7_up, 1girl, solo, beautiful asian woman, detailed skin texture, photorealistic, masterpiece, highres"
        ),
        negative_prompt: str = Input(
            description="Negative prompt",
            default="score_6, score_5, score_4, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, username, blurry, artist name"
        ),
        width: int = Input(
            description="Width of output image",
            default=1024,
            choices=[512, 768, 832, 896, 1024, 1152, 1216, 1344]
        ),
        height: int = Input(
            description="Height of output image",
            default=1024,
            choices=[512, 768, 832, 896, 1024, 1152, 1216, 1344]
        ),
        num_inference_steps: int = Input(
            description="Number of denoising steps",
            ge=15,
            le=50,
            default=28
        ),
        guidance_scale: float = Input(
            description="Classifier-Free Guidance Scale (CFG)",
            ge=1.0,
            le=15.0,
            default=6.0
        ),
        seed: int = Input(
            description="Random seed (-1 for random)",
            default=-1
        )
    ) -> List[Path]:
        """Run a single prediction on the model"""
        if seed < 0:
            seed = int(time.time() * 1000) % 2147483647
        
        generator = torch.Generator("cuda").manual_seed(seed)
        
        print(f"--> Generating image: {width}x{height}, steps={num_inference_steps}, cfg={guidance_scale}, seed={seed}")
        result = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator
        )
        
        output_paths = []
        for i, img in enumerate(result.images):
            out_file = f"/tmp/output_{seed}_{i}.jpg"
            img.save(out_file, format="JPEG", quality=95)
            output_paths.append(Path(out_file))
            
        return output_paths
