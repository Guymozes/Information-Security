def patch_program(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    data_list=list(data)
    data_list[0x6c9]='\x39'#switch the test opcode from 85 to 39 - CMP op
    data_list[0x6cB]='\x74'#switch the jnz op to JZ op -> from 75 to 74
    data="".join(data_list)
    with open(path + '.patched', 'wb') as writer:
        writer.write(data)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <msgcheck-program>'.format(argv[0]))
        return -1
    path = argv[1]
    patch_program(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
