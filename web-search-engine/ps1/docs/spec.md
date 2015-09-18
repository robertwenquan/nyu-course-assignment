### Itemized Requirements
* [x] contact a major web search engine, say Google
* [x] get top-10 results
* [x] focused strategy until get N pages
* [x] each page visited ONLY once
* [x] each page stored in a file in a directory
* [x] output a list of visited URLs into a file, with the order they are visited
* [x] compute the total number of pages, and total size of pages fetched, with the depth of each page
* [x] get priority score for each page

### Hints
* Priority Scores

* Downloading pages
 * use urllib
 * urlretrieve, urlget
 * requests

* Parsing
 * htmllib, xmllib
 * normal url <a href>
 * url on image <img>
 * url in javascript
 * url in Flash?

* Ambiguity of URLs
 * De-dupe
 * http://www.poly.edu vs http://www.poly.edu/index.html vs www.poly.edu without http
 * www.poly.edu/a/access.html vs www.poly.edu/a/b/c/../../access.html
 * same host, different domain name??
 * check urlparse, urljoin
 * check md5 hash for page content?

* Different types of files
 * may end up with Audio, Video, non-html files. Do not crash!
 * try to use the combination of 
  * file name extension
  * MIME type
  * fetch header and detect

* Checking for earlier visits
  * de-dupe
  * use dict() and normalized url as key

* Testing
  * try different n, from smaller to large
  * try different keyword(s)
  * Robot Exlusion Protool
  * deal with CGI script

* Exceptions
  * do not panic with irresponsible server
  * urllib.urlretrieve()
  * try and catch

* Password protected pages
  * do not stuck on password enabeld website/url

* Miscellaneous (from Robert)
  * blacklist
  * resume crawling
  * multi-threading
  * multi-instance large scale crawl on AWS

