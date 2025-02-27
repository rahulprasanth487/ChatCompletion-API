import functions_framework
import vertexai
import os
import openai
from google.auth import default, transport

@functions_framework.http
def hello_http(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    PROJECT_ID = "qwiklabs-gcp-01-6c10741257b9"
    location = "us-central1"

    vertexai.init(project=PROJECT_ID, location=location)

    credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    auth_request = transport.requests.Request()
    credentials.refresh(auth_request)

    client = openai.OpenAI(
        base_url=f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{location}/endpoints/openapi",
        api_key=credentials.token,
    )


    messages = []
    messages.append(
        {
            "role": "system",
            "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous.",
        }
    )
    messages.append({"role": "user", "content": request_json["message"]})

    response = client.chat.completions.create(
        model=request_json["model"],
        messages=messages
    )

    return 'Response is => {}!'.format(response.choices[0].message)
