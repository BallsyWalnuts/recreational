"""

"""

import json
import hashlib

from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(prev_hash=1, proof=100)

    def new_block(self, proof, prev_hash=None):
        """
        Creates a new block and adds it to the chain

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param prev_hash: (Optional) <str> Hash of previous block
        :return: <dict> New Block
        """

        block = {
            "index": len(self.chain) + 1,
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": prev_hash or self.hash(self.chain[-1]),
        }

        # Reset the list of current transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Adds a new transaction to the list of transactions

        :param sender: <str> Address of the sender
        :param recipient: <str> Address of the recipient
        :param amount: <int> Amount to be transferred
        :return: <int> The index of the  Block that will hold this transaction
        """
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

        return self.last_block["index"] + 1

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm
            - Find a number p' such that hash(pp') contains 4 leading zeroes, where p is the previous p'
            - p is the previous proof, and p' is the new proof

        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof=last_proof, proof=proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?

        :param last_proof: <int> previous proof
        :param proof: <int> current proof
        :return: <bool> True if correct, False if not
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block

        :param block: <dict> block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we will have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """ Returns the last block of the chain

        :return:
        """
        pass


# instantiate our Node
app = Flask(__name__)

# generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=["GET"])
def mine():
    return "We'll mine a new Block"


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    return "We'll add a new transaction"


@app.route("/chain", methods=["GET"])
def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0",  port=5000)
