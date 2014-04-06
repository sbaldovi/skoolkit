.. _htmlTemplates:

HTML templates
==============
Every page in an HTML disassembly is built from a single full-page template and
several subtemplates defined by :ref:`template` sections in the `ref` file.

A template may contain 'replacement fields' - identifiers enclosed by braces
(``{`` and ``}``) - that are replaced by appropriate content (typically derived
from the `skool` file or a `ref` file section) when the template is formatted.
The following 'universal' identifiers are available in every template:

* ``Game`` - a dictionary of the parameters in the :ref:`ref-game` section
* ``SkoolKit`` - a dictionary of parameters relevant to the page currently
  being built

The parameters in the ``SkoolKit`` dictionary are:

* ``home`` - the relative path to the disassembly index page
* ``page_header`` - the page header text (as defined in the :ref:`pageHeaders`
  section)
* ``page_id`` - the page ID (e.g. ``GameIndex``, ``MemoryMap``)
* ``title`` - the title of the page (as defined in the :ref:`titles` section)

The parameters in a dictionary are accessed using the ``[param]`` notation;
for example, wherever ``{Game[Copyright]}`` appears in a template, it is
replaced by the value of the ``Copyright`` parameter in the :ref:`ref-game`
section when the template is formatted.

In addition to the universal identifiers, the following page-level identifiers
are available in every full-page template:

* ``m_javascript`` - replaced by any number of copies of the
  :ref:`t_javascript` subtemplate
* ``m_stylesheet`` - replaced by one or more copies of the :ref:`t_stylesheet`
  subtemplate

.. _t_Asm:

Asm
---
The ``Asm`` template is the full-page template that is used to build
disassembly pages.

It contains the following identifiers (in addition to the universal and
page-level identifiers):

* ``disassembly`` - replaced by sequences of copies of the
  :ref:`t_asm_instruction` subtemplate, punctuated by copies of the
  :ref:`t_asm_comment` subtemplate
* ``entry`` - a dictionary of parameters corresponding to the current memory
  map entry (see below)
* ``next_entry`` - a dictionary of parameters corresponding to the next memory
  map entry (see below)
* ``prev_entry`` - a dictionary of parameters corresponding to the previous
  memory map entry (see below)
* ``registers_input`` - replaced by any number of copies of the
  :ref:`t_asm_register` subtemplate
* ``registers_output`` - replaced by any number of copies of the
  :ref:`t_asm_register` subtemplate

The parameters in the ``prev_entry``, ``entry`` and ``next_entry`` dictionaries
are:

* ``address`` - the address of the entry (may be in decimal or hexadecimal
  format, depending on how it appears in the `skool` file, and the options
  passed to :ref:`skool2html.py`)
* ``byte`` - the LSB of the entry address
* ``description`` - the entry description
* ``exists`` - '1' if the entry exists, '0' otherwise
* ``label`` - the ASM label of the first instruction in the entry
* ``labels`` - '1' if any instructions in the entry have an ASM label, '0'
  otherwise
* ``location`` - the address of the entry as a decimal number
* ``map_url`` - the relative path to the entry on the 'Memory Map' page
* ``page`` - the MSB of the entry address
* ``size`` - the size of the entry in bytes
* ``title`` - the title of the entry
* ``type`` - the block type of the entry ('b', 'c', 'g', 's', 't', 'u' or 'w')
* ``url`` - the relative path to the disassembly page for the entry (useful
  only for ``prev_entry`` and ``next_entry``)

To see the default ``Asm`` template, run the following command::

  $ skool2html.py -r Template:Asm

.. _t_GameIndex:

GameIndex
---------
The ``GameIndex`` template is the full-page template that is used to build the
disassembly index page.

It contains the following identifier (in addition to the universal and
page-level identifiers):

* ``m_index_section`` - replaced by any number of copies of the
  :ref:`t_index_section` subtemplate

To see the default ``GameIndex`` template, run the following command::

  $ skool2html.py -r Template:GameIndex

.. _t_MemoryMap:

MemoryMap
---------
The ``MemoryMap`` template is the full-page template that is used to build the
memory map pages and the 'Game status buffer' page.

It contains the following identifiers (in addition to the universal and
page-level identifiers):

