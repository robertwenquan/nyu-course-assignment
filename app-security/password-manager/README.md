* Using your favorite language, implement a little app that has the following features:

 * Given a (Username, Password) pair in ASCII; store the pair to a file
 * Given a (Username, Password) pair in ASCII; check if the username exists and if the password matches the one stored in a file.
 * Using a flag the user should be able to choose ECB, CTR or CBC modes.
 * Program does not need to be interactive. Command line interface is sufficient.
 * Java has great crypto extensions and c/c++ has openssl, however feel free to use python or another scripting language. 
 * A master key needs to exist, could be auto generated and stored somewhere. 

* Grading Criteria

 * Submitted script/executable runs – 10 pts
 * Submitted script/executable meets program specs – 10 pts
 * Clear understanding of crypto engineering – 10 pts
 * Crypto implemented properly – 25 pts
 * ECB, CTR, and CBC block ciphers supported – 20 pts
 * Satisfactory answers to homework questions – 20 pts
 * All materials submitted (source, executables, documentation) – 5 pts

* Investigation
 * What is ECB, CTR or CBC? 
  * They are AES encryption mode.
 * What is master key?
 * How to implemente them?
  * http://stackoverflow.com/questions/1220751/how-to-choose-an-aes-encryption-mode-cbc-ecb-ctr-ocb-cfb
  * http://docs.python-guide.org/en/latest/scenarios/crypto/

* Write-up
 * Think about how shadow files work: If user1 and user2 have the same password, why do they show up differently? 
  * shadow file on Linux
 * How can we make a bruteforcers' job harder if they had the masterkey?

 * encrypted passwd under Linux
 $6$TqX6OQUE$mLPI3rqNWhas.ZPglVRbXB6ODp66k4h.CHCWDtN5gWzARB8JJKyoWj.HAWMzbBQS/GAjv0iB8LQxYh90IfpeE/
 according to crypt(3), $id$salt$encrypted
 so 6 is id
 TqX6OQUE is salt
 mLPI3rqNWhas.ZPglVRbXB6ODp66k4h.CHCWDtN5gWzARB8JJKyoWj.HAWMzbBQS/GAjv0iB8LQxYh90IfpeE/ is encrypted key

 Here is another encrypted key with the same password
 $6$II6OkGSZ$L2ZHP0Pg61X4FO7uZDrnv9M0bJsj218WClhtyXTc1slWCDKB.YKJE9vAvN.mAJnaT9WW5UHZFv5iWBhxkL8yM/

