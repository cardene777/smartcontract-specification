import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';

const contracts = {{CONTRACTS_DATA}};

function ContractCard({ name, path, description }) {
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
            className="button button--primary button--block"
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
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <p>全{{TOTAL_CONTRACTS}}個のスマートコントラクト仕様書</p>
      </div>
    </header>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="{{PROJECT_DESCRIPTION}}">
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
