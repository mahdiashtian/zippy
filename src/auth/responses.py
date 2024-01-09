from fastapi.responses import JSONResponse


class JWTResponse(JSONResponse):
    def __init__(self, access_token, refresh_token, *args, **kwargs):
        content = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        super().__init__(content=content, *args, **kwargs)
