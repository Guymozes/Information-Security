import assemble
def patch_program(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    data_list=list(data)
    first_patch=assemble.assemble_file("patch1.asm")
    second_patch=assemble.assemble_file("patch2.asm")
    for i in range(len(first_patch)):
        data_list[i+0x635]=first_patch[i]
    for i in range(len(second_patch)):
        data_list[i+0x5CD]=second_patch[i]
    data="".join(data_list)    
    with open(path + '.patched', 'wb') as writer:
        writer.write(data)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <readfile-program>'.format(argv[0]))
        return -1
    path = argv[1]
    patch_program(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
