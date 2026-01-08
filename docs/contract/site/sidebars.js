/**
 * Docusaurus用サイドバー設定
 * @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  // ガイドサイドバー（システム概要ページ）
  guidesSidebar: [
    {
      type: 'doc',
      id: 'overview',
      label: '概要',
    },
    {
      type: 'doc',
      id: 'architecture',
      label: 'アーキテクチャ',
    },
    {
      type: 'doc',
      id: 'roles',
      label: 'ロール管理',
    },
    {
      type: 'doc',
      id: 'security',
      label: 'セキュリティ',
    },
    {
      type: 'doc',
      id: 'testing',
      label: 'テスト',
    },
    {
      type: 'doc',
      id: 'upgrade',
      label: 'アップグレード',
    },
    {
      type: 'doc',
      id: 'audit',
      label: '監査',
    },
  ],

  // コントラクトサイドバー
  contractsSidebar: [
    {
      type: 'category',
      label: 'Token',
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'contracts/ERC20/ERC20',
          label: 'ERC20',
        },
      ],
    },
    {
      type: 'category',
      label: 'API仕様書',
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'api/ERC20',
          label: 'ERC20 API',
        },
      ],
    },
  ],
};

module.exports = sidebars;
