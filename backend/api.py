import requests
import json
import random
from random import randint

class Convo():
    BUY_OR_SELL = "Would you like to browse for products or sell them? Send 'buy' or 'sell'."
    LOCATION = "Please share your location with us."
    BUY_CATEGORY = "What kind of food are you looking for today? Send one category such as 'tacos' or 'fruta'."
    BUY_LIST = "The following is a list of vendors near you!"
    SELL_PHONE = "What is your phone number? Send your 10 digit phone number."
    SELL_CREATE = "We cannot find your number in our system. " + 
                "Please help us create your account by providing the following information. "
    SELL_CREATE_CATEGORY = "Please indicate the cateogry of your product below (i.e. 'tacos', 'mangonadas')"
    SELL_CREATE_PRODUCTS = "Please indicate specific products you sell or additional items (i.e. 'carne asada', 'sandia') " +
                "This is optional. To skip, type 'skip'."
    state_properties = ["category", "products", "picture", "address", "open?"]
    SELL_EDIT = "You may edit your "

    def __init__(self):
        self.current_node = BUY_OR_SELL


    
    def reset(self):
        self.history = []
        return "buyer (1) or seller (2)"
    
    def update(self, message, api):
        self.history += [message]

        reply = ""
        if message == "1":
            reply = "you are a buyer! here are the stores: \n" + api.get_stores_list()  
        
        if message == "2":
            reply = "you are a seller! what are you selling? \nmessage="

        self.history += [reply]
        return reply


class API():

    def __init__(self):
        self.users = []
        self.conversations = []
        self.stores = [{"message": "tacos"}]
    
    
    def add_user(self, phone):
        user = {"phone": phone, "conversation": Convo()}
        self.users += [user]
        return user["conversation"].reset()
    
    def get_user(self, phone):
        return [user for user in self.users if user["phone"] == phone][0]
    
    def update(self, phone, message):
        user = self.get_user(phone)
        return user["conversation"].update(message, self)

    def add_store(self, phone, message, location = None):
        store = {"phone": phone, "message": message, "location": location}
        self.stores += [store]

    def get_stores_list(self):
        stores = ""
        for i, store in enumerate(self.stores):
            stores += "({}) {} \n".format(i, store["message"])
        return stores
    

if __name__ == "__main__":
    api = API()
    n = 10
    phone = ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])
    reply = api.add_user(phone)
    while(True):
        print(reply)
        message = input()
        reply = api.update(phone, message)
        
        





    

