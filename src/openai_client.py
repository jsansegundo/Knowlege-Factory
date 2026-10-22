import os

from openai import OpenAI


def required_env(name):

    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Falta la variable de entorno requerida: {name}"
        )

    return value


def create_openai_client():

    endpoint = (
        required_env("AZURE_OPENAI_ENDPOINT")
        .rstrip("/")
        + "/"
    )

    return OpenAI(
        base_url=endpoint,
        api_key=required_env("AZURE_OPENAI_API_KEY"),
    )
