from pymongo import MongoClient

class Database:
    _instance = None

    @staticmethod
    def get_instance():
        if Database._instance is None:
            client = MongoClient("mongodb+srv://prashant:KzQttrqrnCAN1h10@invoice.ewrmw.mongodb.net/?retryWrites=true&w=majority&appName=Invoice")
            Database._instance = client
        return Database._instance
