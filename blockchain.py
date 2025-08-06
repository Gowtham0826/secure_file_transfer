<<<<<<< HEAD
import time, hashlib, json

blockchain = []

def create_genesis_block():
    return {'index': 0, 'timestamp': time.time(), 'data': 'Genesis Block', 'prev_hash': '0', 'hash': '0'}

def hash_block(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def add_transaction(file_id, user, timestamp):
    prev_block = blockchain[-1]
    block = {
        'index': len(blockchain),
        'timestamp': timestamp,
        'data': {'file_id': file_id, 'uploaded_by': user},
        'prev_hash': prev_block['hash'],
    }
    block['hash'] = hash_block(block)
    blockchain.append(block)

def initialize_blockchain():
    if not blockchain:
        blockchain.append(create_genesis_block())
=======
import hashlib
import time

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def add_transaction(self, data):
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain), data, prev_block.hash)
        self.chain.append(new_block)
>>>>>>> f5e8ac0294d88315cdd96ef3848a8f42bbf6a9ec
