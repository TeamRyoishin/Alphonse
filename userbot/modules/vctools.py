# Copyright (C) 2021 TeamUltroid
 #
 # This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
 # PLease read the GNU Affero General Public License in
 # <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
 #
 # Ported by @Ryoishin
 


 from telethon.tl.functions.channels import GetFullChannelRequest as getchat
 from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
 from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
 from telethon.tl.functions.phone import EditGroupCallTitleRequest as settitle
 from telethon.tl.functions.phone import GetGroupCallRequest as getvc
 from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc

 from userbot import CMD_HANDLER as cmd
 from userbot import CMD_HELP, owner
 from userbot.events import register
 from userbot.utils import edit_delete, edit_or_reply, alphonse_cmd


 async def get_call(event):
     mm = await event.client(getchat(event.chat_id))
     xx = await event.client(getvc(mm.full_chat.call, limit=1))
     return xx.call


 def user_list(l, n):
     for i in range(0, len(l), n):
         yield l[i : i + n]


 @alphonse_cmd(pattern="startvc$")
 @register(pattern=r"^\.startvcs$", sudo=True)
 async def start_voice(c):
     chat = await c.get_chat()
     admin = chat.admin_rights
     creator = chat.creator

     if not admin and not creator:
         await edit_delete(c, f"**Sorry {owner} Not Admin **")
         return
     try:
         await c.client(startvc(c.chat_id))
         await edit_or_reply(c, "`Voice Chat Started...`")
     except Exception as ex:
         await edit_delete(c, f"**ERROR:** `{ex}`")


 @alphonse_cmd(pattern="stopvc$")
 @register(pattern=r"^\.stopvcs$", sudo=True)
 async def stop_voice(c):
     chat = await c.get_chat()
     admin = chat.admin_rights
     creator = chat.creator

     if not admin and not creator:
         await edit_delete(c, f"**Sorry {owner} Not Admin **")
         return
     try:
         await c.client(stopvc(await get_call(c)))
         await edit_or_reply(c, "`Voice Chat Stopped...`")
     except Exception as ex:
         await edit_delete(c, f"**ERROR:** `{ex}`")


 @alphonse_cmd(pattern="vcinvite")
 async def _(c):
     xxnx = await edit_or_reply(c, "`Inviting Members to Voice Chat...`")
     users = []
     z = 0
     async for x in c.client.iter_participants(c.chat_id):
         if not x.bot:
             users.append(x.id)
     botman = list(user_list(users, 6))
     for p in botman:
         try:
             await c.client(invitetovc(call=await get_call(c), users=p))
             z += 6
         except BaseException:
             pass
     await xxnx.edit(f"`{z}` **Successfully Invited to VCG**")


 @alphonse_cmd(pattern="vctitle(?: |$)(.*)")
 @register(pattern=r"^\.cvctitle$", sudo=True)
 async def change_title(e):
     title = e.pattern_match.group(1)
     chat = await e.get_chat()
     admin = chat.admin_rights
     creator = chat.creator

     if not title:
         return await edit_delete(e, "**Please Enter Group Voice Chat Title**")

     if not admin and not creator:
         await edit_delete(e, f"**Sorry {owner} Not Admin **")
         return
     try:
         await e.client(settitle(call=await get_call(e), title=title.strip()))
         await edit_or_reply(e, f"**Successfully Changed VCG Title To** `{title}`")
     except Exception as ex:
         await edit_delete(e, f"**ERROR:** `{ex}`")


 CMD_HELP.update(
     {
         "vcg": f"**Plugin : **`vcg`\
         \n\n • **Syntax :** `{cmd}startvc`\
         \n • **Function : **To start a voice chat group\
         \n\n • **Syntax :** `{cmd}stopvc`\
         \n • **Function : **To stop voice chat group\
         \n\n • **Syntax :** `{cmd}vctitle` <title vcg>\
         \n • **Function : **To change the title of the voice chat group\
         \n\n • **Syntax :** `{cmd}vcinvite`\
         \n • **Function : **Invite group members to voice chat group\
     "
     }
 )