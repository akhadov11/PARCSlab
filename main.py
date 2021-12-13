from Pyro4 import expose


def encrypt(message, key, letter_to_index, index_to_letter, alphabet):
    encrypted = ""
    split_message = [
        message[i: i + len(key)] for i in range(0, len(message), len(key))
    ]

    for each_split in split_message:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] + letter_to_index[key[i]]) % len(alphabet)
            encrypted += index_to_letter[number]
            i += 1

    return encrypted


def decrypt(cipher, key, letter_to_index, index_to_letter, alphabet):
    decrypted = ""
    split_encrypted = [
        cipher[i: i + len(key)] for i in range(0, len(cipher), len(key))
    ]

    for each_split in split_encrypted:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] - letter_to_index[key[i]]) % len(alphabet)
            decrypted += index_to_letter[number]
            i += 1

    return decrypted


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Initialized")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))

        lines = self.read_input().split('\n')

        step = len(lines) // len(self.workers)

        mapped = []
        for i in range(0, len(self.workers)):
            print("map %d" % i)
            mapped.append(self.workers[i].mymap(lines[i * step: (i + 1) * step]))

        res = self.myreduce(mapped)

        self.write_output(res)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(lines):
        res = Solver.process(lines)

        return res

    @staticmethod
    @expose
    def myreduce(mapped):
        output = []

        for result in mapped:
            output += result.value

        return output

    def read_input(self):
        with open(self.input_file_name, 'r') as f:
            data = f.read()
        return data

    def write_output(self, output):
        file = open(self.output_file_name, 'w')
        # file.write(output)
        for lst in output:
            file.write("Original message: ")
            file.write(lst[0])
            file.write('\n')
            file.write("Encrypted message: ")
            file.write(lst[1])
            file.write('\n')
            file.write("Decrypted message: ")
            file.write(lst[2])
            file.write('\n')
            file.write('\n')
            # file.write()
        file.close()
        print("output done")

    @staticmethod
    def process(lines):
        key = "abo"
        alphabet = "abcdefghijklmnopqrstuvwxyz "

        letter_to_index = dict(zip(alphabet, range(len(alphabet))))
        index_to_letter = dict(zip(range(len(alphabet)), alphabet))
        res = []

        for line in lines:
            original_val = line
            encrypted = encrypt(line, key, letter_to_index, index_to_letter, alphabet)
            decrypted = decrypt(encrypted, key, letter_to_index, index_to_letter, alphabet)
            res.append([original_val, encrypted, decrypted])

        return res
