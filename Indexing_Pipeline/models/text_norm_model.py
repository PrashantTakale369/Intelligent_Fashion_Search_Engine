"""
Qwen2.5-0.5B-Instruct wrapper for text normalization

"""
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from typing import List


class TextNormalizationModel:
    """Wrapper for Qwen2.5-0.5B-Instruct model"""
    
    def __init__(self, model_path: str, device: str = "cuda"):
        """
        Initialize the text normalization model
        
        Args:
            model_path: Path to the local model
            device: Device to run model on (cuda/cpu)
        """
        self.device = device
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map="auto" if device == "cuda" else None
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        if device == "cpu":
            self.model.to(device)
    
    def normalize_text(self, caption: str) -> str:
        """
        Normalize caption text to structured format
        
        Args:
            caption: Raw caption from image-to-text model
        
        Returns:
            Normalized text (e.g., "white shirt | black jeans | black tie | formal")
        """
        # Prepare prompt
        messages = [
            {
                "You are a fashion search engine text normalization and keyword extraction model.\n"
                    "Extract ONLY essential fashion-related keywords from the input text.\n\n"
                    "Rules:\n"
                    "1. Extract clothing items (e.g., shirt, jacket, raincoat, pants, jeans, tie).\n"
                    "2. Extract colors ONLY if explicitly mentioned.\n"
                    "3. Extract environment or setting ONLY if explicitly mentioned and relevant (e.g., office, park, indoor).\n"
                    "4. Do NOT guess or infer missing information.\n"
                    "5. Do NOT add, explain, or rephrase anything.\n"
                    "6. Do NOT include non-fashion words.\n"
                    "7. Output ONLY the extracted keywords separated by ' | '.\n"
                    "8. Keep the output minimal, precise, and consistent.\n\n"
                    "Example:\n"
                    "Input: A person wearing a bright yellow raincoat and black pants, standing outdoors on a city street.\n"
                    "Output: yellow | raincoat | black | pants | city street"

            },
            {
                "role": "user", 
                "content": f"Extract fashion keywords from: {caption}\n\nKeywords:"
            }
        ]
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=64,  # Reduced from 128 to prevent hallucination
                temperature=0.1,     # Reduced from 0.3 for more deterministic output
                do_sample=False,     # Greedy decoding for consistency
                repetition_penalty=1.2  # Prevent repetition
            )
        
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return response.strip()
    
    def normalize_texts_batch(self, captions: List[str]) -> List[str]:
        """
        Normalize multiple captions
        
        Args:
            captions: List of raw captions
        
        Returns:
            List of normalized texts
        """
        normalized_texts = []
        for caption in captions:
            try:
                normalized = self.normalize_text(caption)
                normalized_texts.append(normalized)
            except Exception as e:
                print(f"Error normalizing text: {e}")
                normalized_texts.append("")
        return normalized_texts
