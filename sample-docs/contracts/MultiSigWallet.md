---
sidebar_position: 14
---

# MultiSigWallet

> **[📋 API仕様書を見る](/api/MultiSigWallet)**

## 概要

汎用的なマルチシグネチャウォレット機能を提供します。

### 継承関係

このコントラクトは以下のコントラクトを継承しています：

- `Initializable`

## 主要機能

### トランザクション提案

任意のトランザクションを提案として登録。複数署名者の承認を待ちます。

### 署名者管理

署名者の追加・削除、必要承認数の変更が可能。

### トランザクション実行

必要な承認数に達したトランザクションを実行。

## 関数一覧

<details>
<summary><strong>変数 (1)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`requiredApprovals`](#requiredapprovals) | requiredApprovals |

### requiredApprovals

requiredApprovals

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | requiredApprovalsの結果を返します。 |

---

</details>

<details>
<summary><strong>Mapping (2)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`getProposal`](#getproposal) | proposal を取得します。 |
| [`isSigner`](#issigner) | signer かどうかを確認します。 |

### getProposal

proposal を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | 提案情報を返します。 |

---

### isSigner

signer かどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | Signerの場合trueを返します。 |

---

</details>

<details>
<summary><strong>読み取り関数 (3)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`getSignerCount`](#getsignercount) | signer count を取得します。 |
| [`getSigners`](#getsigners) | signers を取得します。 |
| [`hasApproved`](#hasapproved) | approved を持っているかどうかを確認します。 |

### getSignerCount

signer count を取得します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | Signerの数を返します。 |

---

### getSigners

signers を取得します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | 署名者アドレスの配列を返します。 |

---

### hasApproved

approved を持っているかどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |
| `signer` | `any` | ✓ | 署名者のアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | 承認済みの場合trueを返します。 |

---

</details>

<details>
<summary><strong>書き込み関数 (9)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`addSigner`](#addsigner) | addSigner |
| [`approve`](#approve) | spenderが指定された量のトークンを使用することを承認します。 |
| [`cancel`](#cancel) | cel が可能かどうかを確認します。 |
| [`changeRequiredApprovals`](#changerequiredapprovals) | changeRequiredApprovals |
| [`execute`](#execute) | 提案を実行します。 |
| [`initialize`](#initialize) | コントラクトを初期化します。 |
| [`propose`](#propose) | 提案を作成します。 |
| [`removeSigner`](#removesigner) | removeSigner |
| [`revokeApproval`](#revokeapproval) | revokeApproval |

### addSigner

addSigner

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `signer` | `any` | ✓ | 署名者のアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.addSigner(signer);
```

---

### approve

spenderが指定された量のトークンを使用することを承認します。

ERC20標準関数です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.approve(proposalId);
```

---

### cancel

cel が可能かどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.cancel(proposalId);
```

---

### changeRequiredApprovals

changeRequiredApprovals

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `newRequired` | `any` | ✓ | 新しいRequiredを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.changeRequiredApprovals(newRequired);
```

---

### execute

提案を実行します。

必要な承認数が揃った後に実行可能です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.execute(proposalId);
```

---

### initialize

コントラクトを初期化します。

プロキシ経由で一度だけ呼び出し可能です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `signers_` | `any` | ✓ | signers_を指定します。 |
| `requiredApprovals_` | `any` | ✓ | 必要な承認数を指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.initialize(signers_, requiredApprovals_);
```

---

### propose

提案を作成します。

マルチシグ承認が必要な操作です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `target` | `any` | ✓ | 対象コントラクトのアドレスを指定します。 |
| `value` | `any` | ✓ | 値を指定します。 |
| `data` | `any` | ✓ | コールデータを指定します。 |
| `duration` | `any` | ✓ | durationを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `proposalId` | `string` | proposalIdを返します。 |

**使用例:**

```solidity
contract.propose(target, value, data, duration);
```

---

### removeSigner

removeSigner

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `signer` | `any` | ✓ | 署名者のアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.removeSigner(signer);
```

---

### revokeApproval

revokeApproval

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.revokeApproval(proposalId);
```

---

</details>

<details>
<summary><strong>イベント (9)</strong></summary>

### events/ApprovalRevoked

承認が取り消された時に発行されるイベントです。所有者、使用者が記録されます。

---

### events/Initialized

コントラクトが初期化された時に発行されるイベントです。初期化バージョンが記録されます。

---

### events/ProposalApproved

マルチシグ提案が承認された時に発行されるイベントです。提案ID、承認者が記録されます。

---

### events/ProposalCancelled

マルチシグ提案がキャンセルされた時に発行されるイベントです。提案IDが記録されます。

---

### events/ProposalCreated

マルチシグ提案が作成された時に発行されるイベントです。提案ID、作成者、対象、データが記録されます。

---

### events/ProposalExecuted

マルチシグ提案が実行された時に発行されるイベントです。提案ID、実行者が記録されます。

---

### events/RequiredApprovalsChanged

必要承認数が変更された時に発行されるイベントです。新しい必要承認数が記録されます。

---

### events/SignerAdded

マルチシグに署名者が追加された時に発行されるイベントです。追加された署名者が記録されます。

---

### events/SignerRemoved

マルチシグから署名者が削除された時に発行されるイベントです。削除された署名者が記録されます。

---

</details>

<details>
<summary><strong>エラー (18)</strong></summary>

| エラー名 | 説明 |
|----------|------|
| `errors/InvalidInitialization` | 初期化が無効な時に返されるエラーです。既に初期化済みか、初期化順序が不正です。 |
| `errors/MultiSig_AlreadyApproved` | 既に承認済みの提案を再度承認しようとした時に返されるエラーです。 |
| `errors/MultiSig_CannotRemoveLastSigner` | 最後の署名者を削除しようとした時に返されるエラーです。 |
| `errors/MultiSig_ExecutionFailed` | 提案の実行が失敗した時に返されるエラーです。 |
| `errors/MultiSig_InsufficientApprovals` | 必要な承認数に達していない時に返されるエラーです。 |
| `errors/MultiSig_InvalidDuration` | 無効な有効期限が指定された時に返されるエラーです。 |
| `errors/MultiSig_InvalidRequiredApprovals` | 無効な必要承認数が指定された時に返されるエラーです。 |
| `errors/MultiSig_InvalidSigner` | 無効な署名者が指定された時に返されるエラーです。 |
| `errors/MultiSig_InvalidTarget` | 無効なターゲットアドレスが指定された時に返されるエラーです。 |
| `errors/MultiSig_NotApproved` | 承認されていない提案を実行しようとした時に返されるエラーです。 |
| `errors/MultiSig_NotSigner` | 署名者ではないアカウントが操作を試みた時に返されるエラーです。 |
| `errors/MultiSig_ProposalAlreadyCancelled` | 既にキャンセルされた提案を操作しようとした時に返されるエラーです。 |
| `errors/MultiSig_ProposalAlreadyExecuted` | 既に実行された提案を再度実行しようとした時に返されるエラーです。 |
| `errors/MultiSig_ProposalExpired` | 提案の有効期限が切れた時に返されるエラーです。 |
| `errors/MultiSig_ProposalNotFound` | 指定された提案が存在しない時に返されるエラーです。 |
| `errors/MultiSig_SignerAlreadyExists` | 既に存在する署名者を追加しようとした時に返されるエラーです。 |
| `errors/NotInitializing` | 初期化中でない時に返されるエラーです。initializer修飾子のコンテキスト外での呼び出しが原因です。 |
| `errors/ReentrancyGuardReentrantCall` | 再入呼び出しが検出された時に返されるエラーです。同一関数への再帰呼び出しは禁止されています。 |

</details>

