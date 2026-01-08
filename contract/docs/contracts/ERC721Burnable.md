---
id: ERC721Burnable
title: ERC721Burnable Solidity Interface
sidebar_label: ERC721Burnable
---

# ERC721Burnable Solidity Interface

NFT保有者が自分のトークンを焼却できる拡張機能。

## 基本情報

| 項目 | 内容 |
|------|------|
| コントラクト名 | ERC721Burnable |
| カテゴリ | ERC721 トークン |
| バージョン | 1.0.0 |

## 概要

ERC721Burnableは、ERC721トークンにNFT焼却(バーン)機能を追加する拡張コントラクトです。NFT保有者は、自身が所有するトークンまたは承認されたトークンを永久に破棄できます。焼却されたNFTは完全に消失し、復元することはできません。この機能は、ゲームアイテムの消費、不要なNFTの処分、トークンエコノミーの調整など、様々なユースケースで使用されます。

`burn`関数を呼び出すと、指定されたトークンIDのNFTが焼却されます。呼び出し元は、トークンの所有者であるか、承認されたオペレーターである必要があります。焼却時には、所有者のbalanceが減少し、トークンの所有権情報が削除されます。また、fromが所有者、toがゼロアドレスのTransferイベントが発行されるため、オフチェーンでの追跡が可能です。

このコントラクトは以下のコントラクトを継承しています：
- ERC721

## 主要機能

### NFTの焼却

`burn`関数を使用して、NFTを永久に破棄できます。呼び出し元がトークンの所有者であるか、承認されたオペレーター(approveまたはsetApprovalForAllで権限付与)である必要があります。焼却されたトークンは、総供給から削除され、二度と使用できなくなります。この操作は不可逆的であり、慎重に実行する必要があります。

```mermaid
sequenceDiagram
    participant Alice
    participant ERC721Burnable
    Alice->>ERC721Burnable: burn(tokenId=1)
    ERC721Burnable->>ERC721Burnable: Check owner[1] == Alice or approved
    ERC721Burnable->>ERC721Burnable: balance[Alice] -= 1
    ERC721Burnable->>ERC721Burnable: delete owner[1]
    ERC721Burnable->>ERC721Burnable: delete tokenApprovals[1]
    ERC721Burnable->>ERC721Burnable: emit Transfer(Alice, 0x0, 1)
    ERC721Burnable-->>Alice: success
```

### 承認されたNFTの焼却

承認されたオペレーターは、トークン所有者に代わってNFTを焼却できます。この機能は、ゲーム内でアイテムを自動的に消費するスマートコントラクトや、DAO が決定に基づいてNFTを削除する場合などに使用されます。焼却には適切な承認が必要であり、承認がない場合はエラーで失敗します。

```mermaid
sequenceDiagram
    participant Game
    participant ERC721Burnable
    participant Alice
    Alice->>ERC721Burnable: approve(Game, tokenId=5)
    ERC721Burnable->>ERC721Burnable: tokenApprovals[5] = Game
    Game->>ERC721Burnable: burn(tokenId=5)
    ERC721Burnable->>ERC721Burnable: Check approved[5] == Game
    ERC721Burnable->>ERC721Burnable: balance[Alice] -= 1
    ERC721Burnable->>ERC721Burnable: delete owner[5]
    ERC721Burnable->>ERC721Burnable: emit Transfer(Alice, 0x0, 5)
    ERC721Burnable-->>Game: success
```

## 要素一覧

<details>
<summary><strong>📋 関数 (1個)</strong></summary>

| 関数名 | 可視性 | 状態変更 | 説明 |
|--------|--------|----------|------|
| `burn(uint256)` | public | - | 指定されたトークンIDのNFTを焼却します。<br />呼び出し元はトークンの所有者であるか、承認されたオペレーターである必要があります。焼却されたNFTは永久に削除され、復元できません。 |


</details>

<details>
<summary><strong>📡 イベント (1個)</strong></summary>

| イベント名 | パラメータ | 説明 |
|-----------|-----------|------|
| `Transfer` | `address indexed from`<br />`address indexed to`<br />`uint256 indexed tokenId` | NFTが焼却された時に発行されるイベントです。toパラメータはゼロアドレスになります。 |


</details>

<details>
<summary><strong>⚠️ エラー (2個)</strong></summary>

| エラー名 | パラメータ | 説明 |
|---------|-----------|------|
| `ERC721InsufficientApproval` | `address operator`<br />`uint256 tokenId` | 呼び出し元に焼却の権限がない時に返されるエラーです。 |
| `ERC721NonexistentToken` | `uint256 tokenId` | 存在しないトークンIDが指定された時に返されるエラーです。 |


</details>

## API仕様書

詳細なAPI仕様は以下のリンクから確認できます。

[ERC721Burnable API仕様書を見る](/api/ERC721Burnable)
