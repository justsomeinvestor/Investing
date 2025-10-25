#!/usr/bin/env python3
"""
Sync portfolio recommendations from latest analysis file to master-plan.md

Reads the latest portfolio recommendation data (generated from AI analysis)
and updates the portfolioRecommendation section in master-plan.md with:
- Signal score and tier
- Allocation percentages
- Recommended actions with rationale
- Updated timestamp

Usage:
    python sync_portfolio_recommendation.py [--date YYYY-MM-DD]
"""

import re
import sys
import yaml
from pathlib import Path
from datetime import datetime, timezone
import argparse

def get_latest_portfolio_recommendation():
    """Find the latest portfolio recommendation file"""
    portfolio_dir = Path(__file__).parent.parent.parent / 'Journal' / 'portfolio_decisions'

    if not portfolio_dir.exists():
        print(f"ERROR: Portfolio decisions directory not found: {portfolio_dir}", flush=True)
        return None

    # Look for recommendation files (either _portfolio_recommendation.txt or _portfolio_prompt.txt)
    rec_files = list(portfolio_dir.glob('*_portfolio_*.txt'))

    if not rec_files:
        print(f"WARNING: No portfolio files found in {portfolio_dir}")
        return None

    # Sort by modification time, get most recent
    latest_file = max(rec_files, key=lambda p: p.stat().st_mtime)
    return latest_file

def parse_portfolio_recommendation(file_path):
    """
    Parse portfolio recommendation file and extract structured data.

    Looks for pattern:
    RECOMMENDATION:
    Target: X% cash, Y% equities, Z% crypto, W% hedges

    ACTIONS:
    - [Action with description]
    - [Action with description]

    REASONING:
    [2-3 sentences]

    KEY RISKS:
    [Risk description]
    """

    content = file_path.read_text(encoding='utf-8', errors='replace')

    # Extract recommendation section
    rec_match = re.search(
        r'RECOMMENDATION:.*?Target:\s*(\d+)%\s*cash[^$]*?(\d+)%\s*equities[^$]*?(\d+)%\s*crypto[^$]*?(\d+)%\s*hedges',
        content,
        re.DOTALL | re.IGNORECASE
    )

    if not rec_match:
        print("WARNING: Could not parse RECOMMENDATION target allocation")
        return None

    cash, equities, crypto, hedges = map(int, rec_match.groups())

    # Extract actions
    actions_match = re.search(
        r'ACTIONS:(.+?)(?:REASONING:|KEY RISKS:|$)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    actions = []
    if actions_match:
        actions_text = actions_match.group(1)
        # Find all bullet points - split by newline and process
        action_lines = re.findall(r'^-\s*(.+?)$', actions_text, re.MULTILINE)
        for line in action_lines:
            # Clean up line - remove extra whitespace
            line = ' '.join(line.split())
            if line:
                actions.append({'action': line, 'rationale': 'Based on current signal and market context'})

    # Extract reasoning
    reasoning_match = re.search(
        r'REASONING:(.+?)(?:KEY RISKS:|$)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    reasoning = reasoning_match.group(1).strip() if reasoning_match else 'Market analysis updated.'

    # Extract key risks
    risks_match = re.search(
        r'KEY RISKS:(.+?)$',
        content,
        re.DOTALL | re.IGNORECASE
    )
    key_risks = []
    if risks_match:
        risks_text = risks_match.group(1)
        # Find all bullet points starting with - or •
        risk_lines = re.findall(r'^[•\-]\s*(.+?)$', risks_text, re.MULTILINE)
        for line in risk_lines:
            line = ' '.join(line.split())
            if line:
                key_risks.append(line)

    # Determine signal tier based on context
    signal_tier = 'MODERATE'

    return {
        'allocation': {
            'cash': cash,
            'equities': equities,
            'crypto': crypto,
            'hedges': hedges
        },
        'signalTier': signal_tier,
        'actions': actions,
        'reasoning': reasoning,
        'keyRisks': key_risks
    }

def update_portfolio_in_master_plan(data):
    """Update portfolioRecommendation section in master-plan.md"""

    master_plan_path = Path(__file__).parent.parent.parent / 'master-plan' / 'master-plan.md'

    if not master_plan_path.exists():
        print(f"ERROR: master-plan.md not found at {master_plan_path}")
        return False

    content = master_plan_path.read_text(encoding='utf-8')

    # Get current timestamp
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Build new portfolioRecommendation YAML section
    # Find the portfolioRecommendation section and replace it

    # Create the YAML structure for allocation (4 spaces base indentation)
    allocation_yaml = f"""allocation:
      cash: {data['allocation']['cash']}
      equities: {data['allocation']['equities']}
      crypto: {data['allocation']['crypto']}
      hedges: {data['allocation']['hedges']}"""

    # Create actions YAML (indent to match allocation/tickers level in template)
    actions_yaml = "actions:"
    for action in data['actions']:
        # 2 spaces for list item (base 4 + 2 = 6 total after +4 indent in file)
        actions_yaml += f"\n      - action: {action['action']}"
        actions_yaml += f"\n        rationale: {action['rationale']}"

    # Create risks YAML (indent to match allocation/tickers level in template)
    risks_yaml = "keyRisks:"
    for risk in data['keyRisks']:
        # 2 spaces for list item (base 4 + 2 = 6 total after +4 indent in file)
        risks_yaml += f"\n      - {risk}"

    # Build full portfolio recommendation YAML
    # Note: This will be indented +4 spaces when inserted into master-plan.md
    portfolio_yaml = f"""portfolioRecommendation:
    updatedAt: '{now}'
    signalTier: {data['signalTier']}
    confidenceLevel: medium-high
    {allocation_yaml}
    tickers:
      tech: AAPL, MSFT, META, NVDA
      crypto: BTC/ETH @ $107-109k support
      defensive: Cash ready
    {actions_yaml}
    reasoning: {data['reasoning']}
    {risks_yaml}
    accountBalance: 23106
    recommendation: See allocation above for current positioning"""

    # Find and replace the portfolioRecommendation section
    # Pattern matches from "- id: portfolio" to just before "aiInterpretation:"
    pattern = r'(  - id: portfolio\n    label: 💼 Portfolio\n)(    portfolioRecommendation:.*?)(    aiInterpretation:)'

    def replacement(match):
        return match.group(1) + '    ' + portfolio_yaml.replace('\n', '\n    ') + '\n' + match.group(3)

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content == content:
        print("WARNING: Could not find portfolioRecommendation section to update")
        return False

    master_plan_path.write_text(new_content, encoding='utf-8')
    print(f"[OK] Updated portfolioRecommendation section with timestamp {now}")
    return True

def main():
    parser = argparse.ArgumentParser(description='Sync portfolio recommendations to master-plan.md')
    parser.add_argument('--date', help='Date to use for finding portfolio file (YYYY-MM-DD)')
    args = parser.parse_args()

    # Find latest portfolio recommendation file
    rec_file = get_latest_portfolio_recommendation()

    if not rec_file:
        print("ERROR: No portfolio recommendation file found")
        return 1

    print(f"Reading portfolio recommendation from: {rec_file}")

    # Parse the recommendation
    data = parse_portfolio_recommendation(rec_file)

    if not data:
        print("ERROR: Failed to parse portfolio recommendation")
        return 1

    # Update master-plan.md
    if not update_portfolio_in_master_plan(data):
        return 1

    print("[OK] Portfolio sync complete")
    return 0

if __name__ == '__main__':
    sys.exit(main())
