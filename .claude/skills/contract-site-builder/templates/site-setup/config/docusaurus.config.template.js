const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

// With JSDoc @type annotations, IDEs can provide config autocompletion
/** @type {import('@docusaurus/types').DocusaurusConfig} */
(module.exports = {
  title: '{{PROJECT_TITLE}}',
  tagline: '{{PROJECT_TAGLINE}}',
  url: 'https://{{GITHUB_ORG}}.github.io',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: '{{GITHUB_ORG}}',
  projectName: '{{PROJECT_REPO_NAME}}',

  presets: [
    [
      '@docusaurus/preset-classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          path: '../docs',
          sidebarPath: require.resolve('./sidebars.js'),
          routeBasePath: '/docs',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  plugins: [
    [
      'docusaurus-plugin-openapi-docs',
      {
        id: 'api',
        docsPluginId: 'default',
        config: {
{{OPENAPI_PLUGIN_CONFIG}}
        },
      },
    ],
  ],

  themes: ['docusaurus-theme-openapi-docs'],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      colorMode: {
        defaultMode: 'dark',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: '{{PROJECT_NAME}}',
        logo: {
          alt: '{{PROJECT_NAME}} Logo',
          src: 'img/logo.svg',
        },
        items: [
          // 概要ドロップダウン（固定・右側）
          {
            type: 'dropdown',
            label: '概要',
            position: 'right',
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
          // コントラクトカテゴリ（動的・右側 - sidebarsから生成）
{{CONTRACTS_NAVBAR}},
        ],
      },
      footer: {
        style: 'dark',
        links: {{FOOTER_LINKS}},
        copyright: `Copyright ${new Date().getFullYear()} {{PROJECT_NAME}} Project. Built with Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: ['solidity'],
      },
    }),
});
