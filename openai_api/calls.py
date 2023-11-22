import openai


def create_prompt(prompt, api_key, system_message):
    """Function that connects to OpenAI API
    Args:
        prompt (String): prompt
        api_key (String): OpenAI API key passed in request
        system_message (String): system message for the model
    Returns:
        str: Response from OpenAI extracted fron json.
    """
    # config
    openai.api_type = "azure"
    openai.api_base = "https://gen-ai-training-avanade-2.openai.azure.com/"
    openai.api_version = "2023-07-01-preview"
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        engine="gpt35_test",
        messages = [
            {"role":"system","content": system_message},
            {"role":"user","content": prompt}
            ],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    
    return response['choices'][0]['message']['content']

def get_openai_api_key(req):
    """API Key"""
    openai_key = req.headers.get('openai_api_key')
    return openai_key

def get_content(req):
    """Prompt. Non-needed now"""
    prompt = req.params.get('prompt')
    return prompt