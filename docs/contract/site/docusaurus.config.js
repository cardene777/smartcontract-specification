// @ts-check
const { themes: prismThemes } = require('prism-react-renderer');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'ERC20 スマートコントラクト仕様書',
  tagline: 'OpenZeppelin ERC20トークン標準の包括的なドキュメント',
  favicon: 'img/favicon.ico',

  url: 'https://example.com',
  baseUrl: '/',

  organizationName: 'example',
  projectName: 'erc20-docs',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'ja',
    locales: ['ja'],
  },

  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: 'docs',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'ERC20 Docs',
        logo: {
          alt: 'Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'dropdown',
            label: '概要',
            position: 'left',
            items: [
              { to: '/docs/overview', label: 'システム概要' },
              { to: '/docs/architecture', label: 'アーキテクチャ' },
              { to: '/docs/roles', label: 'ロール管理' },
              { to: '/docs/security', label: 'セキュリティ' },
              { to: '/docs/testing', label: 'テスト' },
              { to: '/docs/upgrade', label: 'アップグレード' },
              { to: '/docs/audit', label: '監査' },
            ],
          },
          {
            type: 'dropdown',
            label: 'Token',
            position: 'left',
            items: [
              { to: '/docs/contracts/ERC20/', label: 'ERC20' },
            ],
          },
          {
            to: '/docs/api/ERC20',
            label: 'API仕様書',
            position: 'left',
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
              { label: 'セキュリティ', to: '/docs/security' },
            ],
          },
          {
            title: 'コントラクト',
            items: [
              { label: 'ERC20', to: '/docs/contracts/ERC20/' },
              { label: 'API仕様書', to: '/docs/api/ERC20' },
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
        copyright: `Copyright © ${new Date().getFullYear()} Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['solidity', 'json', 'bash'],
      },
    }),
};

module.exports = config;
