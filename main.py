import os
import requests
import discord
import random
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Получить данные из файла и положить в переменную
filename = os.getenv('JOKE_FILE_NAME')
joke_list = []
with open(filename) as file:
    for line in file:
        line = line.rstrip() # myjoke/goes/here
        joke = line.split('/') # ['myjoke', 'goes', 'here']
        joke_list.append(joke)

# Получить данные из файла и положить в переменную


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!meme'):
        # Get the meme template ID and text inputs from the message content
        meme_args = message.content.split()[1:]
        meme_list = [442586480,444444354,444444605,444444945,444445153,444445426,444445596,444445869,444446053,444446432,444446664,444446832,444447320,444447471,444448044,444448287,444448451,444448628,444448796,444472886,444480129,444480518,444480913]
        user_template_id = random.choice(meme_list)
       # user_template_id = meme_args[0]

        # Выбрать шутку из загруженных из файла
        selected_joke = random.choice(joke_list)
        joke_top = selected_joke[0]
        joke_bot = selected_joke[1]

        # Make a request to the Imgflip API to generate the meme
        response = requests.post('https://api.imgflip.com/caption_image', data={
            'template_id': user_template_id,
            'username': os.getenv('IMGFLIP_USERNAME'),
            'password': os.getenv('IMGFLIP_PASSWORD'),
            'text0': joke_top,
            'text1': joke_bot,
        })

        # Get the URL of the generated meme image
        json_response = response.json()
        if json_response['success']:
            meme_url = json_response['data']['url']
            await message.channel.send(meme_url)
        else:
            await message.channel.send('Failed to generate meme :(')

client.run(os.getenv('DISCORD_BOT_TOKEN'))
