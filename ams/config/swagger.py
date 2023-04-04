template = {
    "swagger": "2.0",
    "info": {
        "title": "Attendance system API",
        "description": "API for bookmarks",
        "version": "1.0"
    },
    #"basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',  #for json version of the documentation which you can access from any other tool like post man
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",  #used to generate css to show in the documentation
    "swagger_ui": True,
    "specs_route": "/"
} 