# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from functools import partial
from requests.sessions import HTTPAdapter
from telegram.ext import Dispatcher
from telegram.ext.callbackcontext import CallbackContext
from telegram.files.inputmedia import InputMediaAudio
from telegram.update import Update
from utils.telegram import CustomChosenInlineResultHandler
from ganjoor import Ganjoor
import requests


def init(dispatcher: Dispatcher, ganjoor: Ganjoor):
    dispatcher.add_handler(CustomChosenInlineResultHandler(
        partial(chosen_song, ganjoor=ganjoor), pattern='#poem-songs:')
    )


def chosen_song(update: Update, context: CallbackContext, ganjoor: Ganjoor):
    poem_id = update.chosen_inline_result.result_id.split(':')[1]
    song_id = update.chosen_inline_result.result_id.split(':')[2]

    poem = ganjoor.find_poem_by_id(poem_id, songs=True)
    song = [song for song in poem.songs if str(song.id) == str(song_id)][0]
    track_url = song.track_url
    audio_url = None
    print(InputMediaAudio(song.track_url))
    if 'beeptunes' in track_url:
        audio_url = get_beeptunes_preview(track_url)
    elif 'spotify' in track_url:
        audio_url = get_spotify_preview(
            track_url.replace('/track', '/embed/track'))
    elif 'golha' in track_url:
        audio_url = get_golha_song(track_url)
    if audio_url:
        print(update.chosen_inline_result.inline_message_id)
        context.bot.edit_message_media(
            inline_message_id=update.chosen_inline_result.inline_message_id, media=InputMediaAudio(
                media=audio_url,
                title=song.track_name, caption=f"{song.artist_name}\n[{song.album_name} - {song.track_name}]({audio_url})", parse_mode='markdown'))

    context.bot.edit_message_reply_markup(
        inline_message_id=update.chosen_inline_result.inline_message_id)


def get_spotify_preview(embed_url: str):
    base_url = 'https://p.scdn.co/mp3-preview/'
    embed = requests.get(embed_url)
    try:
        return base_url+str(embed.content).split('mp3-preview%2F')[1].split('%3Fcid')[0]
    except Exception as e:
        return False


def get_beeptunes_preview(url: str):
    s = requests.session()
    s.mount(url, HTTPAdapter(max_retries=0))
    page = s.get(url)
    if page.status_code == 500:
        return False
    try:
        return str(page.content).split("previewHttpPath\":")[1].split("\"")[1]
    except Exception as e:
        return False


def get_golha_song(url: str):
    golha_base_url = 'https://golha.co.uk'
    s = requests.session()
    s.mount(url, HTTPAdapter(max_retries=1))
    page = s.get(url)
    if page.status_code == 500:
        return False
    try:
        return golha_base_url+str(page.content).split('mp3: "')[1].split("\"")[0]
    except Exception as e:
        return False
