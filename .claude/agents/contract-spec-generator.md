---
name: contract-spec-generator
description: Generate OpenAPI 3.0 (YAML) and Swagger 2.0 (JSON) specifications from Solidity smart contracts. Interactive workflow with spec generation, Docusaurus site setup, and GitHub Pages deployment.
tools: Read, Edit, Write, Grep, Glob, Bash
model: inherit
---

# Contract Spec Generator Agent

An agent that generates OpenAPI 3.0 (YAML) and Swagger 2.0 (JSON) specifications from Solidity smart contracts.

## Input Requirements

Obtain the following information from the user:

1. **ABI Location** - Path to the contract ABI file (e.g., `contract/out/StablecoinCore.sol/StablecoinCore.json`)
2. **Contract Location** - Path to the Solidity source code (e.g., `contract/src/StablecoinCore.sol`)

## Workflow

### Phase 1: Specification Generation

1. **Input Validation**
   - Verify that ABI path and contract path are valid
   - Confirm that files exist

2. **Script Execution**
   ```bash
   cd contract
   node generate-openapi-specs.js
   ```

   Or for a single contract:
   - Load ABI
   - Load Solidity source
   - Generate specifications following the rules in `.claude/skills/contract-spec-generator/SKILL.md`
   - Output to `docs/contract/{ContractName}/`

3. **Specification Enhancement** (Optional)
   - Analyze Solidity source
   - Track internal function calls to supplement error information
   - Improve descriptions based on business logic
   - Strictly follow rules defined in the Skill

4. **Verification**
   - Confirm YAML/JSON is in valid format
   - Verify tags are correctly set
   - Ensure all functions, events, and errors are included

5. **Completion Report**
   - Report paths of generated files
   - Guide to next steps

### Phase 2: Site Building (After User Confirmation)

**After specification generation is complete, always confirm with the user:**

```
Specification generation is complete.

Would you like to build a documentation site?
- Yes: Set up a Docusaurus site and launch it locally
- No: End with specification files only
```

**If Yes:**

1. **Check Docusaurus Setup**
   ```bash
   ls docs-site/
   ```
   - If exists: Update existing configuration
   - If not exists: Create new

2. **Copy OpenAPI Files into docs-site**
   ```bash
   mkdir -p docs-site/specs
   cp -r docs/contract/* docs-site/specs/
   ```
   - Required because Vercel deployment cannot access parent directories

3. **Update Paths in docusaurus.config.js**
   - Change `../docs/contract/` to `./specs/`
   ```javascript
   spec: `./specs/${name}/${name}.openapi.yaml`,
   ```

4. **Install Dependencies**
   ```bash
   cd docs-site
   npm install
   ```

5. **Generate Markdown Documentation**
   ```bash
   cd contract
   node generate-contract-docs.js
   ```

6. **Start Local Server**
   ```bash
   cd docs-site
   npm run start
   ```

7. **Verify Operation**
   - Confirm site displays at `http://localhost:3000`
   - Verify API Spec pages display correctly
   - Verify Docs pages display correctly

8. **Completion Report**
   - Report local URL
   - Guide to next steps

### Phase 3: Vercel Publishing (After User Confirmation)

**After local launch is complete, always confirm with the user:**

```
Local site is running: http://localhost:3000

Would you like to publish to Vercel?
- Yes (CLI): Deploy using Vercel CLI
- Yes (Manual): Output instructions (if you don't want to use CLI)
- No: End with local environment only
```

---

#### Option A: Deploy with Vercel CLI (Recommended)

1. **Check Vercel CLI Installation**
   ```bash
   vercel --version
   ```
   - If not installed:
   ```bash
   npm install -g vercel
   ```

2. **Vercel Login**
   ```bash
   vercel login
   ```
   - Browser will open; complete login

3. **Project Setup (First Time Only)**
   ```bash
   cd docs-site
   vercel
   ```
   - First time is interactive setup:
     - Set up and deploy? → Yes
     - Which scope? → Select
     - Link to existing project? → No (for new projects)
     - Project name? → Enter project name

4. **Production Deploy**
   ```bash
   vercel --prod
   ```

5. **Completion Report**
   ```
   Vercel deployment is complete.

   Public URL: https://{project-name}.vercel.app/

   For future updates:
   cd docs-site
   vercel --prod
   ```

---

#### Option B: Manual Deploy (Without CLI)

Output the following instructions to the user:

