import azure.functions as func
import logging
import openai
import os
from dotenv import load_dotenv

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="gen_ai")
def gen_ai(req: func.HttpRequest) -> func.HttpResponse:
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
def hello(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request for /api/hello.')

    return func.HttpResponse("Hello, World!", status_code=200)

@app.route(route="prompt")
def process_prompt(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request for /api/prompt.')


    # config
    load_dotenv()
    openai.api_type = "azure"
    openai.api_base = "https://gen-ai-training-avanade-2.openai.azure.com/"
    openai.api_version = "2023-07-01-preview"
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = req.params.get('prompt')

    if not prompt:
        return func.HttpResponse(
            "Please provide a prompt.",
            status_code=400
        )        
    response = openai.ChatCompletion.create(
        engine="gpt35_test",
        messages = [
            {"role":"system","content":"You are an AI assistant that helps people find information."},
            {"role":"user","content": prompt}
            ],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    
    message = response['choices'][0]['message']['content']
    return func.HttpResponse(message)
