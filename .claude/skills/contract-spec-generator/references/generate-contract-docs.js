/**
 * Markdown Documentation Generator
 *
 * OpenAPI/Swagger仕様ファイルからDocusaurus用のMarkdownドキュメントを生成します。
 *
 * 使用方法:
 *   node generate-contract-docs.js
 *
 * 出力先:
 *   ../docs-site/docs/contracts/{ContractName}.md
 */

const fs = require('fs');
const path = require('path');

// 設定
const CONFIG = {
  specsDir: path.join(__dirname, '../docs/contract'),
  outputDir: path.join(__dirname, '../docs-site/docs/contracts'),
  sidebarPath: path.join(__dirname, '../docs-site/sidebars.js'),
};

// コントラクトのカテゴリ分類
const CONTRACT_CATEGORIES = {
  'Core Contracts': ['StablecoinCore', 'StablecoinProxy', 'StablecoinStorage', 'StablecoinView'],
  'Features': ['StablecoinIssuance', 'StablecoinTransfer', 'StablecoinBank', 'BankPausable'],
  'Access Control': ['StablecoinRoles', 'StablecoinAdmin', 'BankScopedRoles', 'MultiAdminAccessControl'],
  'MultiSig': ['DualKeyMultiSig', 'MultiSigWallet', 'AccessControlMultiSig', 'RoleMultiSigManager'],
  'Others': ['ERC20SoladyUpgradeable', 'Dictionary'],
};

