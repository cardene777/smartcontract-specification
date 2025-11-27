---
name: contract-spec-generator
description: Generate OpenAPI 3.0 (YAML) and Swagger 2.0 (JSON) specifications from Solidity smart contracts using batch generation mode (skeleton script + AI enhancement) or single contract mode, with optional Docusaurus documentation site creation. This skill should be used when converting Solidity contract ABIs and source code into API documentation format, or when setting up a documentation website for blockchain smart contracts.
---

# Contract Spec Generator

## Overview

This skill provides a two-phase workflow for creating comprehensive smart contract documentation:

**Phase 1: Specification Generation**
- Generate OpenAPI 3.0 (YAML) and Swagger 2.0 (JSON) specifications from Solidity contracts
- Transform contract ABIs and source code into standardized API documentation format
- Include all functions, events, errors, structs, and modifiers with detailed descriptions

**Phase 2: Documentation Site Creation (Optional)**
- Set up a Docusaurus-based documentation website with Redocusaurus plugin
- Automatically register all generated specifications
- Deploy-ready static site with interactive API documentation

The generated specifications include:
- All public/external functions (read and write operations)
- State variables, mappings, and constants with auto-generated getters
- Events and custom errors with detailed examples
- Struct definitions with type mappings
- Modifiers and their effects on functions
- Comprehensive error handling with HTTP 500 responses
- **Tag categorization** for UI grouping (Read Functions, Write Functions, Variables, Constants, Mapping, Events, Errors, Structs, Modifier)

## When to Use This Skill

Use this skill when:
- Generating documentation for Solidity smart contracts
- Converting contract ABIs into OpenAPI/Swagger format
- Creating API-style documentation for blockchain contract interfaces
- Setting up a documentation website to visualize contract specifications
- Working with projects that require standardized contract documentation
- Needing interactive API documentation with tools like Redocusaurus or Swagger UI

## SubAgent Available

For interactive workflows, you can use the **SubAgent**:

```
Task(subagent_type="contract-spec-generator", prompt="ABI is at contract/out/MyToken.sol/MyToken.json, contract is at contract/src/MyToken.sol. Please create specifications.")
```

**SubAgent Flow:**
1. **Specification Generation** → Auto-generate from ABI and contract
2. **Site Building Confirmation** → Yes: Launch Docusaurus locally
3. **Vercel Publishing Confirmation** → Yes: Deploy with Vercel CLI

Details: `.claude/agents/contract-spec-generator.md`

---

## Workflow

### Workflow Modes

This skill supports two workflow modes:

1. **Batch Generation Mode**: Generate specifications for multiple contracts efficiently using a two-stage approach (skeleton script + AI enhancement)
2. **Single Contract Mode**: Generate specifications for one contract at a time manually

**Recommendation**: Use **Batch Generation Mode** when working with multiple contracts for better consistency and efficiency.

---

### Batch Generation Mode (Recommended for Multiple Contracts)

For projects with multiple contracts, use the two-stage batch generation workflow:

**Stage 1: Generate Skeletons** - Run a script to create basic structures for all contracts
**Stage 2: Enhance with AI** - Use this skill to add detailed descriptions and error tracking

#### Prerequisites

- Foundry (forge) installed and configured
- Contract source files in `src/` directory
- ABIs generated via `forge build`

#### Steps

**Step 1: Generate Enhanced Skeleton Specifications**

Run the enhanced skeleton generator script to create high-quality structures for all contracts:

```bash
cd contract
node generate-openapi-specs.js
```

This will generate **enhanced** OpenAPI YAML and Swagger JSON files for all contracts with:
- ✅ **Auto-generated function descriptions** (role constants, ERC20 functions, Pausable, AccessControl, Bank operations, Proposal functions, etc.)
- ✅ **Accurate type mappings** with pattern validation and examples (address → `^0x[0-9a-fA-F]{40}$`, bytes4 → `^0x[0-9a-fA-F]{8}$`, etc.)
- ✅ **Common errors pre-added** to write functions (InvalidAddress, AmountZero, AccessControlUnauthorizedAccount, BankNotFound, etc.)
- ✅ **Meaningful parameter descriptions** based on parameter names (e.g., `owner` → "Specifies the owner's address.", `amount` → "Specifies the token amount (in wei).")
- ✅ **Meaningful return value descriptions** based on function names and output names (e.g., `balanceOf` → "Returns the account balance.", named output `primaryKey` → "Returns the primaryKey.")
- ✅ **Tag categorization** for UI grouping (Read Functions, Write Functions, Variables, Constants, Mapping, Events, Errors, Structs, Modifier)
- ✅ Event, error, struct, and modifier paths with complete information
- ✅ Basic schemas (ErrorResponse, Event schemas, Struct schemas)
- ✅ Common errors pre-populated in 500 responses

