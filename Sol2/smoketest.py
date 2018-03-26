import os
import numbers
import signal
import traceback
import sys

from q2_atm import ATM, ServerResponse
import infosec.utils


# Keep imported modules alive, to avoid nasty bugs when they go out of scope.
IMPORTED_MODULES = set()


def import_module(module_path):
    module = infosec.utils.import_module(module_path)
    IMPORTED_MODULES.add(module)
    return module


def error(message, *args, **kwargs):
    if args or kwargs:
        message = message.format(*args, **kwargs)
    print('\x1b[31mERROR: {}\x1b[0m'.format(message))


def warning(message, *args, **kwargs):
    if args or kwargs:
        message = message.format(*args, **kwargs)
    print('\x1b[31mWARNING: {}\x1b[0m'.format(message))


def check_decryption(module_path, function_name, what, encrypted_value, expected_type):
    try:
        module = import_module(module_path)
        function = getattr(module, function_name)
        decrypted_value = function(encrypted_value)
    except Exception as e:
        error('Exception decrypting {} using {}', what, module_path)
        traceback.print_exc()
        return False, None

    if not isinstance(decrypted_value, expected_type):
       error('{} should generate output of type {}, actual type was {}',
             function_name, expected_type, type(decrypted_value))
       return False, decrypted_value

    return True, decrypted_value


def check_extraction(module_path, function_name, what, value, encryption_func, expected_type):
    encrypted_val = encryption_func(value)
    valid_decryption, decrypted_value = check_decryption(module_path, function_name, what, encrypted_val, expected_type)

    if not valid_decryption:
        return False

    if decrypted_value != value:
        error('Decryption of {} doesn\'t work for {} - result was {}', what, value, decrypted_value)
        return False

    return True


class TimeoutError(Exception):
    pass


# Tested
def timed_run(num_secs, action, error_message, *args, **kwargs):
    def signal_handler(signum, frame):
        error(error_message, *args, **kwargs)
        raise TimeoutError()

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(num_secs)
    try:
        result = action()
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        done = True
    except TimeoutError:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        done = False
        result = None

    return done, result


def get_from_module(module_path, name):
    try:
        module = import_module(module_path)
        return True, getattr(module, name)
    except Exception as e:
        error('Exception importing {} from {}', name, module_path)
        traceback.print_exc()
        return False, None


def get_cipher(module_path, str_key):
    import_ok, RKC = get_from_module(module_path, 'RepeatedKeyCipher')
    if not import_ok:
        return None
    return RKC([ord(c) for c in str_key])


def get_breaker(module_path):
    import_ok, BA = get_from_module(module_path, 'BreakerAssistant')
    if not import_ok:
        return None
    return BA()


def check_q1a(module_path):
    cipher = get_cipher(module_path, 'abc')
    if cipher is None:
        return

    try:
        encrypted = cipher.encrypt('abcab')
    except Exception as e:
        error('Exception encrypting with {}', module_path)
        traceback.print_exc()
        return False

    if not isinstance(encrypted, str):
        error('Encryption with {} doesn\'t return a string, it returns a {}',
              module_path, type(encrypted))
        return False

    if encrypted != ('\x00' * 5):
        error('Encryption doesn\'t seem right with {}', module_path)
        return False

    return True


def check_q1b(module_path):
    cipher = get_cipher(module_path, 'abc')
    if cipher is None:
        return

    try:
        decrypted = cipher.decrypt(')+CUP')
    except Exception as e:
        error('Exception decrypting with {}', module_path)
        traceback.print_exc()
        return False

    if not isinstance(decrypted, str):
        error('Decryption with {} doesn\'t return a string, it returns a {}',
              module_path, type(encrypted))
        return False

    if decrypted != 'HI 42':
        error('Decryption doesn\'t seem right with {}', module_path)
        return False

    return True


def check_q1c(module_path):
    breaker = get_breaker(module_path)
    if breaker is None:
        return

    S1, S2 = '1A\xfe~\xf6', 'Hello'
    try:
        score1 = breaker.plaintext_score(S1)
        score2 = breaker.plaintext_score(S2)
    except:
        error('Error computing plaintext scores with {}', module_path)
        traceback.print_exc()
        return False

    for s in [score1, score2]:
        if not isinstance(s, numbers.Number):
            error('Generated score by {} is {} (not a number!)',
                  module_path, type(s))

    if score1 >= score2:
        warning('The score of {} is higher than the score of {}. While'
              'not strictly an error, this is probably bad', repr(S1), repr(S2))
        return False

    return True


def check_q1d(module_path):
    breaker = get_breaker(module_path)
    if breaker is None:
        return

    try:
        result = breaker.brute_force('\x01\x02\x03\x04\x05', 2)
    except:
        error('Error brute forcing cipher text with {}', module_path)
        traceback.print_exc()
        return False

    if not isinstance(result, str):
        error('Brute forcing with {} doesn\'t return a string, it returns a {}',
              module_path, type(result))
        return False

    return True


def check_q1e(module_path):
    breaker = get_breaker(module_path)
    if breaker is None:
        return

    try:
        done, result = timed_run(
            10, lambda: breaker.smarter_break('a' * 32, 16),
            'Smart break with {} timed out (10 seconds)', module_path)
        if not done:
            return False
    except:
        error('Error smart breaking cipher text with {}', module_path)
        traceback.print_exc()
        return False

    if not isinstance(result, str):
        error('Smart breaking with {} doesn\'t return a string, it returns a {}',
              module_path, type(result))
        return False

    return True


def check_q2a(module_path):
    return check_extraction(
        module_path, 'extract_PIN', 'PIN', 1234,
        ATM().encrypt_PIN, (int, long)
    )


def check_q2b(module_path):
    return check_extraction(
        module_path, 'extract_credit_card', 'credit card', 123456789,
        ATM().encrypt_credit_card, (int, long)
    )


def check_q2c(module_path):
    try:
        module = import_module(module_path)
        signature = module.forge_signature()
    except Exception as e:
        error('Exception forging a signature with {}', module_path)
        traceback.print_exc()
        return False

    if not isinstance(signature, ServerResponse):
        error('Signature should be a ServerResponse but is a {}',
              type(signature))
        return False

    try:
        if not ATM().verify_server_approval(signature):
            error('Verification does not pass with signature from {}',
                  module_path)
    except Exception as e:
        error('Exception while running the verification on response from {}',
             module_path)
        traceback.print_exc()
        return False

    return True


def check_if_nonempty(path):
    if not os.path.exists(path):
        error('{} does not exist', path)
        return False
    with open(path) as reader:
        data = reader.read().strip()
    if not data:
        error('{} is empty', path)
        return False
    return True


def smoketest():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if all([
        check_q1a('q1.py'),
        check_q1b('q1.py'),
        check_q1c('q1.py'),
        check_if_nonempty('q1c.txt'),
        check_q1d('q1.py'),
        check_if_nonempty('q1d.txt'),
        check_q1e('q1.py'),
        check_if_nonempty('q1e.txt'),
        check_q2a('q2.py'),
        check_if_nonempty('q2a.txt'),
        check_q2b('q2.py'),
        check_if_nonempty('q2b.txt'),
        check_q2c('q2.py'),
        check_if_nonempty('q2c.txt'),
    ]):
        print('smoketest seems cool')


if __name__ == '__main__':
    smoketest()
