'''
Core of Economy System

Copyright (C) 2024  __OopsYouDiedE__

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import sqlite3
import database_manager
import interactions
from interactions.api.events import MemberRemove, MessageCreate
from interactions.ext.paginators import Paginator
from collections import deque
import asyncio
import datetime
from config import DEV_GUILD
from typing import Optional, Union
import tempfile
import os
import asyncio
import csv

import aiofiles
import aiofiles.ospath
import aiofiles.os
import aioshutil
from aiocsv import AsyncReader, AsyncDictReader, AsyncWriter, AsyncDictWriter

class CoreEconomySystem(interactions.Extension):
    module_base: interactions.SlashCommand = interactions.SlashCommand(
        name="core_economy_system",
        description="Minimize Core For Economy Simulation"
    )

    # 管理员指令：添加指定数量的物品给某人。
    @module_base.subcommand("give", sub_cmd_description="Provide a specific quantity of items to a user.")
    @interactions.check(interactions.is_owner())
    @interactions.slash_option(
        name="id",
        description="id of the member.",
        required=True,
        opt_type=interactions.OptionType.USER
    )
    @interactions.slash_option(
        name="object_name",
        description="Name of the object.",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    @interactions.slash_option(
        name="quantity",
        description="Quantity of the object given.",
        required=True,
        opt_type=interactions.OptionType.NUMBER,
    )
    async def command_give_item(self, ctx: interactions.SlashContext, user_id: str, object_name: str, quantity: float = 1):
        await ctx.send(f"DEBUG:将{object_name}*{quantity}给予{user_id}")
        await ctx.send(f"DEBUG:交易前{user_id},有{database_manager.query_item(user_id, object_name)}个{object_name}")
        database_manager.update_item(user_id, object_name, quantity)

        await ctx.send(f"DEBUG:将{object_name}*{quantity}给予{user_id}")
        await ctx.send(f"DEBUG:交易后{user_id},有{database_manager.query_item(user_id, object_name)}个{object_name}")

    # 管理员指令：将某人的某些物品强制性转移给另一个人。
    @module_base.subcommand("send",
                            sub_cmd_description="Transfer a specific quantity of items from one user to another.")
    @interactions.check(interactions.is_owner())
    @interactions.slash_option(
        name="sender_id",
        description="id of the member send items.",
        required=True,
        opt_type=interactions.OptionType.USER
    )
    @interactions.slash_option(
        name="receiver_id",
        description="id of the member receive items.",
        required=True,
        opt_type=interactions.OptionType.USER
    )
    @interactions.slash_option(
        name="object_name",
        description="Name of the object.",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    @interactions.slash_option(
        name="quantity",
        description="Quantity of the object given.",
        required=True,
        opt_type=interactions.OptionType.INTEGER,
    )
    async def command_give_item(self, ctx: interactions.SlashContext, sender_id: str, receiver_id: str,
                                object_name: str, quantity: int = 1):
        await ctx.send(f"DEBUG:交易前{sender_id},有{database_manager.query_item(sender_id, object_name)}个{object_name}")
        database_manager.update_item(sender_id, object_name, -quantity)
        database_manager.update_item(receiver_id, object_name, quantity)
        await ctx.send(f"DEBUG:交易后{sender_id},有{database_manager.query_item(sender_id, object_name)}个{object_name}")

