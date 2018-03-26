def fix_message(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    data+=chr(0x20)*0x100
    data+='\0'
    list_data=list(data)
    length_data=len(data)
    calc_xor=0x64
    for i in range(2,ord(data[0])+2):
        calc_xor=calc_xor^(ord(list_data[i]))
    list_data[1]=chr(calc_xor)
    data="".join(list_data)    
    with open(path + '.fixed', 'wb') as writer:
        writer.write(data)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <msg-file>'.format(argv[0]))
        return -1
    path = argv[1]
    fix_message(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))