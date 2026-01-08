"""
Chatbot trainer module - Trains Rasa NLU/dialogue model
Configuration-driven training based on config.yaml settings
"""

import os
import logging
from pathlib import Path
import yaml
from rasa.train import train
from data_loader import DataLoader

logger = logging.getLogger(__name__)

class ChatbotTrainer:
      """Trains chatbot using Rasa framework"""

    def __init__(self, config_path: str = "config.yaml"):
              """Initialize trainer with configuration"""
              self.config_path = config_path
              self.config = self._load_config()
              self.data_loader = DataLoader(config_path)

    def _load_config(self) -> dict:
              """Load YAML configuration"""
              with open(self.config_path, 'r') as f:
                            return yaml.safe_load(f)

          def prepare_training_data(self):
                    """Load and prepare training data"""
                    logger.info("Preparing training data...")

        # Load dataset
        training_data = self.data_loader.get_training_data()
        logger.info(f"Loaded {training_data['records']} training records")

        return training_data

    def train_model(self, domain_file: str = "rasa/domain.yml",
                                        config_file: str = "rasa/config.yml"):
                                                  """Train Rasa NLU and dialogue management model"""
                                                  logger.info("Starting model training...")

        try:
                      # Prepare data first
                      self.prepare_training_data()

            # Train Rasa model
                      model = train(
                          domain=domain_file,
                          config=config_file,
                          training_files="data/",
                          output="models/",
                          epochs=self.config['training'].get('epochs', 100),
                          batch_size=self.config['training'].get('batch_size', 32)
                      )

            logger.info(f"Model trained successfully: {model}")
            return model

except Exception as e:
            logger.error(f"Training failed: {e}")
            raise

    def evaluate_model(self, test_data_path: str = "data/test/"):
              """Evaluate trained model on test data"""
              logger.info("Evaluating model...")
              # Evaluation logic would go here
              pass


if __name__ == "__main__":
      logging.basicConfig(level=logging.INFO)

    trainer = ChatbotTrainer()
    model_path = trainer.train_model()
    print(f"Training complete! Model saved to: {model_path}")