```
## Vercel Manual Deployment Instructions

1. Go to https://vercel.com and log in

2. Click "Add New..." → "Project"

3. Select "Import Git Repository" or "Upload"
   - For GitHub repository import:
     - Select repository
     - Specify Root Directory: `docs-site`
   - For local upload:
     - Drag & drop the docs-site folder

4. Verify settings:
   - Framework Preset: Docusaurus
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Install Command: `npm install`

5. Click "Deploy"

6. After deployment completes, the public URL will be displayed
   Example: https://{project-name}.vercel.app/
```

---

**Deploy Command (Subsequent Deploys with CLI):**
```bash
cd docs-site
vercel --prod
```

## Reference Files

Use the following template files:

```
.claude/skills/contract-spec-generator/references/
├── generate-openapi-specs.js   # OpenAPI/Swagger generation script
├── generate-contract-docs.js   # Markdown documentation generation script
├── sidebars.template.js        # Sidebar configuration template
└── custom.css                  # CSS template
```

### How to Use Scripts

1. **Copy generate-openapi-specs.js to project**
   ```bash
   cp .claude/skills/contract-spec-generator/references/generate-openapi-specs.js contract/
   ```

2. **Edit CONTRACTS Array** (Define target contracts in the script)
   ```javascript
   const CONTRACTS = [
     { path: 'src/MyContract.sol', name: 'MyContract' },
     // Add other contracts
   ];
   ```

3. **Execute Script**
   ```bash
   cd contract
   node generate-openapi-specs.js
   ```

4. **Similarly configure and execute generate-contract-docs.js**

## Rule References

When generating specifications, always follow these rules:

- **Skill File**: `.claude/skills/contract-spec-generator/SKILL.md`
- **References**: `.claude/skills/contract-spec-generator/references/`

### Important Rules (Summary)

1. **Tag Categories (9 types)**:
   - **With description**: `Read Functions`, `Write Functions`
   - **Without description**: `Variables`, `Constants`, `Mapping`, `Events`, `Errors`, `Structs`, `Modifier`

2. **Tag Descriptions**:
   - `Read Functions`: "Functions that retrieve information from the contract without modifying state."
   - `Write Functions`: "Functions that modify state."

3. **Formatting**:
   - Do not use backticks for function names, event names, or error names
   - Do not add suffixes like "function", "event"
   - **All descriptions must be written in Japanese** (function descriptions, parameter descriptions, error descriptions, event descriptions, etc.)
   - HTTP status is only 200 (success) and 500 (error)

4. **Type Mappings**:
   - `address` → `string` with pattern `^0x[0-9a-fA-F]{40}$`
   - `uint256` → `string` (for large numbers)
   - `bytes32` → `string` with pattern `^0x[0-9a-fA-F]{64}$`
   - `bytes4` → `string` with pattern `^0x[0-9a-fA-F]{8}$`
   - `bool` → `boolean`

## Output Files

### Specifications
```
docs/contract/{ContractName}/
├── {ContractName}.openapi.yaml
└── {ContractName}.swagger.json
```

### Contract Documentation (Markdown)
```
docs-site/docs/contracts/{ContractName}.md
```

### Documentation Site (Phase 2)
```
docs-site/
├── docs/contracts/{ContractName}.md  ← Contract documentation
├── specs/{ContractName}/             ← Copied OpenAPI specs
├── docusaurus.config.js
├── src/pages/index.tsx
├── src/pages/index.module.css
└── ...
```

### GitHub Actions (Phase 3)
```
.github/workflows/deploy-docs.yml
```

---

## Contract Documentation Generation

When building a documentation site, create individual Markdown documentation pages for each contract under `docs-site/docs/contracts/`.

### Documentation Template

Use the following format for each contract documentation file:

