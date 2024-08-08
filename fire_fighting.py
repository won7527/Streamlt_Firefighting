import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import time
import random

st.title("🔥불을 꺼보세요!!🔥")


def load_image(img_path):
    return Image.open(img_path)


if "map_arr" not in st.session_state:
    st.session_state.map_arr = [
        [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 3, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0],
    ]

if "move_count" not in st.session_state:
    st.session_state.move_count = 0

if "land_arr" not in st.session_state:
    st.session_state.land_arr = []
    st.session_state.fire_arr = []
    for y in range(len(st.session_state.map_arr)):
        for x in range(len(st.session_state.map_arr[0])):
            if st.session_state.map_arr[y][x] == 2:
                st.session_state.land_arr.append((y, x))
            elif st.session_state.map_arr[y][x] == 3:
                st.session_state.fire_arr.append((y, x))

if st.session_state.move_count >= 3:
    fire = random.choice(st.session_state.land_arr)
    st.session_state.map_arr[fire[0]][fire[1]] = 3
    st.session_state.move_count = 0


def generate_map(map_arr, img_arr):
    img_size = img_arr[0].size[0]
    map_img = Image.new("RGBA", (img_size * len(map_arr[0]), img_size * len(map_arr)))

    for x in range(len(map_arr[0])):
        for y in range(len(map_arr)):
            map_img.paste(img_arr[map_arr[y][x]], (x * img_size, y * img_size))
    return map_img


def generate_question_screen(map_arr, img_arr, map_img, text):
    img_size = img_arr[0].size[0]
    opaque_size = (len(map_arr[0]) * img_size, len(map_arr) * img_size)
    opaque_img = Image.new(
        "RGBA",
        opaque_size,
        (
            0,
            0,
            0,
            0,
        ),
    )
    opaque_draw = ImageDraw.Draw(opaque_img)
    opaque_draw.rectangle([(0, 0), opaque_size], fill=(0, 0, 0, 128))
    opaque_map = Image.alpha_composite(map_img, opaque_img)

    text_draw = ImageDraw.Draw(opaque_map)
    font_path = "Fonts/NotoSansKR-Black.ttf"
    font = ImageFont.truetype(font_path, 50)
    text_color = (255, 255, 255, 255)
    text_draw.text((100, 100), text, fill=text_color, font=font)
    return opaque_map


img_path_arr = [
    "Asset/background.png",
    "Asset/ladder.png",
    "Asset/land.png",
    "Asset/fire.png",
]
img_arr = [load_image(img_path) for img_path in img_path_arr]
rain_img = load_image("Asset/rain.png")
rain_size = rain_img.size[0]
if "is_rain" not in st.session_state:
    st.session_state.is_rain = False
player_img = load_image("Asset/clover.png")
if "player_loc" not in st.session_state:
    st.session_state.player_loc = [0, 6]
map_img = generate_map(st.session_state.map_arr, img_arr)
player_size = player_img.size[0]

if "point" not in st.session_state:
    st.session_state.point = 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("L_EXTINGUISH"):
        if (
            st.session_state.map_arr[st.session_state.player_loc[1]][
                st.session_state.player_loc[0] - 1
            ]
            == 3
        ):
            rain_loc = [
                (st.session_state.player_loc[0] - 1) * rain_size,
                st.session_state.player_loc[1] * rain_size,
            ]
            st.session_state.is_rain = "LEFT"
            map_img.paste(rain_img, rain_loc, rain_img)
    if st.button("LEFT"):
        if st.session_state.player_loc[0] - 1 < 0:
            pass
        elif (
            st.session_state.map_arr[st.session_state.player_loc[1]][
                st.session_state.player_loc[0] - 1
            ]
            == 0
        ):
            pass
        else:
            st.session_state.player_loc[0] -= 1
            st.session_state.move_count += 1
with col2:
    if st.button("UP"):
        if st.session_state.player_loc[1] - 1 < 0:
            pass
        elif (
            st.session_state.map_arr[st.session_state.player_loc[1] - 1][
                st.session_state.player_loc[0]
            ]
            == 0
        ):
            pass
        else:
            st.session_state.player_loc[1] -= 1
        dir = True
    if st.button("DOWN"):
        if st.session_state.player_loc[1] + 1 >= len(st.session_state.map_arr):
            pass
        elif (
            st.session_state.map_arr[st.session_state.player_loc[1] + 1][
                st.session_state.player_loc[0]
            ]
            == 0
        ):
            pass
        else:
            st.session_state.player_loc[1] += 1
        dir = False
with col3:
    if st.button("R_EXTINGUISH"):
        if (
            st.session_state.map_arr[st.session_state.player_loc[1]][
                st.session_state.player_loc[0] + 1
            ]
            == 3
        ):
            rain_loc = [
                (st.session_state.player_loc[0] + 1) * rain_size,
                st.session_state.player_loc[1] * rain_size,
            ]
            st.session_state.is_rain = "RIGHT"
            map_img.paste(rain_img, rain_loc, rain_img)
    if st.button("RIGHT"):
        if st.session_state.player_loc[0] + 1 >= len(st.session_state.map_arr[0]):
            pass
        elif (
            st.session_state.map_arr[st.session_state.player_loc[1]][
                st.session_state.player_loc[0] + 1
            ]
            == 0
        ):
            pass
        else:
            st.session_state.player_loc[0] += 1
            st.session_state.move_count += 1
with col4:
    st.write(f"💧POINT : {st.session_state.point}💧")
player_loc = [loc * player_size for loc in st.session_state.player_loc]
map_img.paste(player_img, player_loc, player_img)


if (
    st.session_state.map_arr[st.session_state.player_loc[1]][
        st.session_state.player_loc[0]
    ]
    == 1
):
    time.sleep(0.5)
    if dir:
        st.session_state.player_loc[1] -= 1
    else:
        st.session_state.player_loc[1] += 1
    st.rerun()
if st.session_state.is_rain:
    time.sleep(0.5)
    if st.session_state.is_rain == "LEFT":
        st.session_state.map_arr[st.session_state.player_loc[1]][
            st.session_state.player_loc[0] - 1
        ] = 2
    else:
        st.session_state.map_arr[st.session_state.player_loc[1]][
            st.session_state.player_loc[0] + 1
        ] = 2
    st.session_state.is_rain = False
    st.session_state.point += 1
    question_screen = generate_question_screen(
        st.session_state.map_arr, img_arr, map_img, "안녕하세요 반갑습니다"
    )

    st.image(question_screen)
else:
    st.image(map_img)
