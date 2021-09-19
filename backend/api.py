import requests
import json
import random
from random import randint


QUIT = "('quit' to exit)"
BUY_OR_SELL = "Would you like to browse for products or sell them? Send 'buy' or 'sell'. " + QUIT
SELL_LOCATION = "Please share where you will be selling. LAT, LONG"
BUY_LOCATION = "Please share your location with us. LAT, LONG"
BUY_CATEGORY = "What kind of food are you looking for today?"

SELL_CREATE_MESSAGE = "What are you selling? < 20 characters"

SELL_EDIT = "You have a store associated with that number! Want to delete this store? Y/N"

SELL_PHONE = "What is your phone number? Send your 10 digit phone number."
SELL_CREATE = "We cannot find your number in our system. Please help us create your account by providing the following information. "
SELL_CREATE_CATEGORY = "Please indicate the cateogry of your product below (i.e. 'tacos', 'mangonadas')"
SELL_CREATE_PRODUCTS = "Please indicate specific products you sell or additional items (i.e. 'carne asada', 'sandia') This is optional. To skip, type 'skip'."
state_properties = ["category", "products", "picture", "address", "open?"]
HELP = "We cannot help you. Please make sure you are spelling your response correctly."



class Convo():

    
    def __init__(self, api, phone):
        self.phone = phone
        self.api = api
        self.current_node = BUY_OR_SELL
        self.location = (0, 0)
        self.category = "food"
        self.products = None
    
    def update(self, message):
        if message == "quit":
            self.current_node == BUY_OR_SELL
        
        elif self.current_node == BUY_OR_SELL:
            if message == "buy":
                self.current_node = BUY_LOCATION
            elif message == "sell":
                stores = api.get_my_stores(phone)
                if len(stores) == 0:
                    self.current_node = SELL_LOCATION
                else:
                    self.current_node = SELL_EDIT
        elif self.current_node == SELL_EDIT:
            if message == "Y":
                self.api.delete_store(phone)
                self.current_node = BUY_OR_SELL
                return "Your store was deleted!\n" + BUY_OR_SELL  
            elif message == "N":
                self.current_node = BUY_OR_SELL
        
        elif self.current_node == BUY_LOCATION:
            self.location = message.split(",")
            self.current_node = BUY_CATEGORY
            return BUY_CATEGORY + "\n"+ self.api.get_all_stores_TEXT(self.location)
        
        elif self.current_node == BUY_CATEGORY:
            i = int(message)
            self.current_node = BUY_OR_SELL
            return json.dumps(self.api.stores[i], indent=4) + "\n" + BUY_OR_SELL

        elif self.current_node == SELL_LOCATION:
            self.location = message.split(",")
            self.current_node = SELL_CREATE_MESSAGE
        
        elif self.current_node == SELL_CREATE_MESSAGE:
            self.api.stores.append({"message": message, "phone": self.phone, "location": self.location})
            self.current_node = BUY_OR_SELL

            return "Your store is live! Type 'buy' to see it!"
        
        return self.current_node

def get_distance(origin, stores):
    GOOGLE_KEY = "AIzaSyBfJWN_RlsJaFYolGr2zw4WlevkbDcZw-I"
    origin = ",".join(origin)
    destinations = "|".join([str(store["location"][0])+","+str(store["location"][1]) for store in stores])
    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destinations}&key={GOOGLE_KEY}'
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Request reurned an error  %s : %s" % (response.status_code, response.text))

    parsed = json.loads(response.text)
    return parsed


        

class API():

    def __init__(self):
        self.users = []
        self.conversations = []
        self.stores = [{"message": "tacos", "phone": "9722949822", "location": (42, -72)}, {"message": "pupusas", "phone": "9722949823", "location": (42, -71)}]
    
    
    def add_user(self, phone):
        user = {"phone": phone, "conversation": Convo(self, phone)}
        self.users += [user]
        return user["conversation"].current_node
    
    def get_user(self, phone):
        return [user for user in self.users if user["phone"] == phone][0]
    
    def update(self, phone, message):
        user = self.get_user(phone)
        return user["conversation"].update(message)

    
    def delete_store(self, phone):
        self.stores = [store for store in self.stores if not store['phone'] == phone]

    def get_all_stores_TEXT(self, location):
        res = get_distance(location, self.stores)
        stores = self.stores
        for i, store in enumerate(stores):
            store["address"] = res["destination_addresses"][i]
            store["duration"] = res["rows"][0]['elements'][i]['duration']['text']
            store["distance"] = res["rows"][0]['elements'][i]['duration']['value']
        
        stores.sort(key=lambda x: x["distance"])

        stores_list = ""
        for i, store in enumerate(stores):
            stores_list += "({}) {} - {} \n".format(i, store["message"], store["duration"])
        return stores_list[:-1]

    def get_my_stores_TEXT(self, phone):
        stores = self.get_my_stores(phone)
        stores_list = ""
        for i, store in enumerate(self.stores):
            stores_list += "({}) {} \n".format(i, store["message"])
        return stores_list[:-1]
    
    def get_my_stores(self, phone):
        print()
        return [store for store in self.stores if store["phone"] == phone]
    

if __name__ == "__main__":
    api = API()
    n = 10
    phone = "9722949822"
    reply = api.add_user(phone)
    while(True):
        print(reply)
        message = input()
        if message == 'quit':
            break
        reply = api.update(phone, message)
        
        





    

