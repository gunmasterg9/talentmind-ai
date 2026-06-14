FROM node:18-alpine

WORKDIR /workspace

# Copy dependencies list and install
COPY package.json .
RUN npm install --legacy-peer-deps

# Copy source code
COPY . .

EXPOSE 3000

# Runs Next.js development server
CMD ["npm", "run", "dev"]
