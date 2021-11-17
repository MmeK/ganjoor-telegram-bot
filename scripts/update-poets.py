# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT

import dataclasses
import json
from ganjoor import Ganjoor
POETS_JSON_PATH = 'assets/poets.json'
if __name__ == '__main__':
    go = Ganjoor()
    poets = go.get_all_poets()
    with open(POETS_JSON_PATH, mode='w') as poets_json:
        json_string = json.dump([
            {
                k[1:]:v for k, v in dataclasses.asdict(poet)
                .items()
            } for poet in poets], poets_json)
        # poets_json.write(json_string)
