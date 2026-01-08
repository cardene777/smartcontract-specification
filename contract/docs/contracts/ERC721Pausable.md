---
id: ERC721Pausable
title: ERC721Pausable Solidity Interface
sidebar_label: ERC721Pausable
---

# ERC721Pausable Solidity Interface

NFTの転送を一時停止できる拡張機能。

## 基本情報

| 項目 | 内容 |
|------|------|
| コントラクト名 | ERC721Pausable |
| カテゴリ | ERC721 トークン |
| バージョン | 1.0.0 |

## 概要

ERC721Pausableは、ERC721トークンに一時停止機能を追加する拡張コントラクトです。管理者は、NFTの転送、鋳造、焼却といったすべての状態変更操作を一時的に凍結できます。セキュリティインシデントの発生時や、スマートコントラクトのアップグレード中など、緊急時にNFTの動きを制御する必要がある場合に有用です。

一時停止状態では、すべての転送操作が自動的にブロックされ、EnforcedPauseエラーで失敗します。このコントラクト自体は公開のpause/unpause関数を提供しないため、実装時にはAccessControlやOwnableなどのアクセス制御機構と組み合わせて使用する必要があります。

このコントラクトは以下のコントラクトを継承しています：
- ERC721
- Pausable

## 主要機能

### 一時停止状態の確認

`paused`関数で、現在のコントラクトが一時停止状態かどうかを確認できます。この関数はガスコストなしでいつでも呼び出し可能で、DAppsはこの情報をもとにUIを調整できます。

```mermaid
sequenceDiagram
    participant Client
    participant ERC721Pausable
    Client->>ERC721Pausable: paused()
    ERC721Pausable-->>Client: false
    Note over ERC721Pausable: 管理者が_pause()を実行
    Client->>ERC721Pausable: paused()
    ERC721Pausable-->>Client: true
```

### 一時停止中の転送制限

一時停止状態では、`transferFrom`、`safeTransferFrom`などのすべての転送操作が拒否されます。これにより、セキュリティ上の脅威が検出された場合に、管理者は迅速にNFTの流動性を停止し、被害の拡大を防ぐことができます。

```mermaid
sequenceDiagram
    participant Admin
    participant ERC721Pausable
    participant Alice
    Admin->>ERC721Pausable: _pause()
    ERC721Pausable->>ERC721Pausable: emit Paused(Admin)
    Alice->>ERC721Pausable: transferFrom(Alice, Bob, 1)
    ERC721Pausable->>ERC721Pausable: Check whenNotPaused
    ERC721Pausable-->>Alice: revert EnforcedPause()
    Admin->>ERC721Pausable: _unpause()
    ERC721Pausable->>ERC721Pausable: emit Unpaused(Admin)
    Alice->>ERC721Pausable: transferFrom(Alice, Bob, 1)
    ERC721Pausable->>ERC721Pausable: owner[1] = Bob
    ERC721Pausable-->>Alice: success
```

## 要素一覧

<details>
<summary><strong>📋 関数 (1個)</strong></summary>

| 関数名 | 可視性 | 状態変更 | 説明 |
|--------|--------|----------|------|
| `paused()` | public | view | コントラクトが一時停止状態かどうかを確認します。<br />一時停止状態の場合、NFTの転送、鋳造、焼却が実行できません。 |


</details>

<details>
<summary><strong>📡 イベント (2個)</strong></summary>

| イベント名 | パラメータ | 説明 |
|-----------|-----------|------|
| `Paused` | `address account` | コントラクトが一時停止された時に発行されるイベントです。 |
| `Unpaused` | `address account` | コントラクトの一時停止が解除された時に発行されるイベントです。 |


</details>

<details>
<summary><strong>⚠️ エラー (2個)</strong></summary>

| エラー名 | パラメータ | 説明 |
|---------|-----------|------|
| `EnforcedPause` | なし | 一時停止中に禁止された操作が試みられた時に返されるエラーです。 |
| `ExpectedPause` | なし | 一時停止が必要な操作が非停止状態で試みられた時に返されるエラーです。 |


</details>

## API仕様書

詳細なAPI仕様は以下のリンクから確認できます。

[ERC721Pausable API仕様書を見る](/api/ERC721Pausable)
