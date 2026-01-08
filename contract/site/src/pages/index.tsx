import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

interface ContractCard {
  name: string;
  description: string;
  path: string;
}

interface ContractCategory {
  category: string;
  items: ContractCard[];
}

const contractsData: ContractCategory[] = [
  {
    category: 'ERC20 トークン',
    items: [
      {
        name: 'ERC20',
        path: '/api/ERC20',
        description: 'ERC20標準トークンの基本実装',
      },
      {
        name: 'ERC20Burnable',
        path: '/api/ERC20Burnable',
        description: 'トークン焼却機能を持つERC20',
      },
      {
        name: 'ERC20Capped',
        path: '/api/ERC20Capped',
        description: '供給量上限を持つERC20',
      },
      {
        name: 'ERC20Pausable',
        path: '/api/ERC20Pausable',
        description: '一時停止機能を持つERC20',
      },
      {
        name: 'ERC20Permit',
        path: '/api/ERC20Permit',
        description: '署名ベース承認機能を持つERC20',
      },
      {
        name: 'ERC20Votes',
        path: '/api/ERC20Votes',
        description: '投票・委任機能を持つERC20',
      },
    ],
  },
  {
    category: 'ERC721 NFT',
    items: [
      {
        name: 'ERC721',
        path: '/api/ERC721',
        description: 'ERC721標準NFTの基本実装',
      },
      {
        name: 'ERC721Burnable',
        path: '/api/ERC721Burnable',
        description: 'NFT焼却機能を持つERC721',
      },
      {
        name: 'ERC721Enumerable',
        path: '/api/ERC721Enumerable',
        description: '列挙機能を持つERC721',
      },
      {
        name: 'ERC721Pausable',
        path: '/api/ERC721Pausable',
        description: '一時停止機能を持つERC721',
      },
      {
        name: 'ERC721Royalty',
        path: '/api/ERC721Royalty',
        description: 'ロイヤリティ標準を持つERC721',
      },
      {
        name: 'ERC721URIStorage',
        path: '/api/ERC721URIStorage',
        description: 'ストレージベースURI管理を持つERC721',
      },
    ],
  },
];

function ContractCard({ name, description, path }: ContractCard) {
  return (
    <div className={clsx('col col--4')}>
      <div className="card">
        <div className="card__header">
          <h3>{name}</h3>
        </div>
        <div className="card__body">
          <p>{description}</p>
        </div>
        <div className="card__footer">
          <Link
            className="button button--primary button--block"
            to={path}>
            仕様書を見る
          </Link>
        </div>
      </div>
    </div>
  );
}

function CategorySection({ category, items }: ContractCategory) {
  return (
    <section className={styles.categorySection}>
      <div className="container">
        <h2 className={styles.categoryTitle}>{category}</h2>
        <div className="row">
          {items.map((contract, idx) => (
            <ContractCard key={idx} {...contract} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="OpenZeppelinが提供するERC20とERC721トークン標準の完全な実装仕様書。セキュアで監査済みのスマートコントラクトライブラリです。">
      <header className={clsx('hero hero--primary', styles.heroBanner)}>
        <div className="container">
          <h1 className="hero__title">{siteConfig.title}</h1>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <p className={styles.contractCount}>全12個のスマートコントラクト仕様書</p>
        </div>
      </header>
      <main>
        {contractsData.map((category, idx) => (
          <CategorySection key={idx} {...category} />
        ))}
      </main>
    </Layout>
  );
}
