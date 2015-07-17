
### Think about how shadow files work: If user1 and user2 have the same password, why do they show up differently? 

 * shadow file on Linux uses salt to prevent the situation described above.
 * Salt is a random string that is appended to the original plaintext password.
 * Then the combined string will be hashed to another string that is stored in the shadow file.
 * As the salt is randomly chosen for each password, even if the plaintext password is the same, the salt will most likely to be different. Hence the combined string will be different which leads to a different hashed string that shows up in the shadow file.
 * In order to validate the password, the salt string must be there to compose the combined string with the plaintext. When the user enters the password, the known salt will be appended to the password as the new combined string. Then the combined string will be hashed using the same alrogithm, resulting in a new hashed string. If the new hashed string is identical to the stored hashed string in the shadow file, then the password matches. Otherwise the password eos not match. This makes it possible to validate password without storing the plaintext password in the file.


### How can we make a bruteforcers job harder if they had the masterkey?

 * This depends on how the masterkey is designed to work with the password manager.

 * The way the planitext and encrypted password is calculated and stored in this password manager is like this:

 ```
  masterkey = random(16 bytes), which is saved in ~/.pwmgr.key
  initialize_vector = random(16 bytes)
  encrypted_password = ENCRYPTED_METHOD(plaintext) with masterkey and initialize_vector

  salt = random(16 bytes)
  combined_string = encrypted_password + salt
  hashed_encrypted_password = hash(combined_string)
 ```

 * The information stored in the password database is like this:
  ```
  username, enc_method, salt, hashed_encrypted_password
  ```

 * In order to "decrypt" the plaintext password, bruteforcers need to generate a rainbow table for all the usernames in the dictionary with the salts. With the masterkey compromised, hack will be able to encrypt any dictionary to a encrypted dictionary using the masterkey, to form another dictionary. But this dictionary could not be directly used against the information stored in the database, because the data stored in the database is hashed with combined string. As the salt varies for each password entry, it is almost impossible to generate the rainbow table 

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

### Running examples
```
(v1)Roberts-MacBook-Pro:password-manager robert$ ls -l *.py *.db ~/.pwmgr.key
-rw-r--r--  1 robert  staff     32 Jul 17 12:16 /Users/robert/.pwmgr.key
-rw-r--r--  1 robert  staff   8192 Jul 17 12:58 passwd_manager.db
-rwxr-xr-x  1 robert  staff  12515 Jul 17 12:40 pwmgr.py


(v1)Roberts-MacBook-Pro:password-manager robert$ ./pwmgr.py -l
(v1)Roberts-MacBook-Pro:password-manager robert$


(v1)Roberts-MacBook-Pro:password-manager robert$ ./pwmgr.py -a -u user1 -p password_is_complicated
user user1 with password is created.
(v1)Roberts-MacBook-Pro:password-manager robert$ ./pwmgr.py -c -u user1 -p password_is_complicated
Password verified for user user1


(v1)Roberts-MacBook-Pro:password-manager robert$ ./pwmgr.py -a -u user_cbc -p password_is_random -e CBC
user user_cbc with password is created.
(v1)Roberts-MacBook-Pro:password-manager robert$ ./pwmgr.py -a -u user_ecb -p password_is_random -e ECB
user user_ecb with password is created.
(v1)Roberts-MacBook-Pro:password-manager robert$ ./pwmgr.py -a -u user_ctr -p password_is_random -e CTR
user user_ctr with password is created.
(v1)Roberts-MacBook-Pro:password-manager robert$
(v1)Roberts-MacBook-Pro:password-manager robert$ ./pwmgr.py -c -u user_cbc -p password_is_random -e CBC
Password verified for user user_cbc
(v1)Roberts-MacBook-Pro:password-manager robert$ ./pwmgr.py -c -u user_ecb -p password_is_random -e ECB
Password verified for user user_ecb
(v1)Roberts-MacBook-Pro:password-manager robert$ ./pwmgr.py -c -u user_ctr -p password_is_random -e CTR
Password verified for user user_ctr


(v1)Roberts-MacBook-Pro:password-manager robert$ ./pwmgr.py -l
     user1 ECB hMg0eJxIxmzHrRUr 6c208697535faa24bd22002223cc004974d5e788
  user_cbc CBC xHyUCZa0JQzAof3c d60e89c6d2938b98b62b75b8352da9663028338f
  user_ecb ECB kXMBQfhUXGflBTwf 05b24dc3b0b87c3b2ff0962104b0f8954e830d65
  user_ctr CTR kdzmnOvz5GrbFTYQ 6d1f0f001482487b098860f2bcaff1074481ef94

(v1)Roberts-MacBook-Pro:password-manager robert$ ./pwmgr.py -d -u user1
user user1 deleted from database

(v1)Roberts-MacBook-Pro:password-manager robert$ ./pwmgr.py -l
  user_cbc CBC xHyUCZa0JQzAof3c d60e89c6d2938b98b62b75b8352da9663028338f
  user_ecb ECB kXMBQfhUXGflBTwf 05b24dc3b0b87c3b2ff0962104b0f8954e830d65
  user_ctr CTR kdzmnOvz5GrbFTYQ 6d1f0f001482487b098860f2bcaff1074481ef94

(v1)Roberts-MacBook-Pro:password-manager robert$ ./pwmgr.py -d -u user_cbc
user user_cbc deleted from database

(v1)Roberts-MacBook-Pro:password-manager robert$ ./pwmgr.py -d -u user_ecb
user user_ecb deleted from database

(v1)Roberts-MacBook-Pro:password-manager robert$ ./pwmgr.py -d -u user_ctr
user user_ctr deleted from database

(v1)Roberts-MacBook-Pro:password-manager robert$ ./pwmgr.py -l

```
