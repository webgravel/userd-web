from twisted.internet import reactor
from twisted.protocols import dns
from twisted.names import server, common
from twisted.internet import defer
from twisted.python import failure

verbose = 1

class Resolver(common.ResolverBase):
    def __init__(self, ttl=5 * 60):
        common.ResolverBase.__init__(self)
        self.ttl = ttl

    def lookupAddress(self, name, timeout = None):
        print 'lookup'
        res = '1.2.3.4' if name == 'example.com' else None
        if res:
            return defer.succeed([
                (dns.RRHeader(name, dns.A, dns.IN, self.ttl, dns.Record_A(res, self.ttl)),), (), ()
            ])
        else:
            return defer.fail(failure.Failure(dns.DomainError(name)))


    lookupAllRecords = lookupAddress

if __name__ == '__main__':
    factory = server.DNSServerFactory(clients=[], verbose=verbose)
    factory.resolver = Resolver()
    protocol = dns.DNSDatagramProtocol(factory)
    factory.noisy = protocol.noisy = verbose

    reactor.listenUDP(53, protocol)
    reactor.listenTCP(53, factory)
    reactor.run()
