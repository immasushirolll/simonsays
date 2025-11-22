from google import genai
GEMINI_API_KEY="AIzaSyDttHwJ1BmJxpnP4h-Ta466sfeWverjM5k"

client = genai.Client(api_key=GEMINI_API_KEY)

prompt = "My tasks for today: \n"

with open("tasks.txt", "r") as file:
    prompt += file.read()

prompt += "\nThis is some text from a screenshot, am I doing things related to my tasks?\n"

with open("info.txt", "r") as file:
    prompt += file.read()

prompt += "\nNo other comments, give me a yes or no answer."

print(prompt)
response = client.models.generate_content(
    model="gemini-2.5-flash", contents=prompt
)

print(response.text)

