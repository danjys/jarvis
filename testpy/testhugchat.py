import os
from hugchat import hugchat
from hugchat.login import Login
#loading environment variables from .env files
from dotenv import load_dotenv

load_dotenv()

# Log in to huggingface and grant authorization to huggingchat
HUGCHAT_EMAIL = os.getenv('HUGCHAT_EMAIL')
HUGCHAT_PASSWD = os.getenv('HUGCHAT_PASSWD')
cookie_path_dir = "~/Library/Cookies/Cookies.binarycookies" # NOTE: trailing slash (/) is required to avoid errors
sign = Login(HUGCHAT_EMAIL, HUGCHAT_PASSWD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

# Create your ChatBot
chatbot = hugchat.ChatBot(cookie_path="engine/cookies.json")  # or cookie_path="usercookies/<email>.json"

message_result = chatbot.chat("Hi!") # note: message_result is a generator, the method will return immediately.

# Non stream
message_str: str = message_result.wait_until_done() # you can also print(message_result) directly. 
# get files(such as images)
file_list = message_result.get_files_created() # must call wait_until_done() first!

# tips: model "CohereForAI/c4ai-command-r-plus" can generate images :)

# Stream response
#for resp in chatbot.chat(
#    "Who are you?"
#):
#    print(resp)

# Web search
query_result = chatbot.chat("Who is Iron Man?")
print(query_result)
for source in query_result.web_search_sources:
    print(source.link)
    print(source.title)
    print(source.hostname)

# Create a new conversation
chatbot.new_conversation(switch_to = True) # switch to the new conversation

# Get conversations on the server that are not from the current session (all your conversations in huggingchat)
conversation_list = chatbot.get_remote_conversations(replace_conversation_list=True)
# Get conversation list(local)
conversation_list = chatbot.get_conversation_list()

# Get the available models (not hardcore)
models = chatbot.get_available_llm_models()

# Switch model with given index
chatbot.switch_llm(0) # Switch to the first model
chatbot.switch_llm(1) # Switch to the second model

# Get information about the current conversation
info = chatbot.get_conversation_info()
print(info.id, info.title, info.model, info.system_prompt, info.history)

# Assistant
assistant = chatbot.search_assistant(assistant_name="ChatGpt") # assistant name list in https://huggingface.co/chat/assistants
assistant_list = chatbot.get_assistant_list_by_page(page=0)
chatbot.new_conversation(assistant=assistant, switch_to=True) # create a new conversation with assistant

# [DANGER] Delete all the conversations for the logged in user
chatbot.delete_all_conversations()