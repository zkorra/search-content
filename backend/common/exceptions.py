from flask import jsonify, make_response


def exception_common(desc, code):
    return exception("Search Content", code, desc)


def exception_cse(desc, code):
    return exception("Custom Search Engine", code, desc)


def exception_firestore(desc, code):
    return exception("Firestore", code, desc)


def exception(service, code, desc):
    response = {"service": service, "code": code, "message": str(desc)}
    return make_response(jsonify(response), code)