Output location: `docs/contract/{ContractName}/{ContractName}.openapi.yaml` and `.swagger.json`

**What Stage 1 Already Provides:**
- Complete function descriptions for standard patterns (ERC20, Pausable, AccessControl, etc.)
- Full parameter type mappings with validation patterns and examples
- **Meaningful parameter descriptions** (e.g., `spender` → "Specifies the address to approve for token spending.")
- **Meaningful return value descriptions** (e.g., `balanceOf` → "Returns the account balance.")
- **Named output support** (when return values have names in ABI, those names are used instead of `result0`)
- **Tag categorization** for all operations (9 categories):
  - **With description:**
    - `Read Functions`: "Functions that retrieve information from the contract without modifying state."
    - `Write Functions`: "Functions that modify state."
  - **Without description (name only):**
    - `Variables`: state variables
    - `Constants`: constant values
    - `Mapping`: mapping definitions
    - `Events`: contract events
    - `Errors`: custom errors
    - `Structs`: struct definitions (if present)
    - `Modifier`: modifier definitions (if present)
- **x-tagGroups** for UI grouping in Redocusaurus/Swagger UI
- 500 error responses with common errors already listed
- Properly formatted YAML/JSON following all specification rules
- **No raw type annotations** (no `(Solidity: xxx)` in descriptions)

**Step 2: Enhance Specifications (Optional)**

Stage 1 generates complete specifications. Use this skill for optional enhancements:
- **Internal function error tracking** (add errors from internal function calls to 500 responses)
- **500 error examples** (add `examples` section with named examples for each error)
- **Contract-specific logic descriptions** (enhance generic descriptions with detailed explanations)
- **Modifier information** (add modifier effects to function descriptions)

**How to use** (when enhancement is needed):

1. Open a generated spec file (e.g., `docs/contract/StablecoinCore/StablecoinCore.openapi.yaml`)
2. Call this skill: "Use contract-spec-generator skill to enhance StablecoinCore specifications"
3. The skill will:
   - Load the contract source code to trace internal function calls
   - Load `references/spec-prompt.md` for formatting rules
   - Track internal function errors (e.g., if `approve()` calls `_spendAllowance()` which can throw `InsufficientAllowance`, add it)
   - Add `examples` section to 500 responses
   - Add modifier information to function descriptions
   - Enhance generic descriptions with contract-specific details

**Step 3: Verify Specifications**

After generation/enhancement, verify:
- [ ] **Tags are assigned** to all operations (Read Functions, Write Functions, Events, Errors, Structs, Modifier)
- [ ] **x-tagGroups** are present for UI grouping
- [ ] **500 responses have `examples` section** (each error should have a named example with `summary` and `value`)
- [ ] Internal function errors are tracked in 500 responses (optional enhancement)
- [ ] Modifier information is added to function descriptions where applicable
- [ ] Formatting rules are followed:
  - No backticks around function/event/error names
  - No suffixes like "function", "event", "error"
  - **No raw type annotations** like "(Solidity: address)" in descriptions
- [ ] All descriptions are in the appropriate language
- [ ] HTTP 200 for success, HTTP 500 for all errors
- [ ] Pattern validation and examples are present for all Solidity types (address, bytes4, etc.)
- [ ] **Named return values** use actual names (not `result0`) when available in ABI

For detailed instructions, see `references/batch-generation-guide.md`.

---

### Single Contract Mode

Generate OpenAPI and Swagger specifications for a single Solidity contract manually. This mode is useful when:
- You only have one contract to document
- You want full control over the generation process
- You're testing or learning how the skill works

#### Input Requirements

To generate specifications, provide the following information:

1. **Contract ABI (JSON)** - The Application Binary Interface of the contract
2. **Contract Source Code (Solidity)** - The complete Solidity source code
3. **Optional metadata** (if available):
   - Network name (e.g., "Polygon PoS")
   - Chain ID (e.g., 137)
   - Contract address (e.g., "0x...")

#### Steps

1. **Load the specification prompt template**

   Read the comprehensive prompt template from `references/spec-prompt.md`. This file contains all the rules and formatting guidelines for generating specifications.

