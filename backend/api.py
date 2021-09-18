import requests
import json
import random


class Convo():
    def __init__(self):
        self.history = []
    
    def update(self, message):
        self.history += [message]

        reply = ""
        if message == "1":
            reply = "you replied 1, you are a seller!"

        if message == "2":
            reply = "you replied 1, you are a buyer!"
            
        self.history += [reply]
        return reply


class API():

    def __init__(self):
        self.sellers = []
        self.buyers = []

    def get_buyer(self, phone):
        return [buyer for buyer in self.buyers if buyer["phone"] == phone][0]
    
    def add_buyer(self, phone):
        self.buyers += [{"phone": phone, "conversation": Convo()}]
    
    def update(self, phone, message):
        buyer = self.get_buyer(phone)
        return buyer["conversation"].update(message)

    def add_seller(self, phone, message, location = None):
        new_seller = {"phone": phone, "message": message, "location": location}
        self.sellers.append(new_seller)
        return {"message": "Your store is up!", "seller": new_seller}

    def get_seller(self, phone):
        return [seller for seller in self.sellers if seller["phone"] == phone][0]
 

if __name__ == "__main__":
    api = API()

    api.add_seller("1", "tacos")
    api.add_seller("2", "pupusas")
    api.add_seller("3", "hotdogs", (10,10))

    print(api.sellers)

    api.add_buyer("4")

    print(api.buyers)

    print(api.update("4", "2"))




    

