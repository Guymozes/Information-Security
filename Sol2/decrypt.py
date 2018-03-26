import os
import sys


def main(argv):
    if len(argv) != 2 or '--help' in argv:
        print('Usage: python %s [1d | 1e | 2a | 2b]' % (argv[0] if argv else __file__))
        return

    ex = argv[1].lower()
    curr_dir = os.path.dirname(__file__)

    if ex == '1d':
        with open('q1d.cipher', 'rb') as f:
            cipher = f.read()
        import q1
        print(repr(q1.BreakerAssistant().brute_force(cipher, 2)))
    elif ex == '1e':
        with open('q1e.cipher', 'rb') as f:
            cipher = f.read()
        import q1
        print(repr(q1.BreakerAssistant().smarter_break(cipher, 16)))
    elif ex == '2a':
        with open('q2a-pin.txt', 'rb') as f:
            pin = int(f.read())
        import q2
        print(repr(q2.extract_PIN(pin)))
    elif ex == '2b':
        with open('q2b-card.txt', 'rb') as f:
            card = int(f.read())
        import q2
        print(repr(q2.extract_credit_card(card)))
    else:
        print('Unknown exercise %s' % ex)


if __name__ == '__main__':
    main(sys.argv)
