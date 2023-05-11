from des import DesKey

class DiffieHellman:
  def __init__(self, key):
    self.key= DesKey(key)

  def encryption(self, message):
    encrypted_msg= self.key.encrypt(str(message).encode(), padding = True)
    return encrypted_msg
   
  def decryption(self, message):
    decrypted_msg= self.key.decrypt(message, padding = True)
    return decrypted_msg