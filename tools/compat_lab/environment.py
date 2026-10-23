"""Explicit host adapters. /data and /system are strings in a JSON state ONLY.

No system calls, Binder, native backup, package scanner or Android rendering are
executed. Settings and package cleanup are deliberately simplified fault fixtures.
"""
import copy
import json
from .vm import VM, Obj, JavaFault, Unsupported, PowerCut, is_null

INSTALL = '/data/backup/install.tta'
SSBOOT = '/data/backup/ssboot.tta'
PM = 'Lcom/android/server/pm/PackageManagerService;'
PI = 'Landroid/content/pm/PackageItemInfo;'
DRAW = 'Landroid/graphics/drawable/'


def string(value):
    if isinstance(value, Obj) and value.kind == 'Ljava/lang/String;': return value.fields['value']
    if isinstance(value, str): return value
    if is_null(value): return 'null'
    if isinstance(value, (int, bool)): return str(int(value))
    raise Unsupported('unmodelled Java string conversion')


class Environment:
    def __init__(self, methods, hierarchy, state=None, fault=None, icon_tag='layer-list', icon_id=0):
        self.methods = methods
        self.state = copy.deepcopy(state if state is not None else {
            'files': [], 'dirs': ['/data/app', '/data/app-private', '/system/app'],
            'incomplete': [], 'temporary': [], 'settings_writes': 0})
        self.fault = fault
        self.events, self.adapters = [], set()
        self.icon_tag, self.icon_id = icon_tag, icon_id
        self.vm = VM(self.invoke, hierarchy)
        self.api = {}
        self.ram_incomplete = []
        self.resources = Obj('Landroid/content/res/Resources;')
        self.pm = Obj(PM, {'mInstallLock:Ljava/lang/Object;': Obj('Ljava/lang/Object;'),
                          'mPackages:Ljava/util/HashMap;': Obj('Ljava/util/HashMap;'),
                          'mSettings:Lcom/android/server/pm/Settings;': Obj('Lcom/android/server/pm/Settings;'),
                          'mAddedPackageList:Ljava/util/ArrayList;': []})
        self._register()

    def event(self, name, **details): self.events.append(dict(event=name, **details))

    def bind(self, signature, function): self.api[signature] = function

    def invoke(self, signature, args, vm):
        if signature not in self.api: raise Unsupported('no explicit adapter: ' + signature)
        self.adapters.add(signature)
        return self.api[signature](*args)

    def run(self, name, args): return self.vm.run(self.methods[name], args)

    def _register(self):
        b = self.bind
        b('Ljava/lang/String;-><init>(Ljava/lang/String;)V', lambda o, v: o.fields.update(value=string(v)))
        b('Ljava/lang/String;->length()I', lambda s: len(string(s)))
        b('Ljava/lang/String;->substring(II)Ljava/lang/String;', lambda s, a, z: string(s)[a:z])
        b('Ljava/lang/String;->equals(Ljava/lang/Object;)Z', lambda a, z: int((isinstance(z, str) or isinstance(z, Obj) and z.kind == 'Ljava/lang/String;') and string(a) == string(z)))
        b('Ljava/lang/Object;->toString()Ljava/lang/String;', string)
        b('Ljava/lang/StringBuilder;-><init>()V', lambda o: o.fields.update(value=''))
        def append(o, value): o.fields['value'] += string(value); return o
        for typ in ('Ljava/lang/String;', 'Ljava/lang/Object;', 'I'):
            b('Ljava/lang/StringBuilder;->append(' + typ + ')Ljava/lang/StringBuilder;', append)
        b('Ljava/lang/StringBuilder;->toString()Ljava/lang/String;', lambda o: o.fields['value'])
        for owner in ('Log', 'Slog'):
            for level in ('d', 'i', 'w', 'e', 'v'):
                b('Landroid/util/' + owner + ';->' + level + '(Ljava/lang/String;Ljava/lang/String;)I',
                  lambda tag, message, level=level: self.log(tag, message, level))
        b('Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I',
          lambda tag, msg, exc: self.log(tag, msg, 'e'))
        b('Ljava/lang/Throwable;->printStackTrace()V', lambda exc: self.event('java_printStackTrace', kind=exc.kind))
        b('Ljava/io/File;-><init>(Ljava/lang/String;)V', lambda o, path: o.fields.update(path=string(path)))
        b('Ljava/io/File;->exists()Z', lambda o: int(o.fields['path'] in self.state['files'] + self.state['dirs']))
        b('Ljava/io/File;->getPath()Ljava/lang/String;', lambda o: o.fields['path'])
        b('Ljava/io/File;->createNewFile()Z', self.create)
        b('Ljava/io/File;->delete()Z', self.delete)
        for name in ('setReadable', 'setWritable', 'setExecutable'):
            b('Ljava/io/File;->' + name + '(ZZ)Z',
              lambda o, value, owner, name=name: self.permission(o, name, value, owner))
        def tokenize(o, value, delimiter):
            if string(delimiter) != ' ': raise Unsupported('only space tokenizer modelled')
            o.fields['tokens'] = [x for x in string(value).split(' ') if x]
        b('Ljava/util/StringTokenizer;-><init>(Ljava/lang/String;Ljava/lang/String;)V', tokenize)
        b('Ljava/util/StringTokenizer;->hasMoreTokens()Z', lambda o: int(bool(o.fields['tokens'])))
        b('Ljava/util/StringTokenizer;->nextToken()Ljava/lang/String;', lambda o: o.fields['tokens'].pop(0))
        b('Ljava/util/ArrayList;->size()I', len)
        b('Ljava/util/ArrayList;->get(I)Ljava/lang/Object;', lambda o, i: o[i])
        b('Ljava/util/HashMap;->get(Ljava/lang/Object;)Ljava/lang/Object;', lambda o, key: o.fields.get('map', {}).get(key, 0))
        def map_put(o, key, value):
            mapping = o.fields.setdefault('map', {}); prior = mapping.get(key, 0); mapping[key] = value; return prior
        b('Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;', map_put)
        b('Lcom/android/server/pm/Settings;->readLPw(Ljava/util/List;)Z', self.read_settings)
        b('Lcom/android/server/pm/Settings;->getListOfIncompleteInstallPackagesLPr()Ljava/util/ArrayList;',
          lambda o: [Obj('Lcom/android/server/pm/PackageSetting;', {'name': name}) for name in self.ram_incomplete])
        b('Lcom/android/server/pm/Settings;->writeLPr()V', self.write_settings)
        b(PM + '->cleanupInstallFailedPackage(Lcom/android/server/pm/PackageSetting;)V', self.cleanup)
        b(PM + '->deleteTempPackageFiles()V', self.cleanup_temporary)
        b(PM + '->scanDirWithB(Ljava/io/File;IIJ)Z', self.scan)
        b('Lcom/sony/jp/androidsystemstateservice/AndroidSystemStateService;->resume()Z',
          lambda o: self.event('systemstate_resume_stub') or 1)
        def service(name):
            if name != 'package': raise Unsupported('unknown Binder service')
            self.event('binder_package_stub'); return self.pm
        b('Landroid/os/ServiceManager;->getService(Ljava/lang/String;)Landroid/os/IBinder;', service)
        b('Landroid/content/pm/IPackageManager$Stub;->asInterface(Landroid/os/IBinder;)Landroid/content/pm/IPackageManager;', lambda o: o)
        b('Landroid/content/pm/IPackageManager;->syncAppsFromFilesystemToRam(Ljava/lang/String;)Z', self.sync)
        b('Lcom/sony/scalar/dlsys/scalaralauncher/IconCache$CacheEntry;-><init>(Lcom/sony/scalar/dlsys/scalaralauncher/IconCache$1;)V', lambda o, unused: None)
        b('Landroid/content/pm/PackageManager;->getResourcesForActivity(Landroid/content/ComponentName;)Landroid/content/res/Resources;', lambda o, component: self.resources)
        b('Landroid/content/pm/PackageManager;->getResourcesForApplication(Landroid/content/pm/ApplicationInfo;)Landroid/content/res/Resources;', lambda o, app: self.resources)
        b('Landroid/content/res/Resources;->getText(I)Ljava/lang/CharSequence;', lambda o, rid: 'CineVista fixture label')
        b(PI + '->loadIcon(Landroid/content/pm/PackageManager;)Landroid/graphics/drawable/Drawable;', lambda item, pm: self.run('load_icon', [item, pm]))
        def application_info(item):
            return item.fields.get('applicationInfo:Landroid/content/pm/ApplicationInfo;', item)
        b(PI + '->getApplicationInfo()Landroid/content/pm/ApplicationInfo;', application_info)
        def default_icon(item, pm):
            if item.kind != 'Landroid/content/pm/ActivityInfo;': raise Unsupported('application default icon not modelled')
            return self.run('default_icon', [item, pm])
        b(PI + '->loadDefaultIcon(Landroid/content/pm/PackageManager;)Landroid/graphics/drawable/Drawable;', default_icon)
        b('Landroid/content/pm/PackageManager;->getDrawable(Ljava/lang/String;ILandroid/content/pm/ApplicationInfo;)Landroid/graphics/drawable/Drawable;', self.get_drawable)
        b('Lorg/xmlpull/v1/XmlPullParser;->getName()Ljava/lang/String;', lambda o: o.fields['tag'])
        b(DRAW + 'LayerDrawable;-><init>()V', lambda o: None)
        # Only the exercised XML layer-list constructor is modelled; other tags
        # deliberately stop at their first missing external call.
        b(DRAW + 'Drawable;->inflate(Landroid/content/res/Resources;Lorg/xmlpull/v1/XmlPullParser;Landroid/util/AttributeSet;)V',
          lambda *args: self.event('drawable_children_inflate_stub', assumption='inflation succeeds; pixels not rendered'))
        b(DRAW + 'BitmapDrawable;->getBitmap()Landroid/graphics/Bitmap;', lambda o: Obj('Landroid/graphics/Bitmap;'))

    def log(self, tag, message, level):
        self.event('log', tag=string(tag), message=string(message), level=level); return 0

    def create(self, obj):
        path = obj.fields['path']; self.event('file_create', path=path)
        if self.fault == 'create_io': raise JavaFault('Ljava/io/IOException;', 'injected create failure')
        if path in self.state['files']: return 0
        self.state['files'].append(path); return 1

    def permission(self, obj, mode, value, owner):
        self.event('file_permission_stub', path=obj.fields['path'], mode=mode, value=value, owner_only=owner)
        return 1

    def delete(self, obj):
        path = obj.fields['path']; self.event('file_delete_attempt', path=path)
        if self.fault == 'cut_before_delete': raise PowerCut('injected process loss before File.delete')
        if self.fault == 'delete_false': self.event('file_delete_return', value=False); return 0
        existed = path in self.state['files']
        if existed: self.state['files'].remove(path)
        self.event('file_delete_return', value=existed); return int(existed)

    def read_settings(self, obj, users):
        self.event('settings_read_stub')
        if self.fault == 'read_io': raise JavaFault('Ljava/io/IOException;', 'injected Settings failure')
        self.ram_incomplete = list(self.state['incomplete']); return 1

    def write_settings(self, obj):
        self.event('settings_write_stub')
        if self.fault == 'write_io': raise JavaFault('Ljava/io/IOException;', 'injected Settings failure')
        self.state['incomplete'] = list(self.ram_incomplete)
        self.state['settings_writes'] += 1

    def cleanup(self, obj, package):
        name = package.fields['name']; self.event('cleanup_failed_package_stub', package=name)
        self.ram_incomplete.remove(name)

    def cleanup_temporary(self, obj):
        self.event('cleanup_temporary_stub', files=list(self.state['temporary']))
        self.state['temporary'] = []

    def scan(self, obj, directory, flags, mode, time):
        result = self.fault != 'scan_false'
        self.event('scan_directory_stub', path=directory.fields['path'], parse_flags=flags,
                   scan_flags=mode, time=time, result=result, added_packages=[])
        # No parsing, backup/native reads or package additions are claimed here.
        return int(result)

    def sync(self, obj, paths):
        if self.fault == 'binder_remote': raise JavaFault('Landroid/os/RemoteException;', 'injected Binder failure')
        result = self.run('sync', [obj, paths]); self.event('sync_return', value=result); return result

    def resume(self, mode=8):
        service = Obj('Lcom/android/server/SyncAndroidService;', {
            'systemstateservice:Lcom/sony/jp/androidsystemstateservice/AndroidSystemStateService;':
                Obj('Lcom/sony/jp/androidsystemstateservice/AndroidSystemStateService;')})
        return self.run('resume', [service, mode])

    def stamp(self): return self.run('stamp', [Obj('Lcom/sony/scalar/dlsys/scalarainstaller/InstallAppProgress;')])

    def get_drawable(self, pm, package, rid, app):
        if rid != self.icon_id: raise Unsupported('unexpected icon resource')
        if self.icon_tag == 'png_control':
            self.event('png_decode_stub', assumption='valid direct PNG returns BitmapDrawable')
            return Obj(DRAW + 'BitmapDrawable;')
        self.event('resource_lookup_stub', resource_id=rid, xml_root=self.icon_tag)
        return self.run('xml_drawable', [self.resources, Obj('Lorg/xmlpull/v1/XmlPullParser;', {'tag': self.icon_tag}), Obj('Landroid/util/AttributeSet;')])

    def icon(self):
        app = Obj('Landroid/content/pm/ApplicationInfo;', {'icon:I': self.icon_id, 'packageName:Ljava/lang/String;': 'org.cinevista.probe'})
        activity = Obj('Landroid/content/pm/ActivityInfo;', {'icon:I': 0, 'applicationInfo:Landroid/content/pm/ApplicationInfo;': app,
                       'name:Ljava/lang/String;': 'org.cinevista.probe.MainActivity'})
        cache = Obj('Lcom/sony/scalar/dlsys/scalaralauncher/IconCache;', {
            'mCache:Ljava/util/HashMap;': Obj('Ljava/util/HashMap;'),
            'mPackageManager:Landroid/content/pm/PackageManager;': Obj('Landroid/content/pm/PackageManager;')})
        info = Obj('Landroid/content/pm/ResolveInfo;', {'activityInfo:Landroid/content/pm/ActivityInfo;': activity})
        return self.run('cache', [cache, 'org.cinevista.probe/MainActivity', info])

    def snapshot(self): return json.loads(json.dumps(self.state))
