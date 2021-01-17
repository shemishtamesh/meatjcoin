from Crypto.Hash import SHA256 #Secure Hash Algorithm (of size) 256 (bits)
from Crypto.PublicKey import ECC #Eliptic Curve Cryptography
from Crypto.Signature import DSS #Digital Stardart Signature
import uuid
from datetime import datetime

def sha256_hash(*args):
    """return a sha256 hash of a concatenation of the input input"""
    str_rep = ""
    for arg in args:
        str_rep += str(arg)
    return SHA256.new(str_rep.encode())


class Transaction:
    def __init__(self,
                 receiver,
                 amount,
                 signature,
                 id = uuid.uuid4(),
                 time = datetime.now()):
        self.id = id
        self.time = time
        self.signature = signature  # signature of the wallet that looses money from the transaction
        self.receiver = receiver
        self.amount = amount
        self.fee = 0

    def is_valid(self):
        """returns true iff the transaction is valid"""
        pass

    def __str__(self):
        return f"id: {self.id}\n"\
              +f"time: {self.time}\n"\
              +f"signature: {self.signature}\n"\
              +f"reveiver: {self.receiver}\n"\
              +f"amount: {self.amount}\n"\
              +f"fee: {self.fee}\n"

class Block:
    def __init__(self,
                 time="0000-00-00 00:00:00.000000",
                 prev_hash=None,
                 data=[],
                 validator=None,
                 signature=None):
        self.time = time
        self.prev_hash = prev_hash
        self.data = data
        self.validator = validator
        self.signature = signature

    def __str__(self):
        return f"created at: {self.time}\n" \
               + f"previous hash: {self.prev_hash}\n" \
               + f"current hash: {self.hash_block()}\n" \
               + f"data: {self.data}\n" \
               + f"validator: {self.validator}\n" \
               + f"signature: {self.signature}\n"

    def hash_block(self):
        """returns the hash of the block"""
        # return sha256_hash(self.time, self.prev_hash, self.data, self.validator, self.signature)
        return sha256_hash(self.time, self.prev_hash, self.data)


class Blockchain:
    def __init__(self):
        self.chain = [Block()]

    def __str__(self):
        ret_str = ""
        for indx, block in enumerate(self.chain):
            ret_str += f"block number: {indx}\n{block}\n"
        return ret_str[:-1]

    def next_block(self, data):
        """creates the next block in the chain, add it to the chain, and return it"""
        time = str(datetime.now())
        prev_hash = self.chain[-1].hash_block()
        block = Block(time, prev_hash, data)
        self.chain.append(block)
        return block

    def replace_chain_if_more_reliable(self, new_chain):
        """replaces the chain if the new chain is longer and valid"""
        if len(new_chain) > len(self.chain) and \
                self.is_chain_valid(new_chain):
            self.chain = new_chain
            return True
        else:
            return False

    def is_valid(self):
        """checks if the chain is valid and returns the result"""
        return self.is_chain_valid(self.chain)

    @staticmethod
    def is_chain_valid(chain):
        """checks if a chain is valid and returns the result"""
        if str(chain[0]) != str(Block()):
            return False
        for i in range(1, len(chain)):
            curr_block = chain[i]
            prev_block = chain[i - 1]
            if curr_block.prev_hash != prev_block.hash_block():
                return False
        return True


class Wallet:
    def __init__(self):
        self.secret_key = ECC.generate(curve='NIST P-256')  # secret key = private key
        self.public_key = self.secret_key.public_key()

    def make_transaction(self, receiver, amount):
        """gets a receiver (public key) and an amount, returns a transaction"""
        id = uuid.uuid4()
        time = datetime.now()
        fee = 0 #TODO: change this
        transaction_hash = sha256_hash(id, time, receiver, amount, fee)
        signer = DSS.new(self.secret_key, 'fips-186-3')
        signature = signer.sign(transaction_hash)
        return Transaction(receiver, amount, signature, id, time)


def main():
    w1 = Wallet()
    print(w1.make_transaction("demo_receiver", 100))

if __name__ == "__main__":
    main()