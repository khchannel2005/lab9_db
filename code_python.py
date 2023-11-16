import pymongo

# Підключення до бази даних MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["music_catalog"]
albums_collection = database["albums"]
artists_collection = database["artists"]
tracks_collection = database["tracks"]

# Функція для додавання альбому
def add_album(title, artist, release_year):
    album_data = {
        "title": title,
        "artist": artist,
        "release_year": release_year,
        "tracks": []
    }
    result = albums_collection.insert_one(album_data)
    print(f"Album added with ID: {result.inserted_id}")
    return result.inserted_id

# Функція для додавання виконавця
def add_artist(name, genre):
    artist_data = {
        "name": name,
        "genre": genre
    }
    result = artists_collection.insert_one(artist_data)
    print(f"Artist added with ID: {result.inserted_id}")
    return result.inserted_id

# Функція для додавання трека до альбому
def add_track(album_id, title, duration):
    track_data = {
        "title": title,
        "duration": duration
    }
    albums_collection.update_one(
        {"_id": album_id},
        {"$push": {"tracks": track_data}}
    )
    print(f"Track added to album {album_id}")

# Функція для зчитування альбому за ID
def get_album_by_id(album_id):
    return albums_collection.find_one({"_id": album_id})

# Функція для оновлення інформації про альбом
def update_album(album_id, title, artist, release_year):
    albums_collection.update_one(
        {"_id": album_id},
        {"$set": {"title": title, "artist": artist, "release_year": release_year}}
    )
    print(f"Album {album_id} updated")

# Функція для видалення альбому за ID
def delete_album(album_id):
    albums_collection.delete_one({"_id": album_id})
    print(f"Album {album_id} deleted")

#Приклад використання функцій
artist_id_1 = add_artist("Kelly Clarkson", "Pop")
album_id_1 = add_album("Stronger (Deluxe Version)", artist_id_1, 2011)
add_track(album_id_1, "Because of You", "3:45")

# Зчитування та виведення інформації про альбом
retrieved_album = get_album_by_id(album_id_1)
print("Retrieved Album:")
print(retrieved_album)

# Оновлення інформації про альбом
update_album(album_id_1, "Updated Album 1", artist_id_1, 2023)
retrieved_album = get_album_by_id(album_id_1)
print("Updated Album:")
print(retrieved_album)

# Видалення альбому
delete_album(album_id_1)
