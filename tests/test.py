import os
import sublime
from unittest import TestCase

SAMPLE_TEXT = os.path.join(os.path.dirname(__file__), 'sample.md')

class test_helloworld_command(TestCase):

    def setUp(self):
        sublime.status_message('aaaaaaaaa')
        self.view = sublime.active_window().new_file()
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    # def tearDown(self):
    #     if self.view:
    #         # close file
    #         self.view.set_scratch(True)
    #         self.view.window().focus_view(self.view)
    #         self.view.window().run_command("close_file")

    def setText(self, string):
        self.view.run_command("insert", {"characters": string})

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))


    # ----------

    def test_hello_world(self):
        # 実行ファイルのパス取得
        testdata = open(SAMPLE_TEXT).read()
        self.setText(testdata)
        # self.view.run_command("hello_world")
        first_row = self.getRow(0)
        self.assertEqual(first_row, "# Heading 0")
