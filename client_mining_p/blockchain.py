import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):

        block = {
            'index': len(self.chain) + 1,
            'proof': proof,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'previous_hash': previous_hash,
        }

        self.current_transactions = []

        self.chain.append(block)

        return block

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True)
        string_in_bytes = block_string.encode()

        hash_object = hashlib.sha256(string_in_bytes)
        hash_string = hash_object.hexdigest()

        return hash_string

    @property
    def last_block(self):
        return self.chain[-1]
    """
    def proof_of_work(self, block):
        block_string = json.dumps(block, sort_keys=True)

        proof = 0
        while self.valid_proof(block_string, proof) is False:
            proof += 1

        return proof
    """

    @ staticmethod
    def valid_proof(block_string, proof):

        guess = f'{block_string}{proof}'.encode()

        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:3] == '000000'

app = Flask(__name__)

node_identifer = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
@app.route('/mine', methods=['POST'])
def mine():
    block = blockchain.last_block
    # proof = blockchain.proof_of_work(block)

    block_hash = blockchain.hash(block)
    new_block = blockchain.new_block(proof, block_hash)
    data = request.get_json()

    response = {
        'message': "hey I found a proof and forged a new block",
        'index': new_block['index'],
        'transactions': new_block['transactions'],
        'proof': new_block['proof'],
        'previous_hash': block_hash,
    }
    return jsonify(response), 200
    return jsonify(response) , 400('message': "youve done messed up now!!")


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'chain_length': len(blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
