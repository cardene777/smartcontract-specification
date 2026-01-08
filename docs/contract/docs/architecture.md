---
id: architecture
title: アーキテクチャ
sidebar_label: アーキテクチャ
---

# アーキテクチャ設計

## コントラクト構造

ERC20コントラクトは、モジュラー設計に基づいて構築されています。

```mermaid
classDiagram
    class Context {
        <<abstract>>
        +_msgSender() address
        +_msgData() bytes
    }

    class IERC20 {
        <<interface>>
        +totalSupply() uint256
        +balanceOf(address) uint256
        +transfer(address, uint256) bool
        +allowance(address, address) uint256
        +approve(address, uint256) bool
        +transferFrom(address, address, uint256) bool
    }

    class IERC20Metadata {
        <<interface>>
        +name() string
        +symbol() string
        +decimals() uint8
    }

    class IERC20Errors {
        <<interface>>
    }

    class ERC20 {
        <<abstract>>
        -_balances mapping
        -_allowances mapping
        -_totalSupply uint256
        -_name string
        -_symbol string
        +name() string
        +symbol() string
        +decimals() uint8
        +totalSupply() uint256
        +balanceOf(address) uint256
        +transfer(address, uint256) bool
        +allowance(address, address) uint256
        +approve(address, uint256) bool
        +transferFrom(address, address, uint256) bool
        #_transfer(address, address, uint256)
        #_update(address, address, uint256)
        #_mint(address, uint256)
        #_burn(address, uint256)
        #_approve(address, address, uint256)
        #_spendAllowance(address, address, uint256)
    }

    Context <|-- ERC20
    IERC20 <|.. ERC20
    IERC20Metadata <|.. ERC20
    IERC20Errors <|.. ERC20
```

## 状態変数

| 変数名 | 型 | アクセス | 説明 |
|--------|-----|---------|------|
| `_balances` | `mapping(address => uint256)` | private | 各アドレスのトークン残高 |
| `_allowances` | `mapping(address => mapping(address => uint256))` | private | 所有者からspenderへの許可量 |
| `_totalSupply` | `uint256` | private | トークンの総供給量 |
| `_name` | `string` | private | トークンの名前 |
| `_symbol` | `string` | private | トークンのシンボル |

## 関数の階層

```mermaid
flowchart TD
    subgraph Public["パブリック関数"]
        transfer[transfer]
        transferFrom[transferFrom]
        approve[approve]
    end

    subgraph Internal["内部関数"]
        _transfer[_transfer]
        _update[_update]
        _approve[_approve]
        _spendAllowance[_spendAllowance]
    end

    transfer --> _transfer
    transferFrom --> _spendAllowance
    transferFrom --> _transfer
    approve --> _approve
    _transfer --> _update
    _spendAllowance --> _approve
```

## 拡張ポイント

ERC20コントラクトは以下の関数をオーバーライドすることで拡張できます：

| 関数 | 拡張例 |
|------|--------|
| `_update` | 転送フック、手数料、ブラックリスト |
| `decimals` | カスタム小数点桁数 |
| `_approve` | カスタム許可ロジック |
