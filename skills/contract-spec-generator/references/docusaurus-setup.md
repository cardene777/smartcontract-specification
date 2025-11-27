# Docusaurus Site Setup Guide

This guide explains how to create a Docusaurus site to display generated contract specifications (OpenAPI YAML).

## Prerequisites

- Node.js 18 or higher installed
- npm, yarn, pnpm, or bun installed
- Contract specifications (OpenAPI YAML) already generated

## Setup Instructions

### 1. Initialize Docusaurus Project

Run the following command in the project root:

```bash
npx create-docusaurus@latest docs-site classic --typescript
cd docs-site
```

### 2. Install Required Dependencies

Install the Redocusaurus plugin and other dependencies:

```bash
npm install redocusaurus styled-components
```

Or

```bash
yarn add redocusaurus styled-components
```

### 3. Update package.json

Ensure `docs-site/package.json` includes the following dependencies:

```json
{
  "dependencies": {
    "@docusaurus/core": "^3.9.2",
    "@docusaurus/preset-classic": "^3.9.2",
    "@mdx-js/react": "^3.0.0",
    "clsx": "^1.1.1",
    "prism-react-renderer": "^1.2.1",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "redocusaurus": "^2.5.0",
    "styled-components": "^6.0.5"
  }
}
```

### 4. Configure docusaurus.config.js

Configure `docs-site/docusaurus.config.js` as follows:

```javascript
const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').DocusaurusConfig} */
(module.exports = {
  title: 'Avalanche Stablecoin Contract Specifications',
  tagline: 'OpenAPI specifications for Solidity smart contracts',
  url: 'https://your-site-url.com',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'your-org',
  projectName: 'avalanche-stablecoin',

  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
        },
        blog: false, // Disable blog feature
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
    [
      'redocusaurus',
      {
        specs: [
          // Add contract specifications here
          // {
          //   id: 'contract-name',
          //   spec: '../docs/contract/ContractName/ContractName.openapi.yaml',
          //   route: '/api/contract-name',
          // },
        ],
        theme: {
          primaryColor: '#1890ff',
          options: {
            hideDownloadButton: false,
            disableSearch: false,
            expandResponses: '200',
            requiredPropsFirst: true,
            sortPropsAlphabetically: true,
            showExtensions: true,
            hideLoading: true,
            nativeScrollbars: false,
            theme: {
              sidebar: {
                width: '300px',
              },
            },
          },
        },
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Avalanche Stablecoin',
      logo: {
        alt: 'Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'doc',
          docId: 'intro',
          position: 'left',
          label: 'Docs',
        },
        {
          to: '/api/stablecoin-core',
          label: 'API Specs',
          position: 'left',
        },
      ],
    },
    prism: {
      theme: lightCodeTheme,
      darkTheme: darkCodeTheme,
    },
  },
});
```

### 5. Register Specifications

Register generated OpenAPI YAML files with Redocusaurus. Add each contract to the `specs` array in `docusaurus.config.js`:

```javascript
specs: [
  {
    id: 'stablecoin-core',
    spec: '../docs/contract/StablecoinCore/StablecoinCore.openapi.yaml',
    route: '/api/stablecoin-core',
  },
  {
    id: 'stablecoin-bank',
    spec: '../docs/contract/StablecoinBank/StablecoinBank.openapi.yaml',
    route: '/api/stablecoin-bank',
  },
  // Add other contracts similarly
]
```

## Auto-Registration of Specifications

To register multiple contract specifications at once, use the following script:

```javascript
// Add to docusaurus.config.js
const fs = require('fs');
const path = require('path');

// Auto-detect all contracts from ../docs/contract/ directory
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

// Use in presets
presets: [
  // ...
  [
    'redocusaurus',
    {
      specs: getContractSpecs(),
      theme: {
        // ...
      },
    },
  ],
],
```

## Start Development Server

```bash
npm run start
```

Or

```bash
yarn start
```

Once the server starts, open `http://localhost:3000` in a browser.

## Build

To build for production:

```bash
npm run build
```

Built files are output to the `build/` directory.

## Deployment

### Deploy to GitHub Pages

```bash
npm run deploy
```

### Deploy to Vercel

1. Create a Vercel account
2. Push project to GitHub
3. Click "New Project" in Vercel dashboard
4. Select GitHub repository
5. Set Root Directory to `docs-site`
6. Deploy

### Deploy to Netlify

1. Create a Netlify account
2. Push project to GitHub
3. Click "New site from Git" in Netlify dashboard
4. Select GitHub repository
5. Build command: `npm run build`
6. Publish directory: `docs-site/build`
7. Deploy

## Troubleshooting

### Build Error: "Cannot find module"

Reinstall dependencies:

```bash
rm -rf node_modules package-lock.json
npm install
```

### YAML Parse Error

Check YAML file indentation and syntax. Pay attention to:

- Use 2-space indentation
- Use `|` or `>` for multi-line strings
- Quote special characters

### Redocusaurus Not Displaying

1. Verify paths in `specs` array are correct
2. Confirm YAML files exist
3. Restart development server

## Customization

### Change Theme Color

Modify `theme.primaryColor` in `docusaurus.config.js`:

```javascript
theme: {
  primaryColor: '#1890ff', // Change to any color
}
```

### Change Sidebar Width

```javascript
theme: {
  theme: {
    sidebar: {
      width: '300px', // Change to any width
    },
  },
}
```

### Customize Footer

Edit `themeConfig.footer` in `docusaurus.config.js`:

```javascript
footer: {
  style: 'dark',
  links: [
    {
      title: 'Core Contracts',
      items: [
        { label: 'StablecoinCore', to: '/api/stablecoin-core' },
        { label: 'StablecoinBank', to: '/api/stablecoin-bank' },
      ],
    },
  ],
  copyright: `Copyright © ${new Date().getFullYear()} Your Project.`,
}
```

## Reference Links

- [Docusaurus Official Documentation](https://docusaurus.io/)
- [Redocusaurus Official Documentation](https://redocly.com/docs/redoc/deployment/docusaurus/)
- [OpenAPI Specification](https://swagger.io/specification/)
