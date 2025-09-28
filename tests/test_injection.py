from typing import Callable

from httpx import Client

from jetweb import Context, HTTPException, JetWeb, Request, Response


def test_injection_into_handler(app: JetWeb, client: Client) -> None:
    app.global_context["app_context"] = 1

    @app.middleware
    def middleware(next_handler: Callable, context: Context) -> Response:
        context["middleware_context"] = 2
        return next_handler()

    @app.get("/endpoint/{name}")
    def handle_get(
        request: Request, app: JetWeb, context: Context, app_context: int, middleware_context: int, name: str
    ) -> str:
        assert isinstance(request, Request)
        assert isinstance(app, JetWeb)
        assert isinstance(context, Context)
        assert name == "john"
        assert app_context == 1
        assert middleware_context == 2
        return "Test response"

    response = client.get("/endpoint/john")
    assert response.status_code == 200
    assert response.text == "Test response"


def test_injection_into_exception_handler(app: JetWeb, client: Client) -> None:
    app.global_context["app_context"] = 1

    @app.middleware
    def middleware(next_handler: Callable, context: Context) -> Response:
        context["middleware_context"] = 2
        return next_handler()

    @app.exception_handler(404)
    def handle_404(
        request: Request,
        app: JetWeb,
        context: Context,
        exception: HTTPException,
        app_context: int,
        middleware_context: int,
    ) -> str:
        assert isinstance(request, Request)
        assert isinstance(app, JetWeb)
        assert isinstance(context, Context)
        assert isinstance(exception, HTTPException)
        assert app_context == 1
        assert middleware_context == 2
        return "Test response"

    response = client.get("/non-existing-endpoint")
    assert response.status_code == 200
    assert response.text == "Test response"


def test_injection_into_middleware(app: JetWeb, client: Client) -> None:
    app.global_context["app_context"] = 1

    @app.middleware
    def middleware(
        next_handler: Callable, request: Request, app: JetWeb, context: Context, app_context: int
    ) -> Response:
        assert isinstance(request, Request)
        assert isinstance(app, JetWeb)
        assert isinstance(context, Context)
        assert app_context == 1
        return next_handler()

    @app.get("/endpoint")
    def handle() -> str:
        return "Test response"

    response = client.get("/endpoint")
    assert response.status_code == 200
    assert response.text == "Test response"


def test_without_injection(app: JetWeb, client: Client) -> None:
    app.global_context["app_context"] = 1

    @app.middleware
    def middleware(next_handler: Callable, context: Context) -> Response:
        context["middleware_context"] = 2
        return next_handler()

    @app.get("/endpoint/{name}")
    def handle_get() -> str:
        return "Test response"

    response = client.get("/endpoint/john")
    assert response.status_code == 200
    assert response.text == "Test response"
