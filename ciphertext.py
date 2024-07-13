import random
import string
import numpy as np

# Caesar Cipher
def caesar_cipher(plaintext, shift):
    ciphertext = ''
    for char in plaintext:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            ciphertext += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            ciphertext += char
    return ciphertext

# Monoalphabetic Cipher
def monoalphabetic_cipher(plaintext, keyword):
    alphabet = string.ascii_lowercase
    shuffled = ''.join(random.sample(alphabet, len(alphabet)))
    table = str.maketrans(alphabet, shuffled)
    return plaintext.translate(table)

# Polyalphabetic Substitution Cipher
def polyalphabetic_cipher(plaintext, keyword):
    keyword_repeated = (keyword * (len(plaintext) // len(keyword))) + keyword[:len(plaintext) % len(keyword)]
    ciphertext = ''
    for p, k in zip(plaintext, keyword_repeated):
        if p.isalpha():
            shift_base = ord('A') if p.isupper() else ord('a')
            k = k.upper() if p.isupper() else k.lower()
            ciphertext += chr((ord(p) - shift_base + ord(k) - shift_base) % 26 + shift_base)
        else:
            ciphertext += p
    return ciphertext

# Homophonic Substitution Cipher
def homophonic_substitution_cipher(plaintext, keyword):
    alphabet = string.ascii_lowercase
    sub_dict = {char: random.choice(keyword) for char in alphabet}
    ciphertext = ''.join(sub_dict.get(char, char) for char in plaintext)
    return ciphertext

# Polygram Substitution Cipher
def polygram_substitution_cipher(plaintext, keyword):
    # Simple polygram substitution where plaintext is divided into blocks
    block_size = len(keyword)
    blocks = [plaintext[i:i + block_size] for i in range(0, len(plaintext), block_size)]
    cipher_dict = {block: keyword[i % block_size] for i, block in enumerate(blocks)}
    ciphertext = ''.join(cipher_dict.get(block, block) for block in blocks)
    return ciphertext

# Playfair Cipher
def playfair_cipher(plaintext, keyword):
    def generate_playfair_matrix(keyword):
        keyword = "".join(dict.fromkeys(keyword.upper().replace("J", "I")))
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix = [char for char in keyword + "".join(c for c in alphabet if c not in keyword)]
        return [matrix[i:i + 5] for i in range(0, 25, 5)]

    def find_position(matrix, char):
        for i, row in enumerate(matrix):
            if char in row:
                return i, row.index(char)
        return None

    def playfair_encrypt_pair(matrix, a, b):
        if a == b:
            b = 'X'
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        if row1 == row2:
            return matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            return matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            return matrix[row1][col2] + matrix[row2][col1]

    matrix = generate_playfair_matrix(keyword)
    plaintext_pairs = [plaintext[i:i + 2] for i in range(0, len(plaintext), 2)]
    ciphertext = ''.join(playfair_encrypt_pair(matrix, pair[0], pair[1] if len(pair) > 1 else 'X') for pair in plaintext_pairs)
    return ciphertext

# Hill Cipher
def hill_cipher(plaintext, keyword):
    def create_matrix(keyword):
        return np.array([[ord(char) - ord('A') for char in keyword[i:i + 2]] for i in range(0, len(keyword), 2)])

    def text_to_vector(text):
        return np.array([[ord(char) - ord('A')] for char in text])

    def vector_to_text(vector):
        return ''.join(chr(int(val) + ord('A')) for val in vector)

    keyword_matrix = create_matrix(keyword)
    plaintext_vector = text_to_vector(plaintext)
    ciphertext_vector = np.dot(keyword_matrix, plaintext_vector) % 26
    return vector_to_text(ciphertext_vector)

def get_ciphertext(plaintext, keyword, cipher_type):
    if cipher_type == 'Caesar Cipher':
        shift = int(keyword) if keyword.isdigit() else 3  # Default shift is 3
        return caesar_cipher(plaintext, shift)
    elif cipher_type == 'Monoalphabetic Cipher':
        return monoalphabetic_cipher(plaintext, keyword)
    elif cipher_type == 'Homophonic Substitution Cipher':
        return homophonic_substitution_cipher(plaintext, keyword)
    elif cipher_type == 'Polygram Substitution Cipher':
        return polygram_substitution_cipher(plaintext, keyword)
    elif cipher_type == 'Polyalphabetic Substitution Cipher':
        return polyalphabetic_cipher(plaintext, keyword)
    elif cipher_type == 'Playfair Cipher':
        return playfair_cipher(plaintext, keyword)
    elif cipher_type == 'Hill Cipher':
        return hill_cipher(plaintext, keyword)
    else:
        return "Cipher type not implemented."

def main():
    plaintext = input("Enter the plaintext: ").upper()
    keyword = input("Enter the keyword (for Caesar Cipher, enter shift value): ").upper()
    print("Select the type of cipher:")
    print("1. Caesar Cipher")
    print("2. Monoalphabetic Cipher")
    print("3. Homophonic Substitution Cipher")
    print("4. Polygram Substitution Cipher")
    print("5. Polyalphabetic Substitution Cipher")
    print("6. Playfair Cipher")
    print("7. Hill Cipher")
    
    cipher_choice = int(input("Enter the number corresponding to the cipher type: "))
    
    cipher_types = {
        1: 'Caesar Cipher',
        2: 'Monoalphabetic Cipher',
        3: 'Homophonic Substitution Cipher',
        4: 'Polygram Substitution Cipher',
        5: 'Polyalphabetic Substitution Cipher',
        6: 'Playfair Cipher',
        7: 'Hill Cipher'
    }
    
    cipher_type = cipher_types.get(cipher_choice, "Invalid choice")
    if cipher_type == "Invalid choice":
        print("Invalid choice. Exiting.")
        return
    
    ciphertext = get_ciphertext(plaintext, keyword, cipher_type)
    print(f"The ciphertext using {cipher_type} is: {ciphertext}")

if __name__ == "__main__":
    main()
