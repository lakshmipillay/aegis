
import vertexai
from vertexai.generative_models import GenerativeModel
import argparse

def version_check():
    print(f"Vertex AI SDK version: {vertexai.__version__}")

def list_models_simple(project_id, location):
    vertexai.init(project=project_id, location=location)
    try:
        model = GenerativeModel("gemini-2.5-flash")
        print(f"Successfully initialized model: gemini-2.5-flash")
        response = model.generate_content("Hello")
        print(f"Successfully generated content: {response.text}")
    except Exception as e:
        print(f"Error accessing gemini-2.5-flash: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default="aegis-482716")
    parser.add_argument("--location", default="us-central1")
    args = parser.parse_args()
    
    version_check()
    list_models_simple(args.project, args.location)
