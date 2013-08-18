#!/usr/bin/env python
import sys
import argparse

ARCHIVE_INFO = {
    0: "Full title",
    1: "Software house/publisher",
    2: "Author(s)",
    3: "Year of publication",
    4: "Language",
    5: "Game/utility type",
    6: "Price",
    7: "Protection scheme/loader",
    8: "Origin",
    255: "Comment(s)"
}

def get_word(data, index):
    return data[index] + 256 * data[index + 1]

def get_word3(data, index):
    return get_word(data, index) + 65536 * data[index + 2]

def get_dword(data, index):
    return get_word3(data, index) + 16777216 * data[index + 3]

def bytes_to_str(data):
    return ', '.join(str(b) for b in data)

def get_str(data):
    return ''.join(chr(b) for b in data)

def get_block_info(data, i):
    # http://www.worldofspectrum.org/TZXformat.html
    block_id = data[i]
    header = "Unknown block"
    info = []
    tape_data = []
    i += 1
    if block_id == 16:
        # Standard speed data block
        length = get_word(data, i + 2)
        tape_data = data[i + 4:i + 4 + length]
        header = "Standard speed data block"
        data_type = "Unknown"
        name = ""
        if tape_data[0] == 0:
            data_type = "Header block"
            name = get_str(tape_data[2:12])
        elif tape_data[0] == 255:
            data_type = "Data block"
        info.append("Type: {}".format(data_type))
        if name:
            info.append("Name: {}".format(name))
        info.append("Length: {}".format(length))
        i += 4 + length
    elif block_id == 17:
        # Turbo speed data block
        length = get_word3(data, i + 15)
        tape_data = data[i + 18:i + 18 + length]
        header = "Turbo speed data block"
        info.append("Length: {}".format(length))
        i += 18 + length
    elif block_id == 18:
        # Pure tone
        i += 4
    elif block_id == 19:
        # Sequence of pulses of various lengths
        i += 2 * data[i] + 1
    elif block_id == 20:
        # Pure data block
        i += get_word3(data, i + 7) + 10
    elif block_id == 21:
        # Direct recording block
        i += get_word3(data, i + 5) + 8
    elif block_id == 24:
        # CSW recording block
        i += get_dword(data, i) + 4
    elif block_id == 25:
        # Generalized data block
        i += get_dword(data, i) + 4
    elif block_id == 32:
        # Pause (silence) or 'Stop the tape' command
        i += 2
    elif block_id == 33:
        # Group start
        i += data[i] + 1
    elif block_id == 34:
        # Group end
        pass
    elif block_id == 35:
        # Jump to block
        i += 2
    elif block_id == 36:
        # Loop start
        i += 2
    elif block_id == 37:
        # Loop end
        pass
    elif block_id == 38:
        # Call sequence
        i += get_word(data, i) * 2 + 2
    elif block_id == 39:
        # Return from sequence
        pass
    elif block_id == 40:
        # Select block
        i += get_word(data, i) + 2
    elif block_id == 42:
        # Stop the tape if in 48K mode
        i += 4
    elif block_id == 43:
        # Set signal level
        i += 5
    elif block_id == 48:
        # Text description
        i += data[i] + 1
    elif block_id == 49:
        # Message block
        i += data[i + 1] + 2
    elif block_id == 50:
        # Archive info
        header = "Archive info"
        num_strings = data[i + 2]
        j = i + 3
        for k in range(num_strings):
            str_len = data[j + 1]
            info.append("{}: {1}".format(ARCHIVE_INFO.get(data[j], data[j]), get_str(data[j + 2:j + 2 + str_len])))
            j += 2 + str_len
        i += get_word(data, i) + 2
    elif block_id == 51:
        # Hardware type
        i += data[i] * 3 + 1
    elif block_id == 53:
        # Custom info block
        i += get_dword(data, i + 16) + 20
    elif block_id == 90:
        # "Glue" block
        i += 9
    else:
        sys.stderr.write('Unknown block ID {} at index {}\n'.format(block_id, i - 1))
        sys.exit(1)
    if tape_data:
        if len(tape_data) > 14:
            tape_data_summary = "{} ... {}".format(bytes_to_str(tape_data[:7]), bytes_to_str(tape_data[-7:]))
        else:
            tape_data_summary = bytes_to_str(tape_data)
        info.append("Data: {}".format(tape_data_summary))
    return i, block_id, header, info

def analyse(tzx):
    print('Version: {}.{}'.format(tzx[8], tzx[9]))
    i = 10
    while i < len(tzx):
        i, block_id, header, info = get_block_info(tzx, i)
        print("{} (0x{:02X})".format(header, block_id))
        for line in info:
            print('  ' + line)

###############################################################################
# Begin
###############################################################################
parser = argparse.ArgumentParser(
    usage="analyse-tzx.py FILE.tzx",
    description="Show the blocks in a TZX file.",
    add_help=False
)
parser.add_argument('tzxfile', help=argparse.SUPPRESS, nargs='?')
namespace, unknown_args = parser.parse_known_args()
if unknown_args or namespace.tzxfile is None:
    parser.exit(2, parser.format_help())

with open(namespace.tzxfile, 'rb') as f:
    tzx = bytearray(f.read())

signature = get_str(tzx[:7])
if signature != 'ZXTape!':
    sys.stderr.write("{} is not a TZX file\n".format(namespace.tzxfile))
    sys.exit(1)

analyse(tzx)
