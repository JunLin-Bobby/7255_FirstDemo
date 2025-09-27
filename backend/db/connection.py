from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection settings
MONGO_URI = "mongodb://127.0.0.1:27017"
DATABASE_NAME = "firstdemo"

client = None

def get_database():
    """Retrieve the MongoDB database instance."""
    global client
    if client is None:
        raise Exception("MongoDB client is not initialized.")
    return client[DATABASE_NAME]

async def connect_to_mongo():
    """Establish a connection to MongoDB."""
    global client
    client = AsyncIOMotorClient(MONGO_URI)

async def close_mongo_connection():
    """Close the MongoDB connection."""
    global client
    if client:
        client.close()
        client = None