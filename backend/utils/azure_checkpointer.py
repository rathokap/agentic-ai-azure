"""
Azure Table Storage Checkpointer for LangGraph
Provides persistent session storage using Azure Table Storage (Free Tier)

This is a simple implementation that stores serialized checkpoint data.
Compatible with LangGraph 0.2.64 and Azure SDK.
"""

import json
import logging
from typing import Optional, Iterator, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

# Conditional imports for Azure services
try:
    from azure.data.tables import TableServiceClient, TableClient
    from azure.core.exceptions import ResourceNotFoundError
    AZURE_TABLES_AVAILABLE = True
except ImportError:
    AZURE_TABLES_AVAILABLE = False
    logger.warning("azure-data-tables not installed. Azure Table Storage checkpointer will not be available.")

# Import settings with fallback
try:
    from config.settings import (
        AZURE_STORAGE_CONNECTION_STRING,
        AZURE_TABLE_NAME,
        USE_AZURE_TABLE_STORAGE
    )
except ImportError:
    AZURE_STORAGE_CONNECTION_STRING = None
    AZURE_TABLE_NAME = "checkpoints"
    USE_AZURE_TABLE_STORAGE = False


class AzureTableCheckpointer:
    """
    Simple LangGraph checkpointer that uses Azure Table Storage for persistence.
    Compatible with Azure Free Tier (20,000 operations/month free).
    
    This stores checkpoint data as JSON-serialized strings in Azure Tables.
    """
    
    def __init__(
        self,
        connection_string: Optional[str] = None,
        table_name: str = "checkpoints"
    ):
        """
        Initialize Azure Table Storage checkpointer.
        
        Args:
            connection_string: Azure Storage connection string
            table_name: Name of the table to use
        """
        if not AZURE_TABLES_AVAILABLE:
            raise ImportError(
                "azure-data-tables package is required for Azure Table Storage checkpointer. "
                "Install with: pip install azure-data-tables>=12.4.0"
            )
        
        self.connection_string = connection_string or AZURE_STORAGE_CONNECTION_STRING
        self.table_name = table_name
        self.table_client: Optional[TableClient] = None
        
        if self.connection_string:
            try:
                # Create table service client
                table_service = TableServiceClient.from_connection_string(
                    self.connection_string
                )
                
                # Create table if it doesn't exist
                table_service.create_table_if_not_exists(table_name)
                
                # Get table client
                self.table_client = table_service.get_table_client(table_name)
                logger.info(f"Azure Table Storage checkpointer initialized: {table_name}")
            except Exception as e:
                logger.error(f"Failed to initialize Azure Table Storage: {str(e)}")
                self.table_client = None
        else:
            logger.warning("No Azure Storage connection string provided. Checkpointer disabled.")
    
    def get(self, config: dict) -> Optional[dict]:
        """
        Retrieve checkpoint for a configuration.
        
        Args:
            config: Configuration dict with thread_id
            
        Returns:
            Checkpoint dict or None
        """
        if not self.table_client:
            return None
        
        thread_id = config.get("configurable", {}).get("thread_id")
        if not thread_id:
            return None
        
        try:
            # Query entity from table
            entity = self.table_client.get_entity(
                partition_key="checkpoint",
                row_key=str(thread_id)
            )
            
            # Deserialize checkpoint data
            checkpoint_data = json.loads(entity.get("checkpoint_data", "{}"))
            logger.debug(f"Retrieved checkpoint for thread {thread_id}")
            return checkpoint_data
            
        except ResourceNotFoundError:
            logger.debug(f"No checkpoint found for thread {thread_id}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving checkpoint for thread {thread_id}: {str(e)}")
            return None
    
    def put(self, config: dict, checkpoint: dict) -> dict:
        """
        Store checkpoint for a configuration.
        
        Args:
            config: Configuration dict with thread_id
            checkpoint: Checkpoint dict to store
            
        Returns:
            The stored configuration
        """
        if not self.table_client:
            return config
        
        thread_id = config.get("configurable", {}).get("thread_id")
        if not thread_id:
            return config
        
        try:
            # Create entity
            entity = {
                "PartitionKey": "checkpoint",
                "RowKey": str(thread_id),
                "checkpoint_data": json.dumps(checkpoint),
                "timestamp": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            # Upsert entity (insert or update)
            self.table_client.upsert_entity(entity)
            logger.debug(f"Checkpoint saved for thread {thread_id}")
            
        except Exception as e:
            logger.error(f"Error saving checkpoint for thread {thread_id}: {str(e)}")
        
        return config
    
    def list(self, config: dict) -> Iterator[Tuple[dict, dict]]:
        """
        List checkpoints for a configuration.
        
        Args:
            config: Configuration dict
            
        Yields:
            Tuples of (config, checkpoint)
        """
        if not self.table_client:
            return
        
        thread_id = config.get("configurable", {}).get("thread_id")
        if not thread_id:
            return
        
        try:
            # Get checkpoint for this thread
            checkpoint = self.get(config)
            if checkpoint:
                yield (config, checkpoint)
        except Exception as e:
            logger.error(f"Error listing checkpoints: {str(e)}")
    
def get_checkpointer():
    """
    Factory function to get the appropriate checkpointer based on configuration.
    Falls back to in-memory if Azure Table Storage is not available.
    
    Returns:
        Checkpointer instance (Azure Table Storage or in-memory MemorySaver)
    """
    # Try Azure Table Storage if configured
    if USE_AZURE_TABLE_STORAGE and AZURE_STORAGE_CONNECTION_STRING and AZURE_TABLES_AVAILABLE:
        try:
            checkpointer = AzureTableCheckpointer(
                connection_string=AZURE_STORAGE_CONNECTION_STRING,
                table_name=AZURE_TABLE_NAME
            )
            if checkpointer.table_client:
                logger.info("✓ Using Azure Table Storage for persistent checkpoints")
                return checkpointer
        except Exception as e:
            logger.warning(f"Failed to create Azure Table checkpointer: {str(e)}")
    
    # Fallback to in-memory
    logger.info("Using in-memory checkpointer (sessions will not persist across restarts)")
    try:
        from langgraph.checkpoint.memory import MemorySaver
        return MemorySaver()
    except ImportError:
        logger.error("LangGraph checkpoint module not available")
        return None
