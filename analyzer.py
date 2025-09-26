import re
import json

# Lightweight, explainable heuristics for proposal analysis.
# No external dependencies.

DEFAULT_FLAGS = [
    # id, title, patterns (list), severity
    ('eval_missing', 'Missing evaluation metrics', ['measure success', 'evaluate', 'evaluation', 'success will be'], 'high'),
    ('objectives_unclear', 'Unclear / non-measurable objectives', ['objective', 'aim to', 'we aim to', 'we will'], 'high'),
    ('ethics_personal_data', 'Potential personal / sensitive data collection', ['income', 'name', 'address', 'personal data', 'survey.*income', 'phone'], 'medium'),
    ('budget_vague', 'Vague budget phrases', ['misc', 'other costs', 'sundry', 'unspecified', 'miscellaneous', 'to be determined'], 'medium'),
    ('novelty_unclear', 'Novelty / contribution unclear', ['well[- ]studied', 'extensive literature', 'has been studied', 'many studies', 'however existing'], 'medium'),
    ('impact_weak', 'Impact statement too short or generic', [], 'low')
]

class ProposalAnalyzer:
    def __init__(self):
        # compile regex patterns
        self.flag_specs = []
        for fid, title, pats, sev in DEFAULT_FLAGS:
            compiled = [re.compile(pat, re.IGNORECASE) for pat in pats]
            self.flag_specs.append({'id': fid, 'title': title, 'patterns': compiled, 'severity': sev})

    def _sentences(self, text):
        # very simple sentence splitter
        s = re.split(r'(?<=[.!?])\s+', text.strip())
        return [ss.strip() for ss in s if ss.strip()]

    def _find_excerpt(self, text, pattern):
        # return first matching sentence containing pattern
        for sent in self._sentences(text):
            if pattern.search(sent):
                return sent
        return None

    def analyze(self, text):
        report = {'flags': [], 'strengths': [], 'meta': {}}
        sentences = self._sentences(text)
        # check for explicit evaluation keywords; if none found, add eval_missing
        eval_patterns = [re.compile(p, re.IGNORECASE) for p in ['measure', 'evaluation', 'metric', 'baseline', 'outcome', 'success']]
        if not any(p.search(text) for p in eval_patterns):
            # pick first 2 sentences as context for the flag
            excerpt = ' '.join(sentences[:2]) if sentences else ''
            report['flags'].append({
                'id': 'eval_missing',
                'title': 'Missing evaluation metrics',
                'severity': 'high',
                'excerpt': excerpt,
                'explanation': 'No clear evaluation, metrics, or baseline described. Define measurable success criteria (metric, baseline, timeframe).',
                'suggestion': 'Add explicit evaluation metrics: e.g., "increase yield by 10% within 12 months measured by randomized field trials against baseline."'
            })
        # run through flag_specs patterns
        for spec in self.flag_specs:
            if spec['id'] == 'eval_missing':
                continue
            found = False
            excerpt = None
            for pat in spec['patterns']:
                match = pat.search(text)
                if match:
                    excerpt = self._find_excerpt(text, pat) or match.group(0)
                    found = True
                    break
            if spec['id'] == 'impact_weak':
                # measure impact strength: short impact statements with generic words => flag
                impact_keywords = ['impact', 'benefit', 'contribute', 'improve', 'reduce']
                impact_sents = [s for s in sentences if any(k in s.lower() for k in impact_keywords)]
                if not impact_sents:
                    excerpt = 'No explicit impact sentence found.'
                    found = True
                else:
                    # if the impact sentence is very short (<6 words) or generic, flag
                    for s in impact_sents:
                        if len(s.split()) < 6 or any(w in s.lower() for w in ['important', 'significant', 'meaningful']) and len(s.split())<12:
                            excerpt = s
                            found = True
                            break
            if found:
                report['flags'].append({
                    'id': spec['id'],
                    'title': spec['title'],
                    'severity': spec['severity'],
                    'excerpt': excerpt or '',
                    'explanation': f'Possible issue: {spec["title"]}. See excerpt.',
                    'suggestion': self._suggestion_for(spec['id'])
                })
        # strengths: detect explicit, good impact lines
        strengths = []
        for s in sentences:
            if len(s.split()) > 6 and any(k in s.lower() for k in ['food security', 'sustainable', 'reduce water', 'climate resilience', 'novel approach', 'innovative']):
                strengths.append({'title': 'Clear societal impact', 'excerpt': s, 'note': 'Impact sentence is specific and relevant.'})
        if strengths:
            report['strengths'] = strengths
        # meta: title guess (first line) and word count
        report['meta']['word_count'] = len(text.split())
        report['meta']['title_guess'] = sentences[0] if sentences else ''
        return report

    def _suggestion_for(self, fid):
        # small canned suggestions
        mapping = {
            'objectives_unclear': 'Make objectives specific and measurable: use verbs + metrics + timeline (e.g., "By month 12, increase X by Y% measured by Z").',
            'ethics_personal_data': 'If collecting personal data, add consent procedures, anonymization, and data storage/retention details.',
            'budget_vague': 'Replace vague phrases with line items: unit cost, quantity, justification for each cost.',
            'novelty_unclear': 'Clarify the unique contribution relative to cited literature; say how this differs or improves upon prior work.',
            'impact_weak': 'Expand the impact statement with concrete beneficiaries and measurable outcomes.'
        }
        return mapping.get(fid, 'Please clarify this section with specifics.')

    def render_human_report(self, report):
        lines = []
        lines.append('Proposal Sentinel Report')
        lines.append('========================\n')
        lines.append(f"Title guess: {report.get('meta',{{}}).get('title_guess','(none)')}\n")
        lines.append(f"Word count: {report.get('meta',{{}}).get('word_count',0)}\n")
        lines.append('Flags:')
        if not report.get('flags'):
            lines.append(' - No issues detected.')
        else:
            for f in report['flags']:
                lines.append(f" - [{f['severity'].upper()}] {f['title']}")
                lines.append(f"   Excerpt: {f.get('excerpt','')}")
                lines.append(f"   Suggestion: {f.get('suggestion','')}")
                lines.append('')
        if report.get('strengths'):
            lines.append('\nStrengths:')
            for s in report['strengths']:
                lines.append(f" - {s['title']}: {s['excerpt']}")
        return '\n'.join(lines)
