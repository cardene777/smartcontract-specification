---
allowed-tools: Skill(contract-spec-generator)
description: "SolidityコントラクトからOpenAPI仕様書を生成します。"
---

Generate OpenAPI specifications from Solidity smart contracts.

⚠️ **重要**: ユーザーとのやり取りは必ず日本語で行ってください。

## コマンドの役割

**入力**: Solidityコントラクト (← `packages/contract/src/`) + ABI (← `packages/contract/out/`)
**出力**: OpenAPI仕様書 (→ `docs/contract/specs/`)
**次のステップ**: `/generate-contract-docs` でドキュメント生成

---

## 実行フロー

このコマンドは `contract-spec-generator` スキルを呼び出します。

```javascript
Skill({
  skill: "contract-spec-generator"
})
```

スキル内部で以下の処理が自動実行されます：

### フェーズ1: コントラクト分析
1. 全コントラクトリスト化
2. コントラクトフィルタリング
3. 差分検出

### フェーズ2: 中間表現生成
4. ABI → Contract Spec JSON

### フェーズ3: 中間表現強化
5. NatSpec抽出（Solidityソースから）
6. 仕様書の内容詳細化（spec-reviewer エージェント、バックグラウンド実行）

### フェーズ4: OpenAPI仕様書生成
7. Contract Spec JSON → OpenAPI YAML
8. doc-config.json生成
9. サンプル追加（オプション）

---

## 完了後

仕様書生成が完了したら、次のコマンドでドキュメントを生成してください：

```
/generate-contract-docs
```
