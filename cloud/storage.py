import boto3
from config import Config
import logging

logger = logging.getLogger(__name__)

class CloudStorage:
    """Manages cloud storage with AWS S3."""
    
    def __init__(self, config: Config):
        """Initialize S3 client.
        
        Args:
            config: Config object with AWS settings.
        """
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=config.AWS_ACCESS_KEY,
            aws_secret_access_key=config.AWS_SECRET_KEY
        )
        self.bucket = config.S3_BUCKET
        logger.info("Initialized S3 storage with bucket: %s", self.bucket)
    
    def upload_data(self, key: str, data: str):
        """Upload data to S3.
        
        Args:
            key: S3 object key (e.g., 'trades.csv').
            data: Data to upload as string.
        """
        try:
            self.s3.put_object(Bucket=self.bucket, Key=key, Body=data)
            logger.info("Uploaded data to S3: %s", key)
        except Exception as e:
            logger.error("Failed to upload to S3: %s", e)