#!/usr/bin/env python3

def hamming(data) :
    keysizes = [i for i in range(3, 31)]
    chunks = []
    distances = []

    for size in keysizes :
        chunks = [data[i : i + size] for i in range(0, len(data) - size, size)]
        distance = 0
        for parts in range(0, len(chunks) - 1, 2) :
            for first_chunk_char, second_chunk_char in zip(chunks[parts], chunks[parts + 1]) :
            #for first_chunk_char, second_chunk_char in zip(b"this is a test", b"wokka wokka!!!") : <-- Should be equal to 37
                # On met tout sur 8 bits
                bfirst_chunk_char = '0' * (8 - (len(bin(first_chunk_char)) - 2))
                bfirst_chunk_char += bin(first_chunk_char)[2:] 
                bsecond_chunk_char = '0' * (8 - (len(bin(second_chunk_char)) - 2))
                bsecond_chunk_char += bin(second_chunk_char)[2:] 

                for bit1, bit2 in zip(bfirst_chunk_char, bsecond_chunk_char) :
                    distance += (bit1 != bit2)

        distance_moyenne = distance / (len(chunks) // 2)
        distance_moyenne /= size
        distances.append((size, distance_moyenne))

    print(distances)
            
    return sorted(distances, key=distances[0][1]) 

if __name__ == "__main__" :

    data = b""
    try :
        with open("exclusive_key", "rb") as f :
            for line in f.readlines() :
                data += line
    except Exception as e:
        print("except :", e)
    
    hamming_distance = hamming(data)
    print(hamming_distance)
