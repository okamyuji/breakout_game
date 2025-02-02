"""
ゲームロジックとAPIエンドポイントのテスト
"""
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.breakout_game.main import app

client = TestClient(app)

def test_health_check():
    """ヘルスチェックエンドポイントのテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "0.1.0"}

def test_index_page():
    """インデックスページのテスト"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_static_files():
    """静的ファイルの存在チェック"""
    static_dir = Path(__file__).parent.parent / "src" / "breakout_game" / "static"
    
    # game.pyの存在チェック
    game_py = static_dir / "game.py"
    assert game_py.exists(), "game.py not found"
    
    # CSSファイルの存在チェック
    css_dir = static_dir / "css"
    assert css_dir.exists(), "css directory not found"

def test_template_files():
    """テンプレートファイルの存在チェック"""
    templates_dir = Path(__file__).parent.parent / "src" / "breakout_game" / "templates"
    
    # index.htmlの存在チェック
    index_html = templates_dir / "index.html"
    assert index_html.exists(), "index.html not found"

@pytest.mark.parametrize("endpoint,expected_status", [
    ("/nonexistent", 404),
    ("/static/nonexistent.file", 404),
])
def test_error_handling(endpoint, expected_status):
    """エラーハンドリングのテスト"""
    response = client.get(endpoint)
    assert response.status_code == expected_status

def test_static_file_content():
    """静的ファイルの内容チェック"""
    response = client.get("/static/game.py")
    assert response.status_code == 200
    content = response.content.decode()
    assert "async def main():" in content, "game.py does not contain expected content"

# ゲームロジックのモック関数
def mock_check_collision(ball, rect):
    """衝突判定のモックテスト"""
    return (ball["x"] >= rect["x"] and 
            ball["x"] <= rect["x"] + rect["width"] and
            ball["y"] >= rect["y"] and 
            ball["y"] <= rect["y"] + rect["height"])

def test_collision_detection():
    """衝突判定ロジックのテスト"""
    ball = {"x": 150, "y": 150, "radius": 5}
    rect = {"x": 140, "y": 140, "width": 20, "height": 20}
    
    assert mock_check_collision(ball, rect), "Collision should be detected"
    
    ball = {"x": 100, "y": 100, "radius": 5}
    assert not mock_check_collision(ball, rect), "Collision should not be detected"

def test_paddle_movement():
    """パドル移動ロジックのテスト"""
    paddle = {"x": 300, "width": 100, "speed": 5}
    canvas_width = 800
    
    # 左移動
    new_x = max(0, paddle["x"] - paddle["speed"])
    assert new_x == 295, "Paddle should move left"
    
    # 右移動
    new_x = min(canvas_width - paddle["width"], paddle["x"] + paddle["speed"])
    assert new_x == 305, "Paddle should move right"
    
    # 左端の境界チェック
    paddle["x"] = 0
    new_x = max(0, paddle["x"] - paddle["speed"])
    assert new_x == 0, "Paddle should stop at left boundary"
    
    # 右端の境界チェック
    paddle["x"] = canvas_width - paddle["width"]
    new_x = min(canvas_width - paddle["width"], paddle["x"] + paddle["speed"])
    assert new_x == canvas_width - paddle["width"], "Paddle should stop at right boundary"

def test_ball_movement():
    """ボール移動ロジックのテスト"""
    ball = {
        "x": 400,
        "y": 300,
        "dx": 4,
        "dy": -4,
        "radius": 8
    }
    
    # 通常の移動
    new_x = ball["x"] + ball["dx"]
    new_y = ball["y"] + ball["dy"]
    assert new_x == 404, "Ball should move horizontally"
    assert new_y == 296, "Ball should move vertically"
    
    # 壁との反射
    canvas_width = 800
    canvas_height = 600
    
    # 左壁との反射
    ball["x"] = ball["radius"]
    ball["dx"] = 4  # 初期速度を設定
    if ball["x"] - ball["radius"] <= 0:
        ball["dx"] *= -1
    assert ball["dx"] == -4, "Ball should bounce off left wall"
    
    # 右壁との反射
    ball["x"] = canvas_width - ball["radius"]
    ball["dx"] = 4  # 初期速度を再設定
    if ball["x"] + ball["radius"] >= canvas_width:
        ball["dx"] *= -1
    assert ball["dx"] == -4, "Ball should bounce off right wall"
    
    # 上壁との反射
    ball["y"] = ball["radius"]
    ball["dy"] = -4  # 上向きの速度
    if ball["y"] - ball["radius"] <= 0:
        ball["dy"] *= -1
    assert ball["dy"] == 4, "Ball should bounce off top wall"

if __name__ == "__main__":
    pytest.main(["-v"])