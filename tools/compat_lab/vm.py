"""Small fail-closed interpreter for selected deodexed control-flow methods.

No bytecode verification, threads, native execution, device access or general
Android runtime. External method semantics are explicit adapters. Inputs must be
pinned by the caller. Trace positions refer to the supplied smali, not CPU PCs.
"""
import ast
from dataclasses import dataclass, field
import re


class Unsupported(RuntimeError):
    """Lab limitation, deliberately not catchable by firmware handlers."""


class PowerCut(BaseException):
    """Injected process loss; bypasses Java catch/finally."""


class JavaFault(Exception):
    def __init__(self, kind, detail):
        super().__init__(detail)
        self.kind = kind


@dataclass(eq=False)
class Obj:
    kind: str
    fields: dict = field(default_factory=dict)


def arg_types(signature):
    args = signature.split('(', 1)[1].split(')', 1)[0]
    types = re.findall(r'\[*L[^;]+;|\[*[ZBCSIJFD]', args)
    if ''.join(types) != args: raise Unsupported('bad method descriptor: ' + signature)
    return types


def is_null(value):
    return value is None or (isinstance(value, (int, bool)) and value == 0)


def equal(a, b):
    if is_null(a) and is_null(b): return True
    if isinstance(a, (int, bool)) and isinstance(b, (int, bool)): return a == b
    return a is b


OPS = set('const const/4 const/16 const-wide/16 const-string const-string/jumbo new-instance new-array '
          'move move/from16 move-object move-object/from16 move-result move-result-object move-exception '
          'iget iget-object iget-boolean iput iput-object iput-boolean '
          'check-cast monitor-enter monitor-exit throw return return-object return-void '
          'goto goto/16 if-eq if-ne if-ge if-lt if-lez if-eqz if-nez '
          'add-int/lit8 or-int/lit8 '
          'invoke-direct invoke-virtual invoke-static invoke-interface '
          'invoke-direct/range invoke-virtual/range invoke-static/range invoke-interface/range'.split())


@dataclass
class Method:
    signature: str
    source: str
    registers: int
    param_words: int
    code: list
    labels: dict
    catches: list

    @classmethod
    def parse(cls, text, source, signature):
        lines = text.splitlines()
        starts = [i for i, line in enumerate(lines) if line.startswith('.method ') and line.split()[-1] == signature]
        if len(starts) != 1: raise Unsupported('method missing/ambiguous: ' + signature)
        start = starts[0]
        end = next(i for i in range(start + 1, len(lines)) if lines[i] == '.end method')
        body = '\n'.join(lines[start:end + 1])
        if any(word in body for word in ('AnalysisException', 'Unresolved', 'OdexedInstruction', 'throw-verification-error')):
            raise Unsupported('unresolved deodex method: ' + signature)
        registers = None
        labels, catches, code = {}, [], []
        offset, java_line = None, None
        annotation = False
        for i in range(start + 1, end):
            line = lines[i].strip()
            if line.startswith('.annotation '): annotation = True; continue
            if line == '.end annotation': annotation = False; continue
            if annotation: continue
            if line.startswith('#@'): offset = line[2:]; continue
            if line.startswith('.line '): java_line = int(line.split()[1]); continue
            if line.startswith('.registers '): registers = int(line.split()[1]); continue
            if line.startswith(':'): labels[line] = len(code); continue
            if line.startswith('.catch'):
                match = re.fullmatch(r'\.catch(?: (L[^;]+;)|all) \{(:\w+) \.\. (:\w+)\} (:\w+)', line)
                if not match: raise Unsupported('bad catch: ' + line)
                catches.append(match.groups()); continue
            if not line or line.startswith(('.', '#')): continue
            op = line.split()[0]
            if op not in OPS: raise Unsupported('unsupported opcode: ' + op)
            code.append({'op': op, 'text': line, 'line': i + 1, 'offset': offset, 'java_line': java_line})
        if registers is None: raise Unsupported('registers missing')
        words = (0 if ' static ' in lines[start] else 1) + sum(2 if t in ('J', 'D') else 1 for t in arg_types(signature))
        if words > registers: raise Unsupported('invalid register count')
        for _, lo, hi, handler in catches:
            if any(label not in labels for label in (lo, hi, handler)): raise Unsupported('unknown catch label')
        return cls(signature, source, registers, words, code, labels, catches)


