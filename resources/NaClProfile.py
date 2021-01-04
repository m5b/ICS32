# TODO: Install the pynacl library so that the following modules are available
# to your program.
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box

# TODO: Import the Profile and Post classes
# TODO: Import the NaClDSEncoder module

    
# TODO: Subclass the Profile class
class NaClProfile:
    """
    TODO: Complete the initializer method. Your initializer should create the follow three 
    public data attributes:

    public_key:str
    private_key:str
    keypair:str

    Whether you include them in your parameter list is up to you. Your decision will frame 
    how you expect your class to be used though, so think it through.
    """
    def __init__():
        pass

    """
    TODO: Complete the generate_keypair method.

    This method should use the NaClDSEncoder module to generate a new keypair and populate
    the public data attributes created in the initializer.

    returns keypair:str    
    """
    def generate_keypair(self) -> str:
        pass

    """
    TODO: Complete the import_keypair method.

    This method should use the keypair parameter to populate the public data attributes created by
    the initializer. 
    
    NOTE: you can determine how to split a keypair by comparing the associated data attributes generated
    by the NaClDSEncoder
    """
    def import_keypair(self, keypair: str):
        pass

    """
    TODO: Override the add_post method to encrypt post entries.

    Before a post is added to the profile, it should be encrypted. Remember to take advantage of the
    code that is already written in the parent class.

    NOTE: To call the method you are overriding from the parent class you can use the built-in super:
    super().add_post(...)
    """

    """
    TODO: Override the get_posts method to decrypt post entries.

    Since posts will be encrypted when the add_post method is used, you will need to ensure they are 
    decrypted before returning them to the calling code.

    returns Posts:list
    
    NOTE: To call the method you are overriding from the parent class you can use the built-in super:
    super().get_posts()
    """

    """
    TODO: Complete the encrypte_entry method.
    This method will be used to encrypt messages using a 3rd party public key, such as the one that
    the DS server provides.
    
    returns encrypted_message:bytes 
    """
    def encrypt_entry(self, entry:str, public_key:str) -> str:
        pass