import datetime
import hashlib
import json
import os
from flask import Flask


class Blockchain:

    # This function is created
    # to create the very first
    # block and set its hash to "0"
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
        gen_block = {
                    'index': 0,
                    'timestamp': "2022-12-01 12:00:00.00",
                    'transaction': {
                        'type':"GENESIS BLOCK",
                        'sysname': "Grading System using Blockchain Technology POC",
                        'author': "CARLO VICENTE VILLANOBOS"
                    },
                    'nonce': 0,
                    'hash': 0,
                    'previous_hash': "0"
                }
        mine_gen = self.proof_of_work(gen_block)
        gen_block['nonce'] = mine_gen[0]
        gen_block['hash'] =  mine_gen[1]
        self.chain.append(gen_block)
        json_object = json.dumps(self.chain, indent=4)
        xf = open("gradeschain.json", "w+")
        xf.write(json_object)
        xf.close()
        return gen_block

    # This function is created
    # to add further blocks
    # into the chain

    def add_block(self, ts, data, curr_hash, previous_hash, proof):
        block = {'index': len(self.chain),
                 'timestamp': ts,
                 'transaction': data,
                 'nonce': proof,
                 'previous_hash': previous_hash,
                 'hash': curr_hash
                 }
        if block['index'] != len(self.chain):
            print("Error 1")
            return False
        if block['previous_hash'] != self.hash(self.print_previous_block()):
            print("Error 2")
            return False
        self.chain.append(block)
        json_object = json.dumps(self.chain, indent=4)
        xf = open("gradeschain.json", "w+")
        xf.write(json_object)
        xf.close()
        return block

    # This function is created
    # to display the previous block
    def print_previous_block(self):
        return self.chain[-1]

    

    # This is the function for proof of work
    # and used to successfully mine the block
    def proof_of_work(self, data):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            
            data['nonce'] = new_proof
            xhash = self.gen_hash(new_proof, data)

            if xhash[:4] == '0000' and xhash[4] != '0':
                check_proof = True
            else:
                new_proof += 1

        return new_proof, xhash

    def gen_hash(self, nonce, block):
        x = str(nonce**2)
        y = json.dumps(block, sort_keys=True)
        z = x+y
        hash_c = hashlib.sha256(z.encode()).hexdigest()
        return hash_c
        
    def hash(self, block):
        # set hash to zero first because while we calcuted this blocks hash it's value was zero
        data = block
        dhash = data['hash']
        data['hash'] = 0
        proof = block['nonce']
        bhash = self.gen_hash(proof, data)
        data['hash'] = dhash
        return bhash

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            block_hash = self.hash(previous_block)
            if block['previous_hash'] != block_hash:
                print("Previouse Hash: "+ block['previous_hash'])
                print("Prev Block Hash: "+ block_hash)
                return False


            previous_block = block
            block_index += 1

        return True

    def create_block(self, data):

        previous_block = self.print_previous_block()
        previous_proof = previous_block['nonce']

        ts = str(datetime.datetime.now())
        index = len(self.chain)
        previous_hash = previous_block['hash']

        pending_block = {
            'index': index,
            'timestamp': ts,
            'transaction': data,
            'nonce': 0,
            'hash': 0,
            'previous_hash': previous_hash
        }

        proof = self.proof_of_work(pending_block)
        curr_hash = proof[1]
        block = self.add_block(
            ts, data, curr_hash, previous_hash, proof[0])

        if block is False:
            response = {
                'message': "error"
                }
            return response

        return block

    def show_grades(self, sid):
        chain = self.chain
        index = 1
        grades = []
        while index < len(chain):
            type = chain[index]['transaction']['type']
            
            if type == 'grade':
                stud = chain[index]['transaction']['student']['id']
                if stud == sid:
                    grade = chain[index]['transaction']['grade']
                    subj = chain[index]['transaction']['subject']
                    grades.append({
                        'subject': subj,
                        'grade': grade
                    })

            index += 1

        return grades

