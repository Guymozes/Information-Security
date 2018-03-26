def patch_program(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    data_list=list(data)
    data_list[0x6de]='\x00'#switch the eax t0 0 in invalid
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