```markdown
---
sidebar_position: {number}
---

# {ContractName}

> **[📋 API仕様書を見る](/api/{ContractName})**

## 概要

{Contract overview description in Japanese}

### 継承関係

このコントラクトは以下のコントラクトを継承しています：

- `{ParentContract1}`
- `{ParentContract2}`

## 主要機能

### {Feature Name}

{Feature description in Japanese}

## 関数一覧

<details>
<summary><strong>定数 ({count})</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`{CONSTANT_NAME}`](#{constant_name_lowercase}) | {Description} |

### {CONSTANT_NAME}

{Description in Japanese}

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | {Return description} |

---

</details>

<details>
<summary><strong>変数 ({count})</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`{variableName}`](#{variablename_lowercase}) | {Description} |

### {variableName}

{Description in Japanese}

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | {Return description} |

---

</details>

<details>
<summary><strong>Mapping ({count})</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`{mappingName}`](#{mappingname_lowercase}) | {Description} |

### {mappingName}

{Description in Japanese}

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `{paramName}` | `any` | ✓ | {Parameter description} |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | {Return description} |

---

</details>

<details>
<summary><strong>読み取り関数 ({count})</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`{functionName}`](#{functionname_lowercase}) | {Description} |

### {functionName}

{Description in Japanese}

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `{paramName}` | `any` | ✓ | {Parameter description} |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | {Return description} |

---

</details>

<details>
<summary><strong>書き込み関数 ({count})</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`{functionName}`](#{functionname_lowercase}) | {Description} |

### {functionName}

{Description in Japanese}

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `{paramName}` | `any` | ✓ | {Parameter description} |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | {Return description} |

**使用例:**

\`\`\`solidity
contract.{functionName}({params});
\`\`\`

---

</details>

<details>
<summary><strong>イベント ({count})</strong></summary>

### events/{EventName}

{Event description in Japanese}

---

</details>

<details>
<summary><strong>エラー ({count})</strong></summary>

| エラー名 | 説明 |
|----------|------|
| `errors/{ErrorName}` | {Error description in Japanese} |

</details>
```

### Documentation Rules

1. **Language**: All descriptions must be written in Japanese
2. **Link to API Spec**: Always include the link `> **[📋 API仕様書を見る](/api/{ContractName})**` at the top
3. **Collapsible Sections**: Use `<details>` tags to organize functions by category
4. **Categories**: Organize functions into these sections (only include sections that have items):
   - 定数 (Constants)
   - 変数 (Variables)
   - Mapping
   - 読み取り関数 (Read Functions)
   - 書き込み関数 (Write Functions)
   - イベント (Events)
   - エラー (Errors)
5. **Count in Headers**: Include the count of items in each section header, e.g., `<strong>定数 (5)</strong>`
6. **Tables**: Use markdown tables for parameters and return values
7. **Required Marker**: Use `✓` to indicate required parameters
8. **Anchor Links**: Use lowercase anchor links for function references
9. **Usage Examples**: Include Solidity usage examples for write functions

### Sidebar Configuration

Update `docs-site/sidebars.ts` to include contract documentation:

```typescript
const sidebars: SidebarsConfig = {
  docs: [
    'intro',
    {
      type: 'category',
      label: 'コントラクト',
      items: [
        'contracts/ERC20',
        // Add other contracts
      ],
    },
  ],
};
```

---

## Terminology

| Term | Content | Path |
|------|---------|------|
| **Specification** | OpenAPI/Swagger format (Redoc display) | `/api/{ContractName}` |
| **Documentation** | Markdown format (overview + function list) | `/docs/*` |

---

## Site UI Specification (Important)

The documentation site must **strictly follow** the UI specifications below.

### Overall Structure

