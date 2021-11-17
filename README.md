<!--
 Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
 SPDX-License-Identifier: MIT
-->

# Telegram Persian Poetry Bot

## A telegram bot to view persian poetry using the Ganjoor API.

**Disclamer:** _This is an unofficial bot using the Ganjoor API. I am not affiliated with Ganjoor_

---

### Features:

- View all poems available on Ganjoor
- Search for a specific keyword inside a poem (can also specify poet and book)
- View Recitations, songs and images for the poem (Comments coming soon!)
- View similar poems based on rhythm and rhyme
- Listen to song previews if available
- Get a faal from hafez

![main menu](/assets/images/showcase/main_menu.png)
![faal](/assets/images/showcase/faal.png)
![poet](/assets/images/showcase/poet.png)

### Roamap:

- Adding new poets and poems
- Sending Recications and Comments to Ganjoor for poems
- Saving Favorite poems
- Login to Ganjoor
- ...

---

## Made with:

- [Ganjoor Web Service](https://github.com/ganjoor/GanjoorService "وب سرویس گنجینهٔ گنجور")

- [Ganjoor Api Wrapper](https://github.com/MmeK/ganjoor_api_wrapper "API wrapper written in Python for the Ganjoor Web Service")

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot "A Telegram API wrapper you can't refuse")

---

## Installation

- Clone this repo
- Install pipenv if you don't have it
- Install dependencies

```shell
$ git clone https://github.com/MmeK/ganjoor-telegram-bot.git
$ pip install pipenv
$ cd ganjoor-telegram-bot
$ pipenv install
```

## License

MIT License

Copyright (c) 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
