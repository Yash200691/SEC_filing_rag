from qdrant_client import QdrantClient
from qdrant_client.models import Filter,FieldCondition,MatchValue
from typing import Dict, List, Optional
import logging

from config import (
    QDRANT_URL,
    COLLECTION_NAME
)
logger = logging.getLogger(__name__)

class QdrantDB:

    def __init__(self):

        print("Connecting to Qdrant...")

        self.client = QdrantClient(
            url=QDRANT_URL
        )

        self.collection_name = COLLECTION_NAME

        print("Connected Successfully!")

    def collection_exists(self):

        collections = self.client.get_collections()

        names = [
            c.name
            for c in collections.collections
        ]

        return self.collection_name in names

    def info(self):

        return self.client.get_collection(
            self.collection_name
        )

    def _build_filter(
    self,
    filters: Optional[Dict]
):
        """
        Convert a Python dictionary into a Qdrant Filter object.
        """

        if not filters:
            return None

        conditions = []

        for key, value in filters.items():

            conditions.append(
                FieldCondition(
                    key=key,
                    match=MatchValue(value=value)
                )
            )

        return Filter(
            must=conditions
        )

    def search(
        self,
        collection_name: str,
        query_vector: List[float],
        top_k: int = 5,
        filters: Optional[Dict] = None,
    ) -> List[Dict]:

        qdrant_filter = self._build_filter(filters)

        logger.info(
            "Searching collection '%s' with top_k=%d",
            collection_name,
            top_k,
        )

        try:

            response = self.client.query_points(
                collection_name=collection_name,
                query=query_vector,
                query_filter=qdrant_filter,
                limit=top_k,
                with_payload=True,
                with_vectors=False,
            )
            results = []

            for point in response.points:
                results.append(
                    {
                        "id": point.id,
                        "score": point.score,
                        "payload": point.payload,
                    }
                )

            return results

        except Exception as e:
            print("\nREAL ERROR:\n")
            raise