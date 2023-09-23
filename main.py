from fastapi import FastAPI, HTTPException, Depends
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import List

app = FastAPI()

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017"  # Replace with your MongoDB URI
client = MongoClient(MONGO_URI)
db = client["your_database_name"]  # Replace with your database name
collection_name = "your_collection_name"  # Replace with your collection name
collection: Collection = db[collection_name]

# Models
class Item:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


# Create a new item
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    result = collection.insert_one(item.__dict__)
    item.id = str(result.inserted_id)
    return item


# Get all items
@app.get("/items/", response_model=List[Item])
async def get_items():
    items = list(collection.find())
    return items


# Get a specific item by ID
@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    item = collection.find_one({"_id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return Item(**item)


# Update an item by ID
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, updated_item: Item):
    result = collection.replace_one({"_id": item_id}, updated_item.__dict__)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item.id = item_id
    return updated_item


# Delete an item by ID
@app.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: str):
    item = collection.find_one({"_id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    collection.delete_one({"_id": item_id})
    return Item(**item)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
