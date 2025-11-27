import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    'intro',
    {
      type: 'category',
      label: 'コントラクト',
      items: [
        'contracts/ERC20',
      ],
    },
  ],
};

export default sidebars;