* ``MemoryMap`` - a dictionary of the parameters in the corresponding
  :ref:`memoryMap` section
* ``m_map_entry`` - replaced by one or more copies of the :ref:`t_map_entry`
  subtemplate

To see the default ``MemoryMap`` template, run the following command::

  $ skool2html.py -r Template:MemoryMap

.. _t_Page:

Page
----
The ``Page`` template is the full-page template that is used to build custom
pages defined by :ref:`page` and :ref:`pageContent` sections.

It contains the following identifier (in addition to the universal and
page-level identifiers):

* ``content`` - replaced by the value of the ``PageContent`` parameter in the
  corresponding :ref:`page` section

To see the default ``Page`` template, run the following command::

  $ skool2html.py -r Template:Page

.. _t_Reference:

Reference
---------
The ``Reference`` template is the full-page template that is used to build the
'Bugs', 'Trivia', 'Pokes', 'Glossary', 'Graphic glitches' and 'Changelog'
pages.

It contains the following identifiers (in addition to the universal and
page-level identifiers):

* ``items`` - replaced by one or more copies of the :ref:`t_box` subtemplate
  (on the 'Bugs', 'Trivia', 'Pokes', 'Glossary' and 'Graphic glitches' pages)
  or the :ref:`t_changelog_entry` subtemplate (on the 'Changelog' page)
* ``m_contents_list_item`` - replaced by one or more copies of the
  :ref:`t_contents_list_item` subtemplate

To see the default ``Reference`` template, run the following command::

  $ skool2html.py -r Template:Reference

.. _t_anchor:

anchor
------
The ``anchor`` template is the subtemplate used to format a page anchor (by
default, an ``<a>`` element with a ``name`` attribute).

It contains the following identifier (in addition to the universal
identifiers):

* ``anchor`` - the value of the ``name`` attribute

To see the default ``anchor`` template, run the following command::

  $ skool2html.py -r Template:anchor

.. _t_asm_comment:

asm_comment
-----------
The ``asm_comment`` template is the subtemplate used by the :ref:`t_Asm`
full-page template to format routine-level comments.

It contains the following identifiers (in addition to the universal
identifiers):

* ``m_paragraph`` - replaced by one or more copies of the :ref:`t_paragraph`
  subtemplate
* ``t_anchor`` - replaced by a copy of the :ref:`t_anchor` subtemplate (with
  the address of the next instruction in decimal format as the anchor name)

To see the default ``asm_comment`` template, run the following command::

  $ skool2html.py -r Template:asm_comment

.. _t_asm_instruction:

asm_instruction
---------------
The ``asm_instruction`` template is the subtemplate used by the :ref:`t_Asm`
full-page template to format an instruction (including its label, address,
operation and comment).

It contains the following identifiers (in addition to the universal
identifiers):

* ``entry`` - a dictionary of parameters corresponding to the current memory
  map entry (see :ref:`t_Asm`)
* ``instruction`` - a dictionary of parameters corresponding to the instruction
  (see below)
* ``t_anchor`` - replaced by a copy of the :ref:`t_anchor` subtemplate (with
  the instruction's address in decimal format as the anchor name)

The parameters in the ``instruction`` dictionary are:

* ``address`` - the address of the instruction (may be in decimal or
  hexadecimal format, depending on how it appears in the `skool` file, and the
  options passed to :ref:`skool2html.py`)
* ``annotated`` - '0' if the instruction has no comment (``comment`` is blank),
  '1' otherwise
* ``comment`` - the text of the comment for the instruction
* ``comment_rowspan`` - the number of instructions to which the comment applies
* ``label`` - the instruction's ASM label
* ``operation`` - the assembly language operation (e.g. 'LD A,B'), with operand
  hyperlinked if appropriate

To see the default ``asm_instruction`` template, run the following command::

  $ skool2html.py -r Template:asm_instruction

.. _t_asm_register:

asm_register
------------
The ``asm_register`` template is the subtemplate used by the :ref:`t_Asm`
full-page template to format each row in a table of input register values or
output register values.

It contains the following identifiers (in addition to the universal
identifiers):

* ``description`` - the register's description (as it appears in the register
  section for the current entry in the `skool` file)
* ``entry`` - a dictionary of parameters corresponding to the current memory
  map entry (see :ref:`t_Asm`)
