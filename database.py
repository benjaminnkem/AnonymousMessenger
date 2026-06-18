from mongoengine import connect

connect(
    db="anonymous_messenger",
    host="mongodb://localhost:27017"
)
