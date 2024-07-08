# QDRANT

## Table of Content

- [QDRANT](#qdrant)
  - [Table of Content](#table-of-content)
  - [Installation](#installation)
    - [Docker Setup](#docker-setup)
    - [Client Libraries](#client-libraries)
  - [Examples](#examples)
    - [1. Semantic Search for Beginners](#1-semantic-search-for-beginners)

## [Installation](https://qdrant.tech/documentation/guides/installation/)

### [Docker Setup](https://qdrant.tech/documentation/guides/installation/#development)

- Pull the image:

```sh
docker pull qdrant/qdrant
```

- In the following command, `revise $(pwd)/path/to/data` for your Docker configuration. Then use the updated command to run the container:

```sh
docker run -p 6333:6333 \
    -v $(pwd)/path/to/data:/qdrant/storage \
    qdrant/qdrant
```

- Running with [gRPC](https://qdrant.tech/documentation/interfaces/#grpc-interface).
- If you decide to use `gRPC`, you must expose the port when starting Qdrant.:

```sh
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

### [Client Libraries](https://qdrant.tech/documentation/interfaces/#client-libraries)

```sh
pip install qdrant-client

# Installation with embedding model
pip install qdrant-client[fastembed]
```

## Examples

### 1. [Semantic Search for Beginners](https://qdrant.tech/documentation/tutorials/search-beginners/)

- Install embedding model.

```sh
pip install -U sentence-transformers
```

- Python code:

```py
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer


# Create embedding model
encoder = SentenceTransformer("all-MiniLM-L6-v2")

# Add dataset
documents = [
    {
        "name": "The Time Machine",
        "description": "A man travels through time and witnesses the evolution of humanity.",
        "author": "H.G. Wells",
        "year": 1895,
    },
    {
        "name": "Neuromancer",
        "description": "A hacker is hired to pull off a near-impossible hack and gets pulled into a web of intrigue.",
        "author": "William Gibson",
        "year": 1984,
    },
    ...
    {
        "name": "The Three-Body Problem",
        "description": "Humans encounter an alien civilization that lives in a dying system.",
        "author": "Liu Cixin",
        "year": 2008,
    },
]

# Define storage
# client = QdrantClient(":memory:")
URL: str = "http://localhost:6333"
qdrant = QdrantClient(URL)
INDEX_NAME: str = "my_books"

# Create collection
# Use recreate_collection for repeated experiments. It attempts to remove any existing collection with the same name before creating a new one.
client.recreate_collection(
    collection_name=INDEX_NAME,
    vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(),  # Vector size is defined by used model
        distance=models.Distance.COSINE,
    ),
)


# Upload data to collection
client.upload_points(
    collection_name="my_books",
    points=[
        models.PointStruct(
            id=idx, vector=encoder.encode(doc["description"]).tolist(), payload=doc
        )
        for idx, doc in enumerate(documents)
    ],
)

# Send a query to the collection.
hits = client.search(
    collection_name=INDEX_NAME,
    query_vector=encoder.encode("alien invasion").tolist(),
    limit=3,
)
for hit in hits:
    print(hit.payload, "score:", hit.score)

# Narrow down the query
hits = client.search(
    collection_name="my_books",
    query_vector=encoder.encode("alien invasion").tolist(),
    query_filter=models.Filter(
        must=[models.FieldCondition(key="year", range=models.Range(gte=2000))]
    ),
    limit=1,
)
for hit in hits:
    print(hit.payload, "score:", hit.score)
```
