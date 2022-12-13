import gradingchain as gc

bc = gc.Blockchain()

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

#print(bc.proof_of_work(gen_block))s

grades = bc.show_grades("STUD-00001")
print(len(grades))
print(grades["name"])

for x in range(len(grades)):
    print(x)