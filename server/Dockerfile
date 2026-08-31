# Tapkasa sync relay — bez runtime závislostí, jen Node 22
FROM node:22-alpine

ENV NODE_ENV=production
WORKDIR /app

COPY package.json index.js ./

# obraz node:22-alpine má připraveného neprivilegovaného uživatele "node"
USER node

EXPOSE 8080
CMD ["node", "index.js"]
