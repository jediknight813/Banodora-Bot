import pymongo
import os
from dotenv import load_dotenv
import regex


load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")


client = pymongo.MongoClient(MONGO_DB_URL)
db = client["SummaryBot"]


def get_collection_names():
    return db.list_collection_names()


def create_message_log(server_name, object):
    collection = db[server_name]
    collection.insert_one(object)
    return {"message": "Message added."}


def find_documents_in_channel_for_question(collection_name, limit):
    collection = db[collection_name]
    query = {}
    result = collection.find(query).sort("created_at", -1).limit(int(limit))

    documents = list(result)
    print("documents: ", len(documents))

    documents.reverse()
    documents = list(chunk_list(documents, 20))

    print("chunks: ", len(documents))
    return documents


def chunk_list(input_list, chunk_size):
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i : i + chunk_size]


def find_documents_for_question(question, channels_to_search, limit):
    documents = []

    for collection_name in channels_to_search:
        collection = db[collection_name]

        # Split the input question into individual words
        keywords = question.split()

        # Create a regex pattern for fuzzy matching each keyword
        regex_pattern = "|".join(
            f"(?=.*{regex.escape(keyword)})" for keyword in keywords
        )

        # Use regex for fuzzy matching on the message field
        query = {
            "message": {"$regex": regex_pattern, "$options": "i"},
        }

        result = collection.find(query).sort("created_at", -1).limit(100)

        # Process the result as needed
        for document in result:
            documents.append(document)
            # print(f"Collection: {collection_name}, Document: {document}")

    sorted_documents = sorted(documents, key=lambda x: x["created_at"], reverse=True)[
        :limit
    ]
    return sorted_documents
