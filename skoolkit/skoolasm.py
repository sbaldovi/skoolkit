# -*- coding: utf-8 -*-

# Copyright 2008-2013 Richard Dymond (rjdymond@gmail.com)
#
# This file is part of SkoolKit.
#
# SkoolKit is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# SkoolKit is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# SkoolKit. If not, see <http://www.gnu.org/licenses/>.

import re
import inspect

from . import warn, write_text, wrap, get_int_param, parse_int, get_chr, SkoolParsingError
from . import skoolmacro
from .skoolmacro import parse_ints, parse_params, get_params, get_text_param, MacroParsingError, UnsupportedMacroError
from .skoolparser import TableParser, ListParser, TABLE_MARKER, TABLE_END_MARKER, LIST_MARKER, LIST_END_MARKER

UDGTABLE_MARKER = '#UDGTABLE'

class AsmWriter:
    def __init__(self, parser, crlf, tab, properties, lower, instr_width, show_warnings):
        self.parser = parser
        self.show_warnings = show_warnings

        # Build a label dictionary
        self.labels = {}
        for address, instructions in parser.instructions.items():
            label = instructions[0].asm_label
            if label:
                self.labels[address] = label

        # Determine the base and end addresses
        self.base_address = 16384
        self.end_address = 65535
        if self.labels:
            self.base_address = min([address for address in self.labels.keys()])
        elif self.parser.memory_map:
            self.base_address = self.parser.memory_map[0].instructions[0].address
        if self.parser.memory_map:
            self.end_address = self.parser.memory_map[-1].instructions[-1].address

        self.bullet = properties.get('bullet', '*')
        self.lower = lower

        # Field widths (line = indent + instruction + ' ; ' + comment)
        if tab:
            self.indent_width = 8
        else:
            self.indent_width = self._get_int_property(properties, 'indent', 2)
        self.instr_width = instr_width
        self.min_comment_width = self._get_int_property(properties, 'comment-width-min', 10)
        self.line_width = self._get_int_property(properties, 'line-width', 79)
        self.desc_width = self.line_width - 2

        # Line terminator and indent
        if crlf:
            self.end = '\r\n'
        else:
            self.end = '\n'
        if tab:
            self.indent = '\t'
        else:
            self.indent = ' ' * self.indent_width

        # Label suffix
        if self._get_int_property(properties, 'label-colons', 1):
            self.label_suffix = ':'
        else:
            self.label_suffix = ''

        min_col_width = self._get_int_property(properties, 'wrap-column-width-min', 10)
        self.table_writer = TableWriter(self.desc_width, min_col_width)

        self.handle_unsupported_macros = self._get_int_property(properties, 'handle-unsupported-macros', 0)

        self.snapshot = self.parser.snapshot
        self._snapshots = [(self.snapshot, '')]
        self.entries = self.parser.entries

        self.list_parser = ListParser()

        self._create_macros()

    def _get_int_property(self, properties, name, default):
        try:
            return int(properties[name])
        except (KeyError, ValueError):
            return default

    def warn(self, s):
        if self.show_warnings:
            warn(s)

    def write(self):
        self.print_header(self.parser.header)
        for entry in self.parser.memory_map:
            first_instruction = entry.instructions[0]
            org = first_instruction.org
            if org:
                if self.lower:
                    org_dir = 'org'
                else:
                    org_dir = 'ORG'
                org_addr_str = self.parser.convert_address_operand(org)
                self.write_line('{0}{1} {2}'.format(self.indent, org_dir, org_addr_str))
                self.write_line('')
            self.entry = entry
            self.print_entry()
            self.write_line('')

    def print_header(self, header):
        if header:
            for line in header:
                self.write_line('; {0}'.format(self.expand(line)).rstrip())
            self.write_line('')

    def print_entry(self):
        self.print_comment_lines([self.entry.description], ignoreua=self.entry.ignoretua)
        if self.entry.details:
            self.print_comment_lines(self.entry.details, ignoreua=self.entry.ignoredua, started=True)
        if self.entry.is_routine() and self.entry.registers:
            self.write_line(';')
            prefix_len = max([len(reg.prefix) for reg in self.entry.registers])
            if prefix_len:
                prefix_len += 1
            indent = ''.ljust(prefix_len)
            for reg in self.entry.registers:
                if reg.prefix:
                    prefix = '{0}:'.format(reg.prefix).rjust(prefix_len)
                else:
                    prefix = indent
                self.write_line('; {0}{1} {2}'.format(prefix, reg.name, self.expand(reg.contents)))
        self.print_instructions()
        if self.entry.end_comment:
            self.print_comment_lines(self.entry.end_comment, ignoreua=self.entry.ignoreecua)

    def write_line(self, s):
        write_text('{0}{1}'.format(s, self.end))

    def _expand_item_macro(self, text, index, default):
        end, params, p_text = parse_params(text, index, default)
        return end, p_text

    def pop_snapshot(self):
        """Discard the current memory snapshot and replace it with the one that
        was most recently saved (by
        :meth:`~skoolkit.skoolasm.AsmWriter.push_snapshot`)."""
        self.snapshot = self._snapshots.pop()[0]

    def push_snapshot(self, name=''):
        """Save the current memory snapshot for later retrieval (by
        :meth:`~skoolkit.skoolasm.AsmWriter.pop_snapshot`), and put a copy in
        its place.

        :param name: An optional name for the snapshot.
        """
        self._snapshots.append((self.snapshot[:], name))

    def _create_macros(self):
        self.macros = {}
        prefix = 'expand_'
        for name, method in inspect.getmembers(self, inspect.ismethod):
            search = re.search('{0}[a-z]+'.format(prefix), name)
            if search and name == search.group():
                macro = '#{0}'.format(name[len(prefix):].upper())
                self.macros[macro] = method

    def expand_bug(self, text, index):
        # #BUG[#name][(link text)]
        return self._expand_item_macro(text, index, 'bug')

    def expand_call(self, text, index):
        end, method, args, warning = skoolmacro.parse_call(text, index, self)
        if warning:
            self.warn(warning)
            return end, ''
        retval = method(*args)
        if retval is None:
            retval = ''
        return end, retval

    def expand_chr(self, text, index):
        end, num = skoolmacro.parse_chr(text, index)
        return end, get_chr(num)

    def expand_d(self, text, index):
        return skoolmacro.parse_d(text, index, self.parser)

    def expand_erefs(self, text, index):
        return skoolmacro.parse_erefs(text, index, self.parser)

    def expand_fact(self, text, index):
        # #FACT[#name][(link text)]
        return self._expand_item_macro(text, index, 'fact')

    def expand_font(self, text, index):
        # #FONT[:(text)]addr[,chars,attr,scale][{X,Y,W,H}][(fname)]
        if self.handle_unsupported_macros:
            if index < len(text) and text[index] == ':':
                index, message = get_text_param(text, index + 1)
            end, params, p_text = parse_params(text, index, chars=',{}')
            return end, ''
        raise UnsupportedMacroError()

    def expand_html(self, text, index):
        # #HTML(text)
        end, message = get_text_param(text, index)
        return end, ''

    def expand_link(self, text, index):
        # #LINK:PageId[#name](link text)
        macro = '#LINK'
        if index >= len(text):
            raise MacroParsingError("No parameters")
        if text[index] != ':':
            raise MacroParsingError("Malformed macro: {0}{1}...".format(macro, text[index]))
        end, page_id, link_text = parse_params(text, index + 1)
        if not page_id:
            raise MacroParsingError("No page ID: {}{}".format(macro, text[index:end]))
        if not link_text:
            raise MacroParsingError("No link text specified: {0}{1}".format(macro, text[index:end]))
        return end, link_text

    def expand_poke(self, text, index):
        # #POKE[#name][(link text)]
        return self._expand_item_macro(text, index, 'poke')

    def expand_pokes(self, text, index):
        # #POKESaddr,byte[,length,step][;addr,byte[,length,step];...]
        end, addr, byte, length, step = parse_ints(text, index, 4, (1, 1))
        self.snapshot[addr:addr + length * step:step] = [byte] * length
        while end < len(text) and text[end] == ';':
            end, addr, byte, length, step = parse_ints(text, end + 1, 4, (1, 1))
            self.snapshot[addr:addr + length * step:step] = [byte] * length
        return end, ''

    def expand_pops(self, text, index):
        # #POPS
        self.pop_snapshot()
        return index, ''

    def expand_pushs(self, text, index):
        # #PUSHS[name]
        end, name, p_text = parse_params(text, index)
        self.push_snapshot(name)
        return end, ''

    def expand_r(self, text, index):
        # #Raddr[@code][#anchor][(link text)]
        end, params, p_text = parse_params(text, index, chars='@')
        anchor_index = params.find('#')
        if anchor_index >= 0:
            params = params[:anchor_index]
        code_id = ''
        code_id_index = params.find('@')
        if code_id_index >= 0:
            code_id = params[code_id_index + 1:]
            params = params[:code_id_index]
        addr_str = params
        if not addr_str:
            raise MacroParsingError("No address")
        try:
            address = get_int_param(addr_str)
        except ValueError:
            raise MacroParsingError("Invalid address: {}".format(addr_str))
        if p_text:
            return end, p_text
        if code_id:
            return end, self.parser.get_instruction_addr_str(address, code_id)
        label = self.labels.get(address)
        if label is None:
            if self.base_address <= address <= self.end_address:
                self.warn('Could not convert address {0} to label'.format(addr_str))
            label = self.parser.get_instruction_addr_str(address)
            if label is None:
                if addr_str.startswith('$'):
                    label = addr_str[1:]
                else:
                    label = addr_str
        return end, label

    def expand_refs(self, text, index):
        # #REFSaddr[(prefix)]
        end, addr_str, prefix = parse_params(text, index, '')
        if not addr_str:
            raise MacroParsingError("No address")
        try:
            address = get_int_param(addr_str)
        except ValueError:
            raise MacroParsingError("Invalid address: {}".format(addr_str))
        entry = self.entries.get(address)
        if not entry:
            raise MacroParsingError('No entry at {0}'.format(addr_str))
        if text[index] == '$':
            addr_fmt = '${0:04X}'
        else:
            addr_fmt = '{0}'
        referrers = [ref.address for ref in entry.referrers]
        if referrers:
            referrers.sort()
            rep = '{0} routine at '.format(prefix).lstrip()
            if len(referrers) > 1:
                rep = '{0} routines at '.format(prefix).lstrip()
                rep += ', '.join('#R{0}'.format(addr_fmt.format(addr)) for addr in referrers[:-1])
                rep += ' and '
            addr = referrers[-1]
            rep += '#R{0}'.format(addr_fmt.format(addr))
        else:
            rep = 'Not used directly by any other routines'
        return end, rep

    def expand_reg(self, text, index):
        # #REGreg
        end, reg, p_text = parse_params(text, index, chars="'")
        if not reg:
            raise MacroParsingError('Missing register argument')
        if len(reg) > 3 or any([char not in "abcdefhlirspxy'" for char in reg]):
            raise MacroParsingError('Bad register: "{0}"'.format(reg))
        if self.lower:
            reg_name = reg.lower()
        else:
            reg_name = reg.upper()
        return end, reg_name

    def expand_scr(self, text, index):
        # #SCR[scale,x,y,w,h,dfAddr,afAddr][{X,Y,W,H}][(fname)]
        if self.handle_unsupported_macros:
            end, params, p_text = parse_params(text, index, chars=',{}')
            return end, ''
        raise UnsupportedMacroError()

    def expand_space(self, text, index):
        # #SPACE[num] or #SPACE([num])
        if index < len(text) and text[index] == '(':
            end, _, num_str = parse_params(text, index)
            try:
                num_sp = get_int_param(num_str)
            except ValueError:
                raise MacroParsingError("Invalid integer: '{}'".format(num_str))
        else:
            end, num_sp = parse_ints(text, index, 1, (1,))
        return end, ' ' * num_sp

    def expand_udg(self, text, index):
        # #UDGaddr[,attr,scale,step,inc,flip,rotate][:maskAddr[,maskStep]][{X,Y,W,H}][(fname)]
        if self.handle_unsupported_macros:
            end, params, p_text = parse_params(text, index, chars=',:{}')
            return end, ''
        raise UnsupportedMacroError()

    def expand_udgarray(self, text, index):
        # #UDGARRAYwidth[,attr,scale,step,inc,flip,rotate];addr1[,attr1,step1,inc1][:maskAddr1[,maskStep1]];...[{X,Y,W,H}](fname)
        # #UDGARRAY*frame1[,delay1];frame2[,delay2];...(fname)
        if self.handle_unsupported_macros:
            if index < len(text) and text[index] == '*':
                end, params, p_text = parse_params(text, index, except_chars=' (')
            else:
                end, params, p_text = parse_params(text, index, chars=',:;-x{}')
            return end, ''
        raise UnsupportedMacroError()

    def expand(self, text):
        if text.find('#') < 0:
            return text

        while 1:
            search = re.search('#[A-Z]+', text)
            if not search:
                break
            marker = search.group()
            if not marker in self.macros:
                raise SkoolParsingError('Found unknown macro: {0}'.format(marker))
            repf = self.macros[marker]
            start, index = search.span()
            try:
                end, rep = repf(text, index)
            except UnsupportedMacroError:
                raise SkoolParsingError('Found unsupported macro: {0}'.format(marker))
            except MacroParsingError as e:
                raise SkoolParsingError('Error while parsing {0} macro: {1}'.format(marker, e.args[0]))
            text = "{0}{1}{2}".format(text[:start], rep, text[end:])

        return text.strip()

    def find_markers(self, block_indexes, text, marker, end_marker):
        index = 0
        while text.find(marker, index) >= 0:
            block_index = text.index(marker, index)
            try:
                block_end_index = text.index(end_marker, block_index) + len(end_marker)
            except ValueError:
                raise SkoolParsingError("Missing end marker: {}...".format(text[block_index:block_index + len(marker) + 15]))
            block_indexes.append(block_index)
            block_indexes.append(block_end_index)
            index = block_end_index

    def extract_blocks(self, text):
        # Find table and list markers
        block_indexes = []
        self.find_markers(block_indexes, text, TABLE_MARKER, TABLE_END_MARKER)
        self.find_markers(block_indexes, text, UDGTABLE_MARKER, TABLE_END_MARKER)
        self.find_markers(block_indexes, text, LIST_MARKER, LIST_END_MARKER)

        # Extract blocks
        blocks = []
        all_indexes = [0]
        all_indexes += block_indexes
        all_indexes.sort()
        all_indexes.append(len(text))
        for i in range(len(all_indexes) - 1):
            start = all_indexes[i]
            end = all_indexes[i + 1]
            block = text[start:end].strip()
            if block and not block.startswith(UDGTABLE_MARKER):
                blocks.append(block)

        return blocks

    def format(self, text, width):
        lines = []
        for block in self.extract_blocks(text):
            if block.startswith(TABLE_MARKER):
                table_lines = self.table_writer.format_table(self.expand(block[len(TABLE_MARKER):]))
                if table_lines:
                    table_width = max([len(line) for line in table_lines])
                    if table_width > width:
                        self.warn('Table in entry at {0} is {1} characters wide'.format(self.entry.address, table_width))
                    lines.extend(table_lines)
            elif block.startswith(LIST_MARKER):
                list_obj = self.list_parser.parse_list(self.expand(block[len(LIST_MARKER):]))
                for item in list_obj.items:
                    item_lines = []
                    bullet = self.bullet
                    indent = ' ' * len(bullet)
                    for line in wrap(item, width - len(bullet) - 1):
                        item_lines.append('{0} {1}'.format(bullet, line))
                        bullet = indent
                    lines.extend(item_lines)
            else:
                lines.extend(wrap(self.expand(block), width))
        return lines

    def print_comment_lines(self, paragraphs, instruction=None, ignoreua=False, started=False):
        for paragraph in paragraphs:
            lines = self.format(paragraph, self.desc_width)
            if started and lines:
                self.write_line(';')
            if lines:
                started = True
            for line in lines:
                if not ignoreua:
                    uaddress = self.find_unconverted_address(line)
                    if uaddress:
                        if instruction:
                            if not instruction.ignoremrcua:
                                self.warn('Comment above {0} contains address ({1}) not converted to a label:\n; {2}'.format(instruction.address, uaddress, line))
                        else:
                            self.warn('Comment contains address ({0}) not converted to a label:\n; {1}'.format(uaddress, line))
                self.write_line('; {0}'.format(line).rstrip())

    def print_instruction_prefix(self, instruction):
        mid_routine_comment = instruction.get_mid_routine_comment()
        if mid_routine_comment:
            self.print_comment_lines(mid_routine_comment, instruction)
        if instruction.asm_label:
            self.write_line("{0}{1}".format(instruction.asm_label, self.label_suffix))

    def find_unconverted_address(self, text):
        search = re.search('[1-9][0-9][0-9][0-9][0-9]', text)
        if search:
            start, end = search.span()
            if (start == 0 or text[start - 1] == ' ') and (end == len(text) or not text[end].isalnum()):
                uaddress = int(search.group())
                if self.base_address <= uaddress <= self.end_address:
                    return uaddress

    def print_instructions(self):
        i = 0
        rowspan = 0
        lines = []
        instructions = self.entry.instructions

        while i < len(instructions) or lines:
            if i < len(instructions):
                instruction = instructions[i]
            else:
                instruction = None

            # Deal with remaining comment lines or rowspan on the previous
            # instruction
            if lines or rowspan > 0:
                if rowspan > 0:
                    self.print_instruction_prefix(instruction)
                    operation = instruction.operation
                    rowspan -= 1
                    i += 1
                else:
                    operation = ''

                if lines:
                    line_comment = lines.pop(0)
                    oline = '{0}{1} ; {2}'.format(self.indent, operation.ljust(instr_width), line_comment)
                else:
                    line_comment = ''
                    oline = '{0}{1}'.format(self.indent, operation)
                self.write_line(oline)
                if not ignoreua:
                    uaddress = self.find_unconverted_address(line_comment)
                    if uaddress:
                        self.warn('Comment at {0} contains address ({1}) not converted to a label:\n{2}'.format(iaddress, uaddress, oline))
                if len(oline) > self.line_width:
                    self.warn('Line is {0} characters long:\n{1}'.format(len(oline), oline))
                continue # pragma: no cover

            ignoreua = instruction.ignoreua
            iaddress = instruction.address

            rowspan = instruction.comment.rowspan
            instr_width = max(len(instruction.operation), self.instr_width)
            comment_width = self.line_width - 3 - instr_width - self.indent_width
            lines = wrap(self.expand(instruction.comment.text), max((comment_width, self.min_comment_width)))