// コントラクトの詳細説明（主要機能含む）
const CONTRACT_DESCRIPTIONS = {
  'StablecoinCore': {
    overview: 'ステーブルコインの中核となるコントラクトです。全ての機能モジュールを統合し、ERC20準拠のトークンとして動作します。',
    features: [
      {
        title: 'ERC20トークン機能',
        description: '標準的なERC20インターフェース（transfer, approve, transferFrom等）を実装。Soladyライブラリによる効率的な実装を採用しています。',
      },
      {
        title: 'ロールベースアクセス制御',
        description: 'ISSUER_ROLE、BURNER_ROLE、PAUSER_ROLE等の複数ロールによる細かな権限管理を実現。各ロールに対応した操作のみが許可されます。',
      },
      {
        title: 'Bank機能',
        description: '複数のBank（発行元）による分散発行をサポート。各Bankは独自の発行上限（cap）と発行残高を持ち、独立して運用できます。',
      },
      {
        title: 'デュアルキーマルチシグ',
        description: '重要な操作（ロール変更、キーローテーション等）にはプライマリキーとセカンダリキーの両方の承認が必要。セキュリティを強化します。',
      },
    ],
  },
  'StablecoinProxy': {
    overview: 'UUPS（Universal Upgradeable Proxy Standard）パターンを採用したプロキシコントラクトです。',
    features: [
      {
        title: 'アップグレード機能',
        description: 'UPGRADER_ROLEを持つアカウントがコントラクトの実装を更新可能。ストレージは保持されたまま、ロジックのみを差し替えられます。',
      },
      {
        title: 'delegatecall転送',
        description: '全ての呼び出しを実装コントラクトに転送。ユーザーはプロキシアドレスのみを意識すれば良く、アップグレード後も同じアドレスで利用できます。',
      },
    ],
  },
  'StablecoinStorage': {
    overview: 'ステーブルコインの全状態変数を定義するストレージコントラクトです。',
    features: [
      {
        title: 'ストレージレイアウト管理',
        description: 'アップグレード時のストレージ衝突を防ぐため、全ての状態変数を一元管理。新しい変数は既存レイアウトの末尾に追加されます。',
      },
      {
        title: '定数定義',
        description: 'ロール識別子（ISSUER_ROLE等）、提案の有効期限、必要承認数などの定数を定義。システム全体で一貫した値を使用します。',
      },
    ],
  },
  'StablecoinView': {
    overview: '読み取り専用の関数を集約したビューコントラクトです。ガス消費なしで状態を照会できます。',
    features: [
      {
        title: '残高・供給量の照会',
        description: 'balanceOf、totalSupply等のERC20標準ビュー関数を提供。',
      },
      {
        title: 'ロール・権限の確認',
        description: 'hasRole、getRoleAdmin等でアカウントの権限状態を確認可能。',
      },
      {
        title: 'Bank情報の取得',
        description: 'Bank単位の発行上限、発行残高、一時停止状態などを照会可能。',
      },
    ],
  },
  'StablecoinIssuance': {
    overview: 'トークンの発行（mint）と焼却（burn）機能を提供します。',
    features: [
      {
        title: 'トークン発行（mint）',
        description: 'ISSUER_ROLEを持つアカウントが指定アドレスにトークンを発行。Bank単位の発行上限チェックも行われます。',
      },
      {
        title: 'トークン焼却（burn）',
        description: 'BURNER_ROLEを持つアカウントがトークンを焼却。流通量の調整に使用します。',
      },
      {
        title: 'Bank別発行管理',
        description: '各BankのISSUER_ROLEは自身のBank上限内でのみ発行可能。Bank間の独立性を保証します。',
      },
    ],
  },
  'StablecoinTransfer': {
    overview: 'トークン転送に関する拡張機能を提供します。コンプライアンス要件への対応を含みます。',
    features: [
      {
        title: '強制転送（forceTransfer）',
        description: 'FORCE_TRANSFER_ROLEを持つアカウントが任意のアドレス間でトークンを強制的に移動。法的要件への対応に使用します。',
      },
      {
        title: 'アローリスト',
        description: 'ALLOWLIST_ROLEでアカウントをホワイトリストに追加。許可されたアカウントのみが転送可能な制限モードを実現。',
      },
      {
        title: 'アカウント凍結',
        description: 'FREEZER_ROLEで特定アカウントの転送を禁止。不正行為への対応に使用します。',
      },
    ],
  },
  'StablecoinBank': {
    overview: '複数のBank（発行元）による分散発行をサポートする機能です。',
    features: [
      {
        title: 'Bank登録・管理',
        description: '新しいBankの登録、発行上限（cap）の設定、Bank情報の更新を管理。',
      },
      {
        title: '発行残高追跡',
        description: '各Bankの発行済み残高（outstanding）を追跡。発行上限との比較で発行可能量を判定。',
      },
      {
        title: 'Bank別ロール',
        description: '各BankにISSUER、BURNER、PAUSER等のロールを個別に割り当て可能。Bank単位での権限分離を実現。',
      },
    ],
  },
  'BankPausable': {
    overview: 'Bank単位での一時停止機能を提供します。',
    features: [
      {
        title: 'Bank別一時停止',
        description: 'BANK_PAUSER_ROLEを持つアカウントが特定のBankのみを一時停止。他のBankへの影響を最小限に抑えます。',
      },
      {
        title: 'グローバル一時停止',
        description: 'PAUSER_ROLEによる全体の一時停止も可能。緊急時に全操作を停止できます。',
      },
    ],
  },
  'StablecoinRoles': {
    overview: 'システム全体で使用するロールの定義と管理を行います。',
    features: [
      {
        title: 'ロール定義',
        description: 'ISSUER_ROLE、BURNER_ROLE、PAUSER_ROLE、FREEZER_ROLE、ALLOWLIST_ROLE等の標準ロールを定義。',
      },
      {
        title: 'ロール階層',
        description: '各ロールには管理者ロールが設定され、階層的な権限管理を実現。',
      },
      {
        title: 'Bank固有ロール',
        description: 'Bank単位のロール（BANK_ISSUER_ROLE等）も定義。グローバルロールとBank固有ロールを使い分けます。',
      },
    ],
  },
  'StablecoinAdmin': {
    overview: '管理者向けの設定・操作機能を集約します。',
    features: [
      {
        title: '初期化',
        description: 'コントラクトの初期設定（名前、シンボル、初期管理者等）を行うinitialize関数を提供。',
      },
      {
        title: 'ロール管理',
        description: 'grantRole、revokeRoleによるロールの付与・剥奪。マルチシグ承認が必要な場合もあります。',
      },
      {
        title: '設定変更',
        description: 'システムパラメータの変更機能。変更には適切な権限が必要です。',
      },
    ],
  },
  'BankScopedRoles': {
    overview: 'Bank単位でのロール管理を実現します。',
    features: [
      {
        title: 'Bank固有ロール',
        description: '各BankにISSUER、BURNER、PAUSER、ALLOWLIST等のロールを個別に割り当て。',
      },
      {
        title: 'ロール提案・承認',
        description: 'Bankロールの変更は提案→承認のフローで実行。複数の承認者による確認を必要とします。',
      },
    ],
  },
  'MultiAdminAccessControl': {
    overview: '複数管理者による承認が必要なアクセス制御を実装します。',
    features: [
      {
        title: '複数管理者',
        description: '単一のDEFAULT_ADMIN_ROLEではなく、複数のアドレスが管理者として登録可能。',
      },
      {
        title: '承認フロー',
        description: '重要な操作には複数の管理者からの承認が必要。単独での操作を防止します。',
      },
    ],
  },
  'DualKeyMultiSig': {
    overview: 'プライマリキーとセカンダリキーの2段階承認を実装します。',
    features: [
      {
        title: 'デュアルキー構造',
        description: '各操作主体（Developer、TrustBank等）にプライマリキーとセカンダリキーを設定。',
      },
      {
        title: 'キーローテーション',
        description: 'キーの更新を安全に行うローテーション機能。提案→承認→実行のフローで実施。',
      },
      {
        title: '提案管理',
        description: 'キーローテーション提案の作成、承認、実行、キャンセルを管理。',
      },
    ],
  },
  'MultiSigWallet': {
    overview: '汎用的なマルチシグネチャウォレット機能を提供します。',
    features: [
      {
        title: 'トランザクション提案',
        description: '任意のトランザクションを提案として登録。複数署名者の承認を待ちます。',
      },
      {
        title: '署名者管理',
        description: '署名者の追加・削除、必要承認数の変更が可能。',
      },
      {
        title: 'トランザクション実行',
        description: '必要な承認数に達したトランザクションを実行。',
      },
    ],
  },
  'AccessControlMultiSig': {
    overview: 'ロールベースアクセス制御にマルチシグを統合します。',
    features: [
      {
        title: 'ロール変更のマルチシグ化',
        description: 'grantRole、revokeRoleの操作に複数の承認を必要とします。',
      },
      {
        title: '提案フロー',
        description: 'ロール変更は提案として登録され、必要な承認を得てから実行されます。',
      },
    ],
  },
  'RoleMultiSigManager': {
    overview: 'ロール変更の提案・承認フローを管理します。',
    features: [
      {
        title: 'ロール変更提案',
        description: 'ロールの付与・剥奪を提案として作成。提案には有効期限があります。',
      },
      {
        title: '承認管理',
        description: '複数の承認者からの承認を収集。必要承認数に達すると実行可能になります。',
      },
      {
        title: '提案のキャンセル',
        description: '不要になった提案をキャンセル可能。有効期限切れの提案も自動的に無効化。',
      },
    ],
  },
  'ERC20SoladyUpgradeable': {
    overview: 'Soladyライブラリを使用した効率的なERC20実装です。',
    features: [
      {
        title: 'ガス効率',
        description: 'Soladyの最適化されたERC20実装を採用。標準的な実装より少ないガスで動作します。',
      },
      {
        title: 'アップグレード対応',
        description: 'Initializableパターンを使用し、プロキシ経由でのアップグレードに対応。',
      },
    ],
  },
  'Dictionary': {
    overview: 'キーバリュー形式のオンチェーンデータストアです。',
    features: [
      {
        title: 'データ保存',
        description: 'bytes32キーに対して任意のbytesデータを保存可能。',
      },
      {
        title: 'アクセス制御',
        description: 'データの書き込みには適切な権限が必要。読み取りは誰でも可能。',
      },
    ],
  },
};

