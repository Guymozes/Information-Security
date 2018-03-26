import os

import infosec.utils


def error(message):
    print('\x1b[31m{}\x1b[0m'.format(message))


def check_if_compiles(source_path):
    exit_code, stdout, stderr = infosec.utils.execute('gcc -masm=intel %s -o /dev/null' % source_path)
    if exit_code != 0:
        error('ERROR: %s does not compile:\n%s' % (source_path, stderr))
        return False
    return True


def check_if_nonempty(path):
    with open(path) as reader:
        data = reader.read().strip()
    if not data:
        error('ERROR: %s is empty' % path)
        return False
    return True


def check_fibonacci(source_path):
    try:
        with infosec.utils.temporary_directory() as temporary_directory_path:
            target_path = os.path.join(temporary_directory_path, 'q2')
            exit_code, stdout, stderr = infosec.utils.execute('gcc -masm=intel %s -o %s' % (source_path, target_path))
            a0 = int(infosec.utils.execute('%s 0' % target_path).stdout)
            a1 = int(infosec.utils.execute('%s 1' % target_path).stdout)
            if a0 != 0 or a1 != 1:
                error('ERROR: Fibonacci sequence should begin with 0, 1, ..., not with %s, %s, ...' % (a0, a1))
                return False
            return True
    except Exception:
        return False


def smoketest():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if all([
        check_if_compiles('q1.c'),
        check_if_compiles('q2a.c'),
        check_if_compiles('q2b.c'),
        check_if_nonempty('q3.txt'),
        check_fibonacci('q2a.c'),
        check_fibonacci('q2b.c'),
    ]):
        print('smoketest seems cool')


if __name__ == '__main__':
    smoketest()
