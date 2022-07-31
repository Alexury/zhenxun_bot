# python3
# -*- coding: utf-8 -*-
import nonebot
from typing import Tuple, Any
from nonebot import on_regex, on_command
from nonebot.params import RegexGroup
from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Bot,  MessageEvent, MessageSegment
from nonebot.typing import T_State
import os
from os.path import dirname
import random
import httpx
from configs.config import Config

__zx_plugin_name__ = "三次元"
__plugin_usage__ = """
usage：
    来点三次元
    指令：
    三次元
""".strip()
__plugin_des__ = "来点三次元"
__plugin_cmd__ = ["三次元/san"]
__plugin_type__ = ("来点好康的")
__plugin_version__ = 0.1
__plugin_author__ = "nekopaer"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["三次元","san"]
    }

path = dirname(__file__) + "/resources"
# sanciyuan = on_command("san", aliases={"三次元"}, block=True, priority=5)
sanciyuan = on_regex(r"^(\d?)张?(san|三次元)$", priority=5, block=True)
# sanciyuan = on_regex(r"^(\d)张?(san)|^(san|三次元)$", priority=5, block=True)

@sanciyuan.handle()

async def _(bot: Bot, event: MessageEvent, reg_group: Tuple[Any, ...] = RegexGroup()):
    num = reg_group[0] or 1
    for _ in range(int(num)):
                if not os.path.exists(path):
                    logger.info("创建资源路径")
                    os.mkdir(path)
                if not os.path.exists(path + "/fuli.txt"):
                    async with httpx.AsyncClient() as client:
                        where_fuli = (await client.get("http://150.158.99.87:10088/document/images.txt")).text
                    logger.info(f"从gayhub下载资源文件  {path}/fuli.txt")
                    with open(path + "/fuli.txt", "w", encoding="utf-8") as fulitxt:
                        fulitxt.write(where_fuli)
                img_list = open(path + "/fuli.txt", "r", encoding="utf-8").read().replace("\n", "").split(".jpg")
                img = random.choice(img_list) + ".jpg"
                await bot.send(
                    event=event,
                    message=MessageSegment.image(img)
                    )
