import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import openai

load_dotenv()
app = App(token=os.environ["SLACK_BOT_TOKEN"])
openai.api_key = os.environ["OPENAI_API_KEY"]

@app.event("app_mention")
def chatgpt_reply(event, say):
    input_message = event["text"]
    thread_ts = event.get("thread_ts") or None
    channel = event["channel"]
    input_message = input_message.replace("@U051VJ2D1DY", "")
    system_message = "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": input_message}
            ]
    )
    text = response["choices"][0]["message"]["content"]
    if thread_ts is not None:
        parent_thread_ts = event["thread_ts"]
        say(text=text, thread_ts=parent_thread_ts, channel=channel)
    else:
        say(text=text, channel=channel) 
    
@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
