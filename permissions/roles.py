gov_roles = [
    851077907128647730,  # 創辦人
    851078200892588082,  # 開發者
    849960343844421649,  # 大管家
    849960343844421648,  # 市政府
    849960343844421646,  # 遊戲管理員
    849960343844421643,  # 活動管理員
    849960343844421647,  # discord管理員
]

leader_roles = [
    853903219628310538, # 警察局長
    853903225501515776, # 醫護院長
    853903223357702164, # 車業老闆
    853903348863598593, # 新聞局長
    853903228622209025, # 黑幫1老大
    853903191820861450, # 黑幫2老大
]

manager_roles = [
    849960343814930441, # 警察高層
    849960343814930438, # 醫護高層
    849960343814930435, # 車業高層
    849960343814930432, # 新聞高層
    849960343777968182, # 黑幫1高層
    849960343777968179, # 黑幫2高層
]

job_roles= [
    849960343814930440, # 警察
    849960343814930437, # 醫護
    849960343814930434, # 車業
    849960343777968187, # 新聞
    849960343777968181, # 黑幫1
    849960343777968178, # 黑幫2
]

# 確認身分組
def check_perms(member):
    perms = 0
    if member.guild_permissions.administrator:
        return 5
    roles = member.roles
    for role in roles:
        role_perms = 0
        if role.id in gov_roles:
            role_perms = 4
        elif role.id in leader_roles:
            role_perms = 3
        elif role.id in manager_roles:
            role_perms = 2
        elif role.id in job_roles:
            role_perms = 1
        else:
            role_perms = 0

        if role_perms > perms:
            perms = role_perms
    return perms