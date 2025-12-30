
import vertexai
from vertexai.generative_models import GenerativeModel
import argparse
import google.auth
from google.api_core import exceptions

def check_regions(project_id):
    print(f"--- Regional Availability Check ---")
    print(f"Project: {project_id}")
    
    # Common regions for GenAI
    regions = ["us-central1", "us-west1", "us-east4", "europe-west1", "asia-northeast1"]
    
    model_name = "gemini-2.5-flash"
    
    any_success = False
    
    for location in regions:
        print(f"\nScanning Region: {location} ...", end=" ")
        try:
            vertexai.init(project=project_id, location=location)
            model = GenerativeModel(model_name)
            response = model.generate_content("Hi")
            print(f"[SUCCESS] - Access works here!")
            any_success = True
            break # Found a working region
        except exceptions.NotFound:
            print(f"[404 Not Found]")
        except exceptions.PermissionDenied:
            print(f"[403 Permission Denied]")
        except Exception as e:
            print(f"[Error: {e}]")

    print("\n" + "="*30)
    if any_success:
        print(f"GOOD NEWS: Access works in region '{location}'!")
        print(f"Please update your code to use location='{location}'")
    else:
        print("RESULT: Blocked in ALL regions.")
        print("This confirms the issue is likely the 'Account verification under review' status")
        print("seen in your screenshot, which restricts model access globally.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default="aegis-482716")
    args = parser.parse_args()
    
    check_regions(args.project)
