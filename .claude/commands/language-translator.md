---
name: language-translator
description: Contract Spec JSONを指定言語に翻訳
---

# Language Translator

Contract Spec JSONを指定言語に翻訳します。

## 使用方法

```bash
/language-translator --contract StablecoinBank --language ja
```

## パラメータ

- `--contract`: コントラクト名（必須）
- `--language`: ターゲット言語（ja/ko/zh、デフォルト: ja）

## サポート言語

- `ja`: 日本語
- `ko`: 韓国語
- `zh`: 中国語（簡体字）

## 内部処理

1. `docs/contract/language.json`から言語設定を読み込み
2. Contract Spec JSON (`docs/contract/ir/{ContractName}.json`) を読み込み
3. 全テキストフィールドを指定言語に翻訳
4. 上書き保存
5. 進捗更新（`python3 .claude/skills/contract-spec-generator/scripts/update-progress-translation.py --contract {ContractName}`）

## 翻訳対象フィールド

- `metadata.description`
- `readFunctions[].documentation.summary/details/notice`
- `writeFunctions[].documentation.summary/details/notice`
- `writeFunctions[].errors[].description`
- `writeFunctions[].errors[].exampleValue.message`
- `events[].documentation.summary`
- `events[].parameters[].description`
