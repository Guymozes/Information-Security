#!/usr/bin/python

import infosec.utils


ASSEMBLY_TEMPLATE = '''
.intel_syntax noprefix
.globl main
main:
{data}
'''

ASSEMBLE = 'gcc -xassembler - -o /dev/stdout -m32 -nostdlib -emain -Xlinker --oformat=binary'


def assemble_data(data):
    return infosec.utils.execute(ASSEMBLE, ASSEMBLY_TEMPLATE.format(data=data), raise_error=True).stdout
    

def assemble_file(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    return assemble_data(data)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <asm-file>'.format(argv[0]))
        return -1
    path = argv[1]
    print(repr(assemble_file(path)))


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
