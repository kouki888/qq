import google.generativeai as genai

genai.configure(api_key="AIzaSyCeHCeUDsrOHP0Fziqyr-2vqH7GR1W73Bk")

for m in genai.list_models():
    print(m.name, m.supported_generation_methods)
