from flask import jsonify, request


def bad_request(message):
    return jsonify({"error": message}), 400


def parse_pagination():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 10
    if per_page > 100:
        per_page = 100

    return page, per_page


def paginated_response(items, pagination, key):
    return jsonify(
        {
            key: items,
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
            },
        }
    )
