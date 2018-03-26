from itertools import *
import collections
class RepeatedKeyCipher(object):

    def __init__(self, key=[0, 0, 0, 0, 0]):
        """Initializes the object with a list of integers between 0 and 255."""
        assert all(0 <= k <= 255 and isinstance(k, (int, long)) for k in key)
        self.key = key

    def encrypt(self, plaintext):
    	text_list=list(plaintext)
    	length=len(text_list)
    	for i in range(length):
    		text_list[i]=chr(ord(text_list[i])^(self.key[i%len(self.key)]))
    	encrypted_text="".join(text_list)
    	return encrypted_text

    def decrypt(self, ciphertext):
		return self.encrypt(ciphertext)

class BreakerAssistant(object):

    def plaintext_score(self, plaintext):
    	score=0
    	char_list=list(plaintext)
    	for ch in char_list:
    		if(ord(ch)>96 and ord(ch)<123):
    			score+=6
        return score

    def brute_force(self, cipher_text, key_length):
   		correct_plain_text=""
   		max_score=0
   		ch_range=range(256)
   		temp_score=0
   		for item in product(ch_range,repeat=key_length):
   			temp=RepeatedKeyCipher(item)
   			dec_text=temp.decrypt(cipher_text)
   			temp_score=self.plaintext_score(dec_text)
   			if(temp_score>max_score):
   				correct_plain_text=dec_text
   				max_score=temp_score
   		return correct_plain_text

    def smarter_break(self, cipher_text, key_length):
        rep=RepeatedKeyCipher()
        letter_arr=[' ','e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z']
        text_list=list(cipher_text)
        keys=[0]*key_length
        for i in range(key_length):
          max_score=0
          temp_text=list(text_list[i:len(text_list):key_length])
          count_obj=collections.Counter(temp_text)
          max_freq_char,count_freq=count_obj.most_common(1)[0]
          for j in range(len(letter_arr)):
            rep.key=[ord(max_freq_char)^ord(letter_arr[j])]
            current_subtext=rep.decrypt("".join(temp_text))
            temp_score=self.plaintext_score(current_subtext)
            if(temp_score>max_score):
              max_score=temp_score
              keys[i]=rep.key[0]
        rep.key=keys
        return rep.decrypt(cipher_text)
