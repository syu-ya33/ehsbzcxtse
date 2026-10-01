from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
class MyHandler(BaseHTTPRequestHandler):
    def do_get(self): self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
threading.Thread(target=lambda: HTTPServer(('0.0.0.0', 10000), MyHandler).serve_forever(), daemon=True).start()

import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def roll_dice(num, sides):
    return sum(random.randint(1, sides) for _ in range(num))

def make_coc_6th():
    str_val = roll_dice(3, 6)
    con = roll_dice(3, 6)
    pow_val = roll_dice(3, 6)
    dex = roll_dice(3, 6)
    app = roll_dice(3, 6)
    siz = roll_dice(2, 6) + 6
    int_val = roll_dice(2, 6) + 6
    edu = roll_dice(3, 6) + 3
    
    total = str_val + con + pow_val + dex + app + siz + int_val + edu
    hp = (con + siz + 1) // 2
    mp = pow_val
    san = pow_val * 5
    idea = int_val * 5
    luck = pow_val * 5
    know = min(edu * 5, 99)
    
    return (
        f"**STR**:{str_val}  **CON**:{con}  **POW**:{pow_val}  **DEX**:{dex}  **APP**:{app}\n"
        f"**SIZ**:{siz}  **INT**:{int_val}  **EDU**:{edu}\n"
        f"**[派生]** HP:{hp} / MP:{mp} / SAN:{san}\n"
        f"**[能力]** アイデア:{idea} / 幸運:{luck} / 知識:{know}\n"
        f"**【能力値合計】: {total}**"
    )

def make_coc_7th():
    str_val = roll_dice(3, 6) * 5
    con = roll_dice(3, 6) * 5
    dex = roll_dice(3, 6) * 5
    app = roll_dice(3, 6) * 5
    pow_val = roll_dice(3, 6) * 5
    siz = (roll_dice(2, 6) + 6) * 5
    int_val = (roll_dice(2, 6) + 6) * 5
    edu = (roll_dice(2, 6) + 6) * 5
    
    luck = roll_dice(3, 6) * 5
    
    total = str_val + con + dex + app + pow_val + siz + int_val + edu
    hp = (con + siz) // 10
    mp = pow_val // 5
    san = pow_val
    
    if str_val < siz and dex < siz:
        mov = 7
    elif str_val > siz and dex > siz:
        mov = 9
    else:
        mov = 8

    str_siz = str_val + siz
    if str_siz <= 64:
        db, bd = "-2", -2
    elif str_siz <= 84:
        db, bd = "-1", -1
    elif str_siz <= 124:
        db, bd = "0", 0
    elif str_siz <= 164:
        db, bd = "+1D4", 1
    elif str_siz <= 204:
        db, bd = "+1D6", 2
    elif str_siz <= 284:
        db, bd = "+2D6", 3
    elif str_siz <= 364:
        db, bd = "+3D6", 4
    elif str_siz <= 444:
        db, bd = "+4D6", 5
    else:
        db, bd = "+5D6", 6
    
    return (
        f"**STR**:{str_val}  **CON**:{con}  **DEX**:{dex}  **APP**:{app}  **POW**:{pow_val}\n"
        f"**SIZ**:{siz}  **INT**:{int_val}  **EDU**:{edu}\n"
        f"**[派生]** HP:{hp} / MP:{mp} / 正気度:{san} / 幸運:{luck}\n"
        f"**[戦闘]** MOV:{mov} / DB:{db} / ビルド:{bd}\n"
        f"**【能力値合計】: {total}**"
    )

# --- 特徴表ダイス生成処理 ---
def roll_feature():
    d6 = random.randint(1, 6)
    d10 = random.randint(1, 10)
    result_str = f"**{d6}-{d10}**"
    
    # 4-1 ～ 4-10 はデメリット特徴（追加技能ポイント発生）
    if d6 == 4:
        bonus_dice = random.randint(1, 6)
        points = bonus_dice * 10
        result_str += f" ⚠️ **[デメリット特徴]** ＋{points}pt (1D6:{bonus_dice}×10) の追加技能P獲得！"
        
    return result_str
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name="coc6")
async def coc_6th_cmd(ctx):
    embed = discord.Embed(
        title="🎲 クトゥルフ神話TRPG (6版) キャラクター作成",
        description=f"{ctx.author.mention} さんの探索者候補です。好きなセットを選んでください！",
        color=0x2b2d31
    )
    for i in range(1, 4):
        embed.add_field(name=f"ーーー セット {i} ーーー", value=make_coc_6th(), inline=False)
    embed.set_footer(text="※ハウスルールに合わせて適宜入れ替えや振り直しを行ってください。")
    await ctx.send(embed=embed)

@bot.command(name="coc7")
async def coc_7th_cmd(ctx):
    embed = discord.Embed(
        title="🐙 新クトゥルフ神話TRPG (7版) キャラクター作成",
        description=f"{ctx.author.mention} さんの探索者候補です。好きなセットを選んでください！",
        color=0x992d22
    )
    for i in range(1, 4):
        embed.add_field(name=f"ーーー セット {i} ーーー", value=make_coc_7th(), inline=False)
    embed.set_footer(text="※7版はすでに5倍された数値が出力されています。")
    await ctx.send(embed=embed)

bot.run(os.environ.get('DISCORD_BOT_TOKEN'))