/**
 * Swagger JSONファイルを読み込む
 */
function loadSpec(contractName) {
  const jsonPath = path.join(CONFIG.specsDir, contractName, `${contractName}.swagger.json`);
  if (!fs.existsSync(jsonPath)) {
    console.warn(`  ⚠️ Spec not found: ${jsonPath}`);
    return null;
  }

  const content = fs.readFileSync(jsonPath, 'utf-8');
  return JSON.parse(content);
}

/**
 * パスからタグごとの操作を抽出
 */
function extractOperationsByTag(spec) {
  const operations = {
    '読み取り関数': [],
    '書き込み関数': [],
    '定数': [],
    '変数': [],
    'Mapping': [],
    'イベント': [],
    'エラー': [],
    '構造体': [],
    'Modifier': [],
  };

  if (!spec.paths) return operations;

  for (const [pathName, pathItem] of Object.entries(spec.paths)) {
    for (const [method, operation] of Object.entries(pathItem)) {
      if (method === 'parameters') continue;

      const tags = operation.tags || [];
      const tag = tags[0] || '読み取り関数';

      if (operations[tag]) {
        operations[tag].push({
          path: pathName,
          method,
          ...operation,
        });
      }
    }
  }

  return operations;
}

/**
 * パラメータの型をフォーマット
 */
