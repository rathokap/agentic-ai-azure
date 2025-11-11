"""
Azure Blob Storage Integration for ChromaDB Persistence
Provides backup and restore capabilities for ChromaDB using Azure Blob Storage (Free Tier)

Compatible with Azure SDK and ChromaDB.
"""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Conditional imports for Azure services
try:
    from azure.storage.blob import BlobServiceClient, ContainerClient
    from azure.core.exceptions import ResourceNotFoundError
    AZURE_BLOB_AVAILABLE = True
except ImportError:
    AZURE_BLOB_AVAILABLE = False
    logger.warning("azure-storage-blob not installed. Azure Blob Storage sync will not be available.")

# Import settings with fallback
try:
    from config.settings import (
        AZURE_STORAGE_CONNECTION_STRING,
        AZURE_BLOB_CONTAINER_NAME,
        USE_AZURE_BLOB_STORAGE
    )
except ImportError:
    AZURE_STORAGE_CONNECTION_STRING = None
    AZURE_BLOB_CONTAINER_NAME = "chromadb"
    USE_AZURE_BLOB_STORAGE = False


class ChromaDBAzureBlobSync:
    """
    Synchronizes ChromaDB files with Azure Blob Storage for persistence.
    Compatible with Azure Free Tier (5GB storage, 20,000 operations).
    """
    
    def __init__(
        self,
        connection_string: Optional[str] = None,
        container_name: str = "chromadb",
        local_path: str = "./knowledge_base"
    ):
        """
        Initialize Azure Blob Storage sync for ChromaDB.
        
        Args:
            connection_string: Azure Storage connection string
            container_name: Name of the blob container
            local_path: Local path to ChromaDB files
        """
        if not AZURE_BLOB_AVAILABLE:
            raise ImportError(
                "azure-storage-blob package is required for Azure Blob Storage sync. "
                "Install with: pip install azure-storage-blob>=12.19.0"
            )
        
        self.connection_string = connection_string or AZURE_STORAGE_CONNECTION_STRING
        self.container_name = container_name
        self.local_path = Path(local_path)
        self.container_client: Optional[ContainerClient] = None
        
        if self.connection_string:
            try:
                # Create blob service client
                blob_service = BlobServiceClient.from_connection_string(
                    self.connection_string
                )
                
                # Create container if it doesn't exist
                self.container_client = blob_service.get_container_client(container_name)
                try:
                    self.container_client.create_container()
                    logger.info(f"Created blob container: {container_name}")
                except Exception:
                    logger.debug(f"Container {container_name} already exists")
                
                logger.info(f"Azure Blob Storage sync initialized: {container_name}")
            except Exception as e:
                logger.error(f"Failed to initialize Azure Blob Storage: {str(e)}")
                self.container_client = None
        else:
            logger.warning("No Azure Storage connection string provided. Blob sync disabled.")
    
    def upload_chromadb(self, backup_name: Optional[str] = None) -> bool:
        """
        Upload ChromaDB files to Azure Blob Storage.
        
        Args:
            backup_name: Optional backup name prefix
            
        Returns:
            True if successful, False otherwise
        """
        if not self.container_client:
            logger.warning("Blob storage not configured. Skipping upload.")
            return False
        
        if not self.local_path.exists():
            logger.warning(f"ChromaDB path does not exist: {self.local_path}")
            return False
        
        try:
            backup_prefix = backup_name or "current"
            uploaded_count = 0
            
            # Upload all files in the knowledge base directory
            for file_path in self.local_path.rglob("*"):
                if file_path.is_file():
                    # Create blob name preserving directory structure
                    relative_path = file_path.relative_to(self.local_path)
                    blob_name = f"{backup_prefix}/{relative_path}"
                    
                    # Upload file
                    with open(file_path, "rb") as data:
                        blob_client = self.container_client.get_blob_client(blob_name)
                        blob_client.upload_blob(data, overwrite=True)
                        uploaded_count += 1
                        logger.debug(f"Uploaded: {blob_name}")
            
            logger.info(f"ChromaDB uploaded to Azure Blob Storage: {uploaded_count} files")
            return True
        except Exception as e:
            logger.error(f"Error uploading ChromaDB to blob storage: {str(e)}")
            return False
    
    def download_chromadb(self, backup_name: Optional[str] = None) -> bool:
        """
        Download ChromaDB files from Azure Blob Storage.
        
        Args:
            backup_name: Optional backup name prefix to restore from
            
        Returns:
            True if successful, False otherwise
        """
        if not self.container_client:
            logger.warning("Blob storage not configured. Skipping download.")
            return False
        
        try:
            backup_prefix = backup_name or "current"
            downloaded_count = 0
            
            # List and download all blobs with the prefix
            blob_list = self.container_client.list_blobs(name_starts_with=backup_prefix)
            
            for blob in blob_list:
                # Remove prefix from blob name to get relative path
                relative_path = blob.name.replace(f"{backup_prefix}/", "", 1)
                local_file_path = self.local_path / relative_path
                
                # Create parent directories
                local_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Download blob
                blob_client = self.container_client.get_blob_client(blob.name)
                with open(local_file_path, "wb") as download_file:
                    download_file.write(blob_client.download_blob().readall())
                
                downloaded_count += 1
                logger.debug(f"Downloaded: {blob.name}")
            
            if downloaded_count > 0:
                logger.info(f"ChromaDB downloaded from Azure Blob Storage: {downloaded_count} files")
                return True
            else:
                logger.warning(f"No ChromaDB backup found with prefix: {backup_prefix}")
                return False
        except Exception as e:
            logger.error(f"Error downloading ChromaDB from blob storage: {str(e)}")
            return False
    
    def list_backups(self) -> list:
        """
        List available ChromaDB backups.
        
        Returns:
            List of backup names
        """
        if not self.container_client:
            return []
        
        try:
            blob_list = self.container_client.list_blobs()
            # Extract unique backup prefixes
            backups = set()
            for blob in blob_list:
                backup_name = blob.name.split("/")[0]
                backups.add(backup_name)
            
            return sorted(list(backups))
        except Exception as e:
            logger.error(f"Error listing backups: {str(e)}")
            return []
    
    def delete_backup(self, backup_name: str) -> bool:
        """
        Delete a specific backup from blob storage.
        
        Args:
            backup_name: Name of the backup to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not self.container_client:
            return False
        
        try:
            blob_list = self.container_client.list_blobs(name_starts_with=backup_name)
            deleted_count = 0
            
            for blob in blob_list:
                blob_client = self.container_client.get_blob_client(blob.name)
                blob_client.delete_blob()
                deleted_count += 1
            
            logger.info(f"Deleted backup '{backup_name}': {deleted_count} files")
            return True
        except Exception as e:
            logger.error(f"Error deleting backup {backup_name}: {str(e)}")
            return False


def get_blob_sync(local_path: str = "./knowledge_base") -> Optional[ChromaDBAzureBlobSync]:
    """
    Factory function to get blob sync instance if configured.
    
    Args:
        local_path: Local path to ChromaDB files
        
    Returns:
        ChromaDBAzureBlobSync instance or None
    """
    if USE_AZURE_BLOB_STORAGE and AZURE_STORAGE_CONNECTION_STRING and AZURE_BLOB_AVAILABLE:
        try:
            sync = ChromaDBAzureBlobSync(
                connection_string=AZURE_STORAGE_CONNECTION_STRING,
                container_name=AZURE_BLOB_CONTAINER_NAME,
                local_path=local_path
            )
            if sync.container_client:
                logger.info("✓ Azure Blob Storage sync enabled for ChromaDB")
                return sync
        except Exception as e:
            logger.warning(f"Failed to create blob sync: {str(e)}")
    
    logger.info("Azure Blob Storage sync disabled")
    return None
