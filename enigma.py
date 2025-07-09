import json


class Enigma:
    def __init__(self, hash_map, wheels, reflector_map):
        self.hash_map = hash_map
        self.revers_hash_map = {}
        for ch in hash_map:
            number = hash_map[ch]
            self.revers_hash_map[number] = ch
        self.wheels = list(wheels)  # בשביל ליצור עותק
        self.reflector_map = reflector_map
        self.reset_wheels()

    def reset_wheels(self):
        self.w1 = self.wheels[0]
        self.w2 = self.wheels[1]
        self.w3 = self.wheels[2]
        self.coded_chars_counter = 0

    def encrypt_letter(self, ch):
        if ch not in self.hash_map:
            self.advance_wheels()  ## im trying to add
            return ch

        i = self.hash_map[ch]
        checked_val = (2 * self.w1 - self.w2 + self.w3) % 26
        if checked_val != 0:
            i += checked_val
        else:
            i += 1
        i = i % 26

        c1 = self.revers_hash_map[i]
        c2 = self.reflector_map[c1]
        i = self.hash_map[c2]

        # if checked_val != 0:
        #     i -= checked_val
        # else:
        #     i -= 1
        # i = i % 26

## trying to change to:
        if checked_val != 0:
            i = (i - checked_val) % 26
        else:
            i = (i - 1) % 26
##
        c3 = self.revers_hash_map[i]
        self.advance_wheels()
        return c3

    def advance_wheels(self):
        self.w1 += 1
        if self.w1 > 8:
            self.w1 = 1

        self.coded_chars_counter += 1

        if self.coded_chars_counter % 2 == 0:
            self.w2 *= 2
        else:
            self.w2 -= 1

        if self.coded_chars_counter % 10 == 0:
            self.w3 = 10
        elif self.coded_chars_counter % 3 == 0:
            self.w3 = 5
        else:
            self.w3 = 0

    def encrypt(self, message):
        self.reset_wheels()
        return ''.join([self.encrypt_letter(i) for i in message])



class JSONFileException(Exception):
    pass

def load_enigma_from_path(path):
    try:
        with open(path, 'r') as f:
            config = json.load(f)
        return Enigma(config['hash_map'],config['wheels'],config['reflector_map'])
    except Exception:
        raise JSONFileException()


import sys

if __name__ == "__main__":
    args = sys.argv[1:]

    config_path = None
    input_path = None
    output_path = None

    try:
        i = 0
        while i < len(args):
            if args[i] == "-c":
                config_path = args[i + 1]
            elif args[i] == "-o":
                output_path = args[i + 1]
            elif args[i] == "-i":
                input_path = args[i + 1]

            else:
                raise ValueError()
            i += 2

        if config_path is None or input_path is None:
            raise ValueError()

    except Exception:
        print("Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file>", file=sys.stderr)
        exit(1)

    try:
        enigma = load_enigma_from_path(config_path)

        with open(input_path, 'r') as f:
            lines = f.readlines()

        result = []
        for line in lines:
            result.append(enigma.encrypt(line.rstrip('\n')))

        if output_path is not None:
            with open(output_path, 'w') as f:
                for line in result:
                    f.write(line + '\n')
        else:
            for line in result:
                print(line)

    except Exception:
        print("The enigma script has encountered an error", file=sys.stderr)
        exit(1)