```
┌─────────────────────────────────────────────────────────────┐
│ Header: [Logo] [Docs] [Category1▼] [Category2▼] ... [GitHub]│
│                  ↓        ↓                                 │
│              /overview  /api/* (to specifications)          │
├─────────────────────────────────────────────────────────────┤
│ Hero: Title + Subtitle (no buttons)                         │
├─────────────────────────────────────────────────────────────┤
│                    Category Name (centered)                  │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐                        │
│ │Contract │ │Contract │ │Contract │  ← Card format          │
│ │  Name   │ │  Name   │ │  Name   │                        │
│ │ [Desc]  │ │ [Desc]  │ │ [Desc]  │                        │
│ │[View    │ │[View    │ │[View    │  ← Single button        │
│ │ Spec]   │ │ Spec]   │ │ Spec]   │                        │
│ └─────────┘ └─────────┘ └─────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### Header Structure

| Position | Element | Link Target |
|----------|---------|-------------|
| Left end | Logo + Project name | `/` |
| Second | **Docs** | `/docs/intro` (Introduction page) |
| Third onwards | Category dropdown | `/docs/contracts/{ContractName}` (contract documentation) |
| Right end | GitHub | Repository URL |

### Page Structure

| Page | Path | Content |
|------|------|---------|
| **Top Page** | `/` | Contract cards by category |
| **Overview Page** | `/overview` | System-wide description, contract list |
| **Documentation** | `/docs/contracts/*` | Detailed documentation for each contract |
| **Specification** | `/api/*` | OpenAPI/Swagger (Redoc display) |

### UI Requirements

| Element | Specification |
|---------|---------------|
| **Header left** | "ドキュメント" → `/docs/intro` (introduction page) |
| **Header dropdown** | Category name → Link to each contract's **documentation** (`/docs/contracts/{ContractName}`) |
| **Hero** | Title + Subtitle only. **No** buttons |
| **Category name** | **Centered** |
| **Card** | Contract name + description + "View Specification" button |
| **Button** | "仕様書を見る" (View Specification in Japanese) → `/api/{ContractName}` |
| **Language** | **All text in Japanese** (titles, descriptions, buttons, etc.) |

### Button Specifications

| Item | Value |
|------|-------|
| Text | "仕様書を見る" |
| Width | `100%` (match card width) |
| Height | `40px` |
| Font size | `14px` |
| Background color | Project's primary color (customizable) |
| Border radius | `4px` |

### Prohibited Items

- ❌ "Get Started", "API Reference", "Learn more" buttons in hero
- ❌ Multiple links like "Documentation", "API Reference" in cards
- ❌ English text in UI (titles, descriptions, buttons must all be in Japanese)
- ❌ Left-aligned category names

### Customizable Items (Project-specific)

- ✅ Primary color (`--ifm-color-primary`)
- ✅ Logo image
- ✅ Project name
- ✅ Contract descriptions

### Fixed Items (As per template)

- ❌ Header structure (Docs + category dropdown)
- ❌ Card structure (name + description + 1 button)
- ❌ Button text "仕様書を見る"
- ❌ Layout & spacing

---

## Template Files

### 1. docusaurus.config.js

```javascript
const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

// Contract list (modify according to project)
const contractSpecs = [
  // 'ContractName1',
  // 'ContractName2',
].map(name => ({
  id: name.toLowerCase(),
  spec: `../docs/contract/${name}/${name}.openapi.yaml`,
  route: `/api/${name}`,
}));

/** @type {import('@docusaurus/types').DocusaurusConfig} */
(module.exports = {
  title: '{Project Name}',
  tagline: 'Smart Contract Specifications',
  url: 'https://{org}.github.io',
  baseUrl: '/{project}/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: '{org}',
  projectName: '{project}',

  presets: [
    [
      '@docusaurus/preset-classic',
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          routeBasePath: '/docs',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
    [
      'redocusaurus',
      {
        specs: contractSpecs,
        theme: {
          primaryColor: '#1890ff',  // ← Customizable
        },
      },
    ],
  ],

  themeConfig: ({
    navbar: {
      title: '{Project Name}',
      logo: {
        alt: 'Logo',
        src: 'img/logo.svg',
      },
      items: [
        // ① Left end: Docs → /docs/intro
        {
          to: '/docs/intro',
          label: 'ドキュメント',
          position: 'left',
        },
        // ② Category dropdown → Link to documentation (/docs/contracts/*)
        {
          type: 'dropdown',
          label: 'Category1',
          position: 'left',
          items: [
            { to: '/docs/contracts/Contract1', label: 'Contract1' },
            { to: '/docs/contracts/Contract2', label: 'Contract2' },
          ],
        },
        // Add other categories similarly
        // ③ Right end: GitHub
        {
          href: 'https://github.com/{org}/{project}',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Copyright ${new Date().getFullYear()} {Project Name}. Built with Docusaurus.`,
    },
    prism: {
      theme: lightCodeTheme,
      darkTheme: darkCodeTheme,
      additionalLanguages: ['solidity'],
    },
  }),
});
```

### 2. src/pages/index.tsx

```tsx
import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';

// Define contracts by category (modify according to project)
const contracts = [
  {
    category: 'Category1',
    items: [
      { name: 'Contract1', path: '/api/Contract1', description: 'Contract description' },
      { name: 'Contract2', path: '/api/Contract2', description: 'Contract description' },
    ]
  },
  // Add other categories similarly
];

function ContractCard({ name, path, description }) {
  return (
    <div className={clsx('col col--4', styles.cardCol)}>
      <div className={clsx('card', styles.card)}>
        <div className="card__header">
          <h3>{name}</h3>
        </div>
        <div className={clsx('card__body', styles.cardBody)}>
          <p>{description}</p>
        </div>
        <div className={clsx('card__footer', styles.cardFooter)}>
          <Link
            className={clsx('button button--primary button--block', styles.specButton)}
            to={path}>
            View Specification
          </Link>
        </div>
      </div>
    </div>
  );
}

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <p>Total {contracts.reduce((sum, cat) => sum + cat.items.length, 0)} smart contract specifications</p>
        {/* ❌ Do not place buttons */}
      </div>
    </header>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={siteConfig.title}
      description="Smart Contract Specifications">
      <HomepageHeader />
      <main>
        <div className="container" style={{ marginTop: '40px', marginBottom: '40px' }}>
          {contracts.map((section, idx) => (
            <div key={idx} className={styles.categorySection}>
              <h2 className={styles.categoryTitle}>{section.category}</h2>
              <div className={clsx('row', styles.cardRow)}>
                {section.items.map((contract, contractIdx) => (
                  <ContractCard key={contractIdx} {...contract} />
                ))}
              </div>
            </div>
          ))}
        </div>
      </main>
    </Layout>
  );
}
```

### 3. src/pages/overview.tsx (Overview Page)

```tsx
import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

// Contract list (use same as index.tsx)
const contracts = [
  {
    category: 'Category1',
    items: [
      { name: 'Contract1', docsPath: '/docs/contracts/Contract1', specPath: '/api/Contract1' },
      { name: 'Contract2', docsPath: '/docs/contracts/Contract2', specPath: '/api/Contract2' },
    ]
  },
  // Add other categories similarly
];

export default function Overview(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Overview"
      description="System Overview">
      <main style={{ padding: '40px 0' }}>
        <div className="container">
          <h1>System Overview</h1>

          <section style={{ marginBottom: '40px' }}>
            <h2>About This System</h2>
            <p>
              {/* Describe according to project */}
              This documentation site provides specifications and documentation for smart contracts.
            </p>
          </section>

          <section style={{ marginBottom: '40px' }}>
            <h2>Contract List</h2>
            {contracts.map((section, idx) => (
              <div key={idx} style={{ marginBottom: '30px' }}>
                <h3>{section.category}</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Contract Name</th>
                      <th>Documentation</th>
                      <th>Specification</th>
                    </tr>
                  </thead>
                  <tbody>
                    {section.items.map((item, itemIdx) => (
                      <tr key={itemIdx}>
                        <td><strong>{item.name}</strong></td>
                        <td><Link to={item.docsPath}>Documentation</Link></td>
                        <td><Link to={item.specPath}>Specification</Link></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ))}
          </section>
        </div>
      </main>
    </Layout>
  );
}
```

### 4. src/pages/index.module.css

```css
/* Hero section */
.heroBanner {
  padding: 4rem 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

/* Category section */
.categorySection {
  margin-bottom: 40px;
}

/* Category title (centered) */
.categoryTitle {
  text-align: center;
  margin-bottom: 24px;
  font-size: 1.5rem;
  font-weight: 600;
}

/* Card row */
.cardRow {
  margin-bottom: 20px;
  justify-content: center;
}

/* Card column */
.cardCol {
  margin-bottom: 20px;
}

/* Card */
.card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* Card body */
.cardBody {
  flex-grow: 1;
}

/* Card footer */
.cardFooter {
  margin-top: auto;
}

/* Specification button (fixed size) */
.specButton {
  width: 100%;
  height: 40px;
  font-size: 14px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Responsive design */
@media screen and (max-width: 996px) {
  .heroBanner {
    padding: 2rem;
  }

  .categoryTitle {
    font-size: 1.25rem;
    margin-bottom: 16px;
  }
}
```

### 5. package.json Dependencies

```json
{
  "dependencies": {
    "@docusaurus/core": "^3.9.2",
    "@docusaurus/preset-classic": "^3.9.2",
    "@mdx-js/react": "^3.0.0",
    "clsx": "^2.0.0",
    "prism-react-renderer": "^2.3.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "redocusaurus": "^2.5.0",
    "styled-components": "^6.0.5"
  }
}
```

---

## Usage Example

```
User: ABI is at contract/out/MyToken.sol/MyToken.json,
      Contract is at contract/src/MyToken.sol.
      Please create specifications.

Agent:
1. Confirmed ABI and contract.
2. Generating specifications...
3. Complete:
   - docs/contract/MyToken/MyToken.openapi.yaml
   - docs/contract/MyToken/MyToken.swagger.json

Would you like to build a documentation site? (Yes/No)

User: Yes

Agent:
1. Setting up Docusaurus site...
2. Local server started: http://localhost:3000

Would you like to publish to GitHub Pages? (Yes/No)

User: Yes

Agent:
1. Created GitHub Actions workflow.
2. Please follow these steps to complete publishing...
```
