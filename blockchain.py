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
