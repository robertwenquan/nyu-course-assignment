### Itemized Requirements
* contact a major web search engine, say Google
* get top-10 results
* focused strategy until get N pages
* each page visited ONLY once
* each page stored in a file in a directory
* output a list of visited URLs into a file, with the order they are visited
* compute the total number of pages, and total size of pages fetched, with the depth of each page
* get priority score for each page

### Hints
* Priority Scores
* Downloading pages
 * use urllib
 * urlretrieve, urlget
* Parsing
 * htmllib, xmllib
 * normal url
 * url on image
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
  * multi-instance on AWS