function formatParamType(schema) {
  if (!schema) return 'any';

  if (schema.type === 'array') {
    const itemType = schema.items?.type || 'any';
    return `${itemType}[]`;
  }

  return schema.type || 'any';
}

/**
 * 関数テーブルを生成
 */
function generateFunctionTable(operations, category) {
  if (operations.length === 0) return '';

  let md = `### ${category}\n\n`;
  md += `| 関数名 | 説明 |\n`;
  md += `|--------|------|\n`;

  for (const op of operations) {
    const name = op.path.replace('/', '').split('_')[0];
    const desc = (op.description || '').split('\n')[0].substring(0, 80);
    md += `| [\`${name}\`](#${name.toLowerCase()}) | ${desc} |\n`;
  }

  md += '\n';
  return md;
}

/**
 * 関数詳細セクションを生成
 */
function generateFunctionDetails(operations, category) {
  if (operations.length === 0) return '';

  let md = `## ${category}\n\n`;

  for (const op of operations) {
    const name = op.path.replace('/', '').split('_')[0];
    md += `### ${name}\n\n`;

    if (op.description) {
      md += `${op.description}\n\n`;
    }

    // パラメータ
    if (op.parameters && op.parameters.length > 0) {
      md += `**パラメータ:**\n\n`;
      md += `| 名前 | 型 | 必須 | 説明 |\n`;
      md += `|------|-----|------|------|\n`;

      for (const param of op.parameters) {
        const type = formatParamType(param.schema);
        const required = param.required ? '✓' : '-';
        const desc = param.description || '-';
        md += `| \`${param.name}\` | \`${type}\` | ${required} | ${desc} |\n`;
      }
      md += '\n';
    }

    // 戻り値 (Swagger 2.0形式: response.schema)
    const response200 = op.responses?.['200'];
    if (response200) {
      // Swagger 2.0: schema is directly under response, not under content/application/json
      const schema = response200.schema;
      if (schema?.properties) {
        md += `**戻り値:**\n\n`;
        md += `| 名前 | 型 | 説明 |\n`;
        md += `|------|-----|------|\n`;

        for (const [propName, propSchema] of Object.entries(schema.properties)) {
          const type = formatParamType(propSchema);
          const desc = propSchema.description || '-';
          md += `| \`${propName}\` | \`${type}\` | ${desc} |\n`;
        }
        md += '\n';
      }
    }

    // 使用例（書き込み関数のみ）
    if (category === '書き込み関数') {
      md += `**使用例:**\n\n`;
      md += `\`\`\`solidity\n`;

      const params = op.parameters?.map(p => p.name).join(', ') || '';
      md += `contract.${name}(${params});\n`;
      md += `\`\`\`\n\n`;
    }

    md += `---\n\n`;
  }

  return md;
}

/**
 * イベントセクションを生成
 */
function generateEventsSection(operations) {
  if (operations.length === 0) return '';

  let md = `## イベント\n\n`;

  for (const op of operations) {
    const name = op.path.replace('/', '');
    md += `### ${name}\n\n`;

    if (op.description) {
      md += `${op.description}\n\n`;
    }

    // パラメータ
    if (op.parameters && op.parameters.length > 0) {
      md += `**パラメータ:**\n\n`;
      md += `| 名前 | 型 | indexed | 説明 |\n`;
      md += `|------|-----|---------|------|\n`;

      for (const param of op.parameters) {
        const type = formatParamType(param.schema);
        const indexed = param.name?.includes('indexed') ? '✓' : '-';
        const desc = param.description || '-';
        md += `| \`${param.name}\` | \`${type}\` | ${indexed} | ${desc} |\n`;
      }
      md += '\n';
    }

    md += `---\n\n`;
  }

  return md;
}

/**
 * エラーセクションを生成
 */
