"""
Enhanced configuration management with validation and profiles.
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import os

@dataclass
class ProcessingConfig:
    """Configuration for SRD processing pipeline."""
    # API Configuration
    openai_model: str = "gpt-4o-mini"
    openai_max_tokens: int = 4000
    openai_temperature: float = 0.1
    
    # File Configuration
    input_pdf: str = "SRD_CC_v5.2.1.pdf"
    output_dir: str = "output"
    export_dir: str = "export"
    
    # Processing Options
    enable_ai_cleanup: bool = True
    enable_parallel_processing: bool = True
    max_workers: int = 4
    
    # Chunking Configuration
    chunk_min_words: int = 200
    chunk_max_words: int = 500
    preserve_toc_structure: bool = True
    
    # Quality Settings
    ocr_quality_threshold: float = 0.8
    retry_attempts: int = 3
    cache_ai_responses: bool = True

class ConfigManager:
    """Manage multiple configuration profiles."""
    
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
    def save_profile(self, name: str, config: ProcessingConfig):
        """Save a configuration profile."""
        profile_path = self.config_dir / f"{name}.json"
        with open(profile_path, 'w') as f:
            json.dump(asdict(config), f, indent=2)
    
    def load_profile(self, name: str) -> ProcessingConfig:
        """Load a configuration profile."""
        profile_path = self.config_dir / f"{name}.json"
        if not profile_path.exists():
            raise FileNotFoundError(f"Profile {name} not found")
        
        with open(profile_path, 'r') as f:
            data = json.load(f)
        return ProcessingConfig(**data)
    
    def list_profiles(self) -> list[str]:
        """List available configuration profiles."""
        return [f.stem for f in self.config_dir.glob("*.json")]

# Create default profiles
def create_default_profiles():
    manager = ConfigManager()
    
    # Fast profile for quick testing
    fast_config = ProcessingConfig(
        openai_model="gpt-3.5-turbo",
        chunk_max_words=300,
        enable_ai_cleanup=False
    )
    manager.save_profile("fast", fast_config)
    
    # High quality profile
    quality_config = ProcessingConfig(
        openai_model="gpt-4",
        openai_max_tokens=8000,
        chunk_min_words=300,
        chunk_max_words=700,
        retry_attempts=5
    )
    manager.save_profile("quality", quality_config)
    
    return manager