2. **Prepare the input**

   Format the input by replacing the placeholders in the prompt template:
   - `{{ABI_JSON}}` - Insert the contract ABI JSON
   - `{{CONTRACT_SOURCE}}` - Insert the Solidity source code
   - `{{NETWORK_NAME}}`, `{{CHAIN_ID}}`, `{{CONTRACT_ADDRESS}}` - Insert metadata if available

3. **Execute the generation**

   Follow the detailed rules in the prompt template to generate:
   - OpenAPI 3.0 YAML file: `docs/contract/{{CONTRACT_NAME}}/{{CONTRACT_NAME}}.openapi.yaml`
   - Swagger 2.0 JSON file: `docs/contract/{{CONTRACT_NAME}}/{{CONTRACT_NAME}}.swagger.json`

   **Important**: Create the directory structure if it doesn't exist:
   ```
   docs/contract/{{CONTRACT_NAME}}/
   ├── {{CONTRACT_NAME}}.openapi.yaml
   └── {{CONTRACT_NAME}}.swagger.json
   ```

4. **Verify the output**

   Ensure the generated specifications:
   - Are valid YAML/JSON that can be parsed without errors
   - Include all functions, events, errors, and structures
   - Follow the formatting rules (no backticks for function/event/error names, no suffixes like "function", "event", "error")
   - Include error details from both external functions and internal functions they call
   - Use HTTP 200 for success and HTTP 500 for all errors

#### Key Formatting Rules

The `references/spec-prompt.md` file contains comprehensive rules, but key points include:

- **Identifier formatting**: Do not wrap function names, event names, error names, modifier names, or struct names in backticks
- **Name suffixes**: Do not add suffixes like "function", "event", "error"
- **Error tracking**: Include errors from internal functions called by external functions
- **Response codes**: Use only HTTP 200 (success) and HTTP 500 (all errors)
- **Descriptions**: All descriptions should be clear and descriptive
- **No extensions**: Do not use `x-` prefixed extension fields

#### Example Usage

When asked to generate contract specifications:

1. Read the ABI and source code files
2. Load `references/spec-prompt.md` to access the full specification rules
3. Replace placeholders with actual contract data
4. Generate both OpenAPI YAML and Swagger JSON outputs
5. Save the files in `docs/contract/{{CONTRACT_NAME}}/` directory

---

### Phase 2: Create Documentation Site (Optional, User Confirmation Required)

After generating the contract specifications, ask the user if they want to create a documentation website.

**⚠️ Important**: Always ask the user for confirmation before proceeding with Phase 2. Do not automatically create the documentation site without explicit user approval.

#### Confirmation Prompt

After completing Phase 1, present the following options to the user:

```
Contract specifications have been generated successfully.

Would you like to create a Docusaurus documentation site to view these specifications?

Options:
1. Yes - Set up a complete documentation website with Redocusaurus
2. No - Only keep the generated specification files
```

#### Steps (Only if User Confirms)

1. **Load the Docusaurus setup guide**

   Read `references/docusaurus-setup.md` for detailed instructions on setting up the documentation site.

2. **Check if docs-site already exists**

   Check if `docs-site/` directory already exists in the project root:
   - If exists: Update the existing configuration
   - If not exists: Create a new Docusaurus project

3. **Initialize Docusaurus project (if needed)**

   ```bash
   npx create-docusaurus@latest docs-site classic --typescript
   cd docs-site
   ```

4. **Install required dependencies**

   ```bash
   npm install redocusaurus styled-components
   ```

   Or use the package manager detected in the project (npm/yarn/pnpm/bun).

5. **Update package.json**

   Ensure `docs-site/package.json` includes:
   ```json
   {
     "dependencies": {
       "@docusaurus/core": "^3.9.2",
       "@docusaurus/preset-classic": "^3.9.2",
       "@mdx-js/react": "^3.0.0",
       "redocusaurus": "^2.5.0",
       "styled-components": "^6.0.5"
     }
   }
   ```

