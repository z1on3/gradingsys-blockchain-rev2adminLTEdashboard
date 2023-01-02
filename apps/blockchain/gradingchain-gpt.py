from collections import namedtuple
import datetime
import hashlib
import json
import os
#optimize code from chatgpt
Block = namedtuple('Block', ['index', 'timestamp', 'transaction', 'nonce', 'previous_hash', 'hash'])

class Blockchain:
    def __init__(self):
        gcf = "gradeschain.json"

        if (os.path.exists(gcf)):
            cf = open(gcf, "r")
            self.chain = json.load(cf)
            cf.close()
        else:
            self.chain = []
            self.create_genblock()

    def create_genblock(self):
        gen_block = Block(
            index=0,
            timestamp="2022-12-01 12:00:00.00",
            transaction={
                'type': "GENESIS BLOCK",
                'sysname': "Grading System using Blockchain Technology POC",
                'author': "CARLO VICENTE VILLANOBOS"
            },
            nonce=0,
            hash=0,
            previous_hash="0"
        )
        mine_gen = self.proof_of_work(gen_block)
        nonce = mine_gen[0]
        genhash = mine_gen[1]
        gen_block = gen_block._replace(nonce=nonce, hash=genhash)
        self.chain.append(gen_block)
        json_object = json.dumps(self.chain, indent=4)
        xf = open("gradeschain.json", "w+")
        xf.write(json_object)
        xf.close()
        return gen_block

    def add_block(self, ts, data, curr_hash, previous_hash, proof):
        block = Block(
            index=len(self.chain),
            timestamp=ts,
            transaction=data,
            nonce=proof,
            previous_hash=previous_hash,
            hash=curr_hash
        )
        if block.index != len(self.chain):
            print("Error 1")
            return False
        if block.previous_hash != self.hash(self.print_previous_block()):
            print("Error 2")
            return False
        self.chain.append(block)
        json_object = json.dumps(self.chain, indent=4)
        file = open("gradeschain.json", "w+")
        file.write(json_object)
        file.close()
        return block

    def print_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, data):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            x = str(new_proof**2)
            data = data._replace(nonce=new_proof)
            y = json.dumps(data, sort_keys=True)
            z = x+y
            hash_operation = hashlib.sha256(z.encode()).hexdigest()
            if hash_operation[:4] == '0000' and hash_operation[4] != '0':
                check_proof = True
            else:
                new_proof += 1

        return new_proof, hash_operation

    def hash(self, block):
        data = block._replace(hash=0)
        proof = block.nonce
        x = str(proof**2)
        y = json.dumps(data, sort_keys=True)
        z = x+y
        return hashlib.sha256(z.encode()).hexdigest()

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]

            if block.previous_hash != self.hash(previous_block):
                return False

            proof = block.nonce
            x = str(proof**2)
            y = json.dumps(block, sort_keys=True)
            z = x+y
            hash_operation = hashlib.sha256(z.encode()).hexdigest()

            if hash_operation[:4] != '0000':
                return False

            previous_block = block
            block_index += 1

        return True

                