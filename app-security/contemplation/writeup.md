## Collaborative Vulnerability Disclosure

#### Introduction

In the computer security area, vulnerability disclosure might be one of the most disputable topics all the time. full disclosure, coordinated disclosure, disclosure via bug bounty, and private vulnerability sales are the few common ways for vulnerability disclosure. While each of the vulnerability disclosure method has respective proponents and opponents, I personally prefer the coordinated disclosure process over the others for its mature model and consideration for all involved parties in the community.

In this article, I will start with what vulnerability is, and why vulnerability disclosure is necessary. Then I will deep dive into four common vulnerability processes: full disclosure, collaborative disclosure, disclosure via bug bounty, and private vulnerability sales. The pros and cons of each disclosure method will be discussed thoroughly. Besides, I will talk about my preference in coordinated disclosure and why I think that is the best way for the volnerability disclosure compared with each of the other disclosure method. In the meantime, the downside of the collaborative disclosure will be discussed as well. I will also discuss about how to mitigate those downside and maximize its value for the security community. 

#### Basic Concepts

According to [1], a vulnerability is a weakness which allows an attacker to reduce a system's information assurance. There are three factors for the vulnerability: the system has potential flaw, the attacker acquires the access to the flaw, and the capability of the attacker to exploit the flaw. It is important to distinguish vulnerability from risk. While a vulnerability may be at risk that introduces significant losses, some vulnerability might trigger little interest from the security export community. Withougt loss of potential large values, those vulnerabilities will be of low or no value and will not become risks.

Without any managed disclosure guide, vulnerabilities will still be found every day. The market value of the vulnerability been found may vary according to its value. For high valued vulnerability like flaw in some foundamental service that will put large audiences in threat, the incentive of selling the vulnerability and possily exploits will be high enough for anyone to put it on market in return of money. This kind of deal usually leads to secret trade with criminal groups or governmental secret services, etc. For those kind of vulnerabilities, although the vendor involved will have strong interest and obligation to fix them, they may be revealed to the ones who offer higher rewards and lead to unpredictable consequences. For vulnerability with comparatively lower targeted values, although they may not lead to severe consequences, the vendors may also be lazy to take them and fix them because they do not have much pressure due to the same reason. But still some parties involved will be adversely affected. For the overall benefit of the whole software community, the author still believe a certain disclosure policy will be necessary to exist. Then the involved party will have a general guideline to follow when a security vulnerability is found. And the affected parties will get a general idea of how they will be affected and who to reach when things happen.

#### Security Vulnerability Disclosure Comparison Analysis

 There are a few security vulnerability disclosure methods. 

 As the pros and cons may vary due to different subject. For example, for people who knows how to protect themself against security flaws, they may benefit from some disclosure method. But meanwhile the software company that are affected by the security vulnerability may loose business value. In this article when the author talks about the pros and cons for a disclosure method, he will try to address the most part of the software user communities rather than merely to the business side or the security expert. 

 * Full discloure
  * pros
   * transparency. people who are affected get the first awareness.
   * very fast response from vendor for the fix or workaround.
  * cons
   * the first awareness may be leveraged by hackers as well.
   * commercial software company will lose value on this.

 * Coordinated disclosure
  * pros
  * cons

 * Disclosure via bug bounty
  * pros
  * cons

 * Private vulnerability sales
  * pros
  * cons

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

