from google import genai

client = genai.Client(api_key="AIzaSyCeHCeUDsrOHP0Fziqyr-2vqH7GR1W73Bk")

for model in client.models.list():
    print(model.name)
