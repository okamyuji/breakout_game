"""
FastAPIアプリケーションのメインモジュール
"""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="Breakout Game",
    description="クラシックなブロック崩しゲームのPyScript実装",
    version="0.1.0"
)

# 静的ファイルとテンプレートの設定
static_dir = Path(__file__).parent / "static"
templates_dir = Path(__file__).parent / "templates"

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

@app.get("/", response_class=HTMLResponse)
async def get_index():
    """
    ゲームのメインページを返す

    Returns:
        HTMLResponse: インデックスページのHTML
    """
    try:
        html_file = templates_dir / "index.html"
        if not html_file.exists():
            raise HTTPException(status_code=404, detail="Template not found")
        
        content = html_file.read_text(encoding="utf-8")
        return HTMLResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    ヘルスチェックエンドポイント

    Returns:
        dict: ステータス情報
    """
    return {"status": "healthy", "version": "0.0.1"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)