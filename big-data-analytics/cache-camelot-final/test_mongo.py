#!/usr/bin/python

import pymongo
# Open the MongoDB connection
connMongo = pymongo.Connection('mongodb://localhost:27017')
# Print the available MongoDB databases
print connMongo.database_names()
# Close the MongoDB connection
connMongo.close()

