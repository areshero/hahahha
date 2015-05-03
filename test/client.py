from pysimplesoap.client import SoapClient, SoapFault
import sys
# create a simple consumer
client = SoapClient(
    location = "http://localhost:8008/",
    action = 'http://localhost:8008/', # SOAPAction
    namespace = "http://example.com/sample.wsdl", 
    soap_ns='soap',
    #trace = True,
    ns = False)

# call the remote method
#response = client.Adder(a=sys.argv[1], b=sys.argv[2])
response = client.FileOp(file=sys.argv[1])
# extract and convert the returned value
#result = response.AddResult
result = response.FileResult
print result