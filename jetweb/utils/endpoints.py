"""
Provides utils for endpoints.
"""

from re import Match, Pattern, compile, sub


def convert_to_regex(match: Match, converters: dict) -> str:
    """
    Convert a "{name:type}" placeholder into a named regex group using converters.

    :param match: Match object with path parameter.
    :param converters: Converters for path parameter.
    :returns: Regex substring for path parameter.
    :raises ValueError: If converter identifier is not known.
    """
    param_name, param_type = match.groups()
    param_type = (param_type or "path").lstrip(":")

    if param_type not in converters:
        raise ValueError("Converter must be registered")

    return f"(?P<{param_name}>{converters[param_type].pattern})"


def create_pattern(endpoint: str, converters: dict) -> Pattern:
    """
    Build a compiled regex pattern from a route endpoint.

    :param endpoint: Route endpoint.
    :param converters: Converters for path parameter.
    :returns: Pattern object.
    """
    pattern = sub(r"{(\w+)(:\w+)?}", lambda match: convert_to_regex(match, converters), endpoint)
    return compile("^" + pattern + "$")


def convert_path_params(endpoint: str, path_params: dict, converters: dict) -> dict:
    """
    Convert path parameters to necessary types.

    :param endpoint: Route endpoint.
    :param path_params: Path parameters.
    :param converters: Converters for path parameter.
    :returns: Converted path parameters.
    """
    for param_name in path_params:
        for converter in converters.values():
            if f"{param_name}:{converter.identifier}" in endpoint:
                path_params[param_name] = converter.convert(path_params[param_name])

    return path_params


def normalize_endpoint(endpoint: str) -> str:
    """
    Add leading slash and remove several sequential slashes.

    :param endpoint: Route endpoint.
    :returns: Normalized route endpoint.
    """
    endpoint = "/" + endpoint
    return sub(r"/+", r"/", endpoint)