6. **Configure docusaurus.config.js**

   Create or update `docs-site/docusaurus.config.js` with:
   - Redocusaurus preset configuration
   - Automatic contract specs registration
   - Theme customization

   **Automatic Contract Registration**:

   Add a helper function to automatically detect and register all contracts:

   ```javascript
   const fs = require('fs');
   const path = require('path');

   function getContractSpecs() {
     const contractsDir = path.join(__dirname, '../docs/contract');
     const specs = [];

     if (!fs.existsSync(contractsDir)) {
       return specs;
     }

     const contracts = fs.readdirSync(contractsDir);

     for (const contract of contracts) {
       const yamlPath = path.join(contractsDir, contract, `${contract}.openapi.yaml`);
       if (fs.existsSync(yamlPath)) {
         const id = contract.toLowerCase().replace(/([a-z])([A-Z])/g, '$1-$2').toLowerCase();
         specs.push({
           id: id,
           spec: `../docs/contract/${contract}/${contract}.openapi.yaml`,
           route: `/api/${id}`,
         });
       }
     }

     return specs;
   }
   ```

   Then use this function in the Redocusaurus preset:

   ```javascript
   presets: [
     // ...
     [
       'redocusaurus',
       {
         specs: getContractSpecs(),
         theme: {
           primaryColor: '#1890ff',
           options: {
             hideDownloadButton: false,
             disableSearch: false,
             expandResponses: '200',
             requiredPropsFirst: true,
             sortPropsAlphabetically: true,
           },
         },
       },
     ],
   ],
   ```

7. **Start the development server**

   ```bash
   cd docs-site
   npm run start
   ```

   The site will be available at `http://localhost:3000`.

8. **Verify the site**

   - Open `http://localhost:3000` in a browser
   - Navigate to the API Specs section
   - Verify that all contracts are listed and their specifications are displayed correctly
   - Check that the sidebar shows all functions, events, and errors

#### Site Structure

After setup, the documentation site will have:

```
docs-site/
├── docusaurus.config.js    # Main configuration with Redocusaurus
├── package.json             # Dependencies
├── sidebars.js              # Sidebar configuration
├── src/
│   └── css/
│       └── custom.css       # Custom styles
├── docs/                    # Markdown documentation
├── static/                  # Static assets
└── build/                   # Built static site (after npm run build)
```

The site will automatically:
- Register all contracts found in `../docs/contract/`
- Create navigation links for each contract
- Display interactive API documentation with Redocusaurus
- Support dark/light themes
- Include search functionality

#### Deployment Options

After verifying the site works locally, deploy using Vercel:

**Important**: Before deployment, copy OpenAPI files to docs-site:
```bash
mkdir -p docs-site/specs
cp -r docs/contract/* docs-site/specs/
```

And update `docusaurus.config.js` spec path:
```javascript
spec: `./specs/${name}/${name}.openapi.yaml`,
```

Also set `baseUrl: '/'` for Vercel deployment.

---

**Option A: Vercel CLI (Recommended)**

1. Install Vercel CLI (if not installed):
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Initial setup and deploy:
   ```bash
   cd docs-site
   vercel
   ```

4. Production deploy:
   ```bash
   vercel --prod
   ```

**Subsequent deploys**:
```bash
cd docs-site
vercel --prod
```

---

**Option B: Manual Deploy (without CLI)**

1. Go to https://vercel.com and login

2. Click "Add New..." → "Project"

3. Select "Import Git Repository" or "Upload"
   - For Git import: Select repo, set Root Directory to `docs-site`
   - For upload: Drag & drop the docs-site folder

4. Verify settings:
   - Framework Preset: Docusaurus
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Install Command: `npm install`

5. Click "Deploy"

6. After deployment, you'll get a URL like: `https://{project-name}.vercel.app/`

---

## Resources

### references/spec-prompt.md

The core specification prompt template that defines all rules for generating OpenAPI/Swagger documentation from Solidity contracts. This comprehensive prompt includes:

- Input format and placeholder definitions
- Contract detection and naming rules
- Path and operation design for functions
- Error handling and response structure
- Struct and type mapping rules
- Event and modifier documentation rules
- Output formatting guidelines

Load this file when generating specifications to ensure all rules are followed correctly.

### references/docusaurus-setup.md

Comprehensive guide for setting up a Docusaurus documentation site with Redocusaurus plugin. Includes:

- Installation instructions
- Configuration examples
- Automatic contract registration
- Deployment guide for Vercel CLI
- Troubleshooting tips
- Customization options

Refer to this file when creating the documentation site in Phase 2.

---

## Complete Usage Examples

### Example 1: Batch Generation for Multiple Contracts

**Scenario**: Generate specifications for all 18 contracts in the project

**Stage 1: Generate Skeletons**

User: "Run the batch generation script"

Assistant actions:
```bash
cd contract
node generate-openapi-specs.js
```

Output: Skeleton specification files created in `docs/contract/*/`

