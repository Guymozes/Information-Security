def check_message(path):
	try:
		fd=open(path,"r")
	except IOError:
		print("Error: can't open the file")
		sys.exit(1)
	try:
		buf=fd.read()
	except IOError:
		print("Error: can't read the file")
		sys.exit(1)
	length_buf=len(buf)
	fd.close()
	if(length_buf<2):
		return False
	calc_xor=0x64
	for ch in range(2,ord(buf[0])+2):
		if(length_buf<=ch):
			break
		calc_xor=calc_xor^(ord(buf[ch]))
	if(calc_xor==ord(buf[1])):
		return True
	return False


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <msg-file>'.format(argv[0]))
        return -1
    path = argv[1]
    if check_message(path):
        print('valid message')
        return 0
    else:
        print('invalid message')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
