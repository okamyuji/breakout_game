# API Documentation

## 概要

このドキュメントでは、Breakout GameのAPIエンドポイントとゲームコンポーネントについて説明します。

## エンドポイント

### メインページ取得

- GET /
インデックスページを返します。

**レスポンス**: HTML（ゲームページ）

### ヘルスチェック

- GET /health

サーバーの状態を確認します。

**レスポンス**:

```json
{
    "status": "healthy",
    "version": "0.1.0"
}
```

## ゲームコンポーネント

### パドル

```python
paddle = {
    "x": int,           # X座標位置
    "y": int,           # Y座標位置（固定）
    "width": int,       # パドルの幅
    "height": int,      # パドルの高さ
    "speed": int        # 移動速度
}
```

### ボール

```python
ball = {
    "x": float,         # X座標位置
    "y": float,        # Y座標位置
    "radius": int,     # ボールの半径
    "dx": float,       # X方向の速度
    "dy": float,       # Y方向の速度
    "speed": float     # 基本速度
}
```

## ブロック

```python
block = {
    "x": int,          # X座標位置
    "y": int,          # Y座標位置
    "width": int,      # ブロックの幅
    "height": int,     # ブロックの高さ
    "color": str,      # ブロックの色
    "points": int      # 得点
}
```

## ゲームイベント

### キーボード入力

- ArrowLeft: パドルを左に移動
- ArrowRight: パドルを右に移動
- Space: ゲームオーバー時のリスタート

### コリジョン検出

```python
def check_collision(ball: dict, rect: dict) -> bool:
    """
    ボールと矩形の衝突判定を行う

    Parameters:
        ball (dict): ボールオブジェクト
        rect (dict): 矩形オブジェクト（パドルまたはブロック）

    Returns:
        bool: 衝突している場合はTrue
    """
```

### スコアリング

- 各ブロックの得点は行によって異なります
- 上の行のブロックほど高得点
- 全ブロックの破壊でゲームクリア

## エラーハンドリング

### 404 Not Found

テンプレートファイルが見つからない場合に発生

### 500 Internal Server Error

サーバー内部エラーが発生した場合

## 開発者向けツール

### デバッグモード

```bash
uvicorn src.breakout_game.main:app --reload --log-level debug
```

### テストカバレッジレポート

```bash
python -m pytest --cov=src/breakout_game --cov-report=html
```

## パフォーマンス最適化

### レンダリングの最適化

- requestAnimationFrameの使用
- キャンバスのダブルバッファリング

### 衝突判定の最適化

- 簡易的なバウンディングボックス判定
- 詳細な衝突判定は必要な場合のみ

## バージョニング

- セマンティックバージョニングに従います
    - MAJOR: 互換性のない変更
    - MINOR: 後方互換性のある機能追加
    - PATCH: 後方互換性のあるバグ修正

## セキュリティ

- クロスサイトスクリプティング（XSS）対策済み
- 入力値のバリデーション実装済み
- CORS設定による適切なアクセス制御
