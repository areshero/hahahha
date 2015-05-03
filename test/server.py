from pysimplesoap.server import SoapDispatcher, SOAPHandler
from BaseHTTPServer import HTTPServer
from test import MotionDetectorInstantaneous

def adder(a,b):
    "Add two values"
    return a+b
def fileOp(file):
    detect = MotionDetectorInstantaneous()
    #detect.run()
    #detect.extractMotion()
    
    result = detect.query(file)
    print result
    return result
dispatcher = SoapDispatcher(
    'my_dispatcher',
    location = "http://localhost:8008/",
    action = 'http://localhost:8008/', # SOAPAction
    namespace = "http://example.com/sample.wsdl", prefix="ns0",
    trace = True,
    ns = True)

# register the user function
dispatcher.register_function('Adder', adder,
    returns={'AddResult': int}, 
    args={'a': int,'b': int})

dispatcher.register_function('FileOp', fileOp,
    returns={'FileResult': str}, 
    args={'file': str})

print "Starting server..."
httpd = HTTPServer(("", 8008), SOAPHandler)
httpd.dispatcher = dispatcher
httpd.serve_forever()