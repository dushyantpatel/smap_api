# dictionary of http response codes
__httpRespCode = {
    200: "OK",
    201: "Created. The database has been updated",
    204: "No Content. The data requested for does not exist",
    400: "Bad Request. Please check your request format",
    501: "Not Implemented. The requested resource path/method does not exist"
}

# function to get a description of the response code
def responseCodeDescription(code):
    try:
        return __httpRespCode[code]
    except KeyError:
        return ""