**Stage 2: Enhance Each Contract**

User: "Use contract-spec-generator skill to enhance StablecoinCore specifications"

Assistant actions:
1. Read `docs/contract/StablecoinCore/StablecoinCore.openapi.yaml` (generated spec)
2. Read `contract/src/StablecoinCore.sol` for source code analysis
3. Load `references/spec-prompt.md` for formatting rules
4. Enhance descriptions with contract-specific details
5. Add 500 error responses by analyzing internal functions
6. Add modifier information to function descriptions
7. Add `examples` section to 500 responses
8. Update both YAML and JSON files

User: "Repeat for the remaining 17 contracts"

(Repeat enhancement process for each contract)

**Phase 2: Create Documentation Site (Optional)**

User: "Create a Docusaurus site to view all specifications"

Assistant actions:
1. Check if docs-site/ directory exists (it already exists)
2. Read references/docusaurus-setup.md for guidance
3. Update docs-site/docusaurus.config.js to automatically register all 18 contracts
4. Start development server: npm run start
5. Verify site works at http://localhost:3000

---

### Example 2: Single Contract Mode

**Scenario**: Generate specifications for one contract (StablecoinCore) manually

**Phase 1: Generate Specifications**

User: "Generate contract specifications for StablecoinCore"

Assistant actions:
1. Read `contract/src/StablecoinCore.sol` for source code
2. Read contract ABI (via forge inspect or from build artifacts)
3. Load `references/spec-prompt.md` for generation rules
4. Generate `docs/contract/StablecoinCore/StablecoinCore.openapi.yaml` with complete descriptions
5. Generate `docs/contract/StablecoinCore/StablecoinCore.swagger.json`

**Phase 2: Create Documentation Site (User Confirmation)**

---

### Phase 3: Generate Markdown Documentation + Docusaurus Integration

After generating the OpenAPI/Swagger specifications, generate comprehensive Markdown documentation for the Docusaurus site. This creates a dual-documentation system with both human-readable docs and API specs.

#### Documentation Site Structure

The final site has:
- **API Spec** (`/api/*`): Redoc-based interactive API documentation from OpenAPI/Swagger specs
- **Docs** (`/docs/*`): Human-readable Markdown documentation with overview, features, and function details

**Navigation:**
- **Header**: Category dropdowns (Core Contracts, Features, Access Control, MultiSig & Others) → Docs
- **Homepage**: Contract cards with "View Specification" button → API Spec
- **Each Doc page**: Link to corresponding API Spec at the top

#### Steps

1. **Run the Markdown generation script**

   ```bash
   cd contract
   node generate-contract-docs.js
   ```

   This will generate:
   - Individual Markdown files for each contract in `docs-site/docs/contracts/`
   - An index page (`index.md`) with contract overview
   - Updated `sidebars.js` with proper categorization

2. **Generated Documentation Structure**

   Each contract documentation includes:
   - **API Specification Link**: Link to `/api/{ContractName}` at the top
   - **Overview**: Contract description
   - **Inheritance**: List of inherited contracts
   - **Key Features**: Detailed explanation of main features
   - **Function List**: Collapsible sections by category
     - Constants
     - Variables
     - Mapping
     - Read Functions
     - Write Functions
     - Events
     - Errors

3. **Build and Preview**

   ```bash
   cd docs-site
   npm install
   npm run build
   npm run serve
   ```

4. **Customization**

   The script (`contract/generate-contract-docs.js`) includes:
   - `CONTRACT_CATEGORIES`: Contract categorization for sidebar/navbar
   - `CONTRACT_DESCRIPTIONS`: Contract overview and feature descriptions
     - `overview`: Short description of the contract
     - `features`: Array of `{title, description}` for key features

   Modify these to customize the documentation structure.

#### docusaurus.config.js Configuration

The site uses a dual-preset configuration:

```javascript
presets: [
  // Markdown Docs
  ['@docusaurus/preset-classic', {
    docs: {
      sidebarPath: require.resolve('./sidebars.js'),
      routeBasePath: '/docs',
    },
  }],
  // API Specs (Redoc)
  ['redocusaurus', {
    specs: contractSpecs,  // Array of {id, spec, route}
    theme: { primaryColor: '#1890ff' },
  }],
],
```

**Navbar with Category Dropdowns:**

```javascript
navbar: {
  items: [
    {
      type: 'dropdown',
      label: 'Core Contracts',
      items: [
        { to: '/docs/contracts/StablecoinCore', label: 'StablecoinCore' },
        // ...
      ],
    },
    // Features, Access Control, MultiSig & Others dropdowns
  ],
},
```

