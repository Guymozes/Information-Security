from Crypto.PublicKey import RSA


RSA_PUB_KEY_PIN = RSA.construct((
    # The `n` (modulo) parameter of RSA
    27868931716406380266023588788595709220783271412985725540589503336924335542212836988982790514803413526015395328609052090335839908222282076994940999271040944363058671718331250495389404607367689795561010211924952853432663395032855163818744014456635712279205955773051961167411084853243797540503847024626281064705492826921060618543819621856845100073026477384943096726108770125307933031546925847050585277725348485093744031760263105174434327539528418963473167597399668722233005080296686398421177238362217974996710481201702847205681870170911688958925154041074456550350784804415246077155398147059279589925057100907388222444889L,
    # The `e` (encryption exponent) parameter of RSA
    65537L
))

RSA_PUB_KEY_CARD = RSA.construct((
    # The `n` (modulo) parameter of RSA
    20376884753862275049094180325999569637889182591503729556310621938891776624033788403381733002838516760705828996630570428864849157008695430399492390606333948958611189945019180627086784331308471047803847934316836294301743776169677009776783907483881472479526163954480862341056957817833281709466757243680421537507690984023803519504205700529295684578363546945266113418989997700473707725059357314480282167327113310196038934448754327599496136847796080537641682081674616137036333668342963544030776695183529528224815426819452929269011526039861488573032580092506809347235154888750743007800649440263005956973175500718846666937653L,
    # The `e` (encryption exponent) parameter of RSA
    3L
))


class ATM(object):

    def __init__(self):
        """Initializes the ATM parameters."""
        self.rsa_card = RSA_PUB_KEY_CARD
        self.rsa_pin = RSA_PUB_KEY_PIN

    def is_number_of_max_digits(self, number, max_digits):
        """Check if a number is whole, positive, and has at most the specified number of digits."""
        return isinstance(number, (int, long)) and 0 <= number < (10 ** max_digits)

    def encrypt_number(self, rsa_key, number):
        """Encrypt a numeric value using the specified RSA key."""
        return rsa_key.encrypt(number, None)[0]

    def encrypt_credit_card(self, card_number):
        """Encrypt a credit card number for sending to the server."""
        assert self.is_number_of_max_digits(card_number, 9)
        return self.encrypt_number(self.rsa_card, card_number)

    def encrypt_PIN(self, PIN):
        """Encrypt a PIN for sending to the server."""
        assert self.is_number_of_max_digits(PIN, 4)
        return self.encrypt_number(self.rsa_pin, PIN)

    CODE_NO_RESPONSE = 0L
    CODE_APPROVAL = 1L
    CODE_CARD_NOT_FOUND = 2L
    CODE_PIN_CARD_MISMATCH = 3L
    CODE_ILLEGAL_LENGTH = 4L
    CODE_ILLEGAL_CHARACTER = 5L
    CODE_DO_NOT_ACCEPT_BITCOIN = 6L
    CODE_CARD_REJECTED = 7L
    CODE_CARD_BLOCKED = 8L
    CODE_SERVER_ERROR = 9L
    CODE_SERVER_OVERLOAD = 10L

    def verify_server_approval(self, server_response):
        """Returns True if the server returned a correctly signed approval."""
        return (server_response.status == ATM.CODE_APPROVAL and
                self.rsa_card.verify(server_response.status,
                                     (server_response.signature,)))


class ServerResponse(object):

    def __init__(self, status, signature):
        """Initializes a response with a value for the status and signature."""
        self.status = status
        self.signature = signature