function generateErrorsSection(operations) {
  if (operations.length === 0) return '';

  let md = `## エラー\n\n`;
  md += `| エラー名 | 説明 |\n`;
  md += `|----------|------|\n`;

  for (const op of operations) {
    const name = op.path.replace('/', '');
    const desc = (op.description || '').split('\n')[0];
    md += `| \`${name}\` | ${desc} |\n`;
  }

  md += '\n';
  return md;
}

/**
 * コントラクトのMarkdownドキュメントを生成
 */
function generateContractDoc(contractName, spec) {
  const descInfo = CONTRACT_DESCRIPTIONS[contractName] || {
    overview: `${contractName}コントラクトの仕様書です。`,
    features: [],
  };

  // 継承情報を抽出
  const infoDesc = spec.info?.description || '';
  const inheritanceMatch = infoDesc.match(/このコントラクトは以下のコントラクトを継承しています。\n\n([\s\S]*?)(?:\n\n|$)/);
  const inheritance = inheritanceMatch ? inheritanceMatch[1].split('。\n\n').filter(Boolean) : [];

  const operations = extractOperationsByTag(spec);

  let md = `---
sidebar_position: ${getContractPosition(contractName)}
---

# ${contractName}

> **[📋 API仕様書を見る](/api/${contractName})**

## 概要

${descInfo.overview}

`;

  // 継承関係
  if (inheritance.length > 0) {
    md += `### 継承関係\n\n`;
    md += `このコントラクトは以下のコントラクトを継承しています：\n\n`;
    for (const parent of inheritance) {
      const parentName = parent.replace('。', '');
      md += `- \`${parentName}\`\n`;
    }
    md += '\n';
  }

  // 主要機能
  if (descInfo.features && descInfo.features.length > 0) {
    md += `## 主要機能\n\n`;
    for (const feature of descInfo.features) {
      md += `### ${feature.title}\n\n`;
      md += `${feature.description}\n\n`;
    }
  }

  // 関数一覧（折りたたみセクション）
  md += `## 関数一覧\n\n`;

  // 定数
  if (operations['定数'].length > 0) {
    md += `<details>\n<summary><strong>定数 (${operations['定数'].length})</strong></summary>\n\n`;
    md += generateFunctionTable(operations['定数'], '定数').replace('### 定数\n\n', '');
    md += generateFunctionDetails(operations['定数'], '定数').replace('## 定数\n\n', '');
    md += `</details>\n\n`;
  }

  // 変数
  if (operations['変数'].length > 0) {
    md += `<details>\n<summary><strong>変数 (${operations['変数'].length})</strong></summary>\n\n`;
    md += generateFunctionTable(operations['変数'], '変数').replace('### 変数\n\n', '');
    md += generateFunctionDetails(operations['変数'], '変数').replace('## 変数\n\n', '');
    md += `</details>\n\n`;
  }

  // Mapping
  if (operations['Mapping'].length > 0) {
    md += `<details>\n<summary><strong>Mapping (${operations['Mapping'].length})</strong></summary>\n\n`;
    md += generateFunctionTable(operations['Mapping'], 'Mapping').replace('### Mapping\n\n', '');
    md += generateFunctionDetails(operations['Mapping'], 'Mapping').replace('## Mapping\n\n', '');
    md += `</details>\n\n`;
  }

  // 読み取り関数
  if (operations['読み取り関数'].length > 0) {
    md += `<details>\n<summary><strong>読み取り関数 (${operations['読み取り関数'].length})</strong></summary>\n\n`;
    md += generateFunctionTable(operations['読み取り関数'], '読み取り関数').replace('### 読み取り関数\n\n', '');
    md += generateFunctionDetails(operations['読み取り関数'], '読み取り関数').replace('## 読み取り関数\n\n', '');
    md += `</details>\n\n`;
  }

  // 書き込み関数
  if (operations['書き込み関数'].length > 0) {
    md += `<details>\n<summary><strong>書き込み関数 (${operations['書き込み関数'].length})</strong></summary>\n\n`;
    md += generateFunctionTable(operations['書き込み関数'], '書き込み関数').replace('### 書き込み関数\n\n', '');
    md += generateFunctionDetails(operations['書き込み関数'], '書き込み関数').replace('## 書き込み関数\n\n', '');
    md += `</details>\n\n`;
  }

  // イベント
  if (operations['イベント'].length > 0) {
    md += `<details>\n<summary><strong>イベント (${operations['イベント'].length})</strong></summary>\n\n`;
    md += generateEventsSection(operations['イベント']).replace('## イベント\n\n', '');
    md += `</details>\n\n`;
  }

  // エラー
  if (operations['エラー'].length > 0) {
    md += `<details>\n<summary><strong>エラー (${operations['エラー'].length})</strong></summary>\n\n`;
    md += generateErrorsSection(operations['エラー']).replace('## エラー\n\n', '');
    md += `</details>\n\n`;
  }

  return md;
}

