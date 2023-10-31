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

# Default function
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

# GET function with hardcoded prompt
@app.route(route="hello", methods=["GET"])
def hello_get_method(req:func.HttpRequest) -> func.HttpResponse:
    """
    GET method. 
    Needs only API key, prompt is hardcoded
    """
    logging.info('Python HTTP trigger function processed a GET request.')

    # API key / header
    api_key = get_openai_api_key(req)
    if not api_key:
        return func.HttpResponse("openai_api_key is missing", status_code=400)

    # Hardcoded prompt and sys. message
    prompt = "Hello! Who is the president of Poland?"
    system_message = "You are a helpful AI assistant"

    # OpenAI resposne
    ai_response = create_prompt(prompt, api_key, system_message)

    return func.HttpResponse(ai_response, status_code=200)

# POST prompt function
@app.route(route="prompt", methods=["POST"])
def prompt_post_method(req: func.HttpRequest) -> func.HttpResponse:
    """
    POST method.
    Takes API key and prompt as a param.
    """
    logging.info('Python HTTP trigger function processed a POST request.')

    # API key / header
    api_key = get_openai_api_key(req)
    if not api_key:
        return func.HttpResponse("openai_api_key is missing", status_code=400)

    # Prompt / param
    prompt = req.params.get('prompt')
    if not prompt:
        return func.HttpResponse(
            "Please provide a prompt.",
            status_code=400
        )  

    # System message / param
    system_message = req.params.get('sys_message')
    if not system_message:
        return func.HttpResponse(
            "Please provide a system message.",
            status_code=400
            )
    
    # OpenAI resposne
    ai_response = create_prompt(prompt, api_key, system_message)

    return func.HttpResponse(ai_response, status_code=200)

# POST function / 
@app.route(route="extract_details", methods=["POST"])
def extract_details_method(req: func.HttpRequest) -> func.HttpResponse:
    """
    POST method.
    Takes API key and prompt as a body content.
    """
    logging.info('Python HTTP trigger function processed a POST request.')

    # API key / header
    api_key = get_openai_api_key(req)
    if not api_key:
        return func.HttpResponse("openai_api_key is missing", status_code=400)

    # Get email content from request body
    email_content = req.get_body().decode('utf-8')
    if not email_content:
        return func.HttpResponse(
            "Please provide email content in the request body.",
            status_code=400
        )
    
    # Hardcoded system message
    system_message = "You are a helpful sales assistance."

    #prompt
    prompt = (
        f"Your task is to extract data from the email below. \
        In JSON format return customer name (person that sends the email), \
        order number, order date and product name. \
        Here is the email content: '{email_content}'. \
        Return only JSON with the content, no other words."
    )
    
    # OpenAI resposne
    ai_response = create_prompt(prompt, api_key, system_message)

    return func.HttpResponse(ai_response, status_code=200)