import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'スマートコントラクト仕様書',
  tagline: 'Solidityスマートコントラクトの仕様書',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://your-docusaurus-site.example.com',
  baseUrl: '/',

  organizationName: 'your-org',
  projectName: 'smartcontract-specification',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'ja',
    locales: ['ja'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
    [
      'redocusaurus',
      {
        specs: [
          {
            id: 'erc20',
            spec: './specs/ERC20/ERC20.openapi.yaml',
            route: '/api/ERC20',
          },
        ],
        theme: {
          primaryColor: '#1890ff',
          options: {
            hideDownloadButton: false,
            disableSearch: false,
            expandResponses: '200',
            requiredPropsFirst: true,
            sortPropsAlphabetically: true,
            hideLoading: true,
            nativeScrollbars: false,
          },
        },
      },
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'スマートコントラクト仕様書',
      logo: {
        alt: 'ロゴ',
        src: 'img/logo.svg',
      },
      items: [
        {
          to: '/docs/intro',
          label: 'ドキュメント',
          position: 'left',
        },
        {
          type: 'dropdown',
          label: 'トークンコントラクト',
          position: 'left',
          items: [
            { to: '/api/ERC20', label: 'ERC20' },
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
          title: 'コントラクト',
          items: [
            {
              label: 'ERC20',
              to: '/api/ERC20',
            },
          ],
        },
        {
          title: 'リソース',
          items: [
            {
              label: 'OpenZeppelin ドキュメント',
              href: 'https://docs.openzeppelin.com/contracts',
            },
            {
              label: 'ERC20 標準',
              href: 'https://eips.ethereum.org/EIPS/eip-20',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} スマートコントラクト仕様書. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['solidity'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
