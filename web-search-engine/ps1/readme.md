### Crawler

In this assignment, you are asked to write a (very primitive) foused web rawler in Python that attempts
to do a limited rawl of the web. The purpose of this assignment is to learn about rawling, to start
programming in Python, and to learn a bit about the various strutures and features found in web pages
and how to handle/parse them. You may work on this homework in pairs of two people, but you MUST
both understand all aspets of the projet - there may be a demo for eah group where you both have to
explain the details of your solution! The pro jet must be done in Python (unless I have given you speial
permission to do it in another language, whih I rarely do).
More preisely, given a query (a set of keywords) and a number n provided by the user, your rawler should
ontat a ma jor searh engine, get the top-10 results for this query from the engine, and then rawl starting
from these top-10 results using a foused strategy until you have olleted a total of n pages. Eah page
should be visited only one and stored in a file in your diretory. Your program should output a list of all
visited URLs, in the order they are visited, into a file. Your program should also ompute the total number
and total size (in MB) of the pages that were downloaded, and the depth of eah page, i.e., its distane from
one of the 10 start pages aording to your rawl.
Let me explain what is meant by a foused rawling strategy. Basially, it is a strategy that attempts to
fous on pages that are relevant to a partiular topi, in this ase relevant to the searh terms the user
supplied. For this homework, you may use a very simple strategy where, after downloading a new page and
parsing for hyperlinks, you also hek if the page ontains the searh terms. You should then give highest
priority to following hyperlinks that were parsed from pages that ontain many of the searh terms. Thus, if
your searh terms are \dog at" then a page containing dog twie and at one should have higher priority
(have a higher sore) than one ontaining only at, or one ontaining eah term only one. But suppose you
find the same URL as a hyperlink on two pages you downloaded, one ontaining only at, and then later
one ontaining three ats and one dog. What should you do now to ombine the two priority sores? Add
them, or average them? Come up with a good solution that gives this page the priority it deserves. (For
eah downloaded page, also print out its priority sore.)
There are a ouple of triky issues that ome up in this assignment. Following is a list of hints and omments
on the assignment. More help on this will be provided in the next few days. But please get started right
away, and ask me when you run into problems!
Priority Sores for Foused Crawling: As desribed, you may give priority sores based on just ounting
the number of ourrenes of the searh terms. You may also implement smarter tehniques, say using the
Cosine or BM25 rank sore, by looking at how lose a hyperlink is to a keyword in the page, or other ideas
you an ome up with. You also need a suitable data struture that allows you to maintain the priority
sores of pages, and to selet the page with highest urrent priority sore to be rawled next. Note that the
sore of a page may hange as more links to it are disovered. (Hint: onsider using a heap data struture
for this task, possible in onnetion with a ditionary.)
Downloading Pages: Python has a module alled urllib that ontains funtions for downloading web
pages. Chek it out to find the right funtion for downloading a web page from a given URL. There is one
alled urlretrieve that might be useful, and one alled urlget.
Parsing: For eah web page that you enounter, you will need to parse the file in order to find links from
this to other pages. Python provides some onvenient funtions for these types of problems in modules
alled htmllib and xmllib, whih are explained on the Python web site at www.python.org. Note that in
addition to \normal" hyperlinks, a page may also ontain hyperlinks as part of image maps (i.e., by liking
on an image you get to the linked page) or within javasript or ash; you an either ignore these links and
hope that your rawler will eventually find those pages via other routes, or you an try to parse stu suh
as javasript for some extra redit. (If you miss some pages, it is no big deal.)
You also need to parse a page to find ourrenes of the searh terms, by either using a real HTML parser
(preferred), or by using regular expression mathing (whih is also aeptable).
Ambiguity of URLs: Note that URLs, as enountered as hyperlinks in pages, are \ambiguous" in several
ways. If a URL ends with index.htm, index.html, index.jsp, or main.html, et., then we an usually
omit this last part. For a loal example at Poly, the page loated at http://is.poly.edu/index.shtml
is atually the same as that loated at http://is.poly.edu or http://sserv2.poly.edu. (On the
other hand, typing is.poly.edu/index.html into your browser will not work.) If you are on a loal
mahine at Poly, then just typing is should work with your browser. Also, if the page is.poly.edu
has a link to is.poly.edu/researh/group.html, then this link ould be written in the page as just
researh/group.htm, sine it is in a subdiretory on the same host as the first page. Pathnames an also
go up one diretory (e.g., ../people/bob.html) or the <base> tag might be used in the page. Chek out
the Python module urlparse and the funtion urljoin to deal with these issues.
As already said above, your program should try to avoid visiting the same page several times. In general,
this an be diÆult, sine a single host an have several names (e.g., is.poly.edu is the same mahine as
sserv2.poly.edu). So do as muh as you an in this diretion, but be aware that you will not be able to
ath all ases.
Dierent Types of Files: Apart from HTML files, your rawler may enounter many other types, inluding
images, Java and Perl sripts, audio files, XML, et. You probably do no want to try to parse an audio file
for hyperlinks! Think about a solution for this problem that works most of the time. (That is, if you fail to
disover some outgoing links, that is aeptable, but your program should not rash as a result of parsing
some weird file.) Try to use the information supplied by file endings (e.g., .html, .asp, or .jpg). Also ask
for the MIME type of a file. Make a sensible deision about what types of files you want to parse.
Cheking for Earlier Visits: You need a way to hek whether a page has already been visited. For this
assignment, you should use the ditionary struture provided by Python and use the normalized URL as
key. See the Python intro handout for an example.
Be Considerate when Testing: At first, your rawler will probably be very buggy and thus misbehave
often. So do not run it for large values of n until you have found most of the bugs, and also periodially vary
the keywords you supply between runs so you do not onstantly rawl the same web site. Note that as you
try new keywords, and thus new sites, you will probably onstantly run into new bugs and hallenges that
you an try to resolve { this is the point of the homework. But you will probably not be able to overome all
problems { so do as muh as you an. In general, your rawler will probably not manage to survive for long
on many rawls, so if you an reliably download a few hundred or a thousand pages for most queries that
will be OK. Also, implement the Robot Exlusion Protool, to avoid going into areas that are o-limits. (If
you do not implement robot exlusion, you should at least test for the existene of a robots.txt file and not
rawl any site that has the file.) Also, make reasonable deisions about how to deal, e.g., with CGI sripts.
(For example, you ould deide to not rawl any URLs with the string \gi" in it.)
Exeptions: Make sure that your program does not break if the server at the other end fails to respond.
Use the try ommand and exeptions in Python whenever you request a page using urllib.urlretrieve()
or some other method. Make sure your program does not hang for minutes or forever.
Password-Proteted Pages: Make sure your rawler does not get stuk on links to password-proteted
pages. See the ourse page for details.
To summarize, your task is to build a basi web rawler in python. You may use omponents for tasks such
as HTML parsing, downloading a file loated at a URL, and Robot Exlusion, but of ourse you should not
simply download and reuse a omplete Python rawler. You should maintain your own data strutures for
the queue, figure out how to get results from a searh engine (using APIs as needed), et.

