# credits: SNAPDRAGON 
# originally from xtra-telegram
# ported by Ryoishin

import asyncio
import time

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import alphonse_cmd


@bot.on(
    alphonse_cmd(
        outgoing=True,
pattern=r"webupload ?(.+?|) (?:--)(anonfiles|transfer|filebin|anonymousfiles|megaupload|bayfiles)",
    )
)
async def _(event):
    if event.fwd_from:
        return
    await event.edit("`Processing ...`")
    PROCESS_RUN_TIME = 100
    input_str = event.pattern_match.group(1)
selected_transfer = event.pattern_match.group(2)
    if input_str:
        file_name = input_str
    else:
        reply = await event.get_reply_message()
        file_name = await bot.download_media(reply.media, TEMP_DOWNLOAD_DIRECTORY)
    CMD_WEB = {
"anonfiles": 'curl -F "file=@{}" https://anonfiles.com/api/upload',
        "transfer": 'curl --upload-file "{}" https://transfer.sh/{os.path.basename(file_name)}',
        "filebin": 'curl -X POST --data-binary "@test.png" -H "filename: {}" "https://filebin.net"',
"anonymousfiles": 'curl -F file="@{}" https://api.anonymousfiles.io/',
        "megaupload": 'curl -F "file=@{}" https://megaupload.is/api/upload',
        "bayfiles": '.exec curl -F "file=@{}" https://bayfiles.com/api/upload',
    }
    try:
selected_one = CMD_WEB[selected_transfer].format(file_name)
    except KeyError:
        await event.edit("Invalid selected Transfer")
    cmd = selected_one
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    await event.edit(f"{stdout.decode()}")


CMD_HELP.update(
    {
        "webupload": f"**Plugin : **`webupload`\
\n\n • **Syntax :** `{cmd}webupload --`(`anonfiles`|`transfer`|`filebin`|`anonymousfiles`|`megaupload`|`bayfiles`)\
        \n • **Function : **Reply `{cmd}webupload --anonfiles` or `.webupload --filebin` and the file will be uploaded to that website. \
    "
    }
)
