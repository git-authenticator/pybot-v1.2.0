import requests , traceback, os, sys, psutil, time, jdatetime, pytz
from pyrogram import Client , filters
from pyrogram.types import Message
from pyrogram.errors import *
from datetime import datetime

#import local modules:
# import db.py

app = Client("myappapi" , config_file="deploy.ini")

def get_cmd_param(cmd_str,cmd_len,param_num=50,param_spacer=" "):
    try:
        param0=cmd_str[cmd_len:]
        param= []
        param1=param0.strip()
        param2 = param1.split(param_spacer, cmd_len + 1)
        for i in range(len(param2)):
            if param2[i] != "":
                param.append(param2[i].strip())
        if param_num > len(param):
            param_num = len(param)
        return param[0:param_num]
    except Exception as err_param:
        print(str(err_param))
        a=traceback.print_exc()
def download_file(url, fullname=''):
    file_name=fullname[:fullname.rfind(".")]
    file_type=fullname[fullname.rfind(".")+1:]
    i = 1
    while i < 50:
        try:
            with requests.get(url , stream=True) as req:
                if fullname!='':
                    pass
                else:
                    fullname = url[url.rfind("/")+1:]
                with open(fullname , 'xb') as f:
                    try:
                        for chunk in req.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    except FileExistsError:
                        return "exist"
                return f"done{fullname}"
        except FileExistsError as e:
            i = i + 1
            fullname= file_name + str(i) + "." + file_type
            continue
        except Exception as f:
            app.send_message("me", f"Command Download has rised an error : **\nUrl:{url}\nFilename:{fullname}**\n\n {sys.exc_info()[0]}\n{sys.exc_info()[1]}\n{sys.exc_info()[2]}\n{sys.exc_info()[2].tb_frame}\n{sys.exc_info()[2].tb_lasti}\n{sys.exc_info()[2].tb_lineno}\n{sys.exc_info()[2].tb_next}")
            break
def get_time(timezone="Asia/Tehran"):
    current_tz = pytz.timezone(timezone)
    current_datetime = jdatetime.datetime.now(tz=current_tz).strftime("%a, %d %b %Y , %H:%M:%S")
    return current_datetime,timezone

