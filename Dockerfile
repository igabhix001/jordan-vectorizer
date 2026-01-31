# Multi-stage Dockerfile for RunPod serverless deployment
# GitHub: https://github.com/igabhix001/jordan-vectorizer

FROM node:20-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy package files
COPY package.json package-lock.json ./
COPY Cargo.toml build.rs rustfmt.toml ./

# Install Node.js dependencies
RUN npm ci

# Copy source code
COPY src ./src
COPY index.js index.d.ts ./
COPY cli ./cli

# Build the native module
RUN npm run build

# Production stage
FROM node:20-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy built artifacts from builder
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/index.js ./index.js
COPY --from=builder /app/index.d.ts ./index.d.ts
COPY --from=builder /app/*.node ./

# Copy CLI
COPY --from=builder /app/cli ./cli

# Copy API code
COPY api/requirements.txt ./api/
RUN pip3 install --no-cache-dir --break-system-packages -r api/requirements.txt

COPY api/main.py ./api/
COPY api/vectorizer_wrapper.js ./api/

# Create output directory
RUN mkdir -p /app/output

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Start the API server
CMD ["python3", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
