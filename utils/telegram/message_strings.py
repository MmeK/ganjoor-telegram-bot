# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from ganjoor import Poem, Poet


def poem_string(poem: Poem, p_name='', c_name='') -> str:
    poet_name = str(poem.poet.name)+'\n' if poem.poet else p_name
    cat_name = str(poem.category.title) if poem.category else c_name
    poem_text = poet_name+cat_name + \
        ' - '+str(poem.title)+'\n\n'+str(poem)
    if len(poem_text) > 4096:
        beits = poem_text.split('\n\n')
        for i in range(len(beits)):
            if len(str(beits[:i+1])) > 4000:
                return str(
                    '\n\n'.join(beits[:i]))+"\n\nمطالعه‌ی متن کامل:\n" +\
                    'https://ganjoor.net'+poem.full_url
                break
    else:
        return poem_text


def poet_description_string(poet: Poet) -> str:
    if len(str(poet.description).encode('utf-8')) > 4096:
        paragraphs = str(poet.description).split('\n')
        for i in range(len(paragraphs)):
            if len(str(paragraphs[:i+1]).encode('utf-8')) > 4000:
                return str(
                    '\n\n'.join(paragraphs[:i]))+"\n\nمطالعه‌ی متن کامل:\n" +\
                    'https://ganjoor.net'+poet.full_url
                break
    else:
        return str(poet.description)
