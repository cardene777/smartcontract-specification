import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

// カテゴリ別にコントラクトを定義
const contracts = [
  {
    category: 'トークンコントラクト',
    items: [
      {
        name: 'ERC20',
        path: '/api/ERC20',
        description: '転送、承認、許可メカニズムを備えた標準的な代替可能トークンの実装です。'
      },
    ]
  },
];

function ContractCard({ name, path, description }: { name: string; path: string; description: string }) {
  return (
    <div className={clsx('col col--4', styles.cardCol)}>
      <div className={clsx('card', styles.card)}>
        <div className="card__header">
          <h3>{name}</h3>
        </div>
        <div className={clsx('card__body', styles.cardBody)}>
          <p>{description}</p>
        </div>
        <div className={clsx('card__footer', styles.cardFooter)}>
          <Link
            className={clsx('button button--primary button--block', styles.specButton)}
            to={path}>
            仕様書を見る
          </Link>
        </div>
      </div>
    </div>
  );
}

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <p>全 {contracts.reduce((sum, cat) => sum + cat.items.length, 0)} 件のスマートコントラクト仕様書</p>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={siteConfig.title}
      description="Solidityスマートコントラクトの仕様書">
      <HomepageHeader />
      <main>
        <div className="container" style={{ marginTop: '40px', marginBottom: '40px' }}>
          {contracts.map((section, idx) => (
            <div key={idx} className={styles.categorySection}>
              <h2 className={styles.categoryTitle}>{section.category}</h2>
              <div className={clsx('row', styles.cardRow)}>
                {section.items.map((contract, contractIdx) => (
                  <ContractCard key={contractIdx} {...contract} />
                ))}
              </div>
            </div>
          ))}
        </div>
      </main>
    </Layout>
  );
}
