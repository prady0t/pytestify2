import pytest

from pytestify.fixes.raises import rewrite_raises


@pytest.mark.parametrize(
    'before, after', [
        ('self.assertRaises(Exc)', 'pytest.raises(Exc)'),
        ('with self.assertRaises(Exc): pass', 'with pytest.raises(Exc): pass'),
        (
            'with self.assertRaises(Exc) as e: pass',
            'with pytest.raises(Exc) as e: pass',
        ),
        ('self.assertWarns(Exc)', 'pytest.warns(Exc)'),
        ('with self.assertWarns(Exc): pass', 'with pytest.warns(Exc): pass'),
    ],
)
def test_rewrite_raises(before, after):
    imports = 'import pytest\n'
    assert rewrite_raises(imports + before) == imports + after


@pytest.mark.parametrize(
    'before, after', [
        (
            'self.assertRaises(Exception)',
            'import pytest\n'
            'pytest.raises(Exception)',
        ),
        (
            'import pytest\n'
            'self.assertRaises(Exception)',
            'import pytest\n'
            'pytest.raises(Exception)',
        ),
        (
            'import pytest as pt\n'
            'self.assertRaises(Exception)',
            'import pytest as pt\n'
            'pt.raises(Exception)',
        ),
        (
            'from __future__ import absolute_import\n'
            '\n'
            'self.assertRaises(Exception)',
            'from __future__ import absolute_import\n'
            '\n'
            'import pytest\n'
            'pytest.raises(Exception)',
        ),
    ],
)
def test_adds_import_when_necessary(before, after):
    assert rewrite_raises(before) == after


@pytest.mark.parametrize(
    'line', [
        '# self.assertRaises(SomeException):',
        '# self.assertWarns(SomeException):',
    ],
)
def test_doesnt_rewrite_raises(line):
    assert rewrite_raises(line) == line
