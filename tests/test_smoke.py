import json
from pathlib import Path


REQUIRED_SUBMISSION_FILES = ('config.json', 'paper.md', 'protocol.md', 'index.html')


def test_repository_smoke():
    root = Path(__file__).resolve().parents[1]
    assert root.exists()

    submission = root / 'e156-submission'
    if submission.is_dir():
        for name in REQUIRED_SUBMISSION_FILES:
            assert (submission / name).exists(), name

        config = json.loads((submission / 'config.json').read_text(encoding='utf-8'))
        body = config.get('body', '')
        assert len(body.split()) == 156

        sentences = config.get('sentences', [])
        assert len(sentences) == 7
        assert all((entry.get('text') if isinstance(entry, dict) else str(entry)).strip() for entry in sentences)
        assert config.get('notes', {}).get('code')
        return

    candidates = []
    for base in [root, root / 'src', root / 'app', root / 'scripts']:
        if not base.is_dir():
            continue
        for pattern in ('*.py', '*.R', '*.html', '*.js', '*.ts'):
            candidates.extend(base.glob(pattern))
    assert candidates


def test_static_app_shell_contract():
    root = Path(__file__).resolve().parents[1]
    html = (root / 'index.html').read_text(encoding='utf-8')

    assert '<title>Kanban Lab</title>' in html
    assert 'Persistent drag-and-drop kanban board' in html
    assert 'localStorage' in html
    assert 'dragstart' in html
    assert 'Add Card' in html
    assert '{{' not in html
    assert 'C:\\' not in html
    assert 'D:\\' not in html
