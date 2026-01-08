/**
 * Sidebars configuration template
 *
 * カテゴリとコントラクトをプロジェクトに合わせて修正してください。
 */

module.exports = {
  contractsSidebar: [
    {
      type: 'doc',
      id: 'contracts/index',
      label: 'コントラクト仕様',
    },

    // カテゴリ1
    {
      type: 'category',
      label: 'カテゴリ1',
      items: [
        'contracts/Contract1',
        'contracts/Contract2',
      ]
    },
    // カテゴリ2
    {
      type: 'category',
      label: 'カテゴリ2',
      items: [
        'contracts/Contract3',
        'contracts/Contract4',
      ]
    },
    // 必要に応じてカテゴリを追加

  ],
};
