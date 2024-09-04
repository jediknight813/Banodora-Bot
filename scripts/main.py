import discord
from dotenv import load_dotenv
from database import (
    create_message_log,
    get_collection_names,
    find_documents_in_channel_for_question,
)
from utils import (
    split_message_with_formatting,
    is_number_and_less_than_500,
)
from text_generation import (
    generate_context_prompt,
    generate_google_summary,
    check_if_info_found,
)
from discord import app_commands
from discord import ui
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
MY_GUILD = discord.Object(id=os.getenv("MY_GUILD"))


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.all()
client = MyClient(intents=intents)


messages_list = []


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    await client.tree.sync()


class Modal(ui.Modal, title="Ask Banodora a question."):
    firstfield = ui.TextInput(
        label="Question: ", placeholder="write here", style=discord.TextStyle.short
    )
    secondfield = ui.TextInput(
        label="Channel Name:",
        placeholder="Example: ad_comfyui",
        style=discord.TextStyle.short,
        required=True,
    )
    thirdfield = ui.TextInput(
        label="Messages to fetch:",
        placeholder="max (500)",
        default="100",
        style=discord.TextStyle.short,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        target_channel = interaction.guild.get_channel(interaction.channel_id)
        error = ""

        channel_names = get_collection_names()
        if str(self.secondfield) in channel_names:
            print("channel found")
        else:
            print("channel not found.")
            error = "\nError: channel could not be found."

        print(str(self.firstfield), str(self.secondfield), str(self.thirdfield))

        answer = """"""
        chunks = find_documents_in_channel_for_question(
            str(self.secondfield), str(self.thirdfield)
        )

        if len(chunks) >= 1 and is_number_and_less_than_500(str(self.thirdfield)):
            for chunk in chunks:
                prompt = generate_context_prompt(chunk, 20)
                google_answer = generate_google_summary(str(self.firstfield), prompt)
                print(google_answer)
                if (
                    "yes"
                    in check_if_info_found(google_answer, str(self.firstfield)).lower()
                ):
                    print("answer passed.")
                    answer += google_answer + "\n"

        # check if it failed.
        if answer == "":
            await target_channel.send("Something went wrong." + error)
        else:
            await target_channel.send(
                "<@"
                + str(interaction.user.id)
                + ">, here is what I could find to your question: '"
                + str(self.firstfield)
                + "'"
                + " in the "
                + str(self.secondfield)
                + " channel"
            )
            for chunk in split_message_with_formatting(answer, 1900):
                chunk = chunk.replace("\\n", "\n")
                await target_channel.send(chunk)


@client.tree.command(
    name="ask_banodora_question",
    description="Uses AI to search the server and to try and answer your question.",
)
async def create_ad_video(interaction: discord.Interaction):
    await interaction.response.send_modal(Modal())


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_object = {
        "channel_name": message.channel.name,
        "author": message.author.name,
        "jump_url": message.jump_url,
        "message": message.content,
        "created_at": message.created_at,
    }
    attachments = []
    for file_url in message.attachments:
        attachments.append(file_url.url)

    message_object["file_links"] = attachments
    print("added message.")
    create_message_log(message.channel.name, message_object)


client.run(BOT_TOKEN)
