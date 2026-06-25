name: SUPER-CORE-AFFILIATE

on:
  schedule:
    - cron: '*/5 * * * *'
  workflow_dispatch:

jobs:
  core-evolution:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout Code Matrix
        uses: actions/checkout@v3
        with:
          persist-credentials: true
          fetch-depth: 0

      - name: Initialize Python Runtime
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Execute Super Core Calibration
        run: python "Super Core Affiliate/Super-Core-Affiliate.py"

      - name: Ghost Push Central Gateway
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          git config --global user.name "EATHESEN-CORE-BOT"
          git config --global user.email "core@donabicomedia.net"
          
          git add system_bridge.json
          
          if ! git diff --cached --quiet; then
            git commit -m "¢24-Core-Evolution: Sync Central Matrix $(date -u +'%Y-%m-%d %H:%M:%S') UTC"
            
            # CHIẾN LƯỢC ÉP ĐÈ X-STRATEGY: Ưu tiên tuyệt đối file mới sinh ra khi xảy ra xung đột
            git pull origin main --rebase -X ours
            
            git push https://x-access-token:${GITHUB_TOKEN}@github.com/${{ github.repository }}.git main
          else
            echo "[EATHESEN] Trạng thái ma trận cân bằng, bỏ qua chu kỳ Commit này."
          fi
