"""A unified interface to reader + scanner + metrical_data + identifier."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

import display
import handle_input
import identifier
import metrical_data
import scan


class SimpleIdentifier(object):
  """A single interface to read-scan-data-identify-display."""

  def __init__(self):
    """Initialize whichever of the parts need it."""
    if not metrical_data.known_metre_patterns:
      metrical_data.InitializeData()
    self.identifier = identifier.Identifier(metrical_data)

  def _Reset(self):
    self.output = []
    self.cleaned_output = None
    self.tables = []

  def IdentifyFromLines(self, input_lines):
    """Given bunch of lines of verse, clean-scan-identify-display."""
    self._Reset()
    logging.info('Got input:\n%s', '\n'.join(input_lines))
    cleaner = handle_input.InputHandler()
    (display_lines, cleaned_lines) = cleaner.CleanLines(input_lines)
    self.output.extend(cleaner.error_output)
    self.cleaned_output = cleaner.clean_output
    self.output.extend(cleaner.clean_output)

    pattern_lines = scan.ScanVerse(cleaned_lines)
    if not pattern_lines:
      return None

    result = self.identifier.IdentifyFromLines(pattern_lines)
    if not result:
      pass
    else:
      for m in result:
        known_pattern = metrical_data.GetPattern(m.MetreName())
        if known_pattern:
          alignment = display.AlignVerseToMetre(display_lines,
                                                ''.join(pattern_lines),
                                                known_pattern)
          table = display.HtmlTableFromAlignment(alignment)
          self.tables.append((m.MetreName(), table))
    return result

  def AllDebugOutput(self):
    return '\n'.join(self.output +
                     ['Full:'] + self.identifier.global_info +
                     ['Lines:'] + self.identifier.lines_info +
                     ['Halves:'] + self.identifier.halves_info +
                     ['Quarters:'] + self.identifier.quarters_info)
