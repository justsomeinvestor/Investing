#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wingman Dash - Dashboard Update Workflow
==========================================

Updates research dashboard and master plan using existing data from wingman recon + prep.

CRITICAL: Does NOT re-fetch data or recalculate signals.
Uses only existing research summaries + signal data.

Usage:
    python scripts/automation/wingman_dash.py 2025-10-23

Workflow:
    1. Verify timestamp freshness (check which sections are stale)
    2. Run automated sync scripts (Social, Technicals, News, Daily Planner)
    3. Update master-plan.md with fresh timestamps
    4. Identify stale AI-driven sections
    5. Generate AI update prompts for stale sections
    6. Run final verification (all sections must be current)

Output:
    - Updated master-plan.md (100% current timestamps)
    - Updated research-dashboard.html (fresh data)
    - Timestamp verification report (JSON for AI review)
    - List of stale sections needing AI updates

Input (from wingman prep):
    - Research/Technicals/*/2025-10-23_*_Summary.md (7 summaries)
    - Research/X/2025-10-23_X_*_Summary.md (4 X summaries)
    - Research/2025-10-23_*_Overview.md (category overviews)
    - Research/.cache/2025-10-23_*_Overview.md (final overviews)
    - Research/.cache/signals_2025-10-23.json (signal score)
"""

import sys
import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


class WingmanDash:
    """Dashboard update workflow coordinator"""

    def __init__(self, date_str: str):
        self.date = datetime.strptime(date_str, "%Y-%m-%d")
        self.date_str = date_str
        self.date_display = self.date.strftime('%B %d, %Y')

        # Paths
        self.repo_root = Path(__file__).resolve().parents[2]
        self.master_plan_file = self.repo_root / "master-plan" / "master-plan.md"
        self.html_dashboard_file = self.repo_root / "master-plan" / "research-dashboard.html"
        self.cache_dir = self.repo_root / "Research" / ".cache"
        self.research_dir = self.repo_root / "Research"

        # Script paths
        self.verify_timestamps_script = self.repo_root / "scripts" / "utilities" / "verify_timestamps.py"
        self.update_master_plan_script = self.repo_root / "scripts" / "automation" / "update_master_plan.py"
        self.verify_consistency_script = self.repo_root / "scripts" / "utilities" / "verify_consistency.py"

        # Sync scripts
        self.sync_scripts = [
            ("social_tab_sync", self.repo_root / "scripts" / "utilities" / "sync_social_tab.py"),
            ("x_sentiment_update", self.repo_root / "scripts" / "automation" / "update_x_sentiment_tab.py"),
            ("technicals_tab_sync", self.repo_root / "scripts" / "utilities" / "sync_technicals_tab.py"),
            ("news_tab_sync", self.repo_root / "scripts" / "utilities" / "sync_news_tab.py"),
            ("daily_planner_sync", self.repo_root / "scripts" / "utilities" / "sync_daily_planner.py"),
            ("markets_intelligence_update", self.repo_root / "scripts" / "automation" / "update_markets_intelligence.py"),
            ("quick_actions_sync", self.repo_root / "scripts" / "utilities" / "sync_quick_actions.py"),
            ("risk_items_sync", self.repo_root / "scripts" / "utilities" / "sync_risk_items.py"),
            ("provider_consensus_sync", self.repo_root / "scripts" / "utilities" / "sync_provider_consensus.py"),
            ("portfolio_recommendation_sync", self.repo_root / "scripts" / "utilities" / "sync_portfolio_recommendation.py"),
        ]

        # Results tracking
        self.results = {}
        self.timestamp_report = {}
        self.stale_sections = []
        self.mi_sources = []  # Markets Intelligence research sources

    def run_all(self):
        """Execute complete wingman dash workflow"""
        print("\n" + "=" * 70)
        print("🎯 WINGMAN DASH - DASHBOARD UPDATE")
        print("=" * 70)
        print(f"Date: {self.date_str}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        try:
            # Phase 1: Verify timestamp freshness
            self.run_timestamp_verification()

            # Phase 2: Run automated sync scripts
            self.run_sync_scripts()

            # Phase 3: Update master plan
            self.run_update_master_plan()

            # Phase 4: Final verification
            self.run_final_verification()

            # Phase 5: Generate AI update prompts
            self.generate_ai_prompts()

            # Report results
            self.report_completion()

        except Exception as e:
            print(f"\n[ERROR] Workflow failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    def run_timestamp_verification(self):
        """Phase 1: Check timestamp freshness"""
        print("\n" + "=" * 70)
        print("[PHASE 1] TIMESTAMP VERIFICATION")
        print("=" * 70)

        if not self.verify_timestamps_script.exists():
            print(f"[WARN] Verification script not found: {self.verify_timestamps_script}")
            print("   Continuing without timestamp verification...")
            return

        try:
            cmd = [
                sys.executable,
                str(self.verify_timestamps_script),
                "--date", self.date_str,
                "--json"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.repo_root))

            # Parse JSON output
            try:
                self.timestamp_report = json.loads(result.stdout)
                self.results['timestamp_verify'] = self.timestamp_report

                print(f"\n[RESULT] Timestamp Health: {self.timestamp_report.get('health_percentage', 0):.1f}%")
                print(f"   Current: {self.timestamp_report.get('current_count', 0)}")
                print(f"   Stale: {self.timestamp_report.get('stale_count', 0)}")
                print(f"   Very Stale: {self.timestamp_report.get('very_stale_count', 0)}")
                print(f"   Missing: {self.timestamp_report.get('missing_count', 0)}")

                # Extract stale sections for later AI update
                self.stale_sections = (
                    self.timestamp_report.get('very_stale_count', []) +
                    self.timestamp_report.get('stale_count', [])
                )

                if result.returncode == 2:
                    print("\n[WARN] STALE DATA DETECTED - Will attempt to update stale sections")

            except json.JSONDecodeError:
                print(f"[ERROR] Failed to parse timestamp JSON")
                print(f"stdout: {result.stdout}")
                print(f"stderr: {result.stderr}")

        except Exception as e:
            print(f"[ERROR] Timestamp verification failed: {e}")
            print("   Continuing with workflow...")

    def run_sync_scripts(self):
        """Phase 2: Run automated sync scripts"""
        print("\n" + "=" * 70)
        print("[PHASE 2] AUTOMATED SYNC SCRIPTS")
        print("=" * 70)

        for script_name, script_path in self.sync_scripts:
            if not script_path.exists():
                print(f"[SKIP] {script_name}: Script not found")
                continue

            print(f"\n[RUNNING] {script_name}...")
            try:
                cmd = [sys.executable, str(script_path), self.date_str]
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.repo_root))

                if result.returncode == 0:
                    print(f"   ✅ {script_name} completed")
                    self.results[script_name] = 'success'
                else:
                    print(f"   [WARN] {script_name} returned code {result.returncode}")
                    self.results[script_name] = f'warning:{result.returncode}'
                    if result.stderr:
                        print(f"   stderr: {result.stderr[:200]}")

            except Exception as e:
                print(f"   [WARN] {script_name} failed: {e}")
                self.results[script_name] = f'error:{str(e)[:100]}'

    def run_update_master_plan(self):
        """Phase 3: Update master plan"""
        print("\n" + "=" * 70)
        print("[PHASE 3] UPDATE MASTER PLAN")
        print("=" * 70)

        if not self.update_master_plan_script.exists():
            print(f"[WARN] Update script not found: {self.update_master_plan_script}")
            print("   Skipping master plan update...")
            return

        try:
            cmd = [sys.executable, str(self.update_master_plan_script), self.date_str]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.repo_root))

            if result.returncode == 0:
                print("[OK] Master plan updated")
                self.results['master_plan_update'] = 'success'
            else:
                print(f"[WARN] Master plan update returned code {result.returncode}")
                self.results['master_plan_update'] = f'warning:{result.returncode}'
                if result.stderr:
                    print(f"   stderr: {result.stderr[:200]}")

        except Exception as e:
            print(f"[ERROR] Master plan update failed: {e}")
            self.results['master_plan_update'] = f'error:{str(e)[:100]}'

    def run_final_verification(self):
        """Phase 4: Final verification"""
        print("\n" + "=" * 70)
        print("[PHASE 4] FINAL VERIFICATION")
        print("=" * 70)

        # Re-run timestamp verification
        if self.verify_timestamps_script.exists():
            try:
                cmd = [
                    sys.executable,
                    str(self.verify_timestamps_script),
                    "--date", self.date_str,
                    "--json"
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.repo_root))
                final_report = json.loads(result.stdout)

                health = final_report.get('health_percentage', 0)
                print(f"\n[RESULT] Final Timestamp Health: {health:.1f}%")
                print(f"   Current: {final_report.get('current_count', 0)}")
                print(f"   Stale: {final_report.get('stale_count', 0)}")
                print(f"   Missing: {final_report.get('missing_count', 0)}")

                if health == 100:
                    print("\n✅ ALL SECTIONS CURRENT - Dashboard ready for trading")
                    self.results['final_verify'] = 'success'
                else:
                    print(f"\n⚠️  Some sections still stale (health: {health}%)")
                    print("   AI updates needed for stale sections")
                    self.results['final_verify'] = f'warning:health_{health}'

            except Exception as e:
                print(f"[ERROR] Final verification failed: {e}")
                self.results['final_verify'] = f'error:{str(e)[:100]}'

    def generate_ai_prompts(self):
        """Phase 5: CLAUDE AI MUST READ RESEARCH AND UPDATE INTERPRETATIONS - NOT OPTIONAL"""
        print("\n" + "=" * 70)
        print("[PHASE 5] 🤖 CLAUDE AI: READ RESEARCH AND UPDATE INTERPRETATIONS")
        print("=" * 70)
        print()
        print("⚠️  CRITICAL: This phase CANNOT be skipped or automated.")
        print("    Claude AI MUST:")
        print("    1. Read all research source files")
        print("    2. Synthesize insights into AI-driven interpretations")
        print("    3. Update master-plan.md sections with fresh analysis")
        print("    4. Update timestamps AFTER content is current")
        print()
        print("    Purpose: Dashboard shows HUMAN-READABLE AI insights synthesizing")
        print("    the research, NOT raw data. This is the entire value proposition")
        print("    of wingman dash - data collection (recon) → analysis (prep) → ")
        print("    AI-driven visualization (dash).")
        print()

        # Identify stale AI-driven sections from timestamp report
        # NOTE: verify_timestamps.py outputs keys named 'stale_sections' for VERY_STALE
        # and 'aging_sections' for STALED-YESTERDAY. Be tolerant to both spellings.
        very_stale_from_report = (
            self.timestamp_report.get('very_stale_sections')
            or self.timestamp_report.get('stale_sections')
            or []
        )
        aging_ai_sections = self.timestamp_report.get('aging_sections', [])

        ai_section_keywords = ['aiInterpretation', 'interpretation', 'summary']
        sections_needing_update = [
            s for s in (very_stale_from_report + aging_ai_sections)
            if any(kw in s for kw in ai_section_keywords)
        ]

        # Also ensure Daily Planner Key Levels get an explicit AI prompt when their timestamp is stale
        kl_timestamp_field = 'dashboard.dailyPlanner.keyLevelsUpdated'
        kl_needs_update = any(
            kl_timestamp_field in s for s in (very_stale_from_report + aging_ai_sections + self.timestamp_report.get('missing_sections', []))
        )

        if not sections_needing_update:
            print("\n✅ No AI interpretation sections require updates")
            print("   All aiInterpretation sections are current")
            self.results['ai_updates'] = 'none_needed'
            return

        print(f"\n[REQUIRED] {len(sections_needing_update)} AI interpretation sections require Claude AI updates:\n")

        # Map section paths to research data
        section_mappings = {
            'dashboard.dailyPlanner.aiInterpretation': [
                'Research/.cache/{date}_key_themes.md',
                'Research/.cache/{date}_Market_Sentiment_Overview.md',
            ],
            'tabs.portfolio.aiInterpretation': [
                'Research/.cache/signals_{date}.json',
                'Journal/account_state.json',
                'Journal/positions.json'
            ],
            'tabs.markets.aiInterpretation': [
                'Research/.cache/{date}_Market_Sentiment_Overview.md',
                'Research/{date}_Technical_Category_Overview.md',
            ],
            'tabs.news_catalysts.aiInterpretation': [
                'Research/{date}_RSS_Category_Overview.md',
                'Research/.cache/{date}_key_themes.md',
            ],
            'tabs.xsentiment.aiInterpretation': [
                'Research/{date}_X_Category_Overview.md',
                'Research/X/{date}_X_Crypto_Summary.md',
                'Research/X/{date}_X_Macro_Summary.md',
            ],
            'tabs.technicals.aiInterpretation': [
                'Research/{date}_Technical_Category_Overview.md',
                'Research/Technicals/*_Summary.md',
            ],
            # Daily Planner Key Levels – curated by AI from cross-source context
            'dashboard.dailyPlanner.keyLevels': [
                'Research/.cache/{date}_Market_Sentiment_Overview.md',
                'Research/.cache/signals_{date}.json',
                'Research/.cache/{date}_options_data.json',
                'Research/.cache/{date}_market_data.json',
            ],
            # Daily Planner Recommendation – AI-generated tactical guidance (NEW)
            'dashboard.dailyPlanner.recommendation': [
                'Research/.cache/{date}_Market_Sentiment_Overview.md',
                'Research/.cache/signals_{date}.json',
            ],
            # Daily Planner Action Checklist – AI-generated tactical actions (NEW)
            'dashboard.dailyPlanner.actionChecklist': [
                'Research/.cache/{date}_Market_Sentiment_Overview.md',
                'Research/.cache/signals_{date}.json',
            ],
        }

        ai_prompts = []

        for section in sections_needing_update:
            research_sources = next(
                (section_mappings[key] for key in section_mappings if key in section),
                []
            )
            # Replace {date} placeholder with actual date
            research_sources = [src.replace('{date}', self.date_str) for src in research_sources]

            prompt = {
                'section': section,
                'status': 'stale',
                'research_sources': research_sources,
                'action': f'READ research sources → SYNTHESIZE insights → UPDATE {section} with fresh AI interpretation → UPDATE timestamp',
                'output_field': f'{section}.updatedAt',
            }

            ai_prompts.append(prompt)

            print(f"   📌 {section}")
            print(f"      ➜ Research Sources:")
            for source in research_sources[:2]:
                print(f"         • {source}")
            if len(research_sources) > 2:
                print(f"         ... and {len(research_sources) - 2} more")
            print()

        # If Key Levels need update, add a dedicated prompt with schema instructions
        if kl_needs_update:
            kl_sources = section_mappings['dashboard.dailyPlanner.keyLevels']
            kl_sources = [src.replace('{date}', self.date_str) for src in kl_sources]
            kl_prompt = {
                'section': 'dashboard.dailyPlanner.keyLevels',
                'status': 'stale',
                'research_sources': kl_sources,
                'action': (
                    'READ research sources  SYNTHESIZE confluence across SPY, QQQ, BTC (and others as applicable)  '
                    'OUTPUT YAML list of objects with fields: asset, entry/support, stop/breakdown, target/resistance, optional rationale  '
                    'UPDATE dashboard.dailyPlanner.keyLevels and UPDATE dashboard.dailyPlanner.keyLevelsUpdated (ISO 8601)'
                ),
                'output_field': 'dashboard.dailyPlanner.keyLevelsUpdated',
            }
            ai_prompts.append(kl_prompt)
            print("    Daily Planner Key Levels will be curated by AI (schema: asset, entry, stop, target, rationale)")

        # Markets Intelligence requires RICH AI narrative - dedicated prompt with detailed instructions
        self.mi_sources = section_mappings.get('tabs.markets.aiInterpretation', [])
        self.mi_sources = [src.replace('{date}', self.date_str) for src in self.mi_sources]
        mi_prompt = {
            'section': 'tabs.markets.aiInterpretation',
            'status': 'markets_intelligence_narrative',
            'research_sources': self.mi_sources,
            'fields': {
                'summary': 'Rich unified market intelligence narrative (2-3 paragraphs synthesizing Macro, Crypto, Tech)',
                'keyInsight': 'The ONE critical insight that dominates today\'s market (1 sentence)',
                'action': 'Specific actionable guidance with levels, catalysts, and positioning (2-3 sentences)'
            },
            'action': (
                'READ Research/.cache/{date}_Market_Sentiment_Overview.md and Research/{date}_Technical_Category_Overview.md  '
                'SYNTHESIZE rich AI narrative covering: Macro Environment + Crypto Markets + Tech Sector  '
                'GENERATE THREE sections: summary (unified narrative), keyInsight (critical takeaway), action (specific guidance)  '
                'UPDATE tabs.markets.aiInterpretation.summary, keyInsight, action in master-plan.md  '
                'UPDATE tabs.markets.aiInterpretation.updatedAt with current ISO 8601 timestamp'
            ).replace('{date}', self.date_str),
            'output_fields': [
                'tabs.markets.aiInterpretation.summary',
                'tabs.markets.aiInterpretation.keyInsight',
                'tabs.markets.aiInterpretation.action',
                'tabs.markets.aiInterpretation.updatedAt'
            ],
            'writing_guidelines': {
                'tone': 'Professional Bloomberg-style analysis with specific data points and levels',
                'structure': 'Market Structure → Technical Inflection Points → Structural Themes → Consensus Action',
                'specificity': 'Include actual prices, percentages, support/resistance levels, catalysts',
                'relevance': 'Focus on Macro environment, Crypto markets, Tech sector dynamics',
                'character_limits': {
                    'summary': '≤600 characters (concise market context)',
                    'keyInsight': '≤600 characters (critical single insight)',
                    'action': '≤600 characters (specific actionable guidance)'
                }
            }
        }
        ai_prompts.append(mi_prompt)
        print("    Markets Intelligence will receive RICH AI narrative (summary + keyInsight + action fields)")

        # Daily Planner Recommendation – AI-generated tactical guidance (NEW)
        dp_rec_sources = [
            f'Research/.cache/{self.date_str}_Market_Sentiment_Overview.md',
            f'Research/.cache/signals_{self.date_str}.json',
        ]
        dp_rec_prompt = {
            'section': 'dashboard.dailyPlanner.recommendation',
            'status': 'tactical_guidance',
            'research_sources': dp_rec_sources,
            'fields': {
                'recommendation': 'Concise tactical summary (signal tier + market context + positioning guidance)',
            },
            'action': (
                'READ Market_Sentiment_Overview.md and signals json  '
                'SYNTHESIZE: signal tier (WEAK/MODERATE/STRONG/EXTREME) + key market theme + tactical implication  '
                'GENERATE: "[TIER] tier (XX.XX/100). [1-2 sentence context]. [1-2 sentence guidance]."  '
                'UPDATE dashboard.dailyPlanner.recommendation in master-plan.md'
            ),
            'output_field': 'dashboard.dailyPlanner.recommendation',
            'writing_guidelines': {
                'format': '[TIER] tier (score/100). [Market context]. [Positioning guidance].',
                'tone': 'Professional, concise, actionable',
                'example': 'MODERATE tier (63.22/100). Post-CPI consolidation continues. Selective risk deployment appropriate with quality names showing strong technicals. Market breadth improving but still fragile—maintain hedges for volatility spikes.',
                'character_limit': '≤400 characters'
            }
        }
        ai_prompts.append(dp_rec_prompt)
        print("    Daily Planner Recommendation will receive tactical guidance (tier + context + action)")

        # Daily Planner Action Checklist – AI-generated tactical actions (NEW)
        dp_checklist_prompt = {
            'section': 'dashboard.dailyPlanner.actionChecklist',
            'status': 'tactical_actions',
            'research_sources': dp_rec_sources,
            'fields': {
                'actionChecklist': 'YAML list with priority-tagged actions based on signal + market conditions',
            },
            'action': (
                'READ Market_Sentiment_Overview.md and signals json  '
                'IDENTIFY: 2-4 tactical actions based on signal tier + market structure + key risks  '
                'GENERATE: List of {text, priority} objects where priority = high|critical|monitor  '
                'UPDATE dashboard.dailyPlanner.actionChecklist in master-plan.md'
            ),
            'output_field': 'dashboard.dailyPlanner.actionChecklist',
            'schema': {
                'format': 'YAML list of objects: {text: string, priority: "high"|"critical"|"monitor"}',
                'high': 'Important actions aligned with signal tier (25-50% portfolio impact)',
                'critical': 'Must-do defensive/offensive actions (>50% portfolio impact)',
                'monitor': 'Watch-list items, key levels to observe (no immediate action)',
                'example': [
                    {'text': 'Selective risk deployment to quality names with strong technicals.', 'priority': 'high'},
                    {'text': 'Maintain hedges through week ahead given lingering volatility risks.', 'priority': 'critical'},
                    {'text': 'Monitor key support levels: SPX 6679, BTC $111.9K.', 'priority': 'monitor'}
                ]
            }
        }
        ai_prompts.append(dp_checklist_prompt)
        print("    Daily Planner Action Checklist will receive tactical actions (high/critical/monitor)")

        # Save AI prompts for reference
        prompts_file = self.cache_dir / f"{self.date_str}_ai_update_prompts.json"
        with open(prompts_file, 'w') as f:
            json.dump(ai_prompts, f, indent=2)

        print(f"\n🔍 Detailed prompts saved: {prompts_file}")
        print()
        print("📋 WORKFLOW EXPECTATION:")
        print("   ✅ Phase 1-4: Automated (timestamp verification, sync scripts, master plan update, final verification)")
        print("   ⚠️  Phase 5: CLAUDE AI PERFORMS MANUALLY - Read all research and update interpretations")
        print()
        print("🎯 SUCCESS CRITERIA:")
        print("   • Each aiInterpretation section updated with fresh analysis from TODAY's research")
        print("   • Timestamps updated to current datetime in ISO 8601 format")
        print("   • Next verification run shows ALL sections current (100% health)")
        print()
        print("💡 EXAMPLES OF WHAT CLAUDE SHOULD SYNTHESIZE:")
        print("   • Dashboard.dailyPlanner: Today's trading context based on signal tier + catalysts (≤600 chars per field)")
        print("   • Portfolio: Risk positioning recommendation based on signals + structural themes (≤600 chars per field)")
        print("   • Markets Intelligence: RICH NARRATIVE with Market Structure → Technical Points → Structural Themes")
        print("     - summary: Concise market context (≤600 chars)")
        print("     - keyInsight: Critical single insight (≤600 chars)")
        print("     - action: Specific guidance with levels, catalysts, position sizing (≤600 chars)")
        print("     - sentiment: cautiously bullish/neutral/bearish")
        print("     - confidence: low/medium/medium-high/high")
        print("   • News: Critical catalysts + earnings themes + quantum/Bitcoin structural stories (≤600 chars per field)")
        print()

        self.results['ai_updates'] = f'{len(ai_prompts)}_sections_require_claude_ai'

    def report_completion(self):
        """Report workflow completion"""
        print("\n" + "=" * 70)
        print("📊 WINGMAN DASH COMPLETION REPORT")
        print("=" * 70)

        # Summary
        health = self.timestamp_report.get('health_percentage', 0)
        timestamp_status = "✅ CURRENT" if health == 100 else f"⚠️  AGING ({health:.0f}%)"

        print(f"\n[TIMESTAMP HEALTH] {timestamp_status}")
        print(f"   Current: {self.timestamp_report.get('current_count', 0)}")
        print(f"   Stale: {self.timestamp_report.get('stale_count', 0)}")
        print(f"   Missing: {self.timestamp_report.get('missing_count', 0)}")

        print(f"\n[SYNC SCRIPTS]")
        for script_name, status in self.results.items():
            if 'sync' in script_name or 'update' in script_name:
                print(f"   {script_name}: {status}")

        print(f"\n[AI UPDATES REQUIRED]")
        ai_status = self.results.get('ai_updates', 'none_needed')
        if 'require_claude_ai' in str(ai_status):
            print(f"   ⚠️  {ai_status}")
            print(f"   ACTION: Claude AI must read research sources and update interpretations")
            print(f"   This is MANDATORY for wingman dash completion - not optional")
        else:
            print(f"   {ai_status}")

        # Final status
        print("\n" + "=" * 70)
        if health >= 90 and 'none_needed' in str(ai_status):
            print("✅ DASHBOARD UPDATE COMPLETE")
            print(f"   Health: {health:.1f}%")
            print("   Status: Ready for trading operations")
        else:
            print("⚠️  DASHBOARD PARTIALLY UPDATED")
            print(f"   Health: {health:.1f}%")
            if 'require_claude_ai' in str(ai_status):
                print(f"   Status: AWAITING CLAUDE AI INTERPRETATION UPDATES")
                print(f"")
                print(f"   CRITICAL: Markets Intelligence Tab Requires RICH AI Narrative")
                print(f"   ======================================================")
                print(f"   Markets Intelligence tab needs THREE fields updated:")
                print(f"")
                print(f"   1. tabs.markets.aiInterpretation.summary (≤600 chars)")
                print(f"      → Concise market context synthesizing Macro + Crypto + Tech")
                print(f"      → Include: Market Structure, Technical Inflection Points, Structural Themes")
                print(f"      → Be scannable and specific (prices, levels, catalysts)")
                print(f"")
                print(f"   2. tabs.markets.aiInterpretation.keyInsight (≤600 chars)")
                print(f"      → The ONE critical insight dominating today's market")
                print(f"      → Most important takeaway for traders - be specific")
                print(f"")
                print(f"   3. tabs.markets.aiInterpretation.action (≤600 chars)")
                print(f"      → Specific actionable guidance with levels and catalysts")
                print(f"      → Include: position sizing, risk management, conditional logic")
                print(f"")
                print(f"   4. tabs.markets.aiInterpretation.sentiment")
                print(f"      → One of: cautiously bullish | neutral | cautiously bearish | bullish | bearish")
                print(f"")
                print(f"   5. tabs.markets.aiInterpretation.confidence")
                print(f"      → One of: low | medium | medium-high | high")
                print(f"")
                print(f"   6. tabs.markets.aiInterpretation.updatedAt = current ISO 8601 timestamp")
                print(f"")
                print(f"   Research Sources:")
                for src in self.mi_sources[:3]:
                    print(f"   • {src}")
                if len(self.mi_sources) > 3:
                    print(f"   ... and {len(self.mi_sources) - 3} more")
                print(f"")
                print(f"   Writing Style: Professional Bloomberg-style with specific data/levels")
                print(f"")
                print(f"   Next Steps:")
                print(f"   1. Claude AI reads all research sources identified in Phase 5")
                print(f"   2. Synthesize insights and update ALL aiInterpretation sections (Daily Planner, Markets Intelligence, etc.)")
                print(f"   3. Update timestamps to confirm completion (ISO 8601 format)")
                print(f"   4. Dashboard will reflect fresh AI-driven analysis")
            else:
                print(f"   Status: Awaiting completion")

        print("=" * 70 + "\n")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python scripts/automation/wingman_dash.py YYYY-MM-DD")
        print("Example: python scripts/automation/wingman_dash.py 2025-10-23")
        sys.exit(1)

    date_str = sys.argv[1]

    # Validate date format
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print(f"❌ Invalid date format: {date_str}")
        print("   Expected format: YYYY-MM-DD")
        sys.exit(1)

    # Execute workflow
    dash = WingmanDash(date_str)
    dash.run_all()


if __name__ == "__main__":
    main()
