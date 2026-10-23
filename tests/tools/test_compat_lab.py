"""Host-only contracts for the restricted firmware method replayer."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from compat_lab.vm import Method, VM, Obj, JavaFault, Unsupported, PowerCut


def method(body, signature='sample(I)I', registers=3):
    return Method.parse('.class public LTest;\n.method public ' + signature +
                        '\n.registers ' + str(registers) + '\n' + body + '\n.end method', 'fixture', signature)


class ReplayContracts(unittest.TestCase):
    def test_parameter_aliases_and_branches(self):
        m = method('const/4 v0, 0x2\nif-ne p1, v0, :no\nreturn p1\n:no\nconst/4 v0, 0x0\nreturn v0')
        vm = VM(lambda *a: self.fail('unexpected adapter'))
        self.assertEqual(vm.run(m, [Obj('LTest;'), 2]), 2)
        self.assertEqual(vm.run(m, [Obj('LTest;'), 1]), 0)

    def test_empty_objects_are_not_null(self):
        m = method('if-eqz p1, :null\nconst/4 v0, 0x1\nreturn v0\n:null\nconst/4 v0, 0x0\nreturn v0', 'sample(Ljava/lang/Object;)I')
        self.assertEqual(VM(None).run(m, [Obj('LTest;'), []]), 1)
        self.assertEqual(VM(None).run(m, [Obj('LTest;'), 0]), 0)

    def test_unknown_opcode_even_on_unvisited_branch_rejected(self):
        with self.assertRaises(Unsupported):
            method('return p1\ninvoke-virtual-quick {p0}, vtable@0')

    def test_bad_deodex_rejected(self):
        with self.assertRaises(Unsupported):
            method('# AnalysisException: unresolved\nreturn p1')

    def test_unknown_api_does_not_become_java_exception(self):
        m = method(':start\ninvoke-static {}, LUnknown;->native()V\n:end\nreturn p1\n.catchall {:start .. :end} :caught\n:caught\nmove-exception v0\nreturn p1')
        def unsupported(*args): raise Unsupported('no adapter')
        with self.assertRaises(Unsupported): VM(unsupported).run(m, [Obj('LTest;'), 1])

    def test_fault_caught_but_power_cut_bypasses_handlers(self):
        m = method(':start\ninvoke-static {}, LFixture;->call()V\n:end\nreturn p1\n.catch Ljava/io/IOException; {:start .. :end} :caught\n:caught\nmove-exception v0\nconst/4 v0, 0x7\nreturn v0')
        def fault(*args): raise JavaFault('Ljava/io/IOException;', 'injected')
        self.assertEqual(VM(fault).run(m, [Obj('LTest;'), 0]), 7)
        def cut(*args): raise PowerCut('injected')
        with self.assertRaises(PowerCut): VM(cut).run(m, [Obj('LTest;'), 0])

    def test_cast_uses_hierarchy_and_null_is_legal(self):
        m = method('check-cast p1, LBitmap;\nreturn p1', 'sample(Ljava/lang/Object;)Ljava/lang/Object;')
        vm = VM(None, {'LChild;': 'LBitmap;', 'LBitmap;': 'LDrawable;', 'LLayer;': 'LDrawable;'})
        obj = Obj('LChild;')
        self.assertIs(vm.run(m, [Obj('LTest;'), obj]), obj)
        self.assertEqual(vm.run(m, [Obj('LTest;'), 0]), 0)
        with self.assertRaises(JavaFault) as cm: vm.run(m, [Obj('LTest;'), Obj('LLayer;')])
        self.assertEqual(cm.exception.kind, 'Ljava/lang/ClassCastException;')

    def test_wide_register_word_is_not_extra_argument(self):
        m = method('const-wide/16 v1, 0x0\ninvoke-static/range {v0 .. v2}, LFixture;->call(IJ)V\nreturn p1', registers=5)
        seen = []
        VM(lambda target, args, vm: seen.append((target, args))).run(m, [Obj('LTest;'), 8])
        self.assertEqual(seen[0][1], [0, 0])

    def test_instruction_limit(self):
        m = method(':loop\ngoto :loop')
        with self.assertRaises(Unsupported): VM(None, max_steps=20).run(m, [Obj('LTest;'), 0])

    def test_unbalanced_monitor_rejected(self):
        m = method('monitor-exit p0\nreturn p1')
        with self.assertRaises(Unsupported): VM(None).run(m, [Obj('LTest;'), 0])

class InputContracts(unittest.TestCase):
    def test_changed_and_missing_inputs_fail_closed(self):
        import tempfile
        from compat_lab.inputs import verify_inputs, digest
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); source = root/'source.smali'; source.write_text('original')
            config = {'files':{'source.smali':digest(source)}}
            verify_inputs(root, config)
            source.write_text('changed')
            with self.assertRaises(Unsupported): verify_inputs(root, config)
            source.unlink()
            with self.assertRaises(Unsupported): verify_inputs(root, config)

    def test_missing_external_native_api_is_not_stubbed_to_success(self):
        from compat_lab.environment import Environment
        env = Environment({}, {})
        with self.assertRaises(Unsupported): env.invoke('LNative;->writeBackup()Z', [], env.vm)

    def test_string_equals_null_is_false(self):
        from compat_lab.environment import Environment
        env = Environment({}, {})
        signature = 'Ljava/lang/String;->equals(Ljava/lang/Object;)Z'
        self.assertEqual(env.invoke(signature, ['null', 0], env.vm), 0)
        self.assertEqual(env.invoke(signature, ['same', 'same'], env.vm), 1)


if __name__ == '__main__': unittest.main()
