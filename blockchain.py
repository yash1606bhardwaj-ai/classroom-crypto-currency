import hashlib
import datetime
from collections import defaultdict

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = str(datetime.datetime.now())

    def __str__(self):
        return f"{self.timestamp} - {self.sender} -> {self.receiver} : {self.amount} EDU"

    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = str(datetime.datetime.now())
        self.transactions = transactions  # list of Transaction objects
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{[t.__str__() for t in self.transactions]}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
        self.balances = defaultdict(int)

    def create_genesis_block(self):
        genesis_block = Block(0, [], "0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def mine_block(self, receiver, amount=1):
        transaction = Transaction("Teacher", receiver, amount)
        new_block = Block(
            index=len(self.chain),
            transactions=[transaction],
            previous_hash=self.get_last_block().hash
        )
        self.chain.append(new_block)
        self.balances[receiver] += amount

    def transfer(self, sender, receiver, amount):
        if self.balances[sender] < amount:
            raise Exception("Insufficient balance.")
        transaction = Transaction(sender, receiver, amount)
        new_block = Block(
            index=len(self.chain),
            transactions=[transaction],
            previous_hash=self.get_last_block().hash
        )
        self.chain.append(new_block)
        self.balances[sender] -= amount
        self.balances[receiver] += amount

    def get_balance(self, user):
        return self.balances[user]

    def get_leaderboard(self):
        return sorted(self.balances.items(), key=lambda x: x[1], reverse=True)

    def get_transaction_history(self):
        history = []
        for block in self.chain[1:]:  # skip genesis
            for txn in block.transactions:
                history.append(txn)
        return history
