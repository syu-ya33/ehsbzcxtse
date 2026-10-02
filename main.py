from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
class MyHandler(BaseHTTPRequestHandler):
    def do_get(self): self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
threading.Thread(target=lambda: HTTPServer(('0.0.0.0', 10000), MyHandler).serve_forever(), daemon=True).start()

import discord
from discord.ext import commands
from discord import app_commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def roll_dice(num, sides):
    return sum(random.randint(1, sides) for _ in range(num))

def calc_db_bd(str_val, siz):
    str_siz = str_val + siz
    if str_siz <= 64: return "-2", -2
    elif str_siz <= 84: return "-1", -1
    elif str_siz <= 124: return "0", 0
    elif str_siz <= 164: return "+1D4", 1
    elif str_siz <= 204: return "+1D6", 2
    elif str_siz <= 284: return "+2D6", 3
    elif str_siz <= 364: return "+3D6", 4
    elif str_siz <= 444: return "+4D6", 5
    else: return "+5D6", 6

def calc_mov(str_val, dex, siz):
    if str_val < siz and dex < siz: return 7
    elif str_val > siz and dex > siz: return 9
    else: return 8

# --- 6版 作成 ---
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

# --- 7版 通常作成 ---
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
    mov = calc_mov(str_val, dex, siz)
    db, bd = calc_db_bd(str_val, siz)
    
    return (
        f"**STR**:{str_val}  **CON**:{con}  **DEX**:{dex}  **APP**:{app}  **POW**:{pow_val}\n"
        f"**SIZ**:{siz}  **INT**:{int_val}  **EDU**:{edu}\n"
        f"**[派生]** HP:{hp} / MP:{mp} / 正気度:{san} / 幸運:{luck}\n"
        f"**[戦闘]** MOV:{mov} / DB:{db} / ビルド:{bd}\n"
        f"**【能力値合計】: {total}**"
    )

# --- 7版 小学生作成 ---
def make_coc_7th_elem(age=10):
    str_val = roll_dice(3, 4) * 5
    con = roll_dice(3, 4) * 5
    siz = (roll_dice(2, 3) + 6) * 5
    app = roll_dice(3, 6) * 5
    dex = roll_dice(3, 6) * 5
    pow_val = roll_dice(3, 6) * 5
    int_val = (roll_dice(2, 6) + 6) * 5
    edu = (age - 6) * 5
    
    # 幸運（3D6*5 を2回振る）
    luck1 = roll_dice(3, 6) * 5
    luck2 = roll_dice(3, 6) * 5
    best_luck = max(luck1, luck2)
    
    home_env = random.randint(1, 100)
    
    total = str_val + con + dex + app + pow_val + siz + int_val + edu
    hp = (con + siz) // 10
    mp = pow_val // 5
    san = pow_val
    mov = calc_mov(str_val, dex, siz)
    db, bd = calc_db_bd(str_val, siz)
    
    return (
        f"**STR**:{str_val}  **CON**:{con}  **DEX**:{dex}  **APP**:{app}  **POW**:{pow_val}\n"
        f"**SIZ**:{siz}  **INT**:{int_val}  **EDU**:{edu} (年齢:{age}歳固定)\n"
        f"**[派生]** HP:{hp} / MP:{mp} / 正気度:{san}\n"
        f"**[幸運2回振り]** {luck1} / {luck2} (採用候補: **{best_luck}**)\n"
        f"**[戦闘]** MOV:{mov} / DB:{db} / ビルド:{bd}\n"
        f"**[環境]** 家庭環境: 1D100={home_env}\n"
        f"**【能力値合計】: {total}**"
    )

# --- 7版 中学生作成 ---
def make_coc_7th_jhs(age=13):
    str_val = (roll_dice(2, 6) + 1) * 5
    con = (roll_dice(2, 6) + 1) * 5
    siz = (roll_dice(2, 4) + 6) * 5
    app = roll_dice(3, 6) * 5
    dex = roll_dice(3, 6) * 5
    pow_val = roll_dice(3, 6) * 5
    int_val = (roll_dice(2, 6) + 6) * 5
    edu = (age - 6) * 5
    
    # 幸運（3D6*5 を2回振る）
    luck1 = roll_dice(3, 6) * 5
    luck2 = roll_dice(3, 6) * 5
    best_luck = max(luck1, luck2)
    
    home_env = random.randint(1, 100)
    
    total = str_val + con + dex + app + pow_val + siz + int_val + edu
    hp = (con + siz) // 10
    mp = pow_val // 5
    san = pow_val
    mov = calc_mov(str_val, dex, siz)
    db, bd = calc_db_bd(str_val, siz)
    
    return (
        f"**STR**:{str_val}  **CON**:{con}  **DEX**:{dex}  **APP**:{app}  **POW**:{pow_val}\n"
        f"**SIZ**:{siz}  **INT**:{int_val}  **EDU**:{edu} (年齢:{age}歳固定)\n"
        f"**[派生]** HP:{hp} / MP:{mp} / 正気度:{san}\n"
        f"**[幸運2回振り]** {luck1} / {luck2} (採用候補: **{best_luck}**)\n"
        f"**[戦闘]** MOV:{mov} / DB:{db} / ビルド:{bd}\n"
        f"**[環境]** 家庭環境: 1D100={home_env}\n"
        f"**【能力値合計】: {total}**"
    )

