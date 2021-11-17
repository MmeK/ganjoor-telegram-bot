# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from ganjoor import Poem
from ganjoor.models import Category, Poet
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def poem_keyboard(poem: Poem, m_id: str) -> InlineKeyboardMarkup:

    nav_poems = []
    if poem.previous_poem or poem.next_poem:
        if poem.previous_poem:
            nav_poems.append(InlineKeyboardButton(
                "<", callback_data='change_poem_'+str(poem.previous_poem.id)+"_"+str(m_id)))
        else:
            nav_poems.append(InlineKeyboardButton(
                "🚫", callback_data='no_poems'))
        if poem.next_poem:
            nav_poems.append(InlineKeyboardButton(
                ">", callback_data='change_poem_'+str(poem.next_poem.id)+"_"+str(m_id)))
        else:
            nav_poems.append(InlineKeyboardButton(
                "🚫", callback_data='no_poems'))

    images = []
    if poem.thumbnail_urls:
        images.append(
            InlineKeyboardButton(
                "🖼️ تصاویر", switch_inline_query_current_chat='#poem-images: '+str(poem.id)
            )
        )
    recitations = []
    if poem.recitations:
        recitations.append(
            InlineKeyboardButton(
                "🎤 دکلمه‌ها", switch_inline_query_current_chat='#poem-recitations: '+str(poem.id)
            )
        )

    songs = []
    if poem.songs:
        recitations.append(
            InlineKeyboardButton(
                "🎵 آهنگ‌ها", switch_inline_query_current_chat='#poem-songs: '+str(poem.id)
            )
        )

    similar = [
        InlineKeyboardButton(
            "اشعار هم‌وزن", switch_inline_query_current_chat='#poem_similar: '+poem.ganjoor_metre.rhythm
        )
    ]
    if poem.rhyme_letters:
        similar.append(
            InlineKeyboardButton(
                "اشعار هم‌آهنگ", switch_inline_query_current_chat='#poem_similar: '+poem.ganjoor_metre.rhythm+":"+poem.rhyme_letters
            )
        )

    keyboard = [
        [InlineKeyboardButton(
            "❤️", callback_data='add_fav_'+str(poem.id))],
        nav_poems,
        images,
        recitations,
        songs,
        similar
    ]
    return InlineKeyboardMarkup(keyboard)


def category_keyboard(cat: Category, m_id: str) -> InlineKeyboardMarkup:
    cat_poems = cat.poems
    poems_button = []
    if cat_poems:
        poems_button.append(InlineKeyboardButton(
            "اشعار", switch_inline_query_current_chat='#category_'+str(cat.id)+':\n'))

    children = []
    if cat.children:
        [children.append([InlineKeyboardButton(
            child.title, callback_data='category_'+str(child.id)+"_"+str(m_id))]) for child in cat.children]

    search_button = []
    back_button = []
    if cat.ancestors:
        back_button.append(InlineKeyboardButton(
            "بازگشت", callback_data='category_'+str(cat.ancestors[-1].id)+"_"+str(m_id)))
    else:
        search_button.append(InlineKeyboardButton(
            'جست و جو در اشعار این شاعر', switch_inline_query_current_chat='#poet_poems_'+str(cat.poet.id)+':\n'))
    keyboard = [
        search_button,
        back_button,
        poems_button,
        *children
    ]
    return InlineKeyboardMarkup(keyboard)


def poet_keyboard(poet: Poet, m_id: str) -> InlineKeyboardMarkup:
    cats = [InlineKeyboardButton(cat.title, callback_data='category_'+str(cat.id)+"_"+str(m_id))
            for cat in poet.category.children]

    search_button = [InlineKeyboardButton(
        'جست و جو در اشعار این شاعر', switch_inline_query_current_chat='#poet_poems_'+str(poet.id)+':\n')]
    keyboard = [
        [cat] for cat in cats
    ]
    keyboard.insert(0, search_button)
    return InlineKeyboardMarkup(keyboard)


def start_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(
            "فال حافظ", switch_inline_query_current_chat='#faal')],
        [InlineKeyboardButton(
            "جست و جو در شاعران", switch_inline_query_current_chat='#poet:\n')],
        [
            InlineKeyboardButton(
                "جست و جو در همه‌ی اشعار", switch_inline_query_current_chat='#poems:\n')]
    ]
    return InlineKeyboardMarkup(keyboard)


def loading_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="loading", callback_data='loading')]])
