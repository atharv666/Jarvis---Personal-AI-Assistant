import os
import google.generativeai as genai
from config import apikey
genai.configure(api_key=apikey)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "write an email to boss for resignation\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "## Subject: Resignation - [Your Name]\n\nDear [Boss's Name],\n\nPlease accept this email as formal notification that I am resigning from my position as [Your Job Title] at [Company Name]. My last day of employment will be [Your Last Day].\n\n[Optional: Briefly explain your reason for leaving. This can be a simple statement like \"I have accepted another opportunity,\" or more detailed depending on your relationship with your boss and comfort level.]\n\nI would like to thank you for the opportunity to work at [Company Name] for the past [Number] years/months. I have learned a great deal and appreciate the support I have received during my time here. \n\nI am committed to ensuring a smooth transition and am happy to assist in training my replacement. Please let me know how I can be of assistance during this time.\n\nThank you again for the opportunity. I wish you and the company all the best in the future.\n\nSincerely,\n\n[Your Name] \n",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)