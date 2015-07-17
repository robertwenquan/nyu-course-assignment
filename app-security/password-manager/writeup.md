
### Think about how shadow files work: If user1 and user2 have the same password, why do they show up differently? 

 * shadow file on Linux uses salt to prevent the situation described above.
 * Salt is a random string that is appended to the original plaintext password.
 * Then the combined string will be hashed to another string that is stored in the shadow file.
 * As the salt is randomly chosen for each password, even if the plaintext password is the same, the salt will most likely to be different. Hence the combined string will be different which leads to a different hashed string that shows up in the shadow file.
 * In order to validate the password, the salt string must be there to compose the combined string with the plaintext. When the user enters the password, the known salt will be appended to the password as the new combined string. Then the combined string will be hashed using the same alrogithm, resulting in a new hashed string. If the new hashed string is identical to the stored hashed string in the shadow file, then the password matches. Otherwise the password eos not match. This makes it possible to validate password without storing the plaintext password in the file.


### How can we make a bruteforcers job harder if they had the masterkey?

  This depends on how the masterkey is designed to work with the password manager.

  The way the planitext and encrypted password is calculated and stored in this password manager is like this:

  masterkey = random(16 bytes), which is saved in ~/.pwmgr.key
  initialize_vector = random(16 bytes)
  encrypted_password = ENCRYPTED_METHOD(plaintext) with masterkey and initialize_vector

  salt = random(16 bytes)
  combined_string = encrypted_password + salt
  hashed_encrypted_password = hash(combined_string)

  The information stored in the password database is like this:
  username, enc_method, salt, hashed_encrypted_password

  In order to "decrypt" the plaintext password, bruteforcers need to generate a rainbow table for all the usernames in the dictionary with the salts.
  With the masterkey compromised, hack will be able to encrypt any dictionary to a encrypted dictionary using the masterkey, to form another dictionary.
  But this dictionary could not be directly used against the information stored in the database, because the data stored in the database is hashed with combined string.
  As the salt varies for each password entry, it is almost impossible to generate the rainbow table 

  There are a few factors that increase the difficulties of the bruteforcing when the masterkey is compromised: 

  1. Make it harder to figure out how to use the masterkey

   * Write the code in compiled language
    Programming Language like Python, or any other scriting language are readable in source code when it is deployed. But programs written is C, Java, Go will run with binary compiled code which is not human readable. Even reverse engineering is technically still possible to figure out how the masterkey is used, it is much harder compared to reading the code.

  2. Increase the length of the salt

   * In some old system, the salt is only 2 bytes. Then there are only 64K salt values available. In this situation, it will be still be possible to generate a large rainbow table covering all the 64K salt values. Nowadays, with the distributed computing technology like Hadoop, hackers could leverage Hadoop to do really big computing job. With the availability of public cloud computing, hackers even could have free computing resource to help them crack password like this, using the compromised API keys that link to computing resource like Amazon AWS EC2. 
   * With the increase of the salt length, the salt becomes relatively long and will be almost impossible for most of the normal hackers to generate rainbow table. Because not only a lot of computing resource will be needed, but also a lot of storage will be needed. Even if the rainbow table is available, there is also big challenge to query against them because the data is too big to query in a normal way.

  3. Double hash to increase complexity

   * We can pick a few bytes within the hashed password as a new salt, and rehash it to form a double hashed password. With the combination of *1, it will be very hard to figure pre-generate the rainbow table. 

  The above few methods should all make the bruteforcers job harder even if the masterkey is compromised.