* ``name`` - the register's name (e.g. 'HL')

To see the default ``asm_register`` template, run the following command::

  $ skool2html.py -r Template:asm_register

.. _t_box:

box
---
The ``box`` template is the subtemplate used by the :ref:`t_Reference`
full-page template to format each entry on the 'Bugs', 'Trivia', 'Pokes',
'Glossary' and 'Graphic glitches' pages.

It contains the following identifiers (in addition to the universal
identifiers):

* ``box_num`` - '1' or '2', depending on the order of the entry on the page
* ``contents`` - replaced by the pre-formatted contents of the relevant
  :ref:`ref-Bug`, :ref:`ref-Fact`, :ref:`ref-Poke`, :ref:`ref-Glossary` or
  :ref:`ref-GraphicGlitch` section
* ``title`` - the entry title

To see the default ``box`` template, run the following command::

  $ skool2html.py -r Template:box

.. _t_changelog_entry:

changelog_entry
---------------
The ``changelog_entry`` is the subtemplate used by the :ref:`t_Reference`
full-page template to format each entry on the 'Changelog' page.

It contains the following identifiers (in addition to the universal
identifiers):

* ``changelog_num`` - '1' or '2', depending on the order of the entry on the
  page
* ``description`` - the changelog entry intro text
* ``t_anchor`` - replaced by a copy of the :ref:`t_anchor` subtemplate (with
  the entry title as the anchor name)
* ``t_changelog_item_list`` - replaced by a copy of the
  :ref:`t_changelog_item_list` subtemplate
* ``title`` - the changelog entry title

To see the default ``changelog_entry`` template, run the following command::

  $ skool2html.py -r Template:changelog_entry

.. _t_changelog_item:

changelog_item
--------------
The ``changelog_item`` template is the subtemplate used by the
:ref:`t_changelog_item_list` subtemplate to format each item in a changelog
item list.

It contains the following identifier (in addition to the universal
identifiers):

* ``item`` - replaced by the text of the changelog item, or a copy of the
  :ref:`t_changelog_item_list` subtemplate

To see the default ``changelog_item`` template, run the following command::

  $ skool2html.py -r Template:changelog_item

.. _t_changelog_item_list:

changelog_item_list
-------------------
The ``changelog_item_list`` template is the subtemplate used by the
:ref:`t_changelog_entry` subtemplate to format a list of changelog items, and
also by the :ref:`t_changelog_item` subtemplate to format a list of subitems or
subsubitems etc.

It contains the following identifiers (in addition to the universal
identifiers):

* ``indent`` - the indentation level of the item list: '' (blank string) for
  the list of top-level items, '1' for a list of subitems, '2' for a list of
  subsubitems etc.
* ``m_changelog_item`` - replaced by one or more copies of the
  :ref:`t_changelog_item` subtemplate

To see the default ``changelog_item_list`` template, run the following
command::

  $ skool2html.py -r Template:changelog_item_list

.. _t_contents_list_item:

contents_list_item
------------------
The ``contents_list_item`` template is the subtemplate used by the
:ref:`t_Reference` full-page template to format each item in the contents list
on the 'Bugs', 'Trivia', 'Pokes', 'Glossary', 'Graphic glitches' and
'Changelog' pages.

It contains the following identifiers (in addition to the universal
identifiers):

* ``title`` - the entry title
* ``url`` - the URL to the entry on the page

To see the default ``contents_list_item`` template, run the following command::

  $ skool2html.py -r Template:contents_list_item

.. _t_img:

img
---
The ``img`` template is the subtemplate used to format ``<img>`` elements.

It contains the following identifiers (in addition to the universal
identifiers):

* ``alt`` - the 'alt' text for the image
* ``src`` - the relative path to the image file

To see the default ``img`` template, run the following command::

  $ skool2html.py -r Template:img

.. _t_index_section:

index_section
-------------
The ``index_section`` template is the subtemplate used by the
:ref:`t_GameIndex` full-page template to format each group of links on the
disassembly index page.

It contains the following identifiers (in addition to the universal
identifiers):

* ``header`` - the header text for the group of links (as defined in the name
  of the :ref:`indexGroup` section)
* ``m_index_section_item`` - replaced by one or more copies of the
  :ref:`t_index_section_item` subtemplate