/**
 * コントラクトの表示順序を取得
 */
function getContractPosition(contractName) {
  let position = 1;
  for (const [category, contracts] of Object.entries(CONTRACT_CATEGORIES)) {
    const index = contracts.indexOf(contractName);
    if (index !== -1) {
      return position + index;
    }
    position += contracts.length;
  }
  return 99;
}

/**
 * カテゴリインデックスページを生成
 */
function generateCategoryIndex() {
  let md = `---
sidebar_position: 0
---

# コントラクト仕様

Avalanche Stablecoinプロジェクトのスマートコントラクト仕様書です。

## コントラクト一覧

`;

  for (const [category, contracts] of Object.entries(CONTRACT_CATEGORIES)) {
    md += `### ${category}\n\n`;

    for (const contractName of contracts) {
      const desc = CONTRACT_DESCRIPTIONS[contractName];
      if (desc) {
        md += `- **[${contractName}](./${contractName})** - ${desc.overview.split('。')[0]}\n`;
      } else {
        md += `- **[${contractName}](./${contractName})**\n`;
      }
    }
    md += '\n';
  }

  return md;
}

/**
 * sidebars.jsを生成
 */
function generateSidebars() {
  const items = [];

  for (const [category, contracts] of Object.entries(CONTRACT_CATEGORIES)) {
    const categoryItems = contracts.map(c => `contracts/${c}`);
    items.push({
      type: 'category',
      label: category,
      items: categoryItems,
    });
  }

  return `/**
 * Sidebars configuration
 *
 * 自動生成されたサイドバー設定です。
 * generate-contract-docs.js によって生成されました。
 */

module.exports = {
  contractsSidebar: [
    {
      type: 'doc',
      id: 'contracts/index',
      label: 'コントラクト仕様',
    },
    ${JSON.stringify(items, null, 4).slice(1, -1)}
  ],
};
`;
}

/**
 * メイン処理
 */
function main() {
  console.log('📄 Contract Documentation Generator');
  console.log('====================================');
  console.log(`Output: ${CONFIG.outputDir}\n`);

  // 出力ディレクトリを作成
  if (!fs.existsSync(CONFIG.outputDir)) {
    fs.mkdirSync(CONFIG.outputDir, { recursive: true });
  }

  let generatedCount = 0;

  // 各コントラクトのドキュメントを生成
  for (const [category, contracts] of Object.entries(CONTRACT_CATEGORIES)) {
    console.log(`\n📁 ${category}`);

    for (const contractName of contracts) {
      const spec = loadSpec(contractName);
      if (!spec) {
        console.log(`  ⏭️ ${contractName} (skipped - no spec)`);
        continue;
      }

      const markdown = generateContractDoc(contractName, spec);
      const outputPath = path.join(CONFIG.outputDir, `${contractName}.md`);
      fs.writeFileSync(outputPath, markdown);
      console.log(`  ✅ ${contractName}.md`);
      generatedCount++;
    }
  }

  // インデックスページを生成
  const indexMarkdown = generateCategoryIndex();
  const indexPath = path.join(CONFIG.outputDir, 'index.md');
  fs.writeFileSync(indexPath, indexMarkdown);
  console.log(`\n✅ index.md`);

  // sidebars.jsを生成
  const sidebarsContent = generateSidebars();
  fs.writeFileSync(CONFIG.sidebarPath, sidebarsContent);
  console.log(`✅ sidebars.js`);

  console.log('\n====================================');
  console.log(`✅ Generated: ${generatedCount} contract docs`);
  console.log(`📍 Output directory: ${CONFIG.outputDir}`);
}

main();
