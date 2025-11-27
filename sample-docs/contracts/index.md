---
sidebar_position: 0
---

# コントラクト仕様

Avalanche Stablecoinプロジェクトのスマートコントラクト仕様書です。

## コントラクト一覧

### Core Contracts

- **[StablecoinCore](./StablecoinCore)** - ステーブルコインの中核となるコントラクトです
- **[StablecoinProxy](./StablecoinProxy)** - UUPS（Universal Upgradeable Proxy Standard）パターンを採用したプロキシコントラクトです
- **[StablecoinStorage](./StablecoinStorage)** - ステーブルコインの全状態変数を定義するストレージコントラクトです
- **[StablecoinView](./StablecoinView)** - 読み取り専用の関数を集約したビューコントラクトです

### Features

- **[StablecoinIssuance](./StablecoinIssuance)** - トークンの発行（mint）と焼却（burn）機能を提供します
- **[StablecoinTransfer](./StablecoinTransfer)** - トークン転送に関する拡張機能を提供します
- **[StablecoinBank](./StablecoinBank)** - 複数のBank（発行元）による分散発行をサポートする機能です
- **[BankPausable](./BankPausable)** - Bank単位での一時停止機能を提供します

### Access Control

- **[StablecoinRoles](./StablecoinRoles)** - システム全体で使用するロールの定義と管理を行います
- **[StablecoinAdmin](./StablecoinAdmin)** - 管理者向けの設定・操作機能を集約します
- **[BankScopedRoles](./BankScopedRoles)** - Bank単位でのロール管理を実現します
- **[MultiAdminAccessControl](./MultiAdminAccessControl)** - 複数管理者による承認が必要なアクセス制御を実装します

### MultiSig

- **[DualKeyMultiSig](./DualKeyMultiSig)** - プライマリキーとセカンダリキーの2段階承認を実装します
- **[MultiSigWallet](./MultiSigWallet)** - 汎用的なマルチシグネチャウォレット機能を提供します
- **[AccessControlMultiSig](./AccessControlMultiSig)** - ロールベースアクセス制御にマルチシグを統合します
- **[RoleMultiSigManager](./RoleMultiSigManager)** - ロール変更の提案・承認フローを管理します

### Others

- **[ERC20SoladyUpgradeable](./ERC20SoladyUpgradeable)** - Soladyライブラリを使用した効率的なERC20実装です
- **[Dictionary](./Dictionary)** - キーバリュー形式のオンチェーンデータストアです

