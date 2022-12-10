from semantic_aug.semantic_augmentation import SemanticAugmentation
from diffusers import StableDiffusionImg2ImgPipeline
from diffusers.utils import logging
from PIL import Image
from typing import Any, Tuple
import torch


class RealGuidance(SemanticAugmentation):

    def __init__(self, model_path: str = "CompVis/stable-diffusion-v1-4",
                 prompt: str = "a drone image of a brown field",
                 strength: float = 0.5, 
                 guidance_scale: float = 7.5):

        super(RealGuidance, self).__init__()

        self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            model_path, use_auth_token=True,
            revision="fp16", 
            torch_dtype=torch.float16
        ).to('cuda')

        logging.disable_progress_bar()
        self.pipe.set_progress_bar_config(disable=True)

        self.prompt = prompt
        self.strength = strength
        self.guidance_scale = guidance_scale

    def forward(self, image: torch.Tensor, 
                metadata: Any) -> Tuple[torch.Tensor, Any]:

        canvas = image.resize((512, 512), Image.BILINEAR)

        canvas = self.pipe(
            image=canvas,
            prompt=[self.prompt], 
            strength=self.strength, 
            guidance_scale=self.guidance_scale
        ).images[0]

        image = canvas.resize(image.size, Image.BILINEAR)

        return image, metadata