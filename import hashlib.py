import hashlib
import pymongo
from pymongo import MongoClient
import json
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from PIL import Image, ImageFont, ImageDraw 
import os

def gen_imagen(hash):

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    my_image = Image.open('test/imagen/PINGO.png')
    title_font = ImageFont.truetype('test/imagen/font/Insominia.ttf', 20)

    title_text = hash
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((0,1900), title_text, (237, 230, 211), font=title_font)
    my_image.save(hash + '.png')



def get_database():
    
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "***REMOVED***"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['Wikipedia']

dbname = get_database()
collection_name = dbname["chuso"]


class GeekCoinBlock:
    
    def __init__(self, previous_block_hash, transaction_list):

        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list
        
        item_1 = {
            "data" : self.transaction_list + self.previous_block_hash
                 }
        self.block_hash = hashlib.sha256(str(item_1).encode()).hexdigest()
        item_1 = {
            "data" : self.transaction_list,
            "prev" :  self.previous_block_hash,
            "_id" : self.block_hash
                 }
        try:
            collection_name.insert(item_1)
            self.imagen(self.block_hash)
            
        except:
            print("error")
    def imagen(self, hash):
        gen_imagen(hash)



class Blockchain:
    def __init__(self):
        self.chain = []
        self.generate_genesis_block()

    def generate_genesis_block(self):
        self.chain.append(GeekCoinBlock("0", "Genesis Block"))
        

    
    def create_block_from_transaction(self, transaction_list):
        previous_block_hash = self.last_block.block_hash
        self.chain.append(GeekCoinBlock(previous_block_hash, transaction_list))
        

    def display_chain(self):
        titles_content_map = []
        cursor = collection_name.find({})
        for document in cursor:
            print(document)
            titles_content_map.append(document)
            
        return titles_content_map
        

    

    @property
    def last_block(self):
        return self.chain[-1]
myblockchain = Blockchain()        

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/api/todos/')
def hello_flask():

    
    results = myblockchain.display_chain()
    
    return json.dumps(results)

@app.route('/users/', methods = ['POST'])
def user():
   
    datos = request.get_json()
    print(datos.get('valor'))
    myblockchain.create_block_from_transaction(datos.get('valor'))
    return("todo bien pa")
    


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)

        



