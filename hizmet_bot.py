import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.filters import CommandStart

# ──────────────────────────────────────────────
#  КОНФИГ
# ──────────────────────────────────────────────
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
#  ДАННЫЕ КАТЕГОРИЙ
#  Как добавить PDF:
#  1) Запусти бота
#  2) Отправь боту PDF — он ответит file_id
#  3) Вставь file_id в список "files" нужной категории
# ──────────────────────────────────────────────
CATEGORIES = {
    "atlasiakids": {
        "title": "📚 AtlasiaKids",
        "description": (
            "📖 <b>Книги для детей / Books for children</b>\n\n"
            "Здесь собраны детские книги, сказки и обучающие материалы "
            "\n\n"
            "Here you will find children's books, fairy tales and educational materials.."
        ),
        "files": [
             {"name": "01 Atlasia Kids", "file_id": "BQACAgUAAxkBAAIBGGm8eCbomULbfHtRSt58Rq_T4UjWAAJEHAACtXPpVWC-7lH4VUS_OgQ"},
             {"name": "02 Atlasia Kids", "file_id": "BQACAgUAAxkBAAIBGmm8eGj6HeXzYy-YG13UXB2GY_IYAAJFHAACtXPpVdj6r38SsH_-OgQ"},
             {"name": "03 Atlasia Kids", "file_id": "BQACAgUAAxkBAAIBHGm8eOHv5-yG2MKZyFQvrBlACE5hAAJGHAACtXPpVdngSVrufXOsOgQ"},
             {"name": "04 Atlasia Kids", "file_id": "BQACAgUAAxkBAAIBHmm8eQreqYViOyzTFhIK_zWKi1ARAAJHHAACtXPpVXbsrntwsAEZOgQ"},
             {"name": "05 Atlasia Kids", "file_id": "BQACAgUAAxkBAAIBImm8osntwpOefzLlPaCDnV7zS0m7AAKHHAACtXPpVVFLs3P8AAEWrjoE"},
             {"name": "06 Atlasia Kids", "file_id": "BQACAgUAAxkBAAIBJGm8o-tP90v6uUVmJvHu0sMVEmz_AAKVHAACtXPpVYX1XBZHRYq9OgQ"},
             {"name": "07 Atlasia Kids", "file_id": "BQACAgUAAxkBAAIBJmm8pB6hn0li9boU-9duiXKSKhoaAAKXHAACtXPpVfI9FdKrdTGzOgQ"},
             {"name": "08 Atlasia Kids", "file_id": "BQACAgUAAxkBAAIBKGm8pCeR9ejGJSPBTGr3VZOf7qg5AAKYHAACtXPpVZRwZKU-b728OgQ"},
             {"name": "09 Atlasia Kids", "file_id": "BQACAgUAAxkBAAIBKmm8pGamElErnAABGM7Ninwmj-rRDAACmhwAArVz6VUkn7LFgKDn7zoE"},
             {"name": "10 Atlasia Kids", "file_id": "BQACAgUAAxkBAAIBLGm8pNIs-hwinwSh_8yBzc4_ofpGAAKbHAACtXPpVc9VOZo_7qN-OgQ"},
             {"name": "11 Atlasia Kids", "file_id": "BQACAgUAAxkBAAIBLmm8pN5it2yaNdp2rYPw-QWZ7kCoAAKeHAACtXPpVThZSquqce7AOgQ"},
             {"name": "12 Atlasia Kids", "file_id": "PLACEHOLDER_FILE_ID_FIX_ME"},
                 

        ],  
        "stories": [
            "🌟 <b>О разделе AtlasiaKids</b>\n\nЗдесь будут детские книги, "
            "сказки и истории для самых маленьких читателей.",
        ]
    },

    "books_hizmet": {
        "title": "📗 Hizmet Movement",
        "description": (
            "📚 <b>Книги о движении Хизмет</b>\n\n"
            "Книги, статьи и материалы о движении Гюлена и Хизмет "
            "на разных языках мира."
        ),
        "files": [
            # {"name": "An Introduction to Hizmet", "file_id": "BQACAgI..."},
            # {"name": "Hizmet Explained",           "file_id": "BQACAgI..."},
        ],
        "stories": [
            "📘 <b>О движении Хизмет</b>\n\nХизмет — это гражданское движение, "
            "вдохновлённое идеями Фетхуллаха Гюлена, направленное на образование, "
            "диалог и служение обществу.",
        ]
    },

    "presentations": {
        "title": "🖥 Presentations",
        "description": (
            "🎯 <b>Презентации</b>\n\n"
            "Учебные и информационные презентации на различные темы."
        ),
        "files": [
             # NOTE: Many file_ids below are duplicated from the first one. Please replace with unique file_ids for each file.
             {"name": "1) Azan", "file_id": "BQACAgUAAxkBAAIBRGm90gFQTDsAAVrsvEbbWcSdZ7kweAACXxsAAkav8FXrXeenlTNC5joE"},
             {"name": "2) Al-Fatiha", "file_id": "BQACAgUAAxkBAAIBR2m90sQQPVHNetEeYL55SbF-EzMAA2IbAAJGr_BVid8Juv0-do46BA"},
             {"name": "3) Basics of Islam", "file_id": "BQACAgUAAxkBAAIBSWm900973DpUuPD0vpkORF5i9gJFAAJjGwACRq_wVZ4HgK8JYrO9OgQ"},
             {"name": "4) Beautiful Women in Islamic History ", "file_id": "BQACAgUAAxkBAAIBS2m9058RadH40HGA8956hNiXaL9dAAJkGwACRq_wVW24XB19i-V5OgQ"},
             {"name": "5) Belief in Angels", "file_id": "PLACEHOLDER_FILE_ID_FIX_ME"},
             {"name": "6) Belief in Books", "file_id": "BQACAgUAAxkBAAIBT2m908m63ViF9mL3UsJZJpvoAXTfAAJmGwACRq_wVUpZMJZr0hmZOgQ"},
             {"name": "7) Belief in God,  Pillars of Islam", "file_id": "BQACAgUAAxkBAAIBUWm91ElfXXBAzY0JmDza3Tmh8_ttAAJnGwACRq_wVWqaagHGvLSrOgQ"},
             {"name": "8) Belief in God, Proofs of Existence of the Creator", "file_id": "BQACAgUAAxkBAAIBVWm91LxK_3aRqfJK5jOg2qxUCy38AAJpGwACRq_wVanSx29HsCIaOgQ"},
             {"name": "9) Belief in Hereafter", "file_id": "BQACAgUAAxkBAAIBVWm91LxK_3aRqfJK5jOg2qxUCy38AAJpGwACRq_wVanSx29HsCIaOgQ"},
             {"name": "10) Belief in life after death", "file_id": "BQACAgUAAxkBAAIBV2m91Q0tYwXd053G8635crVg_WSOAAJqGwACRq_wVWlKCMrgUinrOgQ"},
             {"name": "11) Belief in Prophets", "file_id": "BQACAgUAAxkBAAIBWWm91cBOFBokrzDJP86L_3-fLaBoAAJrGwACRq_wVQ1aXdSG7bIdOgQ"},
             {"name": "12) Belief in the last day", "file_id": "BQACAgUAAxkBAAIBW2m91c_Rzs9jXmpfCTDEH9Nm2OZcAAJsGwACRq_wVVps58bL1gdVOgQ"},
             {"name": "13) Belief in the Prophets", "file_id": "BQACAgUAAxkBAAIBXWm91ddnBIP-R6rH7BOS6iSomX_VAAJtGwACRq_wVS6n807J7N7cOgQ"},
             {"name": "14) Belief in Allah", "file_id": "BQACAgUAAxkBAAIBX2m91kMK_hbZ7Ll_WoTsrE4qjV6mAAJuGwACRq_wVYLmgXkyjjt4OgQ"},
             {"name": "15) Believe in Allah and the Last Day", "file_id": "BQACAgUAAxkBAAIBYWm9_iOGqPxMaVhVSfU7RQUOrudJAALdGwACRq_wVYJvcVzAgww5OgQ"},
             {"name": "16) Believing in Angels, Pillars of Faith ", "file_id": "BQACAgUAAxkBAAIBY2m-AAHycZ_wr7u7_asAAS4_WHkjcesAAuAbAAJGr_BVVczNKQjiBbQ6BA"},
             {"name": "17) Believing in Books, Pillars of Faith", "file_id": "BQACAgUAAxkBAAIBZWm-AaYmjIvikdXi-DyCa1c8AoTjAALhGwACRq_wVUoYOB6_zEsDOgQ"},
             {"name": "18) Believing in Hereafter, Pillars of Faith", "file_id": "BQACAgUAAxkBAAIBZ2m-AdAFXvew9b5VlAc06MjeGzo7AALjGwACRq_wVXbfumLQgaXGOgQ"},
             {"name": "19) Believing In Prophets, Pillars of Faith", "file_id": "BQACAgUAAxkBAAIBaWm-Adrb2N1J7xDoYixEPg3R0i4SAALkGwACRq_wVR0FDXoZ8UhBOgQ"},
             {"name": "20) Believing_in_Qada_Decree_and_Qadar_Destiny", "file_id": "BQACAgUAAxkBAAIBa2m-Ak7JZG6Hq8M2KCgQqDz0-Ad2AALmGwACRq_wVbybqy7zOo8jOgQ"},
             {"name": "21) Bismillah", "file_id": "BQACAgUAAxkBAAIBbWm-Ao_kLI51zNhe7qhqFVo2-vRFAALnGwACRq_wVSf_P2uOUWiyOgQ"},
             {"name": "22) Compulsory acts before Salat", "file_id": "BQACAgUAAxkBAAIBb2m-AwtNVNmYpZI86rimK8oXrGH_AALoGwACRq_wVShJFdIBAWeWOgQ"},
             {"name": "23) Daily Life of the Prophet", "file_id": "BQACAgUAAxkBAAIBcWm-A3rTEnviRnjH5OP3jk0cp44cAALqGwACRq_wVQT8y1sv5i1pOgQ"},
             {"name": "24) Despair_2", "file_id": "BQACAgUAAxkBAAIBc2m-A-xbHBKemK02U8uTHKMDvHnFAALtGwACRq_wVQubA564VpsvOgQ"},
             {"name": "25) Divinewill", "file_id": "BQACAgUAAxkBAAIBemm-FpbT0HxgI1cPYncLsSiYxdgPAAIfHAACRq_wVWQLYnLMe-CWOgQ"},
             {"name": "26) Ego and I", "file_id": "BQACAgUAAxkBAAIBfGm-F7Eao7N5SG2AkjNwr_d8lfhqAAIgHAACRq_wVb5vuX4PIyDoOgQ"},
             {"name": "27) Esmaul Husna", "file_id": "BQACAgUAAxkBAAIBfmm-F7qTFKnyY4OY2vuU0AmZAhDWAAIhHAACRq_wVenSGZ_SnYahOgQ"},
             {"name": "28) Essentials of Islamic Faith", "file_id": "BQACAgUAAxkBAAIBgmm-GCva-1hFn_LHjrLzMtJX_V2mAAIjHAACRq_wVSrb1ehOZYQ-OgQ"},
             {"name": "29) Essential of Islamic Faith(2", "file_id": "BQACAgUAAxkBAAIBhGm-GIv92yIl7cLh9Y9cDo8nssH2AAInHAACRq_wVfdETlrx4HtlOgQ"},
             {"name": "30) Evening Prayer", "file_id": "BQACAgUAAxkBAAIBhmm-GKiYjxQeerXhq99DVhWQDLZDAAIoHAACRq_wVWv797hnKqIMOgQ"},
             {"name": "31) Extremism and Islam", "file_id": "BQACAgUAAxkBAAIBiGm-GK8ISWsFsF5h5EUEsTo4eMM-AAIpHAACRq_wVULa5URMcXGuOgQ"},
             {"name": "32) Fasting and Developing Self-Control", "file_id": "BQACAgUAAxkBAAIBimm-GPrS1aHlvXEcQAESmSrfryXWAAIqHAACRq_wVWBkXECM7J99OgQ"},
             {"name": "33) Fasting", "file_id": "BQACAgUAAxkBAAIBjGm-GRUnlvuOXJkEXZUPICN4QN8eAAIrHAACRq_wVcXTm8evzBGmOgQ"},
             {"name": "34) Good and evil in Islam", "file_id": "BQACAgUAAxkBAAIBjmm-GS7OoO6-AXvEtq8zEfBoh6KaAAItHAACRq_wVT8VTTUNgX2FOgQ"},
             {"name": "35) Halal and  Haram in Islam", "file_id": "BQACAgUAAxkBAAIBkGm-GUQAAVzMPx9rIfBdTdljTQqNUwACLhwAAkav8FWgpNvMZmCNFToE"},
             {"name": "36) Helal Haram in Islam in Brief Explanation", "file_id": "BQACAgUAAxkBAAIBlGm-Gfvs4HYtzYFyM7R5vh1Ri0AYAAIzHAACRq_wVfAkjZZ5o4tdOgQ"},
             {"name": "37) Hereafter", "file_id": "BQACAgUAAxkBAAIBlmm-GiJ0hpgWKg9I8wk6m13owQvBAAI2HAACRq_wVdgow0d1tNGXOgQ"},
             {"name": "38) Hereafter(2)", "file_id": "BQACAgUAAxkBAAIBmGm-Gi0U6xOS_GQI1uWArZxcmAABfwACNxwAAkav8FVk479DrAnIoDoE"},
             {"name": "39) How to Pray (Salaat) Fards, inside the Salat", "file_id": "BQACAgUAAxkBAAIBnGm-GrPzQu6sBb6boRAzv4JUUSaqAAI5HAACRq_wVRk6oDbJx26eOgQ"},
             {"name": "40) Islam 101", "file_id": "BQACAgUAAxkBAAIBnmm-Gwc53fd74mpUeGPYjEcjbfMHAAI7HAACRq_wVV5yDDl3sj9aOgQ"},
             {"name": "41) Islam and Brief", "file_id": "BQACAgUAAxkBAAIBoGm-Gzid4HTOgU-IQtIGrrZ_4Y3RAAI9HAACRq_wVedKdxzNPCyPOgQ"},
             {"name": "42) Islam and Peace", "file_id": "BQACAgUAAxkBAAIBomm-G_-mHxLphW_4cSuG_jZhqFPOAAJCHAACRq_wVVshkN9vFr5KOgQ"},
             {"name": "43) Islam Essentials", "file_id": "BQACAgUAAxkBAAIBpGm-HCAtlve1UddoYZ5HA-zZkbsgAAJDHAACRq_wVQap28ftim9fOgQ"},
             {"name": "44) Islam Religion and Peace", "file_id": "BQACAgUAAxkBAAIBpmm-HCRWfL79xjLSOYO3F_UqkLEkAAJEHAACRq_wVR5pzwHGfOF7OgQ"},
             {"name": "45) Islam-101", "file_id": "BQACAgUAAxkBAAIBqGm-HCkx6rW9UDzHG6liBl_JLTv6AAJFHAACRq_wVQWCsv-rfhWEOgQ"},
             {"name": "46) Islamic Perspective on Dialog", "file_id": "BQACAgUAAxkBAAIBqmm-HbhIIQy9_7XMu-MeOcTbXgl1AAJKHAACRq_wVTZWv27C3hlbOgQ"},
             {"name": "47) Isra and Miraj", "file_id": "BQACAgUAAxkBAAIBrGm-Hb6--Q3Vju0yBO0DJep3fG1hAAJLHAACRq_wVWqzQy_8an-mOgQ"},
             {"name": "48) Jihad", "file_id":"BQACAgUAAxkBAAIBrmm-HfRPxAQiYru04lfl8eBQhB2vAAJNHAACRq_wVfO6V0KL8739OgQ"},
             {"name": "49) Jihad 2", "file_id": "BQACAgUAAxkBAAIBsGm-HfwHbMRfiFx3NXJP4gsTcW-nAAJPHAACRq_wVf0EjrD999VwOgQ"},
             {"name": "50) Kadder 1", "file_id": "BQACAgUAAxkBAAIBsmm-HqeukF0k-A50u2Luve8_jD6yAAJQHAACRq_wVSoMmYSpnfvnOgQ"},
             {"name": "51) Kadder 2", "file_id": "BQACAgUAAxkBAAIBtGm-HqzTbzSHtqFQ3NNBcsft260yAAJRHAACRq_wVdeN6vFSD-EAAToE"},
             {"name": "52) Khadija (RA)", "file_id": "BQACAgUAAxkBAAIBtmm-H5LgTo6aQa3cU9WPfw8h-HpjAAJVHAACRq_wVU7Z397ziQ54OgQ"},
             {"name": "53) Know Our Prophet Mohammed PBUH", "file_id": "BQACAgUAAxkBAAIBuGm-H8Ah8ba7QswcfXviI1Sru3AiAAJWHAACRq_wVSJqRCZqAmniOgQ"},
             {"name": "54) Letter’s of The Prophet", "file_id": "BQACAgUAAxkBAAIBumm-H-PT9EQqloVq29P5XsKvkiAPAAJYHAACRq_wVWAMRVwlylmgOgQ"},
             {"name": "55) Love of God and Sufism", "file_id": "BQACAgUAAxkBAAIBvGm-IBpGt062WrAbma_VtLtbQ7CTAAJZHAACRq_wVc3iw0-WODjiOgQ"},
             {"name": "56) Mary & Women in Islam", "file_id": "BQACAgUAAxkBAAIBvmm-IDuxdmy1tDesu7ZrQ8sK-jYwAAJaHAACRq_wVWYAAVtHrz8LnzoE"},
             {"name": "57) Meaning of Ramazan", "file_id": "BQACAgUAAxkBAAIBwGm-IFcNV2AAAVi3xTI3EkcypngBwAACXBwAAkav8FVmRFzYZKiLIToE"},
             {"name": "58) Model of Education", "file_id": "BQACAgUAAxkBAAIBwmm-IIxJau2QdUHD3T3cAp63EhC4AAJhHAACRq_wVbSMR7LpKVKYOgQ"},
             {"name": "59) Model and Challenges of Education 2", "file_id": "BQACAgUAAxkBAAIBxGm-II_QlJBq3u93OMxLAdup8p1CAAJiHAACRq_wVWwpHevSf_MiOgQ"},
             {"name": "60) Nature", "file_id": "BQACAgUAAxkBAAIBxmm-INBGpxpiH0Jljj7Iy_su2HU7AAJlHAACRq_wVT6m_3KrJ-_UOgQ"},
             {"name": "61) Natural Disasters", "file_id": "BQACAgUAAxkBAAIByGm-INQ8rij7ckA0rS8H1DfwiVjlAAJmHAACRq_wVTRcbUL3-aUeOgQ"},
             {"name": "62) Natural Disasters KADDER_3", "file_id": "BQACAgUAAxkBAAIBymm-IPrZyBmuaoAfq67z3nIf8X50AAJoHAACRq_wVQbY09K2Vl8NOgQ"},
             {"name": "63) Nefs Ene Sin", "file_id": "BQACAgUAAxkBAAIBzmm-ItvteR9T5PO1p0Xfibz7wvnaAAJtHAACRq_wVSGMIJ8sk50nOgQ"},
             {"name": "64) Neighborhood", "file_id": "BQACAgUAAxkBAAIB0Gm-It-dXz6-pM6cG3fCq6VEkyxHAAJuHAACRq_wVbiX48bGmf7ROgQ"},
             {"name": "65) Patience", "file_id": "BQACAgUAAxkBAAIB0mm-IuRbQypvs4AfUD7n04VwJBHgAAJvHAACRq_wVZqelqrxYvxtOgQ"},
             {"name": "66) Prayer", "file_id": "BQACAgUAAxkBAAIB1Gm-Iu1tk7mLRMm0BpMAAdVQWBmkvwACcBwAAkav8FV4MsDOhuzE1ToE"},
             {"name": "67) Prophet", "file_id": "BQACAgUAAxkBAAIB1mm-JLxWrS8wHSIiofWYQg8OPEKaAAJ3HAACRq_wVUH7Y26aoD9OOgQ"},
             {"name": "68) Purpose of Life", "file_id": "BQACAgUAAxkBAAIB2Gm-JXqjKStN1aAqWM7oo4DnW2kjAAJ4HAACRq_wVeq1M8LcJF6lOgQ"},
             {"name": "69) Questions and Answers on Islam", "file_id": "BQACAgUAAxkBAAIB2mm-JYUtxUSVa8KhCqeiL60vAsB2AAJ5HAACRq_wVV8MaR6KUbsrOgQ"},
             {"name": "70) Prophets", "file_id": "BQACAgUAAxkBAAIB3Gm-JdrOdQUFL2aXzVuij-Wz0SYEAAJ7HAACRq_wVQGA_gHuWOTCOgQ"},
             {"name": "71) Ramazan", "file_id": "BQACAgUAAxkBAAIB4Gm-KqdmgxWWD6JnCu--m-r_za4vAAKDHAACRq_wVXyxpSuu0hUYOgQ"},
             {"name": "72) Ramadan and Fasting", "file_id": "BQACAgUAAxkBAAIB3mm-KqMRAaKNgNpXvg3DOO9oaZq8AAKCHAACRq_wVZilESFnxF5MOgQ"},
             {"name": "73) Resurrection", "file_id": "BQACAgUAAxkBAAIB4mm-KuH7dky_CQhcYS9xwUwC86iqAAKFHAACRq_wVc41QJSt3BMMOgQ"},
             {"name": "74) Resurrection Kadder Presentation", "file_id": "BQACAgUAAxkBAAIB5Gm-KuqaN16b8f5krb4Xnm13WlvCAAKGHAACRq_wVRE4mIP3AVp0OgQ"},
             {"name": "75) Salat Prayer As Pillar", "file_id": "BQACAgUAAxkBAAIB5mm-KzMgUfRkSid0K470cbt6y21oAAKHHAACRq_wVb20UqKfUCX3OgQ"},
             {"name": "76) Introduction, Creation and Oneness of Allah", "file_id": "BQACAgUAAxkBAAIB6mm-K6IFG9KZFkW6fczKUbCCSr4uAAKKHAACRq_wVV5g93yJgK4BOgQ"},
             {"name": "78) Sickness of Waswasa", "file_id": "BQACAgUAAxkBAAIB72m-P8gOspVq49X6nDYpV1st1ZOFAAIbHQACRq_wVbFTK0t6DUwvOgQ"},
             {"name": "79) Sincerity 1", "file_id": "BQACAgUAAxkBAAIB8Wm-QCSyrYoo7WwN41410_YSNwSCAAIcHQACRq_wVexnvL_NQq4wOgQ"},
             {"name": "80) Sincerity 2", "file_id": "BQACAgUAAxkBAAIB82m-QDA67chI0_vqqYt-N0ZZPEiPAAIdHQACRq_wVfHfRF1Y8ILlOgQ"},
             {"name": "81) Sufism", "file_id": "BQACAgUAAxkBAAIB9Wm-QHdijtzm2sCs-a2Mhi9le0LYAAIeHQACRq_wVet0aNtHfkWdOgQ"},
             {"name": "82) Sufism 2", "file_id": "BQACAgUAAxkBAAIB92m-QHzenywE-FGAcjE9m1rsuDVWAAIfHQACRq_wVToYNVGLqnPEOgQ"},
             {"name": "83) Supplication", "file_id": "BQACAgUAAxkBAAIB-Wm-QPUl-uqUmi6BiNu5AjGw4BySAAIgHQACRq_wVfcdxsbMQJOrOgQ"},
             {"name": "84) Supplication Of Job", "file_id": "BQACAgUAAxkBAAIB-2m-QRjlS4RUfVcEe7h3H2z9J8TXAAIhHQACRq_wVXOFxwvoVUc6OgQ"},
             {"name": "85) Supplication Of Job_2", "file_id": "BQACAgUAAxkBAAIB_Wm-QWZE56a-Bl2ZnZqSXoH82shbAAIiHQACRq_wVcIugOyscj0yOgQ"},
             {"name": "86) Supplication Of Jonah", "file_id": "BQACAgUAAxkBAAIB_2m-QWk7y0WgUjE32hVUyUvsPn2vAAIjHQACRq_wVRAhnH338h23OgQ"},
             {"name": "87) Supplication_2", "file_id": "BQACAgUAAxkBAAIBRGm90gFQTDsAAVrsvEbbWcSdZ7kweAACXxsAAkav8FXrXeenlTNC5joE"},
             {"name": "88) Surah al Fatihah Tafseer Explaination ", "file_id": "BQACAgUAAxkBAAICA2m-QiE3q25Y_NFfi6TSwNEZ6rHfAAImHQACRq_wVc_rrb3rP-ozOgQ"},
             {"name": "89) The Books that defined humanity", "file_id": "BQACAgUAAxkBAAICBWm-Qk5x3YLZDtBh9maT9z55bly7AAInHQACRq_wVXsk2-g5-WfEOgQ"},
             {"name": "90) The Essence of Wisdom", "file_id": "BQACAgUAAxkBAAICB2m-QlNNJfTpp4J__lF0eK30JpEuAAIoHQACRq_wVY6_CtF1cp7VOgQ"},
             {"name": "91) The Fast of Sacrifice and Haj", "file_id": "BQACAgUAAxkBAAIBRGm90gFQTDsAAVrsvEbbWcSdZ7kweAACXxsAAkav8FXrXeenlTNC5joE"},
             {"name": "92) The Gathering", "file_id": "BQACAgUAAxkBAAICC2m-QuNdE8AhSKBLW78BAAHybs_Y-wACKh0AAkav8FVrK1lBI1ofkzoE"},
             {"name": "93) The last day -Deccal Sufyan Mesih", "file_id": "BQACAgUAAxkBAAICDWm-QyxH7Lipxtwf2uI69jpjovcEAAIrHQACRq_wVSwxhgABsY7gYjoE"},
             {"name": "94) The Necessity of Religion", "file_id": "BQACAgUAAxkBAAICD2m-Q1REArq6QeWAuzcfZuPoLwZhAAIsHQACRq_wVRmhZlM8rPMuOgQ"},
             {"name": "95) The Quran and Science", "file_id": "BQACAgUAAxkBAAICEWm-Q1cfepWtdk2BxJAZfc5vk9quAAItHQACRq_wVSk5DRmbR0rvOgQ"},
             {"name": "96) The Quran", "file_id": "BQACAgUAAxkBAAICE2m-Q1yRFROpU2r825GPhi2up5mNAAIuHQACRq_wVekbhRoWB9LzOgQ"},
             {"name": "97) The Value of the Prescribed Prayers", "file_id": "BQACAgUAAxkBAAIBRGm90gFQTDsAAVrsvEbbWcSdZ7kweAACXxsAAkav8FXrXeenlTNC5joE"},
             {"name": "98) The Worth of Bismillah", "file_id": "BQACAgUAAxkBAAICF2m-Q_ZJyNWCb_MEMnxr_wllRhhKAAIwHQACRq_wVVonWgqokbydOgQ"},
             {"name": "99) True Duty of Men", "file_id": "BQACAgUAAxkBAAICGWm-REWo-tTtsuzLbPj0800V5B6OAAIxHQACRq_wVeBPbGTj7462OgQ"},
             {"name": "94) Understanding", "file_id": "BQACAgUAAxkBAAICG2m-RJ_xqF1_3HrzvkKX7lADD7pZAAI5HQACRq_wVU7NuX_ptFzqOgQ"},
             {"name": "95) Understanding Islam", "file_id": "BQACAgUAAxkBAAICHWm-RKQw97Lrh4l-nOV-Cid9LSU1AAI6HQACRq_wVWUps92XxSz3OgQ"},
             {"name": "96) Why_are_the_non_muslim_countries_the_more_powerful", "file_id": "BQACAgUAAxkBAAICH2m-RTgLAAHJJLKLgHM0wolW_ZAsJwACPh0AAkav8FW2GsAnYU_2tjoE"},
             {"name": "97) Why_do_we_believe,_Types_of_Disbelief", "file_id": "BQACAgUAAxkBAAICIWm-RT5AGlvqX2AThx-EI2g71VTYAAI_HQACRq_wVUZC6uCpLXe0OgQ"},
             {"name": "98) Woman in Islam", "file_id": "BQACAgUAAxkBAAICI2m-RZombgf3h-kjH2OP5fzC2yyPAAJCHQACRq_wVUBos8Rd-ZdHOgQ"},
             {"name": "99) Woman to Woman in Islam", "file_id": "BQACAgUAAxkBAAICJWm-RcV-8jsZNEPEV_l8z_N_GRiAAAJDHQACRq_wVZ9sQFZXR476OgQ"},
             {"name": "100) Women an Islamic perspective", "file_id": "BQACAgUAAxkBAAICJ2m-RcgMgxi7Pa3v_igfth5DJWFQAAJEHQACRq_wVcOnYFjCLxq9OgQ"},
             {"name": "101) Worship", "file_id": "BQACAgUAAxkBAAICK2m-Rm4xbtAmZ-Bbp0n1IoVe7uHzAAJHHQACRq_wVQy73HPzXbD7OgQ"},
             {"name": "102) Worship 2", "file_id": "BQACAgUAAxkBAAICLWm-Ro9GC4bLp8CvK5BPyIaN0Rq9AAJJHQACRq_wVbVJfT-WHDDSOgQ"},
             {"name": "103) Worship 2_2", "file_id": "BQACAgUAAxkBAAICMWm-RwtutzvFxoqESDKcw_AVUOpqAAJMHQACRq_wVT9kAw6BcopNOgQ"},
             {"name": "104) Zakah", "file_id": "BQACAgUAAxkBAAICL2m-RvuZZGyus0vMaloexs0Z9aheAAJLHQACRq_wVYNkk0d4gXQZOgQ"},


        ],
        "stories": [
            
        ]
    },

    "reflection": {
        "title": "🎙 Reflection Lecture Series",
        "description": (
            "🎤 <b>Серия лекций Reflection</b>\n\n"
            "Лекции и выступления на духовные, "                                     
            "образовательные и научные темы."                                                                                                                              
        ),
        "files": [                                                                                                                                                                  
            # {"name": "", "file_id": "BQACAgI..."},
            #
            #
            # 
            # 
            # 
            # 
            # 
            #                          
        ],
        "stories": [
            "🎤 <b>Лекция 1 — Размышления о жизни</b>\n\nКраткое описание первой лекции из серии Reflection.",
            "🎤 <b>Лекция 2 — Путь к знаниям</b>\n\nКраткое описание второй лекции из серии Reflection.",
        ]
    },                                                   
                                                         
    "risale_i_nur": {                                
        "title": "📜 Risale-i Nur",
        "description": (
            "✨ <b> Risale-i Nur — works of Said Nursi</b>\n\n"
            "The Complete Works of Badiuzzaman Said Nursi "                                                                                                                                                                                                    
            "PDF книги - PDF books"
        ),
        "files": [
             {"name": "The Words",      "file_id": "BBQACAgUAAxkBAAPoabgSkmEruEwsg7cVSVVX14fzM7UAAuMdAAIB48FV5H9a4Zi31pg6BA"},
             {"name": "The Letters ",     "file_id": "BQACAgUAAxkBAAPYabgCtBx7j7fEw3ST0Foro4fXmgsAArkdAAIB48FVwE1TYxS3tX46BA"},
             {"name": "The Rays",        "file_id": "BQACAgUAAxkBAAPaabgC9L3wKBOXV2k8dC0eMHhGuZgAArsdAAIB48FVk736Tnzcy0I6BA"},
             {"name": "The Staff of Moses_ Reflections",   "file_id": "BQACAgUAAxkBAAPcabgDKCUxZAPcJ8cLgy6IPntE9lMAAr0dAAIB48FVJS9PJE7glZ86BA"},
             {"name": "The Light of Belief ",   "file_id": "BQACAgUAAxkBAAPeabgDLInEm58j50eOXeQW8L_kWRoAAr4dAAIB48FVT7brCLSZBaE6BA"},
             {"name": "The Guide for the Youth",         "file_id": "BQACAgUAAxkBAAPgabgDMrGhF3CsUpb9qdfyUP9BwAsAAr8dAAIB48FVcrNYQDINWNk6BA"},
             {"name": "The Flashes",              "file_id": "BQACAgUAAxkBAAPkabgD5NNT_JIz9pVYxpnReL_DB0cAAsIdAAIB48FV2-GoUvJ7itw6BA"},
             {"name": "Message for The Sick",          "file_id": "BQACAgUAAxkBAAPiabgDtjws_qUU6wPV_8SFYrS5ZegAAsEdAAIB48FVgpNTcxBrnns6BA"},
             {"name": "The Reasonings ", "file_id": "BQACAgUAAxkBAAPmabgEJBUhjB_DniqxZ8eNDc58L3sAAsMdAAIB48FVH9JHHxjqkvo6BA"},
             {"name": "Al Mathnawi Al Nuri", "file_id": "BQACAgUAAxkBAAP-absiVBpSPSkMqzUVDISIxIG9HV4AAtgjAAJaO9lVUINfYkhPK8s6BA"},
             {"name": "The Flashes of Light", "file_id": "BQACAgUAAxkBAAPjabgEJqj8n9sXo2a7l3mLh5sH4AAsMdAAIB48FVH9JHHxjqkvo6BA"},
             {"name": "The Science in Islam", "file_id": "BQACAgUAAxkBAAIBN2m9gsTuJjF2H9H5rAO5m8xoymS9AAJ9HgACtXPxVZ0-uggWBRCKOgQ"},
             {"name": "Gleams Of Truth", "file_id": "BQACAgUAAxkBAAIBPGm9hdsaBE3XghSH8RUa12CmtA9EAAKhHgACtXPxVSm2UA3i17bzOgQ"},
             
             {"name": "A Guide For Women", "file_id": "BQACAgUAAxkBAAIBBGm7JUji3B0kEuDFgd9AGZZOuvghAALbIwACWjvZVTnJNLIsK45DOgQ"},
             {"name": "The Damascus Sermon", "file_id": "BQACAgUAAxkBAAP8absiTJfN3MqEjjvcTA-n-Jgql_UAAtcjAAJaO9lVW_8RLITfPs46BA"},                                                       
             {"name": "Al-Jawshan Al-Kabir", "file_id": "BQACAgUAAxkBAAIBAmm7JTzz8NX3qafwNscKWTa_xH5MAALaIwACWjvZVV65aD6LHtjQOgQ"},
             {"name": "Tesbihat", "file_id": "BQACAgUAAxkBAAIBBmm7Je662Tkg-4F6ieOpboSV_lZSAALcIwACWjvZVeJvgh9UOQABZToE"},
        ],
        "stories": [
            "📖 <b>Об авторе — Саид Нурси</b>\n\nБадиуззаман Саид Нурси (1878–1960) — "
            "выдающийся турецкий богослов и мыслитель, автор Рисале-и Нур.",
            "📖 <b>История Рисале-и Нур</b>\n\nТруды были написаны в условиях "                                                                                                                                                                                                                             
            "преследований и заключения, распространялись от руки.",
        ]
    },

    "pirlanta": {
        "title": "💎 Pirlanta",
        "description": (
            "💎 <b>Pirlanta — жемчужины мудрости</b>\n\n"
            "Коллекция книг и материалов серии Pirlanta. "
            "PDF файлы и тексты."
        ),
        "files": [
             {"name": "The Broken Jug", "file_id": "BQACAgUAAxkBAAO8abbA60rkxBqB9NUdCkI5k3ns9aMAAoocAALlQbFV6uxbo_jvBAQ6BA"},
            # {"name": "Pirlanta 2", "file_id": "BQACAgI..."},
        ],
        "stories": []
    },

    "some_topics": {
        "title": "📌 Some Topics",
        "description": (
            "📌 <b>Избранные темы</b>\n\n"
            "Различные темы и материалы для изучения."
        ),
        "files": [],
        "stories": []
    },

     "others": {
        "title": "🗂 Others",
        "description": (
            "🗂 <b>Другие материалы</b>\n\n"
            "Разные темы и материалы, "
            "которые не вошли в другие категории."
        ),
        "files": [],
        "stories": [
            "📝 <b>Разные материалы</b>\n\nЗдесь собраны материалы на различные темы.",
        ]
    },
    

    # OTHERS — перемещён ПОСЛЕДНИМ (поменян с Weekly Topics)
    "weekly_topics": {
        "title": "📅 Weekly Topics",
        "description": (
            "📅 <b>Темы недели</b>\n\n"
            "Еженедельные материалы, статьи и обсуждения."
        ),
        "files": [],
        "stories": []
    },

}

