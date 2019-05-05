import os
import subprocess
import sys
import unittest

from stcsession import stcsession

test_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(os.path.dirname(os.path.dirname(test_path)))
sample_path = os.path.join(root_path, "sample")

TESTBED_CONFIG = os.path.join(test_path, "testbed.yaml")
TESTBED_DATA = os.path.join(sample_path, "testbed.config.json")
TESTBED_TEMPLATE = os.path.join(sample_path, "testbed-template.yaml")

# Create this file with real Lab Server and chassis to test real setup.
REAL_TESTBED_DATA = os.path.join(test_path, "testbed.config.json")
REAL_CONFIG = os.path.join(test_path, "real_testbed.yaml")


class TestStcSessionInit(unittest.TestCase):

    def test_no_file(self):
        with self.assertRaises(RuntimeError) as e:
            stcsession.StcSession("no_such_file.yaml")
        self.assertTrue(str(e.exception).startswith("no such file"))

    def test_sample_config(self):
        # Generate testbed.yaml
        gen_testbed_config(TESTBED_DATA, TESTBED_TEMPLATE, TESTBED_CONFIG)

        stc = stcsession.StcSession(TESTBED_CONFIG)
        self.assertIsNotNone(stc)

        self.assertNotEqual(len(stc.chassis()), 0)

        ports = stc.ports()
        self.assertTrue(len(ports) > 1)
        for port in ports:
            c, s, p = stc.split_csp(port['location'])
            self.assertIsInstance(s, int)
            self.assertIsInstance(p, int)

        p = stc.port('nothere')
        self.assertIsNone(p)
        p = stc.port('port1')
        self.assertIsNotNone(p)
        p = stc.port('port2')
        self.assertIsNotNone(p)

        tb_txt = str(stc)
        self.assertEqual(len(tb_txt.split("\n")), len(stc.ports()))

        print()
        print(tb_txt)

        # Remove the testbed config file.
        os.unlink(TESTBED_CONFIG)

    @unittest.skipUnless(os.path.exists(REAL_TESTBED_DATA), "requires " + REAL_TESTBED_DATA + " with real LS and chassis")
    def test_start(self):
        gen_testbed_config(REAL_TESTBED_DATA, TESTBED_TEMPLATE, REAL_CONFIG)
        with stcsession.StcSession(REAL_CONFIG, debug_level=1) as stc:
            self.assertTrue(stc.started())
            bll_ver = stc.bll_version()
            self.assertTrue(bll_ver.startswith("9.90."))
        os.unlink(REAL_CONFIG)


def gen_testbed_config(data, template, output):
    if not os.path.exists(data):
        raise RuntimeError("no such file:", data)
    if not os.path.exists(template):
        raise RuntimeError("no such file:", template)
    GEN_CONFIG_SCRIPT = os.path.join(root_path, "script", "generate-config.py")
    with open(output, "w") as f:
        cmd = (GEN_CONFIG_SCRIPT, '-c', data, '-t', template)
        subprocess.call(cmd, stdout=f)


if __name__ == '__main__':
    unittest.main()
