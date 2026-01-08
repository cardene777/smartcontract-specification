import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

interface ContractCard {
  name: string;
  path: string;
  description: string;
}

interface CategoryData {
  category: string;
  items: ContractCard[];
}

const contractsData: CategoryData[] = [
  {
    category: 'Token',
    items: [
      {
        name: 'ERC20',
        path: '/docs/api/ERC20',
        description: 'ERC20トークン標準の実装コントラクト。転送、許可、メタデータ機能を提供します。',
      },
    ],
  },
];

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  const totalContracts = contractsData.reduce((sum, cat) => sum + cat.items.length, 0);

  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <p className={styles.heroSubtext}>
          全 {totalContracts} 個のスマートコントラクト仕様書
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/overview">
            ドキュメントを見る
          </Link>
        </div>
      </div>
    </header>
  );
}

function ContractCard({ name, path, description }: ContractCard) {
  return (
    <div className={clsx('col col--4', styles.featureCard)}>
      <div className="card">
        <div className="card__header">
          <h3>{name}</h3>
        </div>
        <div className="card__body">
          <p>{description}</p>
        </div>
        <div className="card__footer">
          <Link className="button button--primary button--block" to={path}>
            仕様書を見る
          </Link>
        </div>
      </div>
    </div>
  );
}

function ContractSection({ category, items }: CategoryData) {
  return (
    <section className={styles.features}>
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
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={siteConfig.title}
      description={siteConfig.tagline}>
      <HomepageHeader />
      <main>
        {contractsData.map((categoryData, idx) => (
          <ContractSection key={idx} {...categoryData} />
        ))}
      </main>
    </Layout>
  );
}
