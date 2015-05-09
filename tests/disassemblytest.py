# -*- coding: utf-8 -*-
import os
import shutil
from lxml import etree
from xml.dom.minidom import parse
from xml.dom import Node

from skoolkittest import SkoolKitTestCase, SKOOLKIT_HOME

XHTML_XSD = os.path.join(SKOOLKIT_HOME, 'XSD', 'xhtml1-strict.xsd')

def _find_ids_and_hrefs(elements, doc_anchors, doc_hrefs):
    for node in elements:
        if node.nodeType == Node.ELEMENT_NODE:
            element_id = node.getAttribute('id')
            if element_id:
                doc_anchors.add(element_id)
            if node.tagName in ('a', 'link', 'img', 'script'):
                if node.tagName == 'a':
                    element_name = node.getAttribute('name')
                    if element_name:
                        doc_anchors.add(element_name)
                if node.tagName in ('a', 'link'):
                    element_href = node.getAttribute('href')
                    if element_href:
                        doc_hrefs.add(element_href)
                elif node.tagName in ('img', 'script'):
                    element_src = node.getAttribute('src')
                    if element_src:
                        doc_hrefs.add(element_src)
            _find_ids_and_hrefs(node.childNodes, doc_anchors, doc_hrefs)

def _read_files(root_dir):
    all_files = {} # filename -> (element ids and <a> names, hrefs and srcs)
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            fname = os.path.join(root, f)
            all_files[fname] = (set(), set())
            if f.endswith('.html'):
                doc = parse(fname)
                _find_ids_and_hrefs(doc.documentElement.childNodes, *all_files[fname])
    return all_files

def check_links(root_dir):
    missing_files = []
    missing_anchors = []
    all_files = _read_files(root_dir)
    linked = set()
    for fname in all_files:
        for href in all_files[fname][1]:
            if not href.startswith('http://'):
                if href.startswith('#'):
                    link_dest = fname + href
                else:
                    link_dest = os.path.normpath(os.path.join(os.path.dirname(fname), href))
                dest_fname, sep, anchor = link_dest.partition('#')
                linked.add(dest_fname)
                if dest_fname not in all_files:
                    missing_files.append((fname, link_dest))
                elif anchor and anchor not in all_files[dest_fname][0]:
                    missing_anchors.append((fname, link_dest))
    orphans = set()
    for fname in all_files:
        if fname not in linked:
            orphans.add(fname)
    return all_files, orphans, missing_files, missing_anchors

class DisassembliesTestCase(SkoolKitTestCase):
    def _write_skool(self, snapshot, ctl, org):
        if not os.path.isfile(snapshot):
            self.fail("{} not found".format(snapshot))
        os.environ['SKOOLKIT_HOME'] = SKOOLKIT_HOME
        options = '-c {}'.format(ctl)
        if org is not None:
            options += ' -o {}'.format(org)
        output, error = self.run_sna2skool('{} {}'.format(options, snapshot), out_lines=False)
        self.assertEqual(len(error), 0)
        return self.write_text_file(output)

class AsmTestCase(DisassembliesTestCase):
    def _test_asm(self, options, skool=None, snapshot=None, ctl=None, org=None, writer=None, clean=True):
        if not skool:
            skool = self._write_skool(snapshot, ctl, org)
        if writer:
            options += ' -W {}'.format(writer)
        output, stderr = self.run_skool2asm('{} {}'.format(options, skool), err_lines=True)
        if clean:
            self.assertTrue(stderr[0].startswith('Parsed {}'.format(skool)))
            self.assertEqual(len(stderr), 3 if writer else 2)
        else:
            self.assertTrue(any([line.startswith('Parsed {}'.format(skool)) for line in stderr]))
        self.assertTrue(stderr[-1].startswith('Wrote ASM to stdout'))

class CtlTestCase(DisassembliesTestCase):
    def _test_ctl(self, options, skool=None, snapshot=None, ctl=None, org=None):
        if not skool:
            skool = self._write_skool(snapshot, ctl, org)
        args = '{} {}'.format(options, skool)
        output, stderr = self.run_skool2ctl(args)
        self.assertEqual(stderr, '')

class HtmlTestCase(DisassembliesTestCase):
    def setUp(self):
        DisassembliesTestCase.setUp(self)
        self.odir = 'html-{0}'.format(os.getpid())
        self.tempdirs.append(self.odir)

    def _validate_xhtml(self):
        if os.path.isfile(XHTML_XSD):
            xmlschema_doc = etree.parse(XHTML_XSD)
            xmlschema = etree.XMLSchema(xmlschema_doc)
            for root, dirs, files in os.walk(self.odir):
                for fname in files:
                    if fname[-5:] == '.html':
                        htmlfile = os.path.join(root, fname)
                        try:
                            xhtml = etree.parse(htmlfile)
                        except etree.LxmlError as e:
                            self.fail('Error while parsing {}: {}'.format(htmlfile, e.message))
                        try:
                            xmlschema.assertValid(xhtml)
                        except etree.DocumentInvalid as e:
                            self.fail('Error while validating {}: {}'.format(htmlfile, e.message))

    def _check_links(self):
        all_files, orphans, missing_files, missing_anchors = check_links(self.odir)
        if orphans or missing_files or missing_anchors:
            error_msg = []
            if orphans:
                error_msg.append('Orphaned files: {}'.format(len(orphans)))
                for fname in orphans:
                    error_msg.append('  {}'.format(fname))
            if missing_files:
                error_msg.append('Links to non-existent files: {}'.format(len(missing_files)))
                for fname, link_dest in missing_files:
                    error_msg.append('  {} -> {}'.format(fname, link_dest))
            if missing_anchors:
                error_msg.append('Links to non-existent anchors: {}'.format(len(missing_anchors)))
                for fname, link_dest in missing_anchors:
                    error_msg.append('  {} -> {}'.format(fname, link_dest))
            self.fail('\n'.join(error_msg))

    def _test_html(self, options, skool=None, snapshot=None, ctl=None, org=None, output=None, writer=None, ref=None):
        if not skool:
            skool = self._write_skool(snapshot, ctl, org)
            options += ' -c Config/SkoolFile={}'.format(skool)
        if writer:
            options += ' -W {}'.format(writer)
        if not ref:
            ref = skool[:-5] + 'ref'
        shutil.rmtree(self.odir, True)
        stdout, error = self.run_skool2html('-d {} {} {}'.format(self.odir, options, ref))
        self.assertEqual(error, '')
        reps = {'odir': self.odir, 'SKOOLKIT_HOME': SKOOLKIT_HOME, 'skoolfile': skool, 'reffile': ref}
        self.assertEqual(output.format(**reps).split('\n'), stdout)
        self._validate_xhtml()
        self._check_links()

class SftTestCase(DisassembliesTestCase):
    def _test_sft(self, options, skool=None, snapshot=None, ctl=None, org=None):
        if not skool:
            skool = self._write_skool(snapshot, ctl, org)
        with open(skool, 'rt') as f:
            orig_skool = f.read().split('\n')
        args = '{} {}'.format(options, skool)
        sft, stderr = self.run_skool2sft(args, out_lines=False)
        self.assertEqual(stderr, '')
        sftfile = self.write_text_file(sft)
        options = '-T {}'.format(sftfile)
        if org is not None:
            options += ' -o {}'.format(org)
        output, stderr = self.run_sna2skool('{} {}'.format(options, snapshot))
        self.assertEqual(orig_skool[:-1], output)
