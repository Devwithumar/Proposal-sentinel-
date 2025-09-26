import argparse
import json
from .analyzer import ProposalAnalyzer

def main():
    p = argparse.ArgumentParser(prog='proposal-sentinel', description='Analyze a proposal text for red-flags and strengths.')
    p.add_argument('input', help='Path to proposal text file')
    p.add_argument('--out', '-o', help='Output JSON path', default='report.json')
    p.add_argument('--txt', help='Also write human-readable report to this file', default='report.txt')
    args = p.parse_args()
    with open(args.input, 'r', encoding='utf-8') as f:
        text = f.read()
    analyzer = ProposalAnalyzer()
    report = analyzer.analyze(text)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    with open(args.txt, 'w', encoding='utf-8') as f:
        f.write(analyzer.render_human_report(report))
    print(f'Report written to {args.out} and {args.txt}')

if __name__ == '__main__':
    main()
