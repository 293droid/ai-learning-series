from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
aiplatform.init(project="fluid-shoreline-476614-d7", location="europe-west1")

# Initialize the Gemini model
model = GenerativeModel("gemini-2.5-flash-lite")

# Make a simple request
response = model.generate_content("What is AI?")

print("Response:")
print(response.text)

