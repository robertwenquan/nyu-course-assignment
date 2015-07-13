
 * Think about how shadow files work: If user1 and user2 have the same password, why do they show up differently? 
  * shadow file on Linux

 * How can we make a bruteforcers job harder if they had the masterkey?
  This depends on how the masterkey is designed to work with the password manager.

  The way the planitext and encrypted password is calculated and stored is like this:

  random_salt = dynamic_random(16 bytes)
  masterkey = static_random(16 bytes)
  salt = masterkey XOR random_salt
  encrypted_password = ENCRYPTED_METHOD(salt + plaintext)

  The information stored in the password database is like this:
  username, random_salt, enc_method, encrypted_password

  In order to "decrypt" the plaintext password, bruteforcers need to generate a rainbow table for all the usernames in the dictionary with the salts.
But in this case, the salt stored in the password manager is just an intermediate salt which is not directly usable. In order to get the real salt to generate the rainbow table, masterkey must be obtained. 

  When the masterkey is compromised, bruteforcers have a way to combine the master key with our stored intermediate salt to genrate the real salt with the XOR calculation. Then bruteforcers will have the chance to generate his dictionary.

  There are a few factors to affect the difficulties of the bruteforcing: 

  1. Make it harder to figure out how to use the masterkey

   * Write the code in compiled language
    Programming Language like Python, or any other scriting language are readable in source code when it is deployed. But programs written is C, Java, Go will run with binary compiled code which is not human readable.

   * Use more complicate way to incorporate the masterkey

  2. Make it harder to generate the bruteforce rainbow table