botadmins=[1432165830,244640287,1337422169,1360357981]
@app.on_message(filters.me & filters.text & ~filters.edited & ~filters.forwarded, group=0)
# filters.user
async def main(client , m:Message):
    try:
        admintext=m.text.strip()
        chat_info=m.chat
        if admintext=="/check":
            if not m.reply_to_message:
                await m.edit(f"**{admintext}**\n**BOT : I'm on!**")
        elif admintext=="/sysinfo":
            cpu_info = psutil.cpu_times_percent()
            cpu_usage=cpu_info[0]
            memory = psutil.virtual_memory()
            await m.edit(f"**{admintext}**\n\n**System usage information:**\nCpu usage: {cpu_usage}%\nMemory usage: {memory[2]}%")
        elif admintext[0:8]=="/upload ":
            try:
                if not m.reply_to_message:
                    await m.edit(f"**{admintext}**\n\nTrying to download the requested file\nPlease wait...", disable_web_page_preview=True)
                    link_arr=get_cmd_param(admintext,8,2)
                    link_txt=link_arr[0]
                    try:    
                        link_name=link_arr[1]
                    except IndexError:
                        link_name=""
                    download=download_file(link_txt,link_name)
                    if download[0:4]=="done" :
                        res_file_name = download[4:]
                        await m.edit(f"**{admintext}**\n\nYour File has been downloaded, uploading file to telegram\nPlease wait...", disable_web_page_preview=True)
                        res_file=await m.reply_document(res_file_name, quote=True)
                        await m.edit(f"**{admintext}**\n\nYour File has been uploaded to telegram successfully!\nFile Name: " + res_file_name, disable_web_page_preview=True)
                        await m.forward("me")
                        await res_file.forward("me")
                else:
                    await m.edit(f"{admintext}\nNo targets have been provided for the given command!")
            except AttributeError:
                await m.edit(f"{admintext}\nNo targets have been provided for the given command!")
            except Exception as e:
                await app.send_message("me", f"Command has rised an error : **{admintext}**\n\n {sys.exc_info()[0]}\n{sys.exc_info()[1]}\n{sys.exc_info()[2]}\n{sys.exc_info()[2].tb_frame}\n{sys.exc_info()[2].tb_lasti}\n{sys.exc_info()[2].tb_lineno}\n{sys.exc_info()[2].tb_next}")
        elif admintext=="/userinfo":
            try:
                await m.edit(f"**{admintext}**\n*__User information__*\nUsername: {m.reply_to_message.from_user.username}\nFirstName:{m.reply_to_message.from_user.first_name} \nLastName: {m.reply_to_message.from_user.last_name}\nMentionUser: {m.   reply_to_message.from_user.mention} \nNumeric id : {m.reply_to_message.from_user.id}")
            except AttributeError:
                await m.edit(f"{admintext}\nNo targets have been provided for the given command!")
        elif admintext=="/msginfo":
            try:
                if m.reply_to_message:
                    await m.edit(f"**{admintext}\n****<*__Message Information__>**\n\n\n{m.reply_to_message}")
                else:
                    await m.edit(f"{admintext}\nNo targets have been provided for the given command!")
            except AttributeError:
                await m.edit(f"{admintext}\nNo targets have been provided for the given command!")
        elif admintext=="/msgid":
            try:
                if m.reply_to_message:
                    await m.edit(f"**{admintext}\n\n****Message id:** {m.reply_to_message.message_id}")
                else:
                    await m.edit(f"{admintext}\nNo targets have been provided for the given command!")
            except AttributeError:
                await m.edit(f"{admintext}\nNo targets have been provided for the given command!")
        elif admintext=="/chatinfo":
            try:
                await m.edit(f"{admintext}\n*__User information__*\n{m.chat}")
            except:
                pass
        elif admintext=="/countallmsg":
            allmsg=await app.get_history_count(m.chat.id)
            await m.edit(f"**{admintext}**\n\nAll messages in this chat: {allmsg}")
        elif admintext=="/database" :
            try:
                await m.reply_to_message.forward(-1001595898790)
                await m.edit(f"**{admintext}**\nThis message from {m.reply_to_message.from_user.username} with MessageID:{m.reply_to_message.message_id} has been saved to database")
            except AttributeError:
                await m.edit(f"**{admintext}**\nNo targets have been provided for the given command!")
        elif admintext=="/download" :
            try:
                m = await m.edit(f"**{admintext}**\nDownloading this message from {m.reply_to_message.from_user.username} with MessageID:{m.reply_to_message.message_id}\nHas been started...")
                await app.download_media(m.reply_to_message)
                await m.edit(f"**{admintext}**\nThis message from {m.reply_to_message.from_user.username} with MessageID:{m.reply_to_message.message_id} has been downloaded successfuly")
                # m.reply_to_message.reply(str(m), quote=True)
            except AttributeError as err_download:
                await m.edit(f"**{admintext}**\nNo targets have been provided for the given command!")
            except ValueError as err_download:
                await m.edit(f"**{admintext}**\n" + "The provided message has no downloadable content!")
        elif admintext=="/lockpv":
            open("lockpv", "w").write("yes")
            await m.edit(f"**{admintext}**\npv is **__locked__**")
        elif admintext=="/unlockpv":
            open("lockpv", "w").write("no")
            await m.edit(f"**{admintext}**\npv is **__unlocked__**")
        elif admintext=="/join":
            try:
                await m.delete()
                await app.join_chat(m.reply_to_message.text)
                await app.send_message("me",f"**{admintext}**\nSuccessfuly joined the group/channel with id {m.reply_to_message.chat.id}")
            except BadRequest as e:
                if "USER_ALREADY_PARTICIPANT" in str(e):
                    await app.send_message("me",f"**{admintext}**\nYou've already joined the group/channel with id {m.reply_to_message.chat.id}")
        elif admintext[0:6]=="/leave":
            leave_params = get_cmd_param(admintext, 6)
            also_delete_chat = False
            if "del" in leave_params or "delete" in leave_params:
                also_delete_chat = True
            try:
                await m.delete()
                await app.leave_chat(m.chat.id, also_delete_chat)
                await app.send_message("me", f"**{admintext}**\nSuccessfully leaved chat\nChat id:{m.chat.id}")
                # await app.send_message("me", f"**{admintext}**\nSuccessfully leaved chat\nChat id:{m.chat.id}\n{get_time()[0]}\nCurrent TimeZone: {get_time()[1]}")
            except BadRequest as e:
                if "USER_NOT_PARTICIPANT" in str(e):
                    await app.send_message("me",f"**{admintext}**\nYou're **Not** in this group/channel with id {m.reply_to_message.chat.id}")
        elif admintext[0:8]=="/delete ":
            tempmsg = m
            try:
                if tempmsg.reply_to_message:
                    del_num_array = get_cmd_param(admintext,8,1)
                    del_num_str = del_num_array[0]
                    del_num = int(del_num_str) + 1
                    i=1
                    await tempmsg.edit(f"**{admintext}**\nDeleting {del_num_str} messages\nfrom the replied message\nPlease wait...")
                    while i < del_num:
                        del_msg = await app.delete_messages(chat_id=tempmsg.chat.id, message_ids=tempmsg.reply_to_message.message_id - i)
                        if del_msg == True:
                            pass
                        else:
                            del_num = del_num + 1
                        i = i + 1
                    await tempmsg.edit(f"**{admintext}**\nDeleting {del_num_str} messages is done")
                    pass
                else:
                    del_num_array = get_cmd_param(admintext,8,1)
                    del_num_str = del_num_array[0]
                    del_num = int(del_num_str) + 1
                    i=1
                    await tempmsg.edit(f"**{admintext}**\nDeleting {del_num_str} messages\nPlease wait...")
                    while i < del_num:
                        del_msg = await app.delete_messages(chat_id=tempmsg.chat.id, message_ids=tempmsg.message_id - i)
                        if del_msg == True:
                            pass
                        else:
                            del_num = del_num + 1
                        i = i + 1
                    await tempmsg.edit(f"**{admintext}**\nDeleting {del_num_str} messages is done")
            except ValueError:
                await tempmsg.edit(f"**{admintext}**\nYou have not provided right argument!")
        elif admintext[0:4]=="/ban":
            if m.reply_to_message:
                banning_user = m.reply_to_message.from_user
                app.kick_chat_member(m.chat.id, banning_user.id)
                await m.edit(f"**{admintext}**\n\nUser {banning_user.mention}\nwith username {banning_user.username}\nwith user id {banning_user.id}\nhas been **banned**!")
        elif admintext[0:6]=="/unban":
            if m.reply_to_message:
                unbanning_user = m.reply_to_message.from_user
                app.unban_chat_member(m.chat.id, unbanning_user.id)
                await m.edit(f"**{admintext}**\n\nUser {unbanning_user.mention}\nwith username {unbanning_user.username}\nwith user id {unbanning_user.id}\nhas been **unbanned** successfully")
        elif admintext[0:6]=="/block":
            if m.reply_to_message:
                blocking_user = m.reply_to_message.from_user
                app.block_user(blocking_user.id)
                await m.edit(f"**{admintext}**\n\nUser {blocking_user.mention}\nwith username {blocking_user.username}\nwith user id {blocking_user.id}\nhas been **blocked** successfully")
        elif admintext[0:6]=="/unblock":
            if m.reply_to_message:
                unblocking_user = m.reply_to_message.from_user
                app.unblock_user(unblocking_user.id)
                await m.edit(f"**{admintext}**\n\nUser {unblocking_user.mention}\nwith username {unblocking_user.username}\nwith user id {unblocking_user.id}\nhas been **unblocked** successfully")
        elif admintext[0:4]=="/pin":
            try:
                if m.reply_to_message:
                    pin_params = get_cmd_param(admintext,4,2)
                    notif=False ; both = True
                    if "notifoff" in pin_params or "bothoff" in pin_params:
                        notif=True ; both=False
                    print(notif, both)
                    app.pin_chat_message(m.chat.id, m.reply_to_message.message_id,disable_notification=notif,both_sides=both)
                    if len(m.reply_to_message.text) > 20:
                        a = len(m.reply_to_message.text)//3
                    await m.edit(f"**{admintext}**\n\nMessage \'{m.reply_to_message.text[0:a]}....\'\nfrom user {m.reply_to_message.from_user.mention}\nwith message id : {m.reply_to_message.message_id}\nhas been pinned in this chat")
            except Exception as e:
                await app.send_message("me", f"Command has rised an error : **{admintext}**\n\n {sys.exc_info()[0]}\n{sys.exc_info()[1]}\n{sys.exc_info()[2]}\n{sys.exc_info()[2].tb_frame}\n{sys.exc_info()[2].tb_lasti}\n{sys.exc_info()[2].tb_lineno}\n{sys.exc_info()[2].tb_next}")
        elif admintext[0:6]=="/unpin":
                if m.reply_to_message and m.reply_to_message.pinned==True:
                    unpining_msg = app.unpin_chat_message(m.chat.id, m.reply_to_message.message_id)
                    print(unpining_msg, type(unpining_msg))
                    if unpining_msg ==True:
                            await m.edit(f"**{admintext}**\n\nMessage \'{m.reply_to_message[0:{len(m.reply_to_message.text)//3}]}\'...\nfrom user {m.reply_to_message.from_user.mention}\nwith message id : {m.reply_to_message.message_id}\nhas been unpinned")
        elif admintext=="/unpinall":
            unpinall = app.unpin_all_chat_messages(m.chat.id)
            print(unpinall, type(unpinall))
            if unpinall==True:
                await m.edit(f"**{admintext}**\n\nAll pinned messages in this chat have been unpinned successfully")
        elif admintext=="/alluserinfo":
            filename=f"alluserinfo_{m.chat.id}.txt"
            f = open(filename, 'w+')
            f.write(f'{admintext}\n\nGetting all user informations in group/channel with **Chat id:{m.chat.id}**\n\nChat Info: {m.chat.id}\n\n\n'+'='*50+"\n\n\n"+'='*50+"\n\n\n\n\n")
            async for member in app.iter_chat_members(m.chat.id,):
                f.write(f'**chat member: {member.user.id}**\n\n\n{member}\n\n'+'='*50+"\n\n\n"+'='*50+"\n\n\n")
            f.close()
            await app.send_document('me', filename)
            try:
                os.remove(filename)
            except Exception:
                await app.send_message("me", f"Command has rised an error : **{admintext}**\n\n {sys.exc_info()[0]}\n{sys.exc_info()[1]}\n{sys.exc_info()[2]}\n{sys.exc_info()[2].tb_frame}\n{sys.exc_info()[2].tb_lasti}\n{sys.exc_info()[2].tb_lineno}\n{sys.exc_info()[2].tb_next}")
        elif admintext=="/clonegp":
            chatid=m.chat.id
            await m.edit(f"**{admintext}**\n\nTrying to clone all messages in this group or channel\nChat id: {chatid}\nPlease wait...")
            this_chat = app.get_chat(m.chat.id)
            if this_chat.type=="group":
                bak = app.create_group(title=f"Backup for gp/chnl: {m.chat.title}", users=1636601696)
            elif this_chat.type=="supergroup":
                print("***supergroup format set***")
                bak = app.create_group(title=f"Backup for gp/chnl: {m.chat.title}", users=1636601696)
            elif this_chat.type=="channel":
                bak = app.create_channel(title=f"Backup for gp/chnl: {m.chat.title}")
            elif this_chat.type=="private" or this_chat.type=="bot":
                bak = app.create_group(title=f"Backup for user/bot: {m.chat.id}", users=1636601696)
            await m.edit(f"**{admintext}**\n\nTrying to clone all messages in this gp/chnl\nChat id: {m.chat.id}\n**New Event: Backup gp/chnl created\nBackup Type: **{this_chat.type}\n\n**Progress:** Processing...")
            app.kick_chat_member(chat_id=bak.id, user_id=1636601696)
            delete_history = await app.send_message(bak.id, "/delete 1")
            app.delete_messages(delete_history.chat.id, delete_history.message_id)
            await m.edit(f"**{admintext}**\n\n>>Trying to clone all messages in this gp/chnl\n>Chat id: {m.chat.id}\n>>Event:Backup gp/chnl created\n>Backup Type: {this_chat.type}\n**New Event:Backup history cleared**\n\n**Progress:** Processing...")
            for saving_msg in app.iter_history(chat_id=m.chat.id, ):
                try:
                    m.reply(m)
                    forwarding = app.forward_messages(bak.id, chatid, i)
                    forwarding_more = forwarding.reply()
                    await m.edit(f"**{admintext}**\n\n>>Trying to clone all messages in this group or channel\n>Chat id: {m.chat.id}\n>>Event: Backup gp/chnl created\n\n**Progress:** Processing...\n\n**Current message id:** {i}")     
                except bad_request_400.MessageIdInvalid:
                    continue
                except FloodWait as e:
                    await m.edit(f"**{admintext}**\n\nTrying to clone all messages in this group or channel\nChat id: {m.chat.id}\nEvent: Backup gp/chnl created\n\n**New Event: \'420 FLOOD_WAIT_X\' Error occurred, waiting to finish api ban time...**\n\n**Progress:** Waiting...\n\n**Waiting ban time to finish: **{e.x}\n**Current message id:** {i}")
                    time.sleep(1)
                    if i > 1 :
                        i = i - 1
                    continue
            await m.edit(f"**{admintext}**\n\nCloning process finished\nChat id: {m.chat.id}\nCloning is done successfully")
            await m.forward('me')
            for j in range(5, 0, -1):
                await m.edit(f"**{admintext}**\n\nCloning process finished\nChat id: {m.chat.id}\nCloning is done successfully\nDeleting this message in {j} seconds...")
                time.sleep(1)
            await m.delete(revoke=True)
        else:
            pass
    except Exception as all_err:
        await app.send_message("me", f"Command has rised an error : **{admintext}**\n\n {sys.exc_info()[0]}\n{sys.exc_info()[1]}\n{sys.exc_info()[2]}\n{sys.exc_info()[2].tb_frame}\n{sys.exc_info()[2].tb_lasti}\n{sys.exc_info()[2].tb_lineno}\n{sys.exc_info()[2].tb_next}")



