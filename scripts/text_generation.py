import os
from dotenv import load_dotenv
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

TEXT_GENERATION_URL = os.getenv("TEXT_GENERATION_URL")
GOOGLE_API = os.getenv("GOOGLE_API")


def generate_google_summary(question, prompt):
    genai.configure(api_key=GOOGLE_API)
    # print(prompt)

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(
        f"You are a answer bot named Banodora, you will be given a chat to get data from to help answer the user question. You must format it for discord.\nSTART OF CHAT:\n{prompt}\nEND OF CHAT, User Question: "
        + question
        + "Format your response for discord, only respond with the summary and title for the section and nothing else."
    )

    if len(response.parts) >= 1:
        answer = str(response.parts[0])
        answer = answer.replace('text: "', "")
        answer = answer[:-2]
        return answer + "\n"
    else:
        return ""


def check_if_info_found(answer, question):
    genai.configure(api_key=GOOGLE_API)

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(
        f"Your job is to determine if it could answer the question, if it could answer the question, respond with YES, if it didn't respond with NO.\n"
        "Question: what is SVD?"
        + "\nAnswer: I'm sorry, but I cannot answer your question about SVD (Singular Value Decomposition) as I do not have access to the information in the chat you provided."
        + "\nDid that answer the question with the data the user asked for? respond with YES or NO only."
        + "\nResponse: NO"
        "Question: "
        + str(question)
        + "\nAnswer:"
        + str(answer)
        + "\nDid that answer the question with the data the user asked for? respond with YES or NO only."
        + "\nResponse: "
    )

    if len(response.parts) >= 1:
        answer = str(response.parts[0])
        answer = answer.replace('text: "', "")
        answer = answer[:-2]
        formatted_text = answer.replace("\\n", "\n")
        return formatted_text
    else:
        return ""


def generate_context_prompt(message_history, limit):
    chat_prompt = ""
    message_history.reverse()
    for index, message in enumerate(message_history):
        if index == limit:
            return chat_prompt
        name = message["author"].replace(".", "")
        # message_link = message["jump_url"]
        message_text = message["message"]
        chat_prompt += f"""{name}: {message_text}
"""

        if len(message["file_links"]) == 1:
            file_links = "\n".join(message["file_links"])
            chat_prompt += f"FILE LINK: {file_links}"

        if len(message["file_links"]) > 1:
            file_links = "\n".join(message["file_links"])
            chat_prompt += f"FILE LINKS: {file_links}"

    return chat_prompt
