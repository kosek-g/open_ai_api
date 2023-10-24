import azure.functions as func
import logging
import openai
import os
from dotenv import load_dotenv
from openai_api.calls import (
    create_prompt,
    get_openai_api_key
)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="gen_ai")
def gen_ai(req: func.HttpRequest) -> func.HttpResponse:
    """Init/test function."""
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}! Poland GenAI Club is here!")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="hello", methods=["GET"])
def hello_get_method(req:func.HttpRequest) -> func.HttpResponse:
    """
    GET method. 
    Needs only API key, prompt is hardcoded
    """
    logging.info('Python HTTP trigger function processed a GET request.')

    api_key = get_openai_api_key(req)
    if not api_key:
        return func.HttpResponse("openai_api_key is missing", status_code=400)

    prompt = "Hello! Who is the president of Poland?"
    system_message = "You are a helpful AI assistant"
    ai_response = create_prompt(prompt, api_key, system_message)

    return func.HttpResponse(ai_response, status_code=200)

@app.route(route="prompt", methods=["POST"])
def prompt_post_method(req: func.HttpRequest) -> func.HttpResponse:
    """
    POST method.
    Takes API key and prompt as a param.
    """
    logging.info('Python HTTP trigger function processed a POST request.')

    # API key
    api_key = get_openai_api_key(req)
    if not api_key:
        return func.HttpResponse("openai_api_key is missing", status_code=400)

    # Prompt
    prompt = req.params.get('prompt')
    if not prompt:
        return func.HttpResponse(
            "Please provide a prompt.",
            status_code=400
        )  

    # System message
    system_message = req.params.get('sys_message')
    if not system_message:
        return func.HttpResponse(
            "Please provide a system message.",
            status_code=400
            )
    
    ai_response = create_prompt(prompt, api_key, system_message)

    return func.HttpResponse(ai_response, status_code=200)