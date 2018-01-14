"""

"""

import flask
import requests
import json
import hashlib


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