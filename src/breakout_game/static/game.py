import asyncio
import math

from js import Math, console, document
from pyodide.ffi import create_proxy


async def wait_for_dom():
    while document.readyState != "complete":
        await asyncio.sleep(0.1)

async def main():
    await wait_for_dom()

    canvas = document.getElementById("gameCanvas")
    if not canvas:
        console.log("canvasが見つかりません")
        return
    ctx = canvas.getContext("2d")
    WIDTH = canvas.width
    HEIGHT = canvas.height

    # ゲーム状態
    global game_over, paddle, ball, blocks, score
    game_over = False

    def reset_game():
        global game_over, paddle, ball, blocks, score
        game_over = False

        # パドルの初期設定
        paddle = {
            "x": WIDTH // 2 - 50,
            "y": HEIGHT - 30,
            "width": 100,
            "height": 10,
            "speed": 7
        }

        # ボールの初期設定
        ball = {
            "x": WIDTH // 2,
            "y": HEIGHT - 50,
            "radius": 8,
            "dx": 4,
            "dy": -4,
            "speed": 6
        }

        # ブロックの設定
        block_rows = 5
        block_cols = 8
        block_width = 80
        block_height = 20
        block_padding = 10
        blocks.clear()
        
        colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF"]
        
        for row in range(block_rows):
            for col in range(block_cols):
                block = {
                    "x": col * (block_width + block_padding) + block_padding,
                    "y": row * (block_height + block_padding) + block_padding + 50,
                    "width": block_width,
                    "height": block_height,
                    "color": colors[row],
                    "points": (block_rows - row) * 10
                }
                blocks.append(block)

        score = 0

    # 初期化
    blocks = []
    reset_game()

    # キー管理
    keys = {}

    def on_key_down(event):
        global game_over
        if game_over and event.key == " ":
            reset_game()
            return
        keys[event.key] = True

    def on_key_up(event):
        keys[event.key] = False

    keydown_proxy = create_proxy(on_key_down)
    keyup_proxy = create_proxy(on_key_up)
    document.addEventListener("keydown", keydown_proxy)
    document.addEventListener("keyup", keyup_proxy)

    def check_collision(ball, rect):
        closest_x = max(rect["x"], min(ball["x"], rect["x"] + rect["width"]))
        closest_y = max(rect["y"], min(ball["y"], rect["y"] + rect["height"]))
        
        distance_x = ball["x"] - closest_x
        distance_y = ball["y"] - closest_y
        
        return (distance_x * distance_x + distance_y * distance_y) <= (ball["radius"] * ball["radius"])

    def update_game():
        global game_over

        if game_over:
            return

        # パドル移動
        if keys.get("ArrowLeft"):
            paddle["x"] -= paddle["speed"]
        if keys.get("ArrowRight"):
            paddle["x"] += paddle["speed"]
        
        paddle["x"] = max(0, min(paddle["x"], WIDTH - paddle["width"]))

        # ボール移動
        ball["x"] += ball["dx"]
        ball["y"] += ball["dy"]

        # 壁との衝突
        if ball["x"] - ball["radius"] <= 0 or ball["x"] + ball["radius"] >= WIDTH:
            ball["dx"] *= -1
        if ball["y"] - ball["radius"] <= 0:
            ball["dy"] *= -1

        # パドルとの衝突
        if check_collision(ball, paddle):
            relative_intersect_x = (ball["x"] - (paddle["x"] + paddle["width"]/2)) / (paddle["width"]/2)
            bounce_angle = relative_intersect_x * Math.PI/3
            ball["dx"] = ball["speed"] * Math.sin(bounce_angle)
            ball["dy"] = -ball["speed"] * Math.cos(bounce_angle)

        # ブロックとの衝突
        for block in blocks[:]:
            if check_collision(ball, block):
                ball["dy"] *= -1
                blocks.remove(block)
                global score
                score += block["points"]
                break

        # ゲームオーバー判定
        if ball["y"] + ball["radius"] >= HEIGHT:
            game_over = True

        # クリア判定
        if not blocks:
            game_over = True

    def draw_game():
        ctx.clearRect(0, 0, WIDTH, HEIGHT)

        if game_over:
            ctx.fillStyle = "white"
            ctx.font = "30px 'Press Start 2P', sans-serif"
            if not blocks:
                ctx.fillText("GAME CLEAR!", WIDTH // 2 - 150, HEIGHT // 2)
            else:
                ctx.fillText("GAME OVER", WIDTH // 2 - 120, HEIGHT // 2)
            ctx.font = "20px 'Press Start 2P', sans-serif"
            ctx.fillText("Press SPACE to Restart", WIDTH // 2 - 180, HEIGHT // 2 + 40)
            return

        # パドル描画
        ctx.fillStyle = "#00FF00"
        ctx.fillRect(paddle["x"], paddle["y"], paddle["width"], paddle["height"])

        # ボール描画
        ctx.beginPath()
        ctx.arc(ball["x"], ball["y"], ball["radius"], 0, Math.PI * 2)
        ctx.fillStyle = "white"
        ctx.fill()
        ctx.closePath()

        # ブロック描画
        for block in blocks:
            ctx.fillStyle = block["color"]
            ctx.fillRect(block["x"], block["y"], block["width"], block["height"])
            ctx.strokeStyle = "white"
            ctx.strokeRect(block["x"], block["y"], block["width"], block["height"])

        # スコア表示
        ctx.fillStyle = "white"
        ctx.font = "20px 'Press Start 2P', sans-serif"
        ctx.fillText("Score: " + str(score), 10, 30)

    while True:
        update_game()
        draw_game()
        await asyncio.sleep(1/60)

asyncio.create_task(main())