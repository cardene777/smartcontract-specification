---
sidebar_position: 13
---

# DualKeyMultiSig

> **[📋 API仕様書を見る](/api/DualKeyMultiSig)**

## 概要

プライマリキーとセカンダリキーの2段階承認を実装します。

### 継承関係

このコントラクトは以下のコントラクトを継承しています：

- `Initializable`

## 主要機能

### デュアルキー構造

各操作主体（Developer、TrustBank等）にプライマリキーとセカンダリキーを設定。

### キーローテーション

キーの更新を安全に行うローテーション機能。提案→承認→実行のフローで実施。

### 提案管理

キーローテーション提案の作成、承認、実行、キャンセルを管理。

## 関数一覧

<details>
<summary><strong>定数 (1)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`PROPOSAL`](#proposal) | PROPOSAL_EXPIRY 定数の値を取得します。 |

### PROPOSAL

PROPOSAL_EXPIRY 定数の値を取得します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | PROPOSAL_EXPIRYの値を返します。 |

---

</details>

<details>
<summary><strong>Mapping (2)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`getDualKey`](#getdualkey) | dual key を取得します。 |
| [`getKeyRotationProposal`](#getkeyrotationproposal) | key rotation proposal を取得します。 |

### getDualKey

dual key を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `role` | `any` | ✓ | ロールの識別子を指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `primaryKey` | `string` | primaryKeyを返します。 |
| `backupKey` | `string` | backupKeyを返します。 |

---

### getKeyRotationProposal

key rotation proposal を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `role` | `string` | roleを返します。 |
| `oldKey` | `string` | oldKeyを返します。 |
| `newKey` | `string` | newKeyを返します。 |
| `proposer` | `string` | proposerを返します。 |
| `approvalCount` | `string` | approvalCountを返します。 |
| `executed` | `string` | executedを返します。 |
| `createdAt` | `string` | createdAtを返します。 |

---

</details>

<details>
<summary><strong>読み取り関数 (1)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`hasApprovedKeyRotation`](#hasapprovedkeyrotation) | approved key rotation を持っているかどうかを確認します。 |

### hasApprovedKeyRotation

approved key rotation を持っているかどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |
| `approver` | `any` | ✓ | approverを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | ApprovedKeyRotationを持っている場合trueを返します。 |

---

</details>

<details>
<summary><strong>イベント (6)</strong></summary>

### events/DualKeyInitialized

デュアルキーが初期化された時に発行されるイベントです。アドレスと2つのキーが記録されます。

---

### events/Initialized

コントラクトが初期化された時に発行されるイベントです。初期化バージョンが記録されます。

---

### events/KeyRotationApproved

キーローテーションが承認された時に発行されるイベントです。提案ID、承認者が記録されます。

---

### events/KeyRotationCancelled

キーローテーションがキャンセルされた時に発行されるイベントです。提案IDが記録されます。

---

### events/KeyRotationExecuted

キーローテーションが実行された時に発行されるイベントです。古いキーと新しいキーが記録されます。

---

### events/KeyRotationProposed

キーローテーションが提案された時に発行されるイベントです。提案ID、提案者、新しいキーが記録されます。

---

</details>

<details>
<summary><strong>エラー (14)</strong></summary>

| エラー名 | 説明 |
|----------|------|
| `errors/DualKeyMultiSig_AlreadyApproved` | キーローテーション提案が既に承認されている時に返されるエラーです。 |
| `errors/DualKeyMultiSig_AlreadyInitialized` | デュアルキーが既に初期化されている時に返されるエラーです。 |
| `errors/DualKeyMultiSig_InsufficientApprovals` | キーローテーションの承認数が不足している時に返されるエラーです。 |
| `errors/DualKeyMultiSig_InvalidAddress` | 無効なアドレスがデュアルキーに指定された時に返されるエラーです。 |
| `errors/DualKeyMultiSig_InvalidKeyReplacement` | 無効なキー交換が試みられた時に返されるエラーです。 |
| `errors/DualKeyMultiSig_NotAuthorized` | デュアルキー操作の権限がない時に返されるエラーです。 |
| `errors/DualKeyMultiSig_NotInitialized` | デュアルキーが初期化されていない時に返されるエラーです。 |
| `errors/DualKeyMultiSig_ProposalAlreadyExecuted` | キーローテーション提案が既に実行されている時に返されるエラーです。 |
| `errors/DualKeyMultiSig_ProposalExpired` | キーローテーション提案の有効期限が切れた時に返されるエラーです。 |
| `errors/DualKeyMultiSig_ProposalNotFound` | キーローテーション提案が存在しない時に返されるエラーです。 |
| `errors/DualKeyMultiSig_ProposerCannotApprove` | 提案者が自身の提案を承認しようとした時に返されるエラーです。 |
| `errors/InvalidInitialization` | 初期化が無効な時に返されるエラーです。既に初期化済みか、初期化順序が不正です。 |
| `errors/NotInitializing` | 初期化中でない時に返されるエラーです。initializer修飾子のコンテキスト外での呼び出しが原因です。 |
| `errors/ReentrancyGuardReentrantCall` | 再入呼び出しが検出された時に返されるエラーです。同一関数への再帰呼び出しは禁止されています。 |

</details>

