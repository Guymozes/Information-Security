from q2_atm import ATM, ServerResponse,RSA
import math

def extract_PIN(encrypted_PIN):
	item=ATM()
	for i in range(10000):
		if(item.encrypt_PIN(i)==encrypted_PIN):
			return i

def extract_credit_card(encrypted_credit_card):
	return int(round(math.pow(encrypted_credit_card,1/float(3))))

def forge_signature():
    temp=ServerResponse(ATM.CODE_APPROVAL,1)
    return temp
