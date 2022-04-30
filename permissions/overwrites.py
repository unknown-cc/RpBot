from discord import PermissionOverwrite

############# 管理權限 #############

AdminChannelPerm = (
    "manage_channels",
    "manage_messages",
    "manage_permissions",
    "move_members",
    "mute_members",
    "priority_speaker",
    "deafen_members",
    "create_instant_invite",
)

LeaderChannelPerm = (
    "manage_channels",
)

AdvanceChannelPerm = (
    "create_instant_invite",
    "manage_messages",
    "move_members",
    "mute_members",
    "priority_speaker",
    "deafen_members",
)

############# 閱覽訊息 #############

ViewPerm = (
    "view_channel",
    # 觀看權限
    "read_messages"
)

ReadHistoryPerm = (
    # 觀看歷史紀錄
    "read_message_history",
)

############# 使用訊息 #############
SendMessagePerm = (
    # 傳送訊息
    "send_messages",
    # 使用斜線指令
    "use_slash_commands",
    # 使用額外表情
    "use_external_emojis",
    # embed
    "embed_links"
)

# 添加反應
ReactPerm = ("add_reactions",)
# 上傳檔案
AttachFilePerm = ("attach_files",)
# 標註
MentionPerm = ("mention_everyone",)

############# 語音 #############

ConnectPerm = (
    "view_channel",
    # 連接
    "connect",
)

SpeakPerm = (
    # 說話
    "speak",
    # 視訊通話
    "stream",
    # 使用語音活動
    "use_voice_activation",
)

# admin 權限

def AdminRole():
    perms = \
        AdminChannelPerm +\
        ViewPerm +\
        ReadHistoryPerm +\
        SendMessagePerm +\
        AttachFilePerm +\
        MentionPerm +\
        ReactPerm +\
        ConnectPerm +\
        SpeakPerm
    o = PermissionOverwrite()
    o.update(**dict.fromkeys(perms, True))
    return o

def LeaderRole():
    perms = \
        LeaderChannelPerm +\
        AdvanceChannelPerm +\
        ViewPerm +\
        ReadHistoryPerm +\
        SendMessagePerm +\
        AttachFilePerm +\
        MentionPerm +\
        ReactPerm +\
        ConnectPerm +\
        SpeakPerm
    o = PermissionOverwrite()
    o.update(**dict.fromkeys(perms, True))
    return o

def AdvanceRole():
    perms = \
        AdvanceChannelPerm +\
        ViewPerm +\
        ReadHistoryPerm +\
        SendMessagePerm +\
        AttachFilePerm +\
        MentionPerm +\
        ReactPerm +\
        ConnectPerm +\
        SpeakPerm
    o = PermissionOverwrite()
    o.update(**dict.fromkeys(perms, True))
    return o

# 正常權限

def NormalRole():
    perms = \
        ViewPerm +\
        ReadHistoryPerm +\
        SendMessagePerm +\
        AttachFilePerm +\
        MentionPerm +\
        ReactPerm +\
        ConnectPerm +\
        SpeakPerm
    o = PermissionOverwrite()
    o.update(**dict.fromkeys(perms, True))
    return o

# 僅限觀看
def ReadOnlyRole():
    perms = \
        ViewPerm +\
        ReadHistoryPerm
    o = PermissionOverwrite()
    o.update(**dict.fromkeys(perms, True))
    return o

# 限制觀看
def limitReadRole():
    perms = \
        ReadHistoryPerm
    o = PermissionOverwrite()
    o.update(**dict.fromkeys(perms, True))
    return o

# 可看到頻道 , 無法連接 , 但被連接可以說話
def ReadOnlyVoiceRole():
    perms = \
        ViewPerm +\
        SpeakPerm
    o = PermissionOverwrite()
    o.update(**dict.fromkeys(perms, True))
    return o

# 可連接頻道
def NormalVoiceRole():
    perms = \
        ViewPerm +\
        ConnectPerm +\
        SpeakPerm
    o = PermissionOverwrite()
    o.update(**dict.fromkeys(perms, True))
    return o