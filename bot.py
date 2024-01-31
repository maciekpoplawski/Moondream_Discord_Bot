import os

import uuid
import torch
import discord
from PIL import Image
from dotenv import load_dotenv
from huggingface_hub import snapshot_download

import utils
from moondream.moondream import detect_device, VisionEncoder, TextModel


load_dotenv()

# Put discord token in .env file in DISCORD_BOT_TOKEN
discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")

# Default question to ask if no question is provided
DEFAULT_QUESTION = "Describe this image."

# Set to True to collect interactions in a database (FIRST RUN create_db.py)
collect_interactions_in_db = False


class MoonsdreamDiscordBot(discord.Client):
    def __init__(self, use_cpu=False):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.device, self.dtype = self.setup_model(use_cpu)
        self.user_image_map_filename = 'user_image_map.json'
        self.user_image_map = utils.load_from_json(self.user_image_map_filename)
        self.user_image_context = {}  # Mapping of user ID to image context (embeddings)

    def setup_model(self, use_cpu):
        if use_cpu:
            device = torch.device("cpu")
            dtype = torch.float32
        else:
            device, dtype = detect_device()

        model_path = snapshot_download("vikhyatk/moondream1")
        self.vision_encoder = VisionEncoder(model_path).to(device=device, dtype=dtype)
        self.text_model = TextModel(model_path).to(device=device, dtype=dtype)

        return device, dtype

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")
        print(f"Running on {self.device}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.attachments and self.user.mentioned_in(message):
            await self.handle_image_upload(message)
            await self.handle_text_query(message)
        elif self.user.mentioned_in(message):
            await self.handle_text_query(message)

    async def handle_image_upload(self, message):
        attachment = message.attachments[0]
        if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
            save_path = await self.save_attachment(attachment)

            user_id_str = str(message.author.id)
            self.user_image_map[user_id_str] = save_path
            utils.save_to_json(self.user_image_map, self.user_image_map_filename)

            image = Image.open(save_path)
            image_embeds = self.vision_encoder(image)
            self.user_image_context[user_id_str] = image_embeds
        else:
            await message.channel.send("Error: Uploaded file is not a common image format.")

    async def handle_text_query(self, message):
        user_id = str(message.author.id)

        if user_id in self.user_image_context:
            image_embeds = self.user_image_context[user_id]
        else:
            if user_id in self.user_image_map:
                image_path = self.user_image_map[user_id]
                image = Image.open(image_path)
                image_embeds = self.vision_encoder(image)
                self.user_image_context[user_id] = image_embeds
            else:
                await message.channel.send("No image in context. Please upload an image first.")
                return

        question = message.content.replace(f'<@{self.user.id}>', '').strip()
        if not question:
            question = DEFAULT_QUESTION

        response = self.text_model.answer_question(image_embeds, question)
        await message.channel.send(response)

        if collect_interactions_in_db:
            utils.insert_interaction(user_id, self.user_image_map[user_id], question, response)

    async def save_attachment(self, attachment):
        os.makedirs('processed_images', exist_ok=True)

        ext = os.path.splitext(attachment.filename)[1]
        quite_unique_filename = str(uuid.uuid4()) + ext
        save_path = os.path.join('processed_images', quite_unique_filename)

        await attachment.save(save_path)

        return save_path


bot = MoonsdreamDiscordBot(use_cpu=False)
bot.run(discord_bot_token)