def roll_feature():
    d6 = random.randint(1, 6)
    d10 = random.randint(1, 10)
    result_str = f"**{d6}-{d10}**"
    if d6 == 4:
        bonus_dice = random.randint(1, 6)
        points = bonus_dice * 10
        result_str += f" ⚠️️ **[D]** ＋{points}pt (1D6:{bonus_dice}×10) の追加技能Pt"
    return result_str

# --- Embed 生成用関数 ---
def create_coc6_embed(author_mention):
    embed = discord.Embed(
        title="🎲 クトゥルフ神話TRPG (6版) キャラクター作成",
        description=f"{author_mention} さんのダイス結果。",
        color=0x2b2d31
    )
    for i in range(1, 4):
        embed.add_field(name=f"ーーー セット {i} ーーー", value=make_coc_6th(), inline=False)
    embed.set_footer(text="※ハウスルールに合わせて[能力値の調整]や[年齢補正]を行ってください。")
    return embed

def create_coc7_embed(author_mention):
    embed = discord.Embed(
        title="🐙 新クトゥルフ神話TRPG (7版) キャラクター作成",
        description=f"{author_mention} さんのダイス結果。",
        color=0x992d22
    )
    for i in range(1, 4):
        embed.add_field(name=f"ーーー セット {i} ーーー", value=make_coc_7th(), inline=False)
    embed.set_footer(text="※年齢補正は別途適用してください。")
    return embed

def create_coc7_elem_embed(author_mention, age=10):
    embed = discord.Embed(
        title=f"🎒 7版 小学生探索者作成 ({age}歳)",
        description=f"{author_mention} さんのダイス結果。",
        color=0x3498db
    )
    for i in range(1, 4):
        embed.add_field(name=f"ーーー セット {i} ーーー", value=make_coc_7th_elem(age), inline=False)
    embed.set_footer(text="※EDUは (年齢-6)*5 で算出済み。幸運は高い方を採用")
    return embed

def create_coc7_jhs_embed(author_mention, age=13):
    embed = discord.Embed(
        title=f"🏫 7版 中学生探索者作成 ({age}歳)",
        description=f"{author_mention} さんのダイス結果。",
        color=0x2ecc71
    )
    for i in range(1, 4):
        embed.add_field(name=f"ーーー セット {i} ーーー", value=make_coc_7th_jhs(age), inline=False)
    embed.set_footer(text="※EDUは (年齢-6)*5 で算出済み。幸運は高い方を採用。")
    return embed

def create_ft_embed(author_mention):
    embed = discord.Embed(
        title="📜 2015特徴表ダイス (1D6 / 1D10)",
        description=f"{author_mention} さんのダイス結果。",
        color=0xe67e22
    )
    for i in range(1, 4):
        embed.add_field(name=f"候補 {i}", value=roll_feature(), inline=False)
    embed.set_footer(text="※デメリット特徴の追加技能ポイントは算出済み")
    return embed

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name} (Slash Commands Synced)')

# --- 従来型プレフィックスコマンド (!) ---
@bot.command(name="coc6")
async def coc_6th_cmd(ctx): await ctx.send(embed=create_coc6_embed(ctx.author.mention))

@bot.command(name="coc7")
async def coc_7th_cmd(ctx): await ctx.send(embed=create_coc7_embed(ctx.author.mention))

@bot.command(name="coc7elem")
async def coc7_elem_cmd(ctx, age: int = 10):
    age = max(7, min(12, age))
    await ctx.send(embed=create_coc7_elem_embed(ctx.author.mention, age))

@bot.command(name="coc7jhs")
async def coc7_jhs_cmd(ctx, age: int = 13):
    age = max(13, min(14, age))
    await ctx.send(embed=create_coc7_jhs_embed(ctx.author.mention, age))

@bot.command(name="t_特徴表", aliases=["tokucho"])
async def feature_cmd(ctx): await ctx.send(embed=create_ft_embed(ctx.author.mention))

# --- スラッシュコマンド (/) ---
@bot.tree.command(name="coc6", description="6thキャラクターステータス決定")
async def slash_coc6(interaction: discord.Interaction):
    await interaction.response.send_message(embed=create_coc6_embed(interaction.user.mention))

@bot.tree.command(name="coc7", description="7thキャラクターステータス決定")
async def slash_coc7(interaction: discord.Interaction):
    await interaction.response.send_message(embed=create_coc7_embed(interaction.user.mention))

@bot.tree.command(name="coc7_小学生", description="7th小学生探索者作成 (7〜12歳)")
@app_commands.describe(age="対象の年齢 (7〜12)。指定なしで10歳")
async def slash_coc7_elem(interaction: discord.Interaction, age: int = 10):
    age = max(7, min(12, age))
    await interaction.response.send_message(embed=create_coc7_elem_embed(interaction.user.mention, age))

@bot.tree.command(name="coc7_中学生", description="7th中学生探索者作成 (13〜14歳)")
@app_commands.describe(age="対象の年齢 (13〜14)。指定なしで13歳")
async def slash_coc7_jhs(interaction: discord.Interaction, age: int = 13):
    age = max(13, min(14, age))
    await interaction.response.send_message(embed=create_coc7_jhs_embed(interaction.user.mention, age))

@bot.tree.command(name="t_特徴表", description="2015特徴表ダイス決定（3セット）")
async def slash_ft(interaction: discord.Interaction):
    await interaction.response.send_message(embed=create_ft_embed(interaction.user.mention))

bot.run(os.environ.get('DISCORD_BOT_TOKEN'))