# Порядок кнопок в меню (OTHERS последний, поменяли с Weekly Topics)
MENU_ORDER = [
    "atlasiakids",
    "books_hizmet",
    "risale_i_nur",        # ← был последним, теперь 3-й
    "pirlanta",
    "presentations",
    "reflection",
    "weekly_topics",
    "some_topics",
    "others",    # ← теперь последний
]

WELCOME_TEXT = (
    "⭐ <b>Welcome to Hizmet Channel: <i>admin by Tojiddin</i></b>\n\n"
    "Выберите категорию / Choose a category:"
)

# ──────────────────────────────────────────────
#  КЛАВИАТУРЫ
# ──────────────────────────────────────────────
def main_menu_kb() -> InlineKeyboardMarkup:
    buttons = []
    row = []
    for i, key in enumerate(MENU_ORDER):
        cat = CATEGORIES[key]
        row.append(InlineKeyboardButton(
            text=cat["title"],
            callback_data=f"cat_{key}"
        ))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def category_kb(cat_key: str) -> InlineKeyboardMarkup:
    cat = CATEGORIES[cat_key]
    buttons = []

    for i, f in enumerate(cat.get("files", [])):
        buttons.append([InlineKeyboardButton(
            text=f"📄 {f['name']}",
            callback_data=f"file_{cat_key}|{i}"
        )])

    if cat.get("stories"):
        buttons.append([InlineKeyboardButton(
            text="📖 Рассказы / Stories",
            callback_data=f"stories_{cat_key}"
        )])

    if not cat.get("files") and not cat.get("stories"):
        pass  # Нет контента — только кнопка назад

    buttons.append([InlineKeyboardButton(
        text="⬅️ Назад / Back",
        callback_data="menu"
    )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="⬅️ Назад / Back", callback_data="menu")
    ]])

