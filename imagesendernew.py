import discord
import os
import requests

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    # Avoid responding to the bot's own messages
    if message.author == bot.user:
        return

    # Check if there are attachments in the message
    if message.attachments:
        for attachment in message.attachments:
            # Check if the attachment is an image
            if attachment.content_type and attachment.content_type.startswith('image/'):
                # Define the path where the image will be saved
                save_path = os.path.join('images', attachment.filename)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                # Save the image locally
                await attachment.save(save_path)
                print(f'Image saved to {save_path}')

                with open(save_path, 'rb') as image_file:
                    response = requests.post(
                        'https://ed13-2400-adca-119-5d00-b0-b4c9-7486-8c97.ngrok-free.app/process-image/',
                        files={'file': (attachment.filename, image_file, attachment.content_type)}
                    )
                
                    # Process the API response
                    if response.status_code == 200:
                        result = response.json()
                        print(result)
                        await message.channel.send(f'Image processed successfully: {result}')
                    else:
                        await message.channel.send('Failed to process the image.')

bot.run('MTM1MTA1MDIzMjcyODkxMTkwMw.GjU0h3.a3RA149q_gXRLJV1fScAFNnAWtqqru6rC4Kt2w')
