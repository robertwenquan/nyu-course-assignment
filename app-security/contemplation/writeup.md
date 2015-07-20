## Collaborative Vulnerability Disclosure

#### Introduction

In the computer security area, vulnerability disclosure might be one of the most disputable topics all the time. full disclosure, coordinated disclosure, disclosure via bug bounty, and private vulnerability sales are the few common ways for vulnerability disclosure. While each of the vulnerability disclosure method has respective proponents and opponents, I personally prefer the coordinated disclosure process over the others for its mature model and consideration for all involved parties in the community.

In this article, I will start with what vulnerability is, and why vulnerability disclosure is necessary. Then I will deep dive into four common vulnerability processes: full disclosure, collaborative disclosure, disclosure via bug bounty, and private vulnerability sales. The pros and cons of each disclosure method will be discussed thoroughly. Besides, I will talk about my preference in coordinated disclosure and why I think that is the best way for the volnerability disclosure compared with each of the other disclosure method. In the meantime, the downside of the collaborative disclosure will be discussed as well. I will also discuss about how to mitigate those downside and maximize its value for the security community. 

#### Basic Concepts

According to [1], a vulnerability is a weakness which allows an attacker to reduce a system's information assurance. There are three factors for the vulnerability: the system has potential flaw, the attacker acquires the access to the flaw, and the capability of the attacker to exploit the flaw. It is important to distinguish vulnerability from risk. While a vulnerability may be at risk that introduces significant losses, some vulnerability might trigger little interest from the security export community. Withougt loss of potential large values, those vulnerabilities will be of low or no value and will not become risks.

Without any managed disclosure guide, vulnerabilities will still be found every day. The market value of the vulnerability been found may vary according to its value. For high valued vulnerability like flaw in some foundamental service that will put large audiences in threat, the incentive of selling the vulnerability and possily exploits will be high enough for anyone to put it on market in return of money. This kind of deal usually leads to secret trade with criminal groups or governmental secret services, etc. For those kind of vulnerabilities, although the vendor involved will have strong interest and obligation to fix them, they may be revealed to the ones who offer higher rewards and lead to unpredictable consequences. For vulnerability with comparatively lower targeted values, although they may not lead to severe consequences, the vendors may also be lazy to take them and fix them because they do not have much pressure due to the same reason. But still some parties involved will be adversely affected. For the overall benefit of the whole software community, the author still believe a certain disclosure policy will be necessary to exist. Then the involved party will have a general guideline to follow when a security vulnerability is found. And the affected parties will get a general idea of how they will be affected and who to reach when things happen.

#### Security Vulnerability Disclosure Comparison Analysis

 There are a few security vulnerability disclosure methods. 

 Full disclosure is an extreme way to disclose. It is straightforward to understand that for any vulnerability that is found, it should be made public with full details. It might be the most easy process to follow because of no extra effort involved. Anyone who finds a vulnerability and proves it, just choose a media, either a public maillist, forum or an academic conference to disclose. And that is it.

 No disclosure is another extream way to not disclose any information upon vulnerability been found. It is also easy to follow because of no extra effort involed. We will talk about the side effects and compare with each other afterwards.
 
 Collaborative disclosure is the compromise of all involved partied. In combination of full disclosure and no disclosure, it provides privilege to the software vendor that is affected in the vulnerability to have access to full disclosure. At the same time it only gives a limited variable buffer for the vendor to fix the vulnerability before releasing to the public audiences. Determing the length of the buffer involves netogiation between involved parties affected by the vulnerability, possily including the target software users, software vendor, independent vulnerability management organization, governmental organization, independent security analyst or researchers.

 While the above ways all do not involve monetary incentives, private vulnerability sales is yet another way that generates revenue from vulnerabilities. In this disclosure method, vulnerabilities are disclosed partially like communities on the market, with either a fixed price or in a bidding. Normally parties who offer the highest price will get the full disclosure of the vulnerability.

 As the pros and cons may vary due to different subject. For example, for people who knows how to protect themself against security flaws, they may benefit from some disclosure method. But meanwhile the software company that are affected by the security vulnerability may loose business value. In this article when the author talks about the pros and cons for a disclosure method, he will try to address the most part of the software user communities rather than merely to the business side or the security expert. 

 There is another disclosure method that involves incentives. The bug bounty program offered by many software vendors opens a way to reach all the security experts in the world to help enhance the security of their softwares. Anyone who could find an unknown security vulnerability would get corresponding rewards based on their pre-classified level associated with a reward amount. The reward could be either monetary items, or swag of that company, to names on the fame of walls.

 Among all the vulnerability disclosure methods, the author inclines to believe the collaborative disclosure is the best way to disclose security vulnerabilities.

#### Conclusion

In this article, the concept of security vulnerability is introduced. The necessecity of vulnerability disclosure is introduced afterwards. A few common vulnerability disclosure methods are discussed and compared with each other. Although there is no definitive answer about which disclosure method is the best, the author states his preference on collaborative disclosure due to its model maturity and comprehensive consideration for all involved parties. 

#### Reference
 * [1] https://en.wikipedia.org/wiki/Vulnerability_(computing)
 * [2] http://www.cert.org/vulnerability-analysis/vul-disclosure.cfm
 * [3] https://en.wikipedia.org/wiki/Responsible_disclosure
 * [4] https://en.wikipedia.org/wiki/Full_disclosure_(computer_security)
 * [5] https://en.wikipedia.org/wiki/Vulnerability_(computing)#Vulnerability_disclosure
 * [6] https://en.wikipedia.org/wiki/Zero-day_(computing)
 * [7] http://www.forbes.com/sites/andygreenberg/2012/03/23/shopping-for-zero-days-an-price-list-for-hackers-secret-software-exploits/

