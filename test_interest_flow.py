"""Regression checks for market boundaries, working routes and contact safety."""
import unittest
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
from test_launch_gating import build, HERE

SLUGS = ['', 'apply', 'managers', 'invitation-code', 'privacy', 'terms',
         'international', 'shop', 'uk', 'brazil', 'mexico']
PAGES = [(slug + '/' if slug else '') + 'index.html' for slug in SLUGS]


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.nodes = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))


class InterestFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages, _ = build(pages_to_read=PAGES, NETWORK_STATUS='live',
                             BACKSTAGE_APPROVAL='test approval', APPLY_LINK='')

    def test_us_application_and_international_boundaries(self):
        self.assertEqual(len(self.pages), 11)
        home = self.pages['index.html']
        self.assertIn('href="/apply/">Apply to join', home)
        self.assertNotIn('mailto:tiktok@dcassociatesgroup.com?subject=Creator', home)
        self.assertIn('href="https://www.tiktok.com/t/ZTAynpxHM/"', self.pages['apply/index.html'])
        for market in ['uk', 'brazil', 'mexico', 'shop', 'international']:
            source = self.pages[market + '/index.html']
            self.assertNotIn('operating as a TikTok LIVE Creator Network partner', source)
            self.assertNotIn('https://www.tiktok.com/t/ZTAynpxHM/', source)

    def test_localized_private_drafts_and_contact_destination(self):
        for slug, lang, country in [('uk', 'en', 'UK'), ('brazil', 'pt-BR', 'BR'), ('mexico', 'es-MX', 'MX')]:
            source = self.pages[slug + '/index.html']
            self.assertIn('<html lang="' + lang + '">', source)
            self.assertIn('value="' + country + '" selected', source)
            nodes = Document(source).nodes
            forms = [a for t, a in nodes if t == 'form']
            self.assertEqual(len(forms), 1)
            self.assertEqual(forms[0]['onsubmit'], 'return false')
            self.assertNotIn('action', forms[0])
            self.assertEqual(forms[0]['data-whatsapp'], '13053179940')
            self.assertFalse(any(a.get('type') == 'email' for t, a in nodes if t == 'input'))
            self.assertTrue(any('required' in a for t, a in nodes if a.get('id') == 'consent'))
            self.assertTrue(any('hidden' in a for t, a in nodes if 'data-review' in a))
            self.assertTrue(any('disabled' in a for t, a in nodes if 'data-prepare' in a))
            for tag, attrs in nodes:
                if tag == 'a' and attrs.get('href', '').startswith('https://wa.me/'):
                    self.assertEqual(urlparse(attrs['href']).path, '/13053179940')

    def test_internal_routes_anchors_and_unique_ids(self):
        for prefix in ['', '/sparked-live-site']:
            pages = self.pages if not prefix else build(pages_to_read=PAGES, BASE_PATH=prefix,
                    NETWORK_STATUS='live', BACKSTAGE_APPROVAL='test approval')[0]
            docs = {name: Document(source) for name, source in pages.items()}
            for name, doc in docs.items():
                ids = [a['id'] for _, a in doc.nodes if 'id' in a]
                self.assertEqual(len(ids), len(set(ids)), name)
                for tag, attrs in doc.nodes:
                    href = attrs.get('href', '')
                    if tag != 'a' or not href or urlparse(href).scheme:
                        continue
                    parsed = urlparse(href)
                    if parsed.path:
                        self.assertTrue(parsed.path.startswith(prefix + '/'), (name, href))
                        path = parsed.path[len(prefix):].lstrip('/')
                        target = path + 'index.html' if not path or path.endswith('/') else path
                    else:
                        target = name
                    if target.startswith('assets/'):
                        self.assertTrue((HERE / target).is_file(), (name, href))
                        continue
                    self.assertIn(target, docs, (name, href))
                    if parsed.fragment:
                        target_ids = [a.get('id') for _, a in docs[target].nodes]
                        self.assertIn(unquote(parsed.fragment), target_ids, (name, href))

    def test_operator_identity_and_no_stale_phone(self):
        for source in self.pages.values():
            self.assertIn('Derek Coleman &amp; Associates Inc., trading as Sparked Live Network', source)
            self.assertNotIn('856-448-4318', source)
            self.assertNotIn('267-343-9249', source)
            self.assertNotIn('Sparked Live Network Inc.', source)


if __name__ == '__main__':
    unittest.main()
