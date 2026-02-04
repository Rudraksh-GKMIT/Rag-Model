import json
import logging

from src.backend.constants import Constants

logger = logging.getLogger(__name__)


def seed_documents(client):
    logger.info("Starting document seeding")

    collection = client.collections.use("Document")

    documents = [
        {"document_path": "IP/leip1ps.pdf", "metadata": {"document_name": "CH-0"}},
        {"document_path": "IP/leip101.pdf", "metadata": {"document_name": "CH-1"}},
        {"document_path": "IP/leip102.pdf", "metadata": {"document_name": "CH-2"}},
        {"document_path": "IP/leip103.pdf", "metadata": {"document_name": "CH-3"}},
        {"document_path": "IP/leip104.pdf", "metadata": {"document_name": "CH-4"}},
        {"document_path": "IP/leip105.pdf", "metadata": {"document_name": "CH-5"}},
        {"document_path": "IP/leip106.pdf", "metadata": {"document_name": "CH-6"}},
        {"document_path": "IP/leip107.pdf", "metadata": {"document_name": "CH-7"}},
    ]

    logger.info("Fetching existing documents from Weaviate")
    existing = collection.query.fetch_objects(
        return_properties=["document_path"]
    )

    existing_paths = {
        obj.properties["document_path"]
        for obj in existing.objects
    }

    logger.info("Found %d existing documents", len(existing_paths))

    inserted_count = 0
    skipped_count = 0
    current_batch_count = 0
    batch_number = 1

    logger.info("Starting batch insert (batch size = %d)", Constants.BATCH_SIZE)

    with collection.batch.fixed_size(Constants.BATCH_SIZE) as batch:
        for doc in documents:
            path = doc["document_path"]

            if path in existing_paths:
                skipped_count += 1
                continue

            batch.add_object(
                properties={
                    "document_path": path,
                    "metadata": json.dumps(doc["metadata"]),
                }
            )

            inserted_count += 1
            current_batch_count += 1

            if current_batch_count == Constants.BATCH_SIZE:
                logger.info("Batch %d SENT (auto by Weaviate)", batch_number)
                batch_number += 1
                current_batch_count = 0

    if current_batch_count > 0:
        logger.info(
            "Final batch %d SENT on exit (%d items)",
            batch_number,
            current_batch_count,
        )

    logger.info(
        "Document seeding completed | inserted=%d | skipped=%d",
        inserted_count,
        skipped_count,
    )
