#    Copyright (C) 2015 Jeremy S. Sanders
#    Email: Jeremy Sanders <jeremy@jeremysanders.net>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##############################################################################

"""Dialog for filtering data."""

from __future__ import division, print_function

from .. import qtall as qt4
from .. import document
from ..qtwidgets.datasetbrowser import DatasetBrowser
from .veuszdialog import VeuszDialog

def _(text, disambiguation=None, context="FilterDialog"):
    """Translate text."""
    return qt4.QCoreApplication.translate(context, text, disambiguation)

class FilterDialog(VeuszDialog):
    """Preferences dialog."""

    def __init__(self, parent, doc):
        """Setup dialog."""
        VeuszDialog.__init__(self, parent, "filter.ui")
        self.document = doc

        self.dsbrowser = DatasetBrowser(doc, parent, None, checkable=True)
        grplayout = qt4.QVBoxLayout()
        grplayout.addWidget(self.dsbrowser)
        self.filtergroup.setLayout(grplayout)

        self.buttonBox.button(qt4.QDialogButtonBox.Apply).clicked.connect(
            self.applyClicked)
        self.buttonBox.button(qt4.QDialogButtonBox.Reset).clicked.connect(
            self.resetClicked)

    def updateStatus(self, text):
        """Show message in dialog."""
        qt4.QTimer.singleShot(4000, self.statuslabel.clear)
        self.statuslabel.setText(text)

    def applyClicked(self):
        """Do the filtering."""

        prefix = self.prefixcombo.currentText().strip()
        suffix = self.suffixcombo.currentText().strip()
        if not prefix and not suffix:
            self.updateStatus(_("Prefix and/or suffix must be entered"))
            return

        expr = self.exprcombo.currentText().strip()
        if not expr:
            self.updateStatus(_("Enter a valid filter expression"))
            return

        tofilter = self.dsbrowser.checkedDatasets()
        if not tofilter:
            self.updateStatus(_("Choose at least one dataset to filter"))
            return

        invert = self.invertcheck.isChecked()
        replacenans = self.replacenancheck.isChecked()

        op = document.OperationDatasetFilter(
            expr,
            tofilter,
            prefix=prefix, suffix=suffix,
            invert=invert,
            replacenans=replacenans)

        self.document.applyOperation(op)

    def resetClicked(self):
        for cntrl in self.exprcombo, self.prefixcombo, self.suffixcombo:
            cntrl.setEditText("")
        self.dsbrowser.reset()
        self.updateStatus(_("Dialog reset"))

