# Breakout Game

PyScriptとFastAPIを使用したクラシックなブロック崩しゲーム実装です。

## 特徴

- クラシックなレトロゲームデザイン
- ブラウザ上で動作する軽量な実装
- モダンなPythonフレームワークを使用
- レスポンシブなゲームプレイ

## 技術スタック

- バックエンド: FastAPI
- フロントエンド: PyScript
- 開発言語: Python 3.11+
- パッケージ管理: pip

## 必要要件

- Python 3.11以上
- pip（パッケージインストール用）
- モダンなWebブラウザ

## セットアップ

1. リポジトリのクローン

    ```bash
    git clone https://github.com/okamyuji/breakout_game.git
    cd breakout_game
    ```

2. 仮想環境の作成とアクティベート

    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3. 依存パッケージのインストール

    ```bash
    pip install -r requirements.txt
    ```

4. アプリケーションの起動

    ```bash
    uvicorn src.breakout_game.main:app --reload
    ```

5. ブラウザでアクセス

    ```bash
    http://localhost:8000
    ```

## プロジェクト構造

```bash
breakout_game/
├── src/
│   └── breakout_game/
│       ├── static/
│       │   ├── css/
│       │   └── game.py
│       ├── templates/
│       │   └── index.html
│       ├── __init__.py
│       └── main.py
├── tests/
├── docs/
└── requirements.txt
```

## 開発ガイドライン

- コードスタイル: PEP 8に準拠
- コミットメッセージ: 英語で簡潔に
- テストカバレッジ: 80%以上を維持
- ドキュメント: docstringとコメントを適切に使用

## テスト実行

```bash
python -m pytest
```

## ライセンス

このプロジェクトはMITライセンスで提供されています。詳細は[LICENSE](LICENSE)を参照してください。
