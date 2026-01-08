module.exports = {
  contractsSidebar: [
    "overview",
    "architecture",
    "roles",
    "security",
    "testing",
    "upgrade",
    "audit",
    {
        "type": "category",
        "label": "ERC20 トークン",
        "items": [
            "contracts/ERC20",
            "contracts/ERC20Burnable",
            "contracts/ERC20Capped",
            "contracts/ERC20Pausable",
            "contracts/ERC20Permit",
            "contracts/ERC20Votes",
        ]
    },
    {
        "type": "category",
        "label": "ERC721 NFT",
        "items": [
            "contracts/ERC721",
            "contracts/ERC721Burnable",
            "contracts/ERC721Enumerable",
            "contracts/ERC721Pausable",
            "contracts/ERC721Royalty",
            "contracts/ERC721URIStorage",
        ]
    },
],
};
