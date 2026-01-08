# smartcontract-specification

## コントラクトのビルド方法

### 前提条件
- Node.js (v18以上推奨)

### セットアップ
```bash
npm install
```

### ビルド
```bash
npx hardhat compile
```

ビルド成功後、ABIファイルは `artifacts/@openzeppelin/contracts/token/ERC20/ERC20.sol/ERC20.json` に生成されます。

### その他のコマンド
```bash
# クリーンアップ
npx hardhat clean

# ヘルプ
npx hardhat help
```

## 生成

### 仕様書生成

```bash
ABIは artifacts/@openzeppelin/contracts/token/ERC20/ERC20.sol/ERC20.json、コントラクトは node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol にあります。contract-spec-generator agentを使用して仕様書を作成してください。
```

### ドキュメント生成

```
contract-doc-generator skillを使用して、仕様書からドキュメントを作成してください。
```

### サイト生成

```
contract-site-builder skillを使用して、Docusaurusサイトを構築してください。
```