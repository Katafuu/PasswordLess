import math

class PyAvalanche:
    '''
        Create avalance effect for cryptograph testing
        ref : https://www.researchgate.net/post/What_is_the_avalanche_effect_in_cryptography_How_can_we_measure_it
              https://www.educative.io/answers/how-to-convert-string-to-binary-in-python
    '''
    # constructor
    def __init__(self):
        pass

    def str_to_binary(self, a):
        l,m=[],[]
        for i in a:
            l.append(ord(i))

        for i in l:
            m.append(int(bin(i)[2:]))

        return m

    def binary_to_str(self, a):
        l=[]
        m=""
        for i in a:
            b=0
            c=0
            k=int(math.log10(i))+1
            for j in range(k):
                b=((i%10)*(2**j))   
                i=i//10
                c=c+b
            l.append(c)

        for x in l:
            m=m+chr(x)

        return m

    def avalanche_effect(self, chipper1, chipper2):
        '''
            chipper1 and chipper2 in string
        '''
        a = self.str_to_binary(chipper1)
        b = self.str_to_binary(chipper2)

        a = int(''.join([str(i) for i in a]))
        b = int(''.join([str(i) for i in b]))

        # print ('chipper a =',a)
        # print ('chipper b =',b)

        # print bitwise XOR operation
        a_xor_b = a^b
        # print("a ^ b =", a_xor_b)

        # Base 2(binary)
        bin_a_xor_b = bin(a_xor_b)
        # print("the result in decimal =", bin_a_xor_b)

        # next steps to count 1s in binary number
        one_count = 0
        for i in bin_a_xor_b:
            if i == "1":
                one_count+=1
        # print ("the 1s numbers is=", one_count)

        # next steps to calculate equation of avalanche effect
        len_a = len(bin(a))
        len_b = len(bin(b))
        # print(len_a, len_b)

        # if to ensure divide by the longest binary string
        if (len_a) >= (len_b):
            AVA = (one_count/ len_a) * 100
        else:
            AVA = (one_count/ len_b) * 100

        # print ("avalanche effect =", AVA, "%")

        return AVA


# test module level
if __name__=='__main__':
    '''
        Chipper1 is result from any encryption, first run
        Chipper2 is result from same encryption, second run
    '''
    chipper1 = 'Nk9iL05BQmM5bnRES3drVGc0NHZRdz09'
    chipper2 = 'Z3VFbi9lWDJtS1B5UzE4TGVsMzRHQT09'
    print('Chipper 1 = ', chipper1)
    print('Chipper 2 = ', chipper2)
    ava = PyAvalanche()
    result = ava.avalanche_effect(chipper1, chipper2)

    print(result,'%')
    print("If more than 50% output bits have changed then the algo have good avalanche effect.")