#### When to Use Phase 3

- After generating OpenAPI specs (Phase 1)
- When you need both API specs and human-readable documentation
- When deploying a documentation site for developers
- When you want category-based navigation with detailed feature explanations

---

## Summary

This skill provides complete workflows for generating smart contract documentation:

**Workflow Modes:**
- **Batch Generation Mode** (recommended): Two-stage approach using skeleton script + AI enhancement for multiple contracts
- **Single Contract Mode**: Direct generation for individual contracts

**Phases:**
- **Stage/Phase 1**: Generate OpenAPI/Swagger specifications
- **Phase 2**: Create a Docusaurus documentation website (optional, requires user confirmation)
- **Phase 3**: Generate Markdown documentation + Docusaurus integration (recommended)

**Final Documentation Site Structure:**
- **Homepage** (`/`): Contract cards with "View Specification" button → API Spec
- **API Spec** (`/api/*`): Redoc-based interactive documentation
- **Docs** (`/docs/*`): Human-readable Markdown documentation
- **Header Navigation**: Category dropdowns (Core Contracts, Features, Access Control, MultiSig & Others) → Docs

**Site UI Specification (Important):**

| Term | Content | Path |
|------|---------|------|
| **Specification** | OpenAPI/Swagger format (Redoc display) | `/api/{ContractName}` |
| **Documentation** | Markdown format (overview + function list) | `/docs/*` |

**Header Structure:**

| Position | Element | Link Target |
|----------|---------|-------------|
| Left end | Logo + Project name | `/` |
| Second | **Docs** | `/overview` (System overview) |
| Third onwards | Category dropdown | `/api/{ContractName}` (specifications) |
| Right end | GitHub | Repository URL |

**Page Structure:**

| Page | Path | Content |
|------|------|---------|
| **Top Page** | `/` | Contract cards by category |
| **Overview Page** | `/overview` | System-wide description, contract list |
| **Documentation** | `/docs/contracts/*` | Detailed documentation for each contract |
| **Specification** | `/api/*` | OpenAPI/Swagger (Redoc display) |

**UI Element Specifications:**

| Element | Specification |
|---------|---------------|
| **Header left** | "Docs" → `/overview` (system overview page) |
| **Header dropdown** | Category name → Link to each contract's **specification** |
| **Hero** | Title + Subtitle only. **No** buttons |
| **Category name** | **Centered** |
| **Card** | Contract name + description + "View Specification" button |
| **Button** | "View Specification" → `/api/{ContractName}` |

**Button Specifications:**

| Item | Value |
|------|-------|
| Text | "View Specification" |
| Width | `100%` (match card width) |
| Height | `40px` |
| Font size | `14px` |
| Background color | Project's primary color (customizable) |
| Border radius | `4px` |

**Prohibited Items:**
- ❌ "Get Started", "API Reference", "Learn more" buttons in hero
- ❌ Multiple links like "Documentation", "API Reference" in cards
- ❌ Left-aligned category names

**Customizable Items:**
- ✅ Primary color (`--ifm-color-primary`)
- ✅ Logo image
- ✅ Project name
- ✅ Contract descriptions

**Fixed Items (As per template):**
- ❌ Header structure (Docs + category dropdown)
- ❌ Card structure (name + description + 1 button)
- ❌ Button text "View Specification"
- ❌ Layout, spacing, button size

**Detailed Templates:** See "Template Files" section in `.claude/agents/contract-spec-generator.md`

**Key Resources:**
- `contract/generate-openapi-specs.js` - OpenAPI/Swagger skeleton generator
- `contract/generate-contract-docs.js` - Markdown documentation generator
- `docs-site/docusaurus.config.js` - Site configuration with dual presets
- `references/spec-prompt.md` - Specification generation rules
- `references/docusaurus-setup.md` - Documentation site setup guide

**Recommended Workflow:**
1. Run `node generate-openapi-specs.js` to generate OpenAPI/Swagger specs
2. Run `node generate-contract-docs.js` to generate Markdown documentation
3. Build and deploy the Docusaurus site: `cd docs-site && npm run build`

**Generated Documentation Features:**
- Each Markdown doc has a link to corresponding API Spec at the top
- Main features are explained in detail (not just function listing)
- Function lists are collapsible (`<details>` sections)
- Category-based navigation in header dropdowns
