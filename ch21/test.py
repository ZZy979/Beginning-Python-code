import test_utils


class Ch21Tests(test_utils.TestCase):
    dirname = 'ch21'

    def _test_generate_pdf(self, script, filename):
        import os
        self.run_script(script)
        pdf_file = self.src_dir / filename
        self.assertTrue(pdf_file.exists())
        os.remove(pdf_file)

    def test_hello_report(self):
        self._test_generate_pdf('hello_report.py', 'hello.pdf')

    def test_draw_polyline(self):
        self._test_generate_pdf('draw_polyline.py', 'polyline.pdf')

    def test_1st_impl(self):
        self._test_generate_pdf('sunspots_proto.py', 'report1.pdf')

    def test_2nd_impl(self):
        self._test_generate_pdf('sunspots.py', 'report2.pdf')