To see the default ``index_section`` template, run the following command::

  $ skool2html.py -r Template:index_section

.. _t_index_section_item:

index_section_item
------------------
The ``index_section_item`` template is the subtemplate used by the
:ref:`t_index_section` subtemplate to format each link in a link group on the
disassembly index page.

It contains the following identifiers (in addition to the universal
identifiers):

* ``href`` - the relative path to the page being linked to
* ``link_text`` - the link text for the page (as defined in the :ref:`links`
  section)
* ``other_text`` - the supplementary text displayed alongside the link (as
  defined in the :ref:`links` section)

To see the default ``index_section_item`` template, run the following
command::

  $ skool2html.py -r Template:index_section_item

.. _t_javascript:

javascript
----------
The ``javascript`` template is the subtemplate used by the full-page templates
to format each ``<script>`` element in the head of a page.

It contains the following identifier (in addition to the universal
identifiers):

* ``src`` - the relative path to the JavaScript file

To see the default ``javascript`` template, run the following command::

  $ skool2html.py -r Template:javascript

.. _t_link:

link
----
The ``link`` template is the subtemplate used to format the hyperlinks created
by the :ref:`BUG`, :ref:`FACT`, :ref:`POKE`, :ref:`LINK` and :ref:`R` macros,
and the hyperlinks in instruction operands on disassembly pages.

It contains the following identifiers (in addition to the universal
identifiers):

* ``href`` - the relative path to the page being linked to
* ``link_text`` - the link text for the page

To see the default ``link`` template, run the following command::

  $ skool2html.py -r Template:link

.. _t_map_entry:

map_entry
---------
The ``map_entry`` template is the subtemplate used by the :ref:`t_MemoryMap`
full-page template to format each entry on the memory map pages and the 'Game
status buffer' page.

It contains the following identifiers (in addition to the universal
identifiers):

* ``MemoryMap`` - a dictionary of parameters from the corresponding
  :ref:`memoryMap` section
* ``entry`` - a dictionary of parameters corresponding to the current memory
  map entry

The parameters in the ``entry`` dictionary are:

* ``address`` - the address of the entry (may be in decimal or hexadecimal
  format, depending on how it appears in the `skool` file, and the options
  passed to :ref:`skool2html.py`)
* ``byte`` - the LSB of the entry address
* ``description`` - the entry description
* ``exists`` - '1' if the entry exists, '0' otherwise
* ``label`` - the ASM label of the first instruction in the entry
* ``labels`` - '1' if any instructions in the entry have an ASM label, '0'
  otherwise
* ``location`` - the address of the entry as a decimal number
* ``page`` - the MSB of the entry address
* ``size`` - the size of the entry in bytes
* ``title`` - the title of the entry
* ``type`` - the block type of the entry ('b', 'c', 'g', 's', 't', 'u' or 'w')
* ``url`` - the relative path to the disassembly page for the entry

To see the default ``map_entry`` template, run the following command::

  $ skool2html.py -r Template:map_entry

.. _t_paragraph:

paragraph
---------
The ``paragraph`` template is the subtemplate used to format each paragraph in
the following items:

* memory map entry descriptions (on disassembly pages and memory map pages)
* routine-level comments on disassembly pages
* entries on the 'Bugs', 'Trivia', 'Pokes', 'Glossary', 'Graphic glitches' and
  'Changelog' pages

It contains the following identifier (in addition to the universal
identifiers):

* ``paragraph`` - the text of the paragraph

To see the default ``paragraph`` template, run the following command::

  $ skool2html.py -r Template:paragraph

.. _t_reg:

reg
---
The ``reg`` template is the subtemplate used by the :ref:`REG` macro to format
a register name.

It contains the following identifier (in addition to the universal
identifiers):

* ``reg`` - the register name (e.g. 'HL')

To see the default ``reg`` template, run the following command::

  $ skool2html.py -r Template:reg

.. _t_stylesheet:

stylesheet
----------
The ``stylesheet`` template is the subtemplate used by the full-page templates
to format each ``<link>`` element for a CSS file in the head of a page.

It contains the following identifier (in addition to the universal
identifiers):

* ``href`` - the relative path to the CSS file

To see the default ``stylesheet`` template, run the following command::

  $ skool2html.py -r Template:stylesheet