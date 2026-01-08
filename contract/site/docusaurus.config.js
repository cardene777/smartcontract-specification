// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'OpenZeppelin ERC20 & ERC721 契約仕様書',
  tagline: 'Ethereum スマートコントラクトのセキュアな実装',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://OpenZeppelin.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'OpenZeppelin', // Usually your GitHub org/user name.
  projectName: 'openzeppelin-contracts', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'ja',
    locales: ['ja', 'en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          path: '../docs',
          routeBasePath: 'docs',
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/OpenZeppelin/openzeppelin-contracts/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
    [
      'redocusaurus',
      {
        // Plugin Options for loading OpenAPI files
        specs: [
          {
            spec: '../specs/ERC20/ERC20.openapi.yaml',
            route: '/api/ERC20',
          },
          {
            spec: '../specs/ERC20Burnable/ERC20Burnable.openapi.yaml',
            route: '/api/ERC20Burnable',
          },
          {
            spec: '../specs/ERC20Capped/ERC20Capped.openapi.yaml',
            route: '/api/ERC20Capped',
          },
          {
            spec: '../specs/ERC20Pausable/ERC20Pausable.openapi.yaml',
            route: '/api/ERC20Pausable',
          },
          {
            spec: '../specs/ERC20Permit/ERC20Permit.openapi.yaml',
            route: '/api/ERC20Permit',
          },
          {
            spec: '../specs/ERC20Votes/ERC20Votes.openapi.yaml',
            route: '/api/ERC20Votes',
          },
          {
            spec: '../specs/ERC721/ERC721.openapi.yaml',
            route: '/api/ERC721',
          },
          {
            spec: '../specs/ERC721Burnable/ERC721Burnable.openapi.yaml',
            route: '/api/ERC721Burnable',
          },
          {
            spec: '../specs/ERC721Enumerable/ERC721Enumerable.openapi.yaml',
            route: '/api/ERC721Enumerable',
          },
          {
            spec: '../specs/ERC721Pausable/ERC721Pausable.openapi.yaml',
            route: '/api/ERC721Pausable',
          },
          {
            spec: '../specs/ERC721Royalty/ERC721Royalty.openapi.yaml',
            route: '/api/ERC721Royalty',
          },
          {
            spec: '../specs/ERC721URIStorage/ERC721URIStorage.openapi.yaml',
            route: '/api/ERC721URIStorage',
          },
        ],
        // Theme Options for modifying how redoc renders them
        theme: {
          // Change with your site colors
          primaryColor: '#1890ff',
        },
      },
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'OpenZeppelin Contracts',
        logo: {
          alt: 'OpenZeppelin Contracts Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'dropdown',
            label: '概要',
            position: 'left',
            items: [
              { type: 'doc', docId: 'overview', label: 'システム概要' },
              { type: 'doc', docId: 'architecture', label: 'アーキテクチャ' },
              { type: 'doc', docId: 'roles', label: 'ロール管理' },
              { type: 'doc', docId: 'security', label: 'セキュリティ' },
              { type: 'doc', docId: 'testing', label: 'テスト' },
              { type: 'doc', docId: 'upgrade', label: 'アップグレード' },
              { type: 'doc', docId: 'audit', label: '監査' },
            ],
          },
          {
            type: 'dropdown',
            label: 'ERC20 トークン',
            position: 'left',
            items: [
              {
                type: 'doc',
                docId: 'contracts/ERC20',
                label: 'ERC20',
              },
              {
                type: 'doc',
                docId: 'contracts/ERC20Burnable',
                label: 'ERC20Burnable',
              },
              {
                type: 'doc',
                docId: 'contracts/ERC20Capped',
                label: 'ERC20Capped',
              },
              {
                type: 'doc',
                docId: 'contracts/ERC20Pausable',
                label: 'ERC20Pausable',
              },
              {
                type: 'doc',
                docId: 'contracts/ERC20Permit',
                label: 'ERC20Permit',
              },
              {
                type: 'doc',
                docId: 'contracts/ERC20Votes',
                label: 'ERC20Votes',
              },
            ],
          },
          {
            type: 'dropdown',
            label: 'ERC721 NFT',
            position: 'left',
            items: [
              {
                type: 'doc',
                docId: 'contracts/ERC721',
                label: 'ERC721',
              },
              {
                type: 'doc',
                docId: 'contracts/ERC721Burnable',
                label: 'ERC721Burnable',
              },
              {
                type: 'doc',
                docId: 'contracts/ERC721Enumerable',
                label: 'ERC721Enumerable',
              },
              {
                type: 'doc',
                docId: 'contracts/ERC721Pausable',
                label: 'ERC721Pausable',
              },
              {
                type: 'doc',
                docId: 'contracts/ERC721Royalty',
                label: 'ERC721Royalty',
              },
              {
                type: 'doc',
                docId: 'contracts/ERC721URIStorage',
                label: 'ERC721URIStorage',
              },
            ],
          },
          {
            href: 'https://github.com/OpenZeppelin/openzeppelin-contracts',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: '概要',
            items: [
              { label: 'システム概要', to: '/docs/overview' },
              { label: 'アーキテクチャ', to: '/docs/architecture' },
              { label: 'ロール管理', to: '/docs/roles' },
              { label: 'セキュリティ', to: '/docs/security' },
              { label: 'テスト', to: '/docs/testing' },
              { label: 'アップグレード', to: '/docs/upgrade' },
              { label: '監査', to: '/docs/audit' },
            ],
          },
          {
            title: 'コントラクト',
            items: [
              {
                label: 'ERC20',
                to: '/docs/contracts/ERC20',
              },
              {
                label: 'ERC20Burnable',
                to: '/docs/contracts/ERC20Burnable',
              },
              {
                label: 'ERC20Capped',
                to: '/docs/contracts/ERC20Capped',
              },
              {
                label: 'ERC20Pausable',
                to: '/docs/contracts/ERC20Pausable',
              },
              {
                label: 'ERC20Permit',
                to: '/docs/contracts/ERC20Permit',
              },
            ],
          },
          {
            title: 'コミュニティ',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/OpenZeppelin/openzeppelin-contracts',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} OpenZeppelin Contracts. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['solidity'],
      },
    }),
};

export default config;
