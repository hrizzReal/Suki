import discord
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the tokens from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Set up intents for reading message content
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Configure the Gemini API with the API Key
genai.configure(api_key=GEMINI_API_KEY)

def get_ai_response(prompt):
    try:
        # Use the Gemini API to generate content
        model = genai.GenerativeModel("gemini-1.5-flash")  # Use the specific Gemini model
        response = model.generate_content(prompt)  # Generate the response based on the prompt
        return response.text.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't fetch a response right now."

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('%'):
        prompt = message.content[1:].strip()  # Get the prompt from the message
        response = get_ai_response(prompt)  # Get the AI response using Gemini API
        await message.channel.send(response)  # Send the response back to the Discord channel

client.run(DISCORD_TOKEN)
