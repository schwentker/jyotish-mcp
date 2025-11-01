#!/bin/bash

# Jyotish MCP Setup Script
# Automates installation and configuration

set -e  # Exit on error

echo "=========================================="
echo "Jyotish MCP Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "Checking prerequisites..."

# Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.11+${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found. Please install Node.js 18+${NC}"
    exit 1
fi
NODE_VERSION=$(node --version)
echo -e "${GREEN}✓ Node.js $NODE_VERSION found${NC}"

# PostgreSQL
if ! command -v psql &> /dev/null; then
    echo -e "${YELLOW}⚠ PostgreSQL not found. Install it later for data persistence.${NC}"
else
    PG_VERSION=$(psql --version | cut -d' ' -f3)
    echo -e "${GREEN}✓ PostgreSQL $PG_VERSION found${NC}"
fi

echo ""
echo "=========================================="
echo "Setting up Python environment..."
echo "=========================================="

cd calculations

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

echo ""
echo "=========================================="
echo "Downloading Swiss Ephemeris data..."
echo "=========================================="

# Create ephemeris data directory
mkdir -p ephemeris_data
cd ephemeris_data

# Download essential ephemeris files (~100MB total)
echo "Downloading planetary ephemeris files..."
echo "(This may take a few minutes depending on your connection)"

# Function to download with progress
download_file() {
    local url=$1
    local filename=$(basename $url)
    
    if [ -f "$filename" ]; then
        echo -e "${GREEN}✓ $filename already exists${NC}"
    else
        echo "Downloading $filename..."
        if command -v wget &> /dev/null; then
            wget -q --show-progress "$url" || echo -e "${YELLOW}⚠ Failed to download $filename${NC}"
        elif command -v curl &> /dev/null; then
            curl -# -O "$url" || echo -e "${YELLOW}⚠ Failed to download $filename${NC}"
        else
            echo -e "${RED}❌ Neither wget nor curl found. Please install one.${NC}"
            exit 1
        fi
    fi
}

# Download files
download_file "ftp://ftp.astro.com/pub/swisseph/ephe/sepl_18.se1"
download_file "ftp://ftp.astro.com/pub/swisseph/ephe/semo_18.se1"
download_file "ftp://ftp.astro.com/pub/swisseph/ephe/seas_18.se1"

cd ../..

echo ""
echo "=========================================="
echo "Setting up MCP server..."
echo "=========================================="

cd mcp-server

# Install Node dependencies
echo "Installing Node.js dependencies..."
npm install
echo -e "${GREEN}✓ Node.js dependencies installed${NC}"

# Build TypeScript
echo "Building TypeScript..."
npm run build
echo -e "${GREEN}✓ MCP server built${NC}"

cd ..

echo ""
echo "=========================================="
echo "Setting up database (optional)..."
echo "=========================================="

if command -v createdb &> /dev/null; then
    read -p "Create PostgreSQL database 'jyotish'? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if createdb jyotish 2>/dev/null; then
            echo -e "${GREEN}✓ Database 'jyotish' created${NC}"
        else
            echo -e "${YELLOW}⚠ Database might already exist or permission denied${NC}"
        fi
    fi
else
    echo -e "${YELLOW}⚠ PostgreSQL not available. Skipping database creation.${NC}"
fi

echo ""
echo "=========================================="
echo "Creating environment file..."
echo "=========================================="

# Create .env file
cat > .env << EOF
# Jyotish MCP Configuration

# Database
DATABASE_URL=postgresql://localhost/jyotish

# Ephemeris
EPHEMERIS_PATH=$(pwd)/calculations/ephemeris_data

# Optional: Logging level
LOG_LEVEL=INFO
EOF

echo -e "${GREEN}✓ .env file created${NC}"

echo ""
echo "=========================================="
echo "✨ Setup Complete! ✨"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Configure Claude Desktop MCP settings:"
echo "   File: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo ""
echo "   Add this configuration:"
echo '   {'
echo '     "mcpServers": {'
echo '       "jyotish": {'
echo '         "command": "node",'
echo "         \"args\": [\"$(pwd)/mcp-server/dist/index.js\"],"
echo '         "env": {'
echo "           \"DATABASE_URL\": \"postgresql://localhost/jyotish\","
echo "           \"EPHEMERIS_PATH\": \"$(pwd)/calculations/ephemeris_data\""
echo '         }'
echo '       }'
echo '     }'
echo '   }'
echo ""
echo "2. Restart Claude Desktop"
echo ""
echo "3. Test by asking Claude:"
echo "   'Calculate a birth chart for September 27, 1953, 9:10 AM"
echo "    in Amritapuri, India (9°08'N, 76°48'E)'"
echo ""
echo "For more information, see:"
echo "  - README.md (full documentation)"
echo "  - QUICK_START.md (usage guide)"
echo "  - CONTRIBUTING.md (contribution guidelines)"
echo ""
echo -e "${GREEN}Happy chart reading! 🌟${NC}"
echo ""
