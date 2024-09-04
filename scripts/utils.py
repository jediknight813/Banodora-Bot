import re


def split_message_with_formatting(message, chunk_size):
    chunks = []
    current_chunk = ""
    words = re.findall(r"\S+|\s+", message)

    for word in words:
        if len(current_chunk) + len(word) <= chunk_size:
            current_chunk += word
        else:
            chunks.append(current_chunk)
            current_chunk = word

    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def is_number_and_less_than_500(input_string):
    try:
        number = float(input_string)
        if number <= 500:
            return True
        else:
            return False
    except ValueError:
        return False


async def set_bot_personality(client):
    for guild in client.guilds:
        await guild.me.edit(nick="Banodora")
    fp = open("Images/Banodora.png", "rb")
    pfp = fp.read()
    await client.user.edit(avatar=pfp)

    # sync the bot commands.
    await client.tree.sync()