class TableWriter:
    def __init__(self, max_width, min_col_width):
        self.max_width = max_width
        self.min_col_width = min_col_width
        self.table = None
        self.table_parser = TableParser()
        self.cell_matrix = None

    def format_table(self, text):
        self.table = self.table_parser.parse_table(text)
        self.table.cell_padding = 3
        self.table.prepare_cells()
        self.table.reduce_width(self.max_width, self.min_col_width)
        self.cell_matrix = self._build_cell_matrix()
        return self._create_table_text()

    def _build_cell_matrix(self):
        cell_matrix = []
        for row in self.table.rows:
            cell_matrix.append([None] * self.table.num_cols)
        for cell in self.table.cells:
            for x in range(cell.col_index, cell.col_index + cell.colspan):
                for y in range(cell.row_index, cell.row_index + cell.rowspan):
                    cell_matrix[y][x] = cell
        return cell_matrix

    def _get_cell(self, col_index, row_index):
        if 0 <= row_index < len(self.cell_matrix) and 0 <= col_index < self.table.num_cols:
            return self.cell_matrix[row_index][col_index]

    def _render_row(self, lines, row_index, first_line=True):
        rendered = False
        line = ''
        col_index = 0
        cell_left_transparent = True
        cell = self._get_cell(col_index, row_index)
        while cell:
            if cell.transparent and cell_left_transparent:
                border = ' '
            else:
                border = '|'
            text = ''
            if cell.contents and (first_line or row_index == cell.row_index + cell.rowspan - 1):
                text = cell.contents.pop(0)
                rendered = True
            line += "{} {} ".format(border, text.ljust(self.table.get_cell_width(col_index, cell.colspan)))
            col_index += cell.colspan
            cell_left_transparent = cell.transparent
            cell = self._get_cell(col_index, row_index)
        if rendered:
            if (cell and not cell.transparent) or (cell is None and not cell_left_transparent):
                line += '|'
            lines.append(line.rstrip())
        return rendered

    def _create_table_text(self):
        lines = []
        max_row_index = len(self.table.rows)
        if max_row_index == 0:
            return lines
        separator_row_indexes = set((0, max_row_index))
        separator_row_indexes.update([i + 1 for i in self.table.get_header_rows()])
        for row_index in range(max_row_index):
            if row_index in separator_row_indexes:
                lines.append(self._create_row_separator(row_index))
            self._render_row(lines, row_index)
            while self._render_row(lines, row_index, False):
                pass
        lines.append(self._create_row_separator(max_row_index))
        return lines

    def _create_row_separator(self, row_index):
        # Return a separator between rows `row_index - 1` and `row_index`
        line = ''
        col_index = 0
        cell_left_contents = True

        while col_index < self.table.num_cols:
            cell_above = self._get_cell(col_index, row_index - 1)
            if row_index < len(self.table.rows):
                cell = self._get_cell(col_index, row_index)
            else:
                cell = cell_above
            if cell is None:
                break
            cell_above_transparent = cell_above is None or cell_above.transparent
            cell_above_left = self._get_cell(col_index - 1, row_index - 1)
            cell_above_left_transparent = cell_above_left is None or cell_above_left.transparent
            cell_left = self._get_cell(col_index - 1, row_index)
            cell_left_transparent = cell_left is None or cell_left.transparent
            cell_contents = bool(cell_above and cell_above.contents)
            if cell.transparent and cell_above_transparent and cell_above_left_transparent and cell_left_transparent:
                line += ' '
            elif cell_contents and cell_left_contents:
                line += '|'
            else:
                line += '+'
            if cell_contents:
                text = cell.contents.pop(0)
                line += ' {} '.format(text.ljust(self.table.get_cell_width(col_index, cell_above.colspan)))
            else:
                if cell.transparent and cell_above_transparent:
                    spacer = ' '
                else:
                    spacer = '-'
                line += spacer * (2 + self.table.get_cell_width(col_index, cell.colspan))
            cell_left_contents = cell_contents
            col_index += cell.colspan

        if cell_contents:
            return line + '|'
        if line.endswith(' '):
            return line.rstrip()
        return line + '+'
