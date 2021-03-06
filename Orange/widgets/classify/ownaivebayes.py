"""
Naive Bayes Learner

"""

from  Orange.data import Table
from Orange.classification.naive_bayes import NaiveBayesLearner, NaiveBayesModel
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.owlearnerwidget import OWProvidesLearner


class OWNaiveBayes(OWProvidesLearner, widget.OWWidget):
    name = "Naive Bayes"
    description = "Naive Bayesian classifier."
    icon = "icons/NaiveBayes.svg"
    inputs = [("Data", Table, "set_data")] + OWProvidesLearner.inputs
    outputs = [("Learner", NaiveBayesLearner),
               ("Classifier", NaiveBayesModel)]

    want_main_area = False
    resizing_enabled = False

    learner_name = settings.Setting("Naive Bayes")

    def __init__(self):
        super().__init__()

        # GUI
        gui.lineEdit(gui.widgetBox(self.controlArea, self.tr("Name")),
                     self, "learner_name")

        gui.rubber(self.controlArea)

        gui.button(self.controlArea, self, self.tr("&Apply"),
                   callback=self.apply)
        self.controlArea.layout().addWidget(self.report_button)

        self.data = None
        self.preprocessors = None

        self.initialize()

    def initialize(self):
        """
        Initialize the widget's state.
        """
        learner = NaiveBayesLearner()
        learner.name = self.learner_name
        self.send("Learner", learner)
        self.send("Classifier", None)

    def set_data(self, data):
        self.data = data
        if data is not None:
            self.apply()
        else:
            self.send("Classifier", None)

    LEARNER = NaiveBayesLearner

    def apply(self):
        learner = self.LEARNER(
            preprocessors=self.preprocessors
        )
        learner.name = self.learner_name
        classifier = None

        if self.data is not None:
            self.error(0)
            if not learner.check_learner_adequacy(self.data.domain):
                self.error(0, learner.learner_adequacy_err_msg)
            else:
                classifier = learner(self.data)
                classifier.name = self.learner_name

        self.send("Learner", learner)
        self.send("Classifier", classifier)

    def send_report(self):
        self.report_items((("Name", self.learner_name),))


if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication

    a = QApplication(sys.argv)
    ow = OWNaiveBayes()
    d = Table('iris')
    ow.set_data(d)
    ow.show()
    a.exec_()
    ow.saveSettings()
