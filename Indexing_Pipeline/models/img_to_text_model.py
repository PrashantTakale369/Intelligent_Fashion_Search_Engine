"""
Qwen2-VL wrapper for image to text caption generation
"""
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
import torch
from PIL import Image
from typing import List, Union


class ImageToTextModel:
    """Wrapper for Qwen2-VL-2B-Instruct model"""
    
    def __init__(self, model_path: str, device: str = "cuda"):
        """
        Initialize the image to text model
        
        Args:
            model_path: Path to the local model
            device: Device to run model on (cuda/cpu)
        """
        self.device = device
        self.model = Qwen2VLForConditionalGeneration.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map="auto" if device == "cuda" else None
        )
        self.processor = AutoProcessor.from_pretrained(model_path)
        
        if device == "cpu":
            self.model.to(device)
    
    def generate_caption(self, image_path: str) -> str:
        """
        Generate caption for a single image
        
        Args:
            image_path: Path to the image file
        
        Returns:
            Generated caption describing fashion items
        """
        # Load image
        image = Image.open(image_path).convert('RGB')
        
        # Prepare prompt for fashion description
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": image_path,
                    },
                    {
                        "type": "text", 
                        "text": """
                        You are a professional fashion image caption generator for an intelligent fashion search engine. 
                        Describe the image in one clear in short line statement but correct including
                        Upper body clothing with type and color  exapmle : black shirt.
                        body clothing with type and color example : blue jeans.
                        visible accessories with color example : red tai,black hat
                        Background or environment if relevant example : office,indoor,city street,park etc.
                        Posture or action if visible exaple : standing,walking,sitting etc.
                        
                        Focus only on visible, factual details dont guess.
                        Example:
                        "A person wearing a bright yellow raincoat and black pants, standing outdoors on a city street."
                        
                        """,
                    },
                ],
            }
        ]
        
        # Prepare for inference
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to(self.device)
        
        # Generate
        with torch.no_grad():
            generated_ids = self.model.generate(**inputs, max_new_tokens=128)
        
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        
        output_text = self.processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        
        return output_text[0]
    
    def generate_captions_batch(self, image_paths: List[str]) -> List[str]:
        """
        Generate captions for multiple images
        
        Args:
            image_paths: List of image file paths
        
        Returns:
            List of generated captions
        """
        captions = []
        for image_path in image_paths:
            try:
                caption = self.generate_caption(image_path)
                captions.append(caption)
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
                captions.append("")
        return captions
