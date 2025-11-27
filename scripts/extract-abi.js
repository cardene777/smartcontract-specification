import hre from "hardhat";
import fs from "fs";
import path from "path";

async function main() {
  const abiDir = "./abi";

  // Create abi directory if it doesn't exist
  if (!fs.existsSync(abiDir)) {
    fs.mkdirSync(abiDir, { recursive: true });
  }

  // Debug: check what methods are available on hre.artifacts
  console.log("Available methods on hre.artifacts:", Object.keys(hre.artifacts));

  // Try different APIs
  if (typeof hre.artifacts.getArtifactPaths === "function") {
    const paths = await hre.artifacts.getArtifactPaths();
    console.log("Artifact paths:", paths);
  }

  // List all available artifacts
  try {
    const names = await hre.artifacts.getAllFullyQualifiedNames();
    console.log("Fully qualified names:", names);
  } catch (e) {
    console.log("getAllFullyQualifiedNames error:", e.message);
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