# ──────────────────────────────────────────────
#  РОУТЕР И ХЕНДЛЕРЫ
# ──────────────────────────────────────────────
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Команда /start — показывает приветствие с фото"""
    try:
        await message.answer_photo(
            # Замени на свой file_id после загрузки картинки
            # Или оставь URL картинки-заглушки
            photo="https://d3i6fh83elv35t.cloudfront.net/static/2024/10/2024-10-21T061202Z_511124637_RC2E278IJ69H_RTRMADP_3_PEOPLE-FETHULLAH-GULEN-1024x794.jpg",
            caption=WELCOME_TEXT,
            reply_markup=main_menu_kb()
        )
    except Exception:
        # Если картинка недоступна — отправляем просто текст
        await message.answer(
            text=WELCOME_TEXT,
            reply_markup=main_menu_kb()
        )


@router.message(F.document)
async def get_file_id(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    fid = message.document.file_id
    fname = message.document.file_name or "Unknown"
    await message.answer(
        f"✅ Файл получен!\n\n"
        f"📄 Имя: <b>{fname}</b>\n\n"
        f"🔑 file_id (скопируй в CATEGORIES):\n"
        f"<code>{fid}</code>"
    )


@router.callback_query(F.data == "menu")
async def back_to_menu(callback: CallbackQuery):
    """Кнопка Назад — возврат в главное меню"""
    try:
        await callback.message.edit_caption(
            caption=WELCOME_TEXT,
            reply_markup=main_menu_kb()
        )
    except Exception:
        await callback.message.edit_text(
            text=WELCOME_TEXT,
            reply_markup=main_menu_kb()
        )
    await callback.answer()


@router.callback_query(F.data.startswith("cat_"))
async def show_category(callback: CallbackQuery):
    """Открывает выбранную категорию"""
    cat_key = callback.data[4:]

    if cat_key not in CATEGORIES:
        await callback.answer("Категория не найдена", show_alert=True)
        return

    cat = CATEGORIES[cat_key]
    n_files = len(cat.get("files", []))
    n_stories = len(cat.get("stories", []))

    text = cat["description"] + "\n\n"
    if n_files:
        text += f"📄 PDF файлов: <b>{n_files}</b>\n"
    if n_stories:
        text += f"📖 Историй: <b>{n_stories}</b>\n"
    if not n_files and not n_stories:
        text += "🔜 Материалы скоро будут добавлены..."

    try:
        await callback.message.edit_caption(
            caption=text,
            reply_markup=category_kb(cat_key)
        )
    except Exception:
        await callback.message.edit_text(
            text=text,
            reply_markup=category_kb(cat_key)
        )
    await callback.answer()


@router.callback_query(F.data.startswith("file_"))
async def send_pdf(callback: CallbackQuery):
    """Отправляет PDF файл пользователю"""
    # Формат: file_CATKEY|INDEX
    raw = callback.data[5:]  # убираем "file_"
    if "|" not in raw:
        await callback.answer("Ошибка формата", show_alert=True)
        return

    cat_key, idx_str = raw.rsplit("|", 1)

    if cat_key not in CATEGORIES or not idx_str.isdigit():
        await callback.answer("Файл не найден", show_alert=True)
        return

    files = CATEGORIES[cat_key].get("files", [])
    idx = int(idx_str)

    if idx >= len(files):
        await callback.answer("Файл не найден", show_alert=True)
        return

    file_info = files[idx]
    await callback.answer(f"📤 Отправляю {file_info['name']}…")

    try:
        cat_title = CATEGORIES[cat_key]["title"]
        await callback.message.answer_document(
            document=file_info["file_id"],
            caption=f"📄 <b>{file_info['name']}</b>\n📂 {cat_title}"
        )
    except Exception as e:
        logger.error(f"Failed to send document {file_info['name']}: {e}")
        await callback.message.answer("❌ Ошибка при отправке файла. Попробуйте позже.")


@router.callback_query(F.data.startswith("stories_"))
async def show_stories(callback: CallbackQuery):
    """Показывает рассказы/описания категории"""
    cat_key = callback.data[8:]  # убираем "stories_"

    if cat_key not in CATEGORIES:
        await callback.answer("Не найдено", show_alert=True)
        return

    cat = CATEGORIES[cat_key]
    stories = cat.get("stories", [])

    if not stories:
        await callback.answer("Рассказы пока не добавлены", show_alert=True)
        return

    text = f"{cat['title']} — Рассказы\n\n" + "\n\n".join(stories)

    try:
        await callback.message.edit_caption(
            caption=text,
            reply_markup=back_kb()
        )
    except Exception:
        await callback.message.edit_text(
            text=text,
            reply_markup=back_kb()
        )
    await callback.answer()


# ──────────────────────────────────────────────
#  ЗАПУСК
# ──────────────────────────────────────────────
async def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found in environment variables. Please set it in .env file.")
        return
    if not ADMIN_ID:
        logger.error("ADMIN_ID not found in environment variables. Please set it in .env file.")
        return

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_router(router)

    logger.info("✅ Hizmet Bot запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())