from scrapy.exceptions import NotConfigured
from scrapy.http import Response
from twisted.internet import defer, protocol, reactor

class PhantomJsProcessProtocol(protocol.ProcessProtocol):

  def __init__(self, request):
    self.request = request
    self.deferred = defer.Deferred()
    self.out = ''
    self.err = ''
    self.exitcode = None

  def outReceived(self, data):
    self.out += data

  def errReceived(self, data):
    self.err += data

  def processEnded(self, status):
    """Create a Response object based on the output, and callback the deferred with it."""
    self.exitcode = status.value.exitCode
    # TODO(madadam): handle failures.
    response_body = self.out
    response = Response(url=self.request.url, body=self.out)
    self.deferred.callback(response)


# Note that this is a DownloadHandler, not a DownloadMiddleware.  Middleware's process_request
# cannot return a Deferred, so it can't do asynchronous downloading.  The phantomjs process can
# take quite a while, and calling it synchronously would block the main python thread, gumming
# up the works.

class PhantomJsDownloadHandler(object):
  """A downloader that fetches results via phantomjs."""

  def __init__(self, settings):
    self.settings = settings
    self.phantomjs_path = settings.get('PHANTOMJS_BIN')
    if not self.phantomjs_path:
      raise NotConfigured

  def download_request(self, request, spider):
    script = request.meta['script']
    query = request.meta['query']
    num = request.meta['num']

    protocol = PhantomJsProcessProtocol(request)
    args = [self.phantomjs_path, script, query, str(num)]

    #pylint: disable=no-member
    transport = reactor.spawnProcess(protocol, self.phantomjs_path, args=args)
    return protocol.deferred
