import json
import os
import subprocess

from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

MUSIC = 0


def music(update, context):
    supported_patterns = ["youtube.com", "youtu.be"]
    url = update.message.text
    link_correct = False
    for sl in supported_patterns:
        if sl in url:
            link_correct = True

    if not link_correct:
        update.message.reply_text("Неправильне посилання. Спробуйте ще раз.")
        return ConversationHandler.END
    chat_id = update.message.chat_id
    message = context.bot.send_message(chat_id, "Почав завантажувати файл!")
    message_id = message.message_id
    # video_info = json.loads(os.popen(f"youtube-dlc -j {url}").read()) # title, uploader, creator
    # video_duration = os.popen(f"youtube-dlc --get-duration {url}").read() # video duration
    os.system(
        f'youtube-dlc --embed-thumbnail -x --audio-format mp3 --add-metadata --max-filesize 50.0m -i -o "%(title)s.%(ext)s" {url}')
    context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Ще трохи. Вже завантажую тобі.")
    fileNames = [i for i in os.listdir(os.getcwd()) if i.endswith('.mp3')]
    if len(fileNames) != 0:
        fileName = fileNames[0]
        context.bot.send_audio(update.message.chat_id, open(fileName, 'rb'))
        os.remove(fileName)
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)

    return ConversationHandler.END


def get_music(update, context):
    update.message.reply_text('Відправте посилання на відео. Якщо передумали, відправте /cancel.')

    return MUSIC


def cancel(update, context):
    update.message.reply_text('Буває. В інший раз.')

    return ConversationHandler.END


music_handler = ConversationHandler(
    entry_points=[CommandHandler("getmusic", get_music)],
    states={
        MUSIC: [MessageHandler(Filters.text & ~Filters.command, music), CommandHandler('cancel', cancel)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
