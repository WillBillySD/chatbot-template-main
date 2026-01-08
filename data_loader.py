"""
Data loader module - Handles loading datasets from configured sources
This module is configuration-driven and loads datasets based on config.yaml
"""

import json
import requests
import pandas as pd
from typing import Dict, List, Any
import logging
import yaml

logger = logging.getLogger(__name__)

class DataLoader:
      """Loads training data from configured sources"""

    def __init__(self, config_path: str = "config.yaml"):
              """Initialize data loader with configuration"""
              self.config = self._load_config(config_path)
              self.dataset_config = self.config.get('dataset', {})

    def _load_config(self, config_path: str) -> Dict:
              """Load YAML configuration file"""
              try:
                            with open(config_path, 'r') as f:
                                              return yaml.safe_load(f)
              except FileNotFoundError:
                            logger.warning(f"Config file not found at {config_path}, using defaults")
                            return {'dataset': {'name': 'toxic_conversations'}}

          def load_dataset(self) -> pd.DataFrame:
                    """Load dataset from configured URL"""
                    dataset_name = self.dataset_config.get('name', 'toxic_conversations')
                    dataset_url = self.dataset_config.get('url')

        logger.info(f"Loading dataset: {dataset_name}")

        if not dataset_url:
                      raise ValueError(f"No URL configured for dataset: {dataset_name}")

        try:
                      response = requests.get(dataset_url)
                      response.raise_for_status()
                      data = response.json()

            df = pd.DataFrame(data)
            logger.info(f"Successfully loaded {len(df)} records from {dataset_name}")
            return df
except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            raise

    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
              """Preprocess dataset for training"""
              # Remove duplicates
              df = df.drop_duplicates(subset=['text'], keep='first')

        # Remove null values
              df = df.dropna(subset=['text'])

        # Convert to lowercase
              if 'text' in df.columns:
                            df['text'] = df['text'].str.lower()

              logger.info(f"Preprocessed data: {len(df)} records remaining")
              return df

    def get_training_data(self) -> Dict[str, Any]:
              """Load and preprocess training data"""
              df = self.load_dataset()
              df = self.preprocess_data(df)

        return {
                      'data': df,
                      'records': len(df),
                      'columns': df.columns.tolist()
        }


if __name__ == "__main__":
      loader = DataLoader()
      training_data = loader.get_training_data()
      print(f"Loaded {training_data['records']} training records")
  
