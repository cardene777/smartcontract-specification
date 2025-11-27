import fs from 'fs';
import path from 'path';

const ozDir = './node_modules/@openzeppelin/contracts';
const contractsDir = './contracts';

// Ensure contracts directory exists
if (!fs.existsSync(contractsDir)) {
  fs.mkdirSync(contractsDir, { recursive: true });
}

function findSolFiles(dir, files = []) {
  const items = fs.readdirSync(dir);
  for (const item of items) {
    const fullPath = path.join(dir, item);
    if (fs.statSync(fullPath).isDirectory()) {
      findSolFiles(fullPath, files);
    } else if (item.endsWith('.sol')) {
      files.push(fullPath);
    }
  }
  return files;
}

const solFiles = findSolFiles(ozDir);
console.log(`Found ${solFiles.length} Solidity files`);

// Group imports by category (top-level folder under contracts/)
const imports = {};
for (const file of solFiles) {
  // ./node_modules/@openzeppelin/contracts/access/AccessControl.sol
  // We want the part after contracts/
  const afterContracts = file.split('/contracts/')[1];
  // access/AccessControl.sol -> category is 'access'
  const category = afterContracts.split('/')[0];

  if (!imports[category]) {
    imports[category] = [];
  }
  imports[category].push(`@openzeppelin/contracts/${afterContracts}`);
}

console.log('Categories:', Object.keys(imports));

// Create import files for each category
for (const [category, paths] of Object.entries(imports)) {
  const categoryName = category.charAt(0).toUpperCase() + category.slice(1);
  const importStatements = paths.map(p => `import "${p}";`).join('\n');
  const content = `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

${importStatements}
`;

  const outputPath = path.join(contractsDir, `Import${categoryName}.sol`);
  fs.writeFileSync(outputPath, content);
  console.log(`Created ${outputPath} with ${paths.length} imports`);
}

console.log('Done!');
