# dictionary of http response codes
__http_resp_code = {
    200: "OK",
    201: "Created. The database has been updated",
    204: "No Content. The data requested for does not exist",
    400: "Bad Request. Please check your request format",
    501: "Not Implemented. The requested resource path/method does not exist",
    520: "Unknown error occurred, please let the API developer know immediately"
}


# function to get a description of the response code
def responseCodeDescription(code):
    try:
        return __http_resp_code[code]
    except KeyError:
        raise Exception("The HTTP response code " + str(code) + " does not exist")