@app.on_message(filters.user(botadmins) & filters.text & ~filters.edited & ~filters.forwarded, group=1)
# filters.user
async def main(client , m:Message):
    try:
        admintext=m.text.strip()
        chat_info=m.chat 
        if admintext=="/check":
            if not m.reply_to_message:
                await m.reply_text(f"**{admintext}**\n**BOT : I'm on!**", )
        elif admintext=="/all" or admintext=="@all":
            # rep = await m.reply_text(f"{m.from_user.id} : **{admintext}**\n**All friends please pay attention**\n\n",quote=True)
            async for member in app.iter_chat_members(m.chat.id):
            #     rep = await rep.edit(f"{rep.text} {member.user.mention} ")
                rep = await m.reply_text(f"{member.user.mention}",quote=False)
                # rep = await m.reply_text(f"{m.from_user.id} : **{admintext}**\n**All friends please pay attention**\n\n {app.iter_chat_members} ",quote=False)
    except Exception as all_err:
        await app.send_message("me", f"Command has rised an error : **{admintext}**\n\n {sys.exc_info()[0]}\n{sys.exc_info()[1]}\n{sys.exc_info()[2]}\n{sys.exc_info()[2].tb_frame}\n{sys.exc_info()[2].tb_lasti}\n{sys.exc_info()[2].tb_lineno}\n{sys.exc_info()[2].tb_next}")




#lockpv checks and delete messages if lock is active
@app.on_message(filters.private , group =3)
async def private(Client, m:Message):
    lock = open("lockpv").read()
    islock = True if lock == "yes" else False
    if islock:
        a = await m.forward("me")
        await m.delete()
    else:
        await m.continue_propagation()


app.run()