class VM:
    def __init__(self, invoke, hierarchy=None, max_steps=20000):
        self.invoke = invoke
        self.hierarchy = hierarchy or {}
        self.max_steps = max_steps
        self.trace = []
        self.monitors = {}

    def instance_of(self, value, expected):
        if is_null(value): return True
        if isinstance(value, JavaFault): kind = value.kind
        elif isinstance(value, Obj): kind = value.kind
        elif isinstance(value, str): kind = 'Ljava/lang/String;'
        else: raise Unsupported('unmodelled cast value')
        while kind:
            if kind == expected: return True
            kind = self.hierarchy.get(kind)
        return False

    def run(self, method, words):
        if len(words) != method.param_words: raise Unsupported('wrong parameter word count')
        regs = [0] * method.registers
        if words: regs[-len(words):] = words
        def index(name):
            name = name.strip()
            if not re.fullmatch('[vp][0-9]+', name): raise Unsupported('bad register: ' + name)
            n = int(name[1:]) + (method.registers - method.param_words if name[0] == 'p' else 0)
            if n < 0 or n >= len(regs): raise Unsupported('register out of bounds')
            return n
        def get(name): return regs[index(name)]
        def put(name, value): regs[index(name)] = value
        def target(label):
            if label not in method.labels: raise Unsupported('unknown label: ' + label)
            return method.labels[label]
        pc, result, pending = 0, None, None
        while pc < len(method.code):
            if len(self.trace) >= self.max_steps: raise Unsupported('instruction limit reached')
            ins = method.code[pc]
            row = dict(ins, source=method.source, method=method.signature)
            self.trace.append(row)
            op = ins['op']
            rest = ins['text'][len(op):].strip()
            parts = [p.strip() for p in rest.split(',')]
            next_pc = pc + 1
            try:
                if op in ('const-string', 'const-string/jumbo'):
                    register, literal = rest.split(',', 1)
                    put(register, ast.literal_eval(literal.strip()))
                elif op.startswith('const'):
                    put(parts[0], int(parts[1], 0))
                    if op == 'const-wide/16': regs[index(parts[0]) + 1] = 0
                elif op == 'new-instance': put(parts[0], Obj(parts[1]))
                elif op == 'new-array': put(parts[0], Obj(parts[2], {'items': [0] * get(parts[1])}))
                elif op.startswith('move-result'): put(rest, result)
                elif op == 'move-exception': put(rest, pending)
                elif op.startswith('move'): put(parts[0], get(parts[1]))
                elif op.startswith(('iget', 'iput')):
                    obj = get(parts[1]); name = parts[2].split('->')[1]
                    if is_null(obj): raise JavaFault('Ljava/lang/NullPointerException;', 'field on null')
                    if not isinstance(obj, Obj): raise Unsupported('field receiver is not object')
                    if op.startswith('iget'): put(parts[0], obj.fields.get(name, 0))
                    else: obj.fields[name] = get(parts[0])
                elif op == 'check-cast':
                    if not self.instance_of(get(parts[0]), parts[1]):
                        raise JavaFault('Ljava/lang/ClassCastException;', getattr(get(parts[0]), 'kind', '?') + ' cannot cast to ' + parts[1])
                elif op.startswith('invoke-'):
                    match = re.fullmatch(r'\{([^}]*)\}, (L[^;]+;->\S+)', rest)
                    if not match: raise Unsupported('bad invocation: ' + rest)
                    names, callee = match.groups()
                    if '..' in names:
                        lo, hi = [index(v) for v in names.split('..')]
                        values = regs[lo:hi + 1]
                    else: values = [get(v) for v in names.split(',') if v.strip()]
                    types = ([] if op.startswith('invoke-static') else ['receiver']) + arg_types(callee)
                    logical, pos = [], 0
                    for typ in types:
                        if pos >= len(values): raise Unsupported('short invoke args')
                        logical.append(values[pos]); pos += 2 if typ in ('J', 'D') else 1
                    if pos != len(values): raise Unsupported('extra invoke args')
                    if types and types[0] == 'receiver' and is_null(logical[0]):
                        raise JavaFault('Ljava/lang/NullPointerException;', 'invoke on null')
                    if self.invoke is None: raise Unsupported('no adapter for ' + callee)
                    result = self.invoke(callee, logical, self)
                elif op.startswith('if-'):
                    a = get(parts[0]); b = 0 if op.endswith('z') else get(parts[1])
                    cmp = op[3:]; cmp = cmp[:-1] if cmp.endswith('z') else cmp
                    conditions = {'eq': lambda: equal(a, b), 'ne': lambda: not equal(a, b),
                                  'ge': lambda: a >= b, 'lt': lambda: a < b, 'le': lambda: a <= b}
                    if conditions[cmp](): next_pc = target(parts[-1])
                elif op.startswith('goto'): next_pc = target(rest)
                elif op == 'add-int/lit8': put(parts[0], get(parts[1]) + int(parts[2], 0))
                elif op == 'or-int/lit8': put(parts[0], get(parts[1]) | int(parts[2], 0))
                elif op.startswith('monitor-'):
                    obj = get(rest)
                    if is_null(obj): raise JavaFault('Ljava/lang/NullPointerException;', 'null monitor')
                    key = id(obj); count = self.monitors.get(key, 0)
                    if op == 'monitor-exit' and count == 0: raise Unsupported('unbalanced monitor')
                    self.monitors[key] = count + (1 if op == 'monitor-enter' else -1)
                elif op == 'throw':
                    value = get(rest)
                    if not isinstance(value, JavaFault): raise Unsupported('throw value not modelled exception')
                    raise value
                elif op.startswith('return'): return None if op == 'return-void' else get(rest)
                else: raise Unsupported('opcode not implemented: ' + op)
            except JavaFault as exc:
                row['java_fault'] = exc.kind
                handler = next((label for kind, lo, hi, label in method.catches
                                if target(lo) <= pc < target(hi) and (kind is None or self.instance_of(exc, kind))), None)
                if handler is None: raise
                row['handler'] = handler
                pending = exc; next_pc = target(handler)
            pc = next_pc
        raise Unsupported('fell off method')
