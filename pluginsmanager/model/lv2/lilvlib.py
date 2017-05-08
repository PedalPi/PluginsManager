"""
File copy from https://github.com/moddevices/lilvlib
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------------------------------------
# Imports

import json
import lilv
import os

from math import fmod

# ------------------------------------------------------------------------------------------------------------
# Utilities

def LILV_FOREACH(collection, func):
    itr = collection.begin()
    while itr:
        yield func(collection.get(itr))
        itr = collection.next(itr)

class NS(object):
    def __init__(self, world, base):
        self.world = world
        self.base = base
        self._cache = {}

    def __getattr__(self, attr):
        if attr.endswith("_"):
            attr = attr[:-1]
        if attr not in self._cache:
            self._cache[attr] = lilv.Node(self.world.new_uri(self.base+attr))
        return self._cache[attr]

def is_integer(string):
    return string.strip().lstrip("-+").isdigit()

def get_short_port_name(portName):
    if len(portName) <= 16:
        return portName

    portName = portName.split("/",1)[0].split(" (",1)[0].split(" [",1)[0].strip()

    # cut stuff if too big
    if len(portName) > 16:
        portName = portName[0] + portName[1:].replace("a","").replace("e","").replace("i","").replace("o","").replace("u","")

        if len(portName) > 16:
            portName = portName[:16]

    return portName.strip()

# ------------------------------------------------------------------------------------------------------------

def get_category(nodes):
    lv2_category_indexes = {
        'DelayPlugin': ['Delay'],
        'DistortionPlugin': ['Distortion'],
        'WaveshaperPlugin': ['Distortion', 'Waveshaper'],
        'DynamicsPlugin': ['Dynamics'],
        'AmplifierPlugin': ['Dynamics', 'Amplifier'],
        'CompressorPlugin': ['Dynamics', 'Compressor'],
        'ExpanderPlugin': ['Dynamics', 'Expander'],
        'GatePlugin': ['Dynamics', 'Gate'],
        'LimiterPlugin': ['Dynamics', 'Limiter'],
        'FilterPlugin': ['Filter'],
        'AllpassPlugin': ['Filter', 'Allpass'],
        'BandpassPlugin': ['Filter', 'Bandpass'],
        'CombPlugin': ['Filter', 'Comb'],
        'EQPlugin': ['Filter', 'Equaliser'],
        'MultiEQPlugin': ['Filter', 'Equaliser', 'Multiband'],
        'ParaEQPlugin': ['Filter', 'Equaliser', 'Parametric'],
        'HighpassPlugin': ['Filter', 'Highpass'],
        'LowpassPlugin': ['Filter', 'Lowpass'],
        'GeneratorPlugin': ['Generator'],
        'ConstantPlugin': ['Generator', 'Constant'],
        'InstrumentPlugin': ['Generator', 'Instrument'],
        'OscillatorPlugin': ['Generator', 'Oscillator'],
        'ModulatorPlugin': ['Modulator'],
        'ChorusPlugin': ['Modulator', 'Chorus'],
        'FlangerPlugin': ['Modulator', 'Flanger'],
        'PhaserPlugin': ['Modulator', 'Phaser'],
        'ReverbPlugin': ['Reverb'],
        'SimulatorPlugin': ['Simulator'],
        'SpatialPlugin': ['Spatial'],
        'SpectralPlugin': ['Spectral'],
        'PitchPlugin': ['Spectral', 'Pitch Shifter'],
        'UtilityPlugin': ['Utility'],
        'AnalyserPlugin': ['Utility', 'Analyser'],
        'ConverterPlugin': ['Utility', 'Converter'],
        'FunctionPlugin': ['Utility', 'Function'],
        'MixerPlugin': ['Utility', 'Mixer'],
        #'MIDIPlugin': ['MIDI', 'Utility'],
    }
    mod_category_indexes = {
        'DelayPlugin': ['Delay'],
        'DistortionPlugin': ['Distortion'],
        'DynamicsPlugin': ['Dynamics'],
        'FilterPlugin': ['Filter'],
        'GeneratorPlugin': ['Generator'],
        'ModulatorPlugin': ['Modulator'],
        'ReverbPlugin': ['Reverb'],
        'SimulatorPlugin': ['Simulator'],
        'SpatialPlugin': ['Spatial'],
        'SpectralPlugin': ['Spectral'],
        'UtilityPlugin': ['Utility'],
        'MIDIPlugin': ['Utility', 'MIDI'],
    }

    def fill_in_lv2_category(node):
        category = node.as_string().replace("http://lv2plug.in/ns/lv2core#","")
        if category in lv2_category_indexes.keys():
            return lv2_category_indexes[category]
        return []

    def fill_in_mod_category(node):
        category = node.as_string().replace("http://moddevices.com/ns/mod#","")
        if category in mod_category_indexes.keys():
            return mod_category_indexes[category]
        return []

    categories = []
    for cat in [cat for catlist in LILV_FOREACH(nodes, fill_in_mod_category) for cat in catlist]:
        if cat not in categories:
            categories.append(cat)

    if len(categories) > 0:
        return categories

    for cat in [cat for catlist in LILV_FOREACH(nodes, fill_in_lv2_category) for cat in catlist]:
        if cat not in categories:
            categories.append(cat)

    return categories

def get_port_data(port, subj):
    nodes = port.get_value(subj.me)
    data  = []

    it = lilv.lilv_nodes_begin(nodes)
    while not lilv.lilv_nodes_is_end(nodes, it):
        dat = lilv.lilv_nodes_get(nodes, it)
        it  = lilv.lilv_nodes_next(nodes, it)
        if dat is None:
            continue
        data.append(lilv.lilv_node_as_string(dat))

    return data

def get_port_unit(miniuri):
  # using label, render, symbol
  units = {
      's': ["seconds", "%f s", "s"],
      'ms': ["milliseconds", "%f ms", "ms"],
      'min': ["minutes", "%f mins", "min"],
      'bar': ["bars", "%f bars", "bars"],
      'beat': ["beats", "%f beats", "beats"],
      'frame': ["audio frames", "%f frames", "frames"],
      'm': ["metres", "%f m", "m"],
      'cm': ["centimetres", "%f cm", "cm"],
      'mm': ["millimetres", "%f mm", "mm"],
      'km': ["kilometres", "%f km", "km"],
      'inch': ["inches", """%f\"""", "in"],
      'mile': ["miles", "%f mi", "mi"],
      'db': ["decibels", "%f dB", "dB"],
      'pc': ["percent", "%f%%", "%"],
      'coef': ["coefficient", "* %f", "*"],
      'hz': ["hertz", "%f Hz", "Hz"],
      'khz': ["kilohertz", "%f kHz", "kHz"],
      'mhz': ["megahertz", "%f MHz", "MHz"],
      'bpm': ["beats per minute", "%f BPM", "BPM"],
      'oct': ["octaves", "%f octaves", "oct"],
      'cent': ["cents", "%f ct", "ct"],
      'semitone12TET': ["semitones", "%f semi", "semi"],
      'degree': ["degrees", "%f deg", "deg"],
      'midiNote': ["MIDI note", "MIDI note %d", "note"],
  }
  if miniuri in units.keys():
      return units[miniuri]
  return ("","","")

# ------------------------------------------------------------------------------------------------------------
# get_bundle_dirname

def get_bundle_dirname(bundleuri):
    bundle = lilv.lilv_uri_to_path(bundleuri)

    if not os.path.exists(bundle):
        raise IOError(bundleuri)
    if os.path.isfile(bundle):
        bundle = os.path.dirname(bundle)

    return bundle

# ------------------------------------------------------------------------------------------------------------
# get_pedalboard_info

# Get info from an lv2 bundle
# @a bundle is a string, consisting of a directory in the filesystem (absolute pathname).
def get_pedalboard_info(bundle):
    # lilv wants the last character as the separator
    bundle = os.path.abspath(bundle)
    if not bundle.endswith(os.sep):
        bundle += os.sep

    # Create our own unique lilv world
    # We'll load a single bundle and get all plugins from it
    world = lilv.World()

    # this is needed when loading specific bundles instead of load_all
    # (these functions are not exposed via World yet)
    lilv.lilv_world_load_specifications(world.me)
    lilv.lilv_world_load_plugin_classes(world.me)

    # convert bundle string into a lilv node
    bundlenode = lilv.lilv_new_file_uri(world.me, None, bundle)

    # load the bundle
    world.load_bundle(bundlenode)

    # free bundlenode, no longer needed
    lilv.lilv_node_free(bundlenode)

    # get all plugins in the bundle
    plugins = world.get_all_plugins()

    # make sure the bundle includes 1 and only 1 plugin (the pedalboard)
    if plugins.size() != 1:
        raise Exception('get_pedalboard_info(%s) - bundle has 0 or > 1 plugin'.format(bundle))

    # no indexing in python-lilv yet, just get the first item
    plugin = None
    for p in plugins:
        plugin = p
        break

    if plugin is None:
        raise Exception('get_pedalboard_info(%s) - failed to get plugin, you are using an old lilv!'.format(bundle))

    # define the needed stuff
    ns_rdf      = NS(world, lilv.LILV_NS_RDF)
    ns_lv2core  = NS(world, lilv.LILV_NS_LV2)
    ns_ingen    = NS(world, "http://drobilla.net/ns/ingen#")
    ns_mod      = NS(world, "http://moddevices.com/ns/mod#")
    ns_modpedal = NS(world, "http://moddevices.com/ns/modpedal#")

    # check if the plugin is a pedalboard
    def fill_in_type(node):
        return node.as_string()
    plugin_types = [i for i in LILV_FOREACH(plugin.get_value(ns_rdf.type_), fill_in_type)]

    if "http://moddevices.com/ns/modpedal#Pedalboard" not in plugin_types:
        raise Exception('get_pedalboard_info(%s) - plugin has no mod:Pedalboard type'.format(bundle))

    # let's get all the info now
    ingenarcs   = []
    ingenblocks = []

    info = {
        'name'  : plugin.get_name().as_string(),
        'uri'   : plugin.get_uri().as_string(),
        'author': plugin.get_author_name().as_string() or "", # Might be empty
        'hardware': {
            # we save this info later
            'audio': {
                'ins' : 0,
                'outs': 0
             },
            'cv': {
                'ins' : 0,
                'outs': 0
             },
            'midi': {
                'ins' : 0,
                'outs': 0
             }
        },
        'size': {
            'width' : plugin.get_value(ns_modpedal.width).get_first().as_int(),
            'height': plugin.get_value(ns_modpedal.height).get_first().as_int(),
        },
        'screenshot' : os.path.basename(plugin.get_value(ns_modpedal.screenshot).get_first().as_string() or ""),
        'thumbnail'  : os.path.basename(plugin.get_value(ns_modpedal.thumbnail).get_first().as_string() or ""),
        'connections': [], # we save this info later
        'plugins'    : []  # we save this info later
    }

    # connections
    arcs = plugin.get_value(ns_ingen.arc)
    it = arcs.begin()
    while not arcs.is_end(it):
        arc = arcs.get(it)
        it  = arcs.next(it)

        if arc.me is None:
            continue

        head = lilv.lilv_world_get(world.me, arc.me, ns_ingen.head.me, None)
        tail = lilv.lilv_world_get(world.me, arc.me, ns_ingen.tail.me, None)

        if head is None or tail is None:
            continue

        ingenarcs.append({
            "source": lilv.lilv_uri_to_path(lilv.lilv_node_as_string(tail)).replace(bundle,"",1),
            "target": lilv.lilv_uri_to_path(lilv.lilv_node_as_string(head)).replace(bundle,"",1)
        })

    # hardware ports
    handled_port_uris = []
    ports = plugin.get_value(ns_lv2core.port)
    it = ports.begin()
    while not ports.is_end(it):
        port = ports.get(it)
        it   = ports.next(it)

        if port.me is None:
            continue

        # check if we already handled this port
        port_uri = port.as_uri()
        if port_uri in handled_port_uris:
            continue
        if port_uri.endswith("/control_in") or port_uri.endswith("/control_out"):
            continue
        handled_port_uris.append(port_uri)

        # get types
        port_types = lilv.lilv_world_find_nodes(world.me, port.me, ns_rdf.type_.me, None)

        if port_types is None:
            continue

        portDir  = "" # input or output
        portType = "" # atom, audio or cv

        it2 = lilv.lilv_nodes_begin(port_types)
        while not lilv.lilv_nodes_is_end(port_types, it2):
            port_type = lilv.lilv_nodes_get(port_types, it2)
            it2 = lilv.lilv_nodes_next(port_types, it2)

            if port_type is None:
                continue

            port_type_uri = lilv.lilv_node_as_uri(port_type)

            if port_type_uri == "http://lv2plug.in/ns/lv2core#InputPort":
                portDir = "input"
            elif port_type_uri == "http://lv2plug.in/ns/lv2core#OutputPort":
                portDir = "output"
            elif port_type_uri == "http://lv2plug.in/ns/lv2core#AudioPort":
                portType = "audio"
            elif port_type_uri == "http://lv2plug.in/ns/lv2core#CVPort":
                portType = "cv"
            elif port_type_uri == "http://lv2plug.in/ns/ext/atom#AtomPort":
                portType = "atom"

        if not (portDir or portType):
            continue

        if portType == "audio":
            if portDir == "input":
                info['hardware']['audio']['ins'] += 1
            else:
                info['hardware']['audio']['outs'] += 1

        elif portType == "atom":
            if portDir == "input":
                info['hardware']['midi']['ins'] += 1
            else:
                info['hardware']['midi']['outs'] += 1

        elif portType == "cv":
            if portDir == "input":
                info['hardware']['cv']['ins'] += 1
            else:
                info['hardware']['cv']['outs'] += 1

    # plugins
    blocks = plugin.get_value(ns_ingen.block)
    it = blocks.begin()
    while not blocks.is_end(it):
        block = blocks.get(it)
        it    = blocks.next(it)

        if block.me is None:
            continue

        protouri1 = lilv.lilv_world_get(world.me, block.me, ns_lv2core.prototype.me, None)
        protouri2 = lilv.lilv_world_get(world.me, block.me, ns_ingen.prototype.me, None)

        if protouri1 is not None:
            proto = protouri1
        elif protouri2 is not None:
            proto = protouri2
        else:
            continue

        instance = lilv.lilv_uri_to_path(lilv.lilv_node_as_string(block.me)).replace(bundle,"",1)
        uri      = lilv.lilv_node_as_uri(proto)

        enabled  = lilv.lilv_world_get(world.me, block.me, ns_ingen.enabled.me, None)
        builder  = lilv.lilv_world_get(world.me, block.me, ns_mod.builderVersion.me, None)
        release  = lilv.lilv_world_get(world.me, block.me, ns_mod.releaseNumber.me, None)
        minorver = lilv.lilv_world_get(world.me, block.me, ns_lv2core.minorVersion.me, None)
        microver = lilv.lilv_world_get(world.me, block.me, ns_lv2core.microVersion.me, None)

        ingenblocks.append({
            "instance": instance,
            "uri"     : uri,
            "x"       : lilv.lilv_node_as_float(lilv.lilv_world_get(world.me, block.me, ns_ingen.canvasX.me, None)),
            "y"       : lilv.lilv_node_as_float(lilv.lilv_world_get(world.me, block.me, ns_ingen.canvasY.me, None)),
            "enabled" : lilv.lilv_node_as_bool(enabled) if enabled is not None else False,
            "builder" : lilv.lilv_node_as_int(builder) if builder else 0,
            "release" : lilv.lilv_node_as_int(release) if release else 0,
            "minorVersion": lilv.lilv_node_as_int(minorver) if minorver else 0,
            "microVersion": lilv.lilv_node_as_int(microver) if microver else 0,
        })

    info['connections'] = ingenarcs
    info['plugins']     = ingenblocks

    return info

# ------------------------------------------------------------------------------------------------------------
# get_pedalboard_name

# Faster version of get_pedalboard_info when we just need to know the pedalboard name
# @a bundle is a string, consisting of a directory in the filesystem (absolute pathname).
def get_pedalboard_name(bundle):
    # lilv wants the last character as the separator
    bundle = os.path.abspath(bundle)
    if not bundle.endswith(os.sep):
        bundle += os.sep

    # Create our own unique lilv world
    # We'll load a single bundle and get all plugins from it
    world = lilv.World()

    # this is needed when loading specific bundles instead of load_all
    # (these functions are not exposed via World yet)
    lilv.lilv_world_load_specifications(world.me)
    lilv.lilv_world_load_plugin_classes(world.me)

    # convert bundle string into a lilv node
    bundlenode = lilv.lilv_new_file_uri(world.me, None, bundle)

    # load the bundle
    world.load_bundle(bundlenode)

    # free bundlenode, no longer needed
    lilv.lilv_node_free(bundlenode)

    # get all plugins in the bundle
    plugins = world.get_all_plugins()

    # make sure the bundle includes 1 and only 1 plugin (the pedalboard)
    if plugins.size() != 1:
        raise Exception('get_pedalboard_info(%s) - bundle has 0 or > 1 plugin'.format(bundle))

    # no indexing in python-lilv yet, just get the first item
    plugin = None
    for p in plugins:
        plugin = p
        break

    if plugin is None:
        raise Exception('get_pedalboard_info(%s) - failed to get plugin, you are using an old lilv!'.format(bundle))

    # define the needed stuff
    ns_rdf = NS(world, lilv.LILV_NS_RDF)

    # check if the plugin is a pedalboard
    def fill_in_type(node):
        return node.as_string()
    plugin_types = [i for i in LILV_FOREACH(plugin.get_value(ns_rdf.type_), fill_in_type)]

    if "http://moddevices.com/ns/modpedal#Pedalboard" not in plugin_types:
        raise Exception('get_pedalboard_info(%s) - plugin has no mod:Pedalboard type'.format(bundle))

    return plugin.get_name().as_string()

# ------------------------------------------------------------------------------------------------------------
# plugin_has_modgui

# Check if a plugin has modgui
def plugin_has_modgui(world, plugin):
    # define the needed stuff
    ns_modgui = NS(world, "http://moddevices.com/ns/modgui#")

    # --------------------------------------------------------------------------------------------------------
    # get the proper modgui

    modguigui = None

    nodes = plugin.get_value(ns_modgui.gui)
    it    = nodes.begin()
    while not nodes.is_end(it):
        mgui = nodes.get(it)
        it   = nodes.next(it)
        if mgui.me is None:
            continue
        resdir = world.find_nodes(mgui.me, ns_modgui.resourcesDirectory.me, None).get_first()
        if resdir.me is None:
            continue
        modguigui = mgui
        if os.path.expanduser("~") in lilv.lilv_uri_to_path(resdir.as_string()):
            # found a modgui in the home dir, stop here and use it
            break

    del nodes, it

    # --------------------------------------------------------------------------------------------------------
    # check selected modgui

    if modguigui is None or modguigui.me is None:
        return False

    # resourcesDirectory *must* be present
    modgui_resdir = world.find_nodes(modguigui.me, ns_modgui.resourcesDirectory.me, None).get_first()

    if modgui_resdir.me is None:
        return False

    return os.path.exists(lilv.lilv_uri_to_path(modgui_resdir.as_string()))

# ------------------------------------------------------------------------------------------------------------
# get_plugin_info

# Get info from a lilv plugin
# This is used in get_plugins_info below and MOD-SDK
def get_plugin_info(world, plugin, useAbsolutePath = True):
    # define the needed stuff
    ns_doap    = NS(world, lilv.LILV_NS_DOAP)
    ns_foaf    = NS(world, lilv.LILV_NS_FOAF)
    ns_rdf     = NS(world, lilv.LILV_NS_RDF)
    ns_rdfs    = NS(world, lilv.LILV_NS_RDFS)
    ns_lv2core = NS(world, lilv.LILV_NS_LV2)
    ns_atom    = NS(world, "http://lv2plug.in/ns/ext/atom#")
    ns_midi    = NS(world, "http://lv2plug.in/ns/ext/midi#")
    ns_morph   = NS(world, "http://lv2plug.in/ns/ext/morph#")
    ns_pprops  = NS(world, "http://lv2plug.in/ns/ext/port-props#")
    ns_pset    = NS(world, "http://lv2plug.in/ns/ext/presets#")
    ns_units   = NS(world, "http://lv2plug.in/ns/extensions/units#")
    ns_mod     = NS(world, "http://moddevices.com/ns/mod#")
    ns_modgui  = NS(world, "http://moddevices.com/ns/modgui#")

    bundleuri = plugin.get_bundle_uri().as_string()
    bundle    = lilv.lilv_uri_to_path(bundleuri)

    errors   = []
    warnings = []

    # --------------------------------------------------------------------------------------------------------
    # uri

    uri = plugin.get_uri().as_string() or ""

    if not uri:
        errors.append("plugin uri is missing or invalid")
    elif uri.startswith("file:"):
        errors.append("plugin uri is local, and thus not suitable for redistribution")
    #elif not (uri.startswith("http:") or uri.startswith("https:")):
        #warnings.append("plugin uri is not a real url")

    # --------------------------------------------------------------------------------------------------------
    # name

    name = plugin.get_name().as_string() or ""

    if not name:
        errors.append("plugin name is missing")

    # --------------------------------------------------------------------------------------------------------
    # binary

    binary = lilv.lilv_uri_to_path(plugin.get_library_uri().as_string() or "")

    if not binary:
        errors.append("plugin binary is missing")
    elif not useAbsolutePath:
        binary = binary.replace(bundle,"",1)

    # --------------------------------------------------------------------------------------------------------
    # license

    license = plugin.get_value(ns_doap.license).get_first().as_string() or ""

    if not license:
        prj = plugin.get_value(ns_lv2core.project).get_first()
        if prj.me is not None:
            licsnode = lilv.lilv_world_get(world.me, prj.me, ns_doap.license.me, None)
            if licsnode is not None:
                license = lilv.lilv_node_as_string(licsnode)
            del licsnode
        del prj

    if not license:
        errors.append("plugin license is missing")

    elif license.startswith(bundleuri):
        license = license.replace(bundleuri,"",1)
        warnings.append("plugin license entry is a local path instead of a string")

    # --------------------------------------------------------------------------------------------------------
    # comment

    comment = (plugin.get_value(ns_rdfs.comment).get_first().as_string() or "").strip()

    # sneaky empty comments!
    if len(comment) > 0 and comment == len(comment) * comment[0]:
        comment = ""

    if not comment:
        errors.append("plugin comment is missing")

    # --------------------------------------------------------------------------------------------------------
    # version

    microver = plugin.get_value(ns_lv2core.microVersion).get_first()
    minorver = plugin.get_value(ns_lv2core.minorVersion).get_first()

    if microver.me is None and minorver.me is None:
        errors.append("plugin is missing version information")
        minorVersion = 0
        microVersion = 0

    else:
        if minorver.me is None:
            errors.append("plugin is missing minorVersion")
            minorVersion = 0
        else:
            minorVersion = minorver.as_int()

        if microver.me is None:
            errors.append("plugin is missing microVersion")
            microVersion = 0
        else:
            microVersion = microver.as_int()

    del minorver
    del microver

    version = "%d.%d" % (minorVersion, microVersion)

    # 0.x is experimental
    if minorVersion == 0:
        stability = "experimental"

    # odd x.2 or 2.x is testing/development
    elif minorVersion % 2 != 0 or microVersion % 2 != 0:
        stability = "testing"

    # otherwise it's stable
    else:
        stability = "stable"

    # --------------------------------------------------------------------------------------------------------
    # author

    author = {
        'name'    : plugin.get_author_name().as_string() or "",
        'homepage': plugin.get_author_homepage().as_string() or "",
        'email'   : plugin.get_author_email().as_string() or "",
    }

    if not author['name']:
        errors.append("plugin author name is missing")

    if not author['homepage']:
        prj = plugin.get_value(ns_lv2core.project).get_first()
        if prj.me is not None:
            maintainer = lilv.lilv_world_get(world.me, prj.me, ns_doap.maintainer.me, None)
            if maintainer is not None:
                homepage = lilv.lilv_world_get(world.me, maintainer, ns_foaf.homepage.me, None)
                if homepage is not None:
                    author['homepage'] = lilv.lilv_node_as_string(homepage)
                del homepage
            del maintainer
        del prj

    if not author['homepage']:
        warnings.append("plugin author homepage is missing")

    if not author['email']:
        pass
    elif author['email'].startswith(bundleuri):
        author['email'] = author['email'].replace(bundleuri,"",1)
        warnings.append("plugin author email entry is missing 'mailto:' prefix")
    elif author['email'].startswith("mailto:"):
        author['email'] = author['email'].replace("mailto:","",1)

    # --------------------------------------------------------------------------------------------------------
    # brand

    brand = plugin.get_value(ns_mod.brand).get_first().as_string() or ""

    if not brand:
        brand = author['name'].split(" - ",1)[0].split(" ",1)[0]
        brand = brand.rstrip(",").rstrip(";")
        if len(brand) > 11:
            brand = brand[:11]
        warnings.append("plugin brand is missing")

    elif len(brand) > 11:
        brand = brand[:11]
        errors.append("plugin brand has more than 11 characters")

    # --------------------------------------------------------------------------------------------------------
    # label

    label = plugin.get_value(ns_mod.label).get_first().as_string() or ""

    if not label:
        if len(name) <= 16:
            label = name
        else:
            labels = name.split(" - ",1)[0].split(" ")
            if labels[0].lower() in bundle.lower() and len(labels) > 1 and not labels[1].startswith(("(","[")):
                label = labels[1]
            else:
                label = labels[0]

            if len(label) > 16:
                label = label[:16]

            warnings.append("plugin label is missing")
            del labels

    elif len(label) > 16:
        label = label[:16]
        errors.append("plugin label has more than 16 characters")

    # --------------------------------------------------------------------------------------------------------
    # bundles

    bundles = []

    if useAbsolutePath:
        bnodes = lilv.lilv_plugin_get_data_uris(plugin.me)

        it = lilv.lilv_nodes_begin(bnodes)
        while not lilv.lilv_nodes_is_end(bnodes, it):
            bnode = lilv.lilv_nodes_get(bnodes, it)
            it    = lilv.lilv_nodes_next(bnodes, it)

            if bnode is None:
                continue
            if not lilv.lilv_node_is_uri(bnode):
                continue

            bpath = os.path.abspath(os.path.dirname(lilv.lilv_uri_to_path(lilv.lilv_node_as_uri(bnode))))

            if not bpath.endswith(os.sep):
                bpath += os.sep

            if bpath not in bundles:
                bundles.append(bpath)

        if bundle not in bundles:
            bundles.append(bundle)

        del bnodes, it

    # --------------------------------------------------------------------------------------------------------
    # get the proper modgui

    modguigui = None

    nodes = plugin.get_value(ns_modgui.gui)
    it    = nodes.begin()
    while not nodes.is_end(it):
        mgui = nodes.get(it)
        it   = nodes.next(it)
        if mgui.me is None:
            continue
        resdir = world.find_nodes(mgui.me, ns_modgui.resourcesDirectory.me, None).get_first()
        if resdir.me is None:
            continue
        modguigui = mgui
        if not useAbsolutePath:
            # special build, use first modgui found
            break
        if os.path.expanduser("~") in lilv.lilv_uri_to_path(resdir.as_string()):
            # found a modgui in the home dir, stop here and use it
            break

    del nodes, it

    # --------------------------------------------------------------------------------------------------------
    # gui

    gui = {}

    if modguigui is None or modguigui.me is None:
        warnings.append("no modgui available")

    else:
        # resourcesDirectory *must* be present
        modgui_resdir = world.find_nodes(modguigui.me, ns_modgui.resourcesDirectory.me, None).get_first()

        if modgui_resdir.me is None:
            errors.append("modgui has no resourcesDirectory data")

        else:
            if useAbsolutePath:
                gui['resourcesDirectory'] = lilv.lilv_uri_to_path(modgui_resdir.as_string())

                # check if modgui is defined in a separate file
                gui['usingSeeAlso'] = os.path.exists(os.path.join(bundle, "modgui.ttl"))

                # check if the modgui definition is on its own file and in the user dir
                gui['modificableInPlace'] = bool((bundle not in gui['resourcesDirectory'] or gui['usingSeeAlso']) and
                                                os.path.expanduser("~") in gui['resourcesDirectory'])
            else:
                gui['resourcesDirectory'] = modgui_resdir.as_string().replace(bundleuri,"",1)

            # icon and settings templates
            modgui_icon  = world.find_nodes(modguigui.me, ns_modgui.iconTemplate    .me, None).get_first()
            modgui_setts = world.find_nodes(modguigui.me, ns_modgui.settingsTemplate.me, None).get_first()

            if modgui_icon.me is None:
                errors.append("modgui has no iconTemplate data")
            else:
                iconFile = lilv.lilv_uri_to_path(modgui_icon.as_string())
                if os.path.exists(iconFile):
                    gui['iconTemplate'] = iconFile if useAbsolutePath else iconFile.replace(bundle,"",1)
                else:
                    errors.append("modgui iconTemplate file is missing")
                del iconFile

            if modgui_setts.me is not None:
                settingsFile = lilv.lilv_uri_to_path(modgui_setts.as_string())
                if os.path.exists(settingsFile):
                    gui['settingsTemplate'] = settingsFile if useAbsolutePath else settingsFile.replace(bundle,"",1)
                else:
                    errors.append("modgui settingsTemplate file is missing")
                del settingsFile

            # javascript and stylesheet files
            modgui_script = world.find_nodes(modguigui.me, ns_modgui.javascript.me, None).get_first()
            modgui_style  = world.find_nodes(modguigui.me, ns_modgui.stylesheet.me, None).get_first()

            if modgui_script.me is not None:
                javascriptFile = lilv.lilv_uri_to_path(modgui_script.as_string())
                if os.path.exists(javascriptFile):
                    gui['javascript'] = javascriptFile if useAbsolutePath else javascriptFile.replace(bundle,"",1)
                else:
                    errors.append("modgui javascript file is missing")
                del javascriptFile

            if modgui_style.me is None:
                errors.append("modgui has no stylesheet data")
            else:
                stylesheetFile = lilv.lilv_uri_to_path(modgui_style.as_string())
                if os.path.exists(stylesheetFile):
                    gui['stylesheet'] = stylesheetFile if useAbsolutePath else stylesheetFile.replace(bundle,"",1)
                else:
                    errors.append("modgui stylesheet file is missing")
                del stylesheetFile

            # template data for backwards compatibility
            # FIXME remove later once we got rid of all templateData files
            modgui_templ = world.find_nodes(modguigui.me, ns_modgui.templateData.me, None).get_first()

            if modgui_templ.me is not None:
                warnings.append("modgui is using old deprecated templateData")
                templFile = lilv.lilv_uri_to_path(modgui_templ.as_string())
                if os.path.exists(templFile):
                    with open(templFile, 'r') as fd:
                        try:
                            data = json.loads(fd.read())
                        except:
                            data = {}
                        keys = list(data.keys())

                        if 'author' in keys:
                            gui['brand'] = data['author']
                        if 'label' in keys:
                            gui['label'] = data['label']
                        if 'color' in keys:
                            gui['color'] = data['color']
                        if 'knob' in keys:
                            gui['knob'] = data['knob']
                        if 'controls' in keys:
                            index = 0
                            ports = []
                            for ctrl in data['controls']:
                                ports.append({
                                    'index' : index,
                                    'name'  : ctrl['name'],
                                    'symbol': ctrl['symbol'],
                                })
                                index += 1
                            gui['ports'] = ports
                del templFile

            # screenshot and thumbnail
            modgui_scrn  = world.find_nodes(modguigui.me, ns_modgui.screenshot.me, None).get_first()
            modgui_thumb = world.find_nodes(modguigui.me, ns_modgui.thumbnail .me, None).get_first()

            if modgui_scrn.me is not None:
                gui['screenshot'] = lilv.lilv_uri_to_path(modgui_scrn.as_string())
                if not os.path.exists(gui['screenshot']):
                    errors.append("modgui screenshot file is missing")
                if not useAbsolutePath:
                    gui['screenshot'] = gui['screenshot'].replace(bundle,"",1)
            else:
                errors.append("modgui has no screnshot data")

            if modgui_thumb.me is not None:
                gui['thumbnail'] = lilv.lilv_uri_to_path(modgui_thumb.as_string())
                if not os.path.exists(gui['thumbnail']):
                    errors.append("modgui thumbnail file is missing")
                if not useAbsolutePath:
                    gui['thumbnail'] = gui['thumbnail'].replace(bundle,"",1)
            else:
                errors.append("modgui has no thumbnail data")

            # extra stuff, all optional
            modgui_brand = world.find_nodes(modguigui.me, ns_modgui.brand.me, None).get_first()
            modgui_label = world.find_nodes(modguigui.me, ns_modgui.label.me, None).get_first()
            modgui_model = world.find_nodes(modguigui.me, ns_modgui.model.me, None).get_first()
            modgui_panel = world.find_nodes(modguigui.me, ns_modgui.panel.me, None).get_first()
            modgui_color = world.find_nodes(modguigui.me, ns_modgui.color.me, None).get_first()
            modgui_knob  = world.find_nodes(modguigui.me, ns_modgui.knob .me, None).get_first()

            if modgui_brand.me is not None:
                gui['brand'] = modgui_brand.as_string()
            if modgui_label.me is not None:
                gui['label'] = modgui_label.as_string()
            if modgui_model.me is not None:
                gui['model'] = modgui_model.as_string()
            if modgui_panel.me is not None:
                gui['panel'] = modgui_panel.as_string()
            if modgui_color.me is not None:
                gui['color'] = modgui_color.as_string()
            if modgui_knob.me is not None:
                gui['knob'] = modgui_knob.as_string()

            # ports
            errpr = False
            sybls = []
            ports = []
            nodes = world.find_nodes(modguigui.me, ns_modgui.port.me, None)
            it    = lilv.lilv_nodes_begin(nodes.me)
            while not lilv.lilv_nodes_is_end(nodes.me, it):
                port = lilv.lilv_nodes_get(nodes.me, it)
                it   = lilv.lilv_nodes_next(nodes.me, it)
                if port is None:
                    break
                port_indx = world.find_nodes(port, ns_lv2core.index .me, None).get_first()
                port_symb = world.find_nodes(port, ns_lv2core.symbol.me, None).get_first()
                port_name = world.find_nodes(port, ns_lv2core.name  .me, None).get_first()

                if None in (port_indx.me, port_name.me, port_symb.me):
                    if not errpr:
                        errors.append("modgui has some invalid port data")
                        errpr = True
                    continue

                port_indx = port_indx.as_int()
                port_symb = port_symb.as_string()
                port_name = port_name.as_string()

                ports.append({
                    'index' : port_indx,
                    'symbol': port_symb,
                    'name'  : port_name,
                })

                if port_symb not in sybls:
                    sybls.append(port_symb)
                elif not errpr:
                    errors.append("modgui has some duplicated port symbols")
                    errpr = True

            # sort ports
            if len(ports) > 0:
                ports2 = {}

                for port in ports:
                    ports2[port['index']] = port
                gui['ports'] = [ports2[i] for i in ports2]

                del ports2

            # cleanup
            del ports, nodes, it

    # --------------------------------------------------------------------------------------------------------
    # ports

    index = 0
    ports = {
        'audio'  : { 'input': [], 'output': [] },
        'control': { 'input': [], 'output': [] },
        'midi'   : { 'input': [], 'output': [] }
    }

    portsymbols = []
    portnames   = []

    # function for filling port info
    def fill_port_info(port):
        # base data
        portname = lilv.lilv_node_as_string(port.get_name()) or ""

        if not portname:
            portname = "_%i" % index
            errors.append("port with index %i has no name" % index)

        portsymbol = lilv.lilv_node_as_string(port.get_symbol()) or ""

        if not portsymbol:
            portsymbol = "_%i" % index
            errors.append("port with index %i has no symbol" % index)

        # check for duplicate names
        if portname in portsymbols:
            warnings.append("port name '%s' is not unique" % portname)
        else:
            portnames.append(portname)

        # check for duplicate symbols
        if portsymbol in portsymbols:
            errors.append("port symbol '%s' is not unique" % portsymbol)
        else:
            portsymbols.append(portsymbol)

        # short name
        psname = lilv.lilv_nodes_get_first(port.get_value(ns_lv2core.shortName.me))

        if psname is not None:
            psname = lilv.lilv_node_as_string(psname) or ""

        if not psname:
            psname = get_short_port_name(portname)
            if len(psname) > 16:
                warnings.append("port '%s' name is too big, reduce the name size or provide a shortName" % portname)

        elif len(psname) > 16:
            psname = psname[:16]
            errors.append("port '%s' short name has more than 16 characters" % portname)

        # check for old style shortName
        if port.get_value(ns_lv2core.shortname.me) is not None:
            errors.append("port '%s' short name is using old style 'shortname' instead of 'shortName'" % portname)

        # port types
        types = [typ.rsplit("#",1)[-1].replace("Port","",1) for typ in get_port_data(port, ns_rdf.type_)]

        if "Atom" in types \
            and port.supports_event(ns_midi.MidiEvent.me) \
            and lilv.Nodes(port.get_value(ns_atom.bufferType.me)).get_first() == ns_atom.Sequence:
                types.append("MIDI")

        #if "Morph" in types:
            #morphtyp = lilv.lilv_nodes_get_first(port.get_value(ns_morph.supportsType.me))
            #if morphtyp is not None:
                #morphtyp = lilv.lilv_node_as_uri(morphtyp)
                #if morphtyp:
                    #types.append(morphtyp.rsplit("#",1)[-1].replace("Port","",1))

        # port comment
        pcomment = (get_port_data(port, ns_rdfs.comment) or [""])[0]

        # port designation
        designation = (get_port_data(port, ns_lv2core.designation) or [""])[0]

        # port rangeSteps
        rangeSteps = (get_port_data(port, ns_mod.rangeSteps) or get_port_data(port, ns_pprops.rangeSteps) or [None])[0]

        # port properties
        properties = [typ.rsplit("#",1)[-1] for typ in get_port_data(port, ns_lv2core.portProperty)]

        # data
        ranges      = {}
        scalepoints = []

        # unit block
        ulabel  = ""
        urender = ""
        usymbol = ""

        # control and cv must contain ranges, might contain scale points
        if "Control" in types or "CV" in types:
            isInteger = "integer" in properties

            if isInteger and "CV" in types:
                errors.append("port '%s' has integer property and CV type" % portname)

            xdefault = lilv.lilv_nodes_get_first(port.get_value(ns_mod.default.me)) or \
                       lilv.lilv_nodes_get_first(port.get_value(ns_lv2core.default.me))
            xminimum = lilv.lilv_nodes_get_first(port.get_value(ns_mod.minimum.me)) or \
                       lilv.lilv_nodes_get_first(port.get_value(ns_lv2core.minimum.me))
            xmaximum = lilv.lilv_nodes_get_first(port.get_value(ns_mod.maximum.me)) or \
                       lilv.lilv_nodes_get_first(port.get_value(ns_lv2core.maximum.me))

            if xminimum is not None and xmaximum is not None:
                if isInteger:
                    if is_integer(lilv.lilv_node_as_string(xminimum)):
                        ranges['minimum'] = lilv.lilv_node_as_int(xminimum)
                    else:
                        ranges['minimum'] = lilv.lilv_node_as_float(xminimum)
                        if fmod(ranges['minimum'], 1.0) == 0.0:
                            warnings.append("port '%s' has integer property but minimum value is float" % portname)
                        else:
                            errors.append("port '%s' has integer property but minimum value has non-zero decimals" % portname)
                        ranges['minimum'] = int(ranges['minimum'])

                    if is_integer(lilv.lilv_node_as_string(xmaximum)):
                        ranges['maximum'] = lilv.lilv_node_as_int(xmaximum)
                    else:
                        ranges['maximum'] = lilv.lilv_node_as_float(xmaximum)
                        if fmod(ranges['maximum'], 1.0) == 0.0:
                            warnings.append("port '%s' has integer property but maximum value is float" % portname)
                        else:
                            errors.append("port '%s' has integer property but maximum value has non-zero decimals" % portname)
                        ranges['maximum'] = int(ranges['maximum'])

                else:
                    ranges['minimum'] = lilv.lilv_node_as_float(xminimum)
                    ranges['maximum'] = lilv.lilv_node_as_float(xmaximum)

                    if is_integer(lilv.lilv_node_as_string(xminimum)):
                        warnings.append("port '%s' minimum value is an integer" % portname)

                    if is_integer(lilv.lilv_node_as_string(xmaximum)):
                        warnings.append("port '%s' maximum value is an integer" % portname)

                if ranges['minimum'] >= ranges['maximum']:
                    ranges['maximum'] = ranges['minimum'] + (1 if isInteger else 0.1)
                    errors.append("port '%s' minimum value is equal or higher than its maximum" % portname)

                if xdefault is not None:
                    if isInteger:
                        if is_integer(lilv.lilv_node_as_string(xdefault)):
                            ranges['default'] = lilv.lilv_node_as_int(xdefault)
                        else:
                            ranges['default'] = lilv.lilv_node_as_float(xdefault)
                            if fmod(ranges['default'], 1.0) == 0.0:
                                warnings.append("port '%s' has integer property but default value is float" % portname)
                            else:
                                errors.append("port '%s' has integer property but default value has non-zero decimals" % portname)
                            ranges['default'] = int(ranges['default'])
                    else:
                        ranges['default'] = lilv.lilv_node_as_float(xdefault)

                        if is_integer(lilv.lilv_node_as_string(xdefault)):
                            warnings.append("port '%s' default value is an integer" % portname)

                    testmin = ranges['minimum']
                    testmax = ranges['maximum']

                    if "sampleRate" in properties:
                        testmin *= 48000
                        testmax *= 48000

                    if not (testmin <= ranges['default'] <= testmax):
                        ranges['default'] = ranges['minimum']
                        errors.append("port '%s' default value is out of bounds" % portname)

                else:
                    ranges['default'] = ranges['minimum']

                    if "Input" in types:
                        errors.append("port '%s' is missing default value" % portname)

            else:
                if isInteger:
                    ranges['minimum'] = 0
                    ranges['maximum'] = 1
                    ranges['default'] = 0
                else:
                    ranges['minimum'] = -1.0 if "CV" in types else 0.0
                    ranges['maximum'] = 1.0
                    ranges['default'] = 0.0

                if "CV" not in types and designation != "http://lv2plug.in/ns/lv2core#latency":
                    errors.append("port '%s' is missing value ranges" % portname)

            nodes = port.get_scale_points()

            if nodes is not None:
                scalepoints_unsorted = []

                it = lilv.lilv_scale_points_begin(nodes)
                while not lilv.lilv_scale_points_is_end(nodes, it):
                    sp = lilv.lilv_scale_points_get(nodes, it)
                    it = lilv.lilv_scale_points_next(nodes, it)

                    if sp is None:
                        continue

                    label = lilv.lilv_scale_point_get_label(sp)
                    value = lilv.lilv_scale_point_get_value(sp)

                    if label is None:
                        errors.append("a port scalepoint is missing its label")
                        continue

                    label = lilv.lilv_node_as_string(label) or ""

                    if not label:
                        errors.append("a port scalepoint is missing its label")
                        continue

                    if value is None:
                        errors.append("port scalepoint '%s' is missing its value" % label)
                        continue

                    if isInteger:
                        if is_integer(lilv.lilv_node_as_string(value)):
                            value = lilv.lilv_node_as_int(value)
                        else:
                            value = lilv.lilv_node_as_float(value)
                            if fmod(value, 1.0) == 0.0:
                                warnings.append("port '%s' has integer property but scalepoint '%s' value is float" % (portname, label))
                            else:
                                errors.append("port '%s' has integer property but scalepoint '%s' value has non-zero decimals" % (portname, label))
                            value = int(value)
                    else:
                        if is_integer(lilv.lilv_node_as_string(value)):
                            warnings.append("port '%s' scalepoint '%s' value is an integer" % (portname, label))
                        value = lilv.lilv_node_as_float(value)

                    if ranges['minimum'] <= value <= ranges['maximum']:
                        scalepoints_unsorted.append((value, label))
                    else:
                        errors.append(("port scalepoint '%s' has an out-of-bounds value:\n" % label) +
                                      ("%d < %d < %d" if isInteger else "%f < %f < %f") % (ranges['minimum'], value, ranges['maximum']))

                if len(scalepoints_unsorted) != 0:
                    unsorted = dict(s for s in scalepoints_unsorted)
                    values   = list(v for v, l in scalepoints_unsorted)
                    values.sort()
                    scalepoints = list({ 'value': v, 'label': unsorted[v] } for v in values)
                    del unsorted, values

                del scalepoints_unsorted

            if "enumeration" in properties and len(scalepoints) <= 1:
                errors.append("port '%s' wants to use enumeration but doesn't have enough values" % portname)
                properties.remove("enumeration")

        # control ports might contain unit
        if "Control" in types:
            # unit
            uunit = lilv.lilv_nodes_get_first(port.get_value(ns_units.unit.me))

            if uunit is not None:
                uuri = lilv.lilv_node_as_uri(uunit)

                # using pre-existing lv2 unit
                if uuri is not None and uuri.startswith("http://lv2plug.in/ns/"):
                    uuri  = uuri.replace("http://lv2plug.in/ns/extensions/units#","",1)
                    alnum = uuri.isalnum()

                    if not alnum:
                        errors.append("port '%s' has wrong lv2 unit uri" % portname)
                        uuri = uuri.rsplit("#",1)[-1].rsplit("/",1)[-1]

                    ulabel, urender, usymbol = get_port_unit(uuri)

                    if alnum and not (ulabel and urender and usymbol):
                        errors.append("port '%s' has unknown lv2 unit (our bug?, data is '%s', '%s', '%s')" % (portname,
                                                                                                               ulabel,
                                                                                                               urender,
                                                                                                               usymbol))

                # using custom unit
                else:
                    xlabel  = world.find_nodes(uunit, ns_rdfs  .label.me, None).get_first()
                    xrender = world.find_nodes(uunit, ns_units.render.me, None).get_first()
                    xsymbol = world.find_nodes(uunit, ns_units.symbol.me, None).get_first()

                    if xlabel.me is not None:
                        ulabel = xlabel.as_string()
                    else:
                        errors.append("port '%s' has custom unit with no label" % portname)

                    if xrender.me is not None:
                        urender = xrender.as_string()
                    else:
                        errors.append("port '%s' has custom unit with no render" % portname)

                    if xsymbol.me is not None:
                        usymbol = xsymbol.as_string()
                    else:
                        errors.append("port '%s' has custom unit with no symbol" % portname)

        return (types, {
            'name'   : portname,
            'symbol' : portsymbol,
            'ranges' : ranges,
            'units'  : {
                'label' : ulabel,
                'render': urender,
                'symbol': usymbol,
            } if "Control" in types and ulabel and urender and usymbol else {},
            'comment'    : pcomment,
            'designation': designation,
            'properties' : properties,
            'rangeSteps' : rangeSteps,
            'scalePoints': scalepoints,
            'shortName'  : psname,
        })

    for p in (plugin.get_port_by_index(i) for i in range(plugin.get_num_ports())):
        types, info = fill_port_info(p)

        info['index'] = index
        index += 1

        isInput = "Input" in types
        types.remove("Input" if isInput else "Output")

        for typ in [typl.lower() for typl in types]:
            if typ not in ports.keys():
                ports[typ] = { 'input': [], 'output': [] }
            ports[typ]["input" if isInput else "output"].append(info)

    # --------------------------------------------------------------------------------------------------------
    # presets

    def get_preset_data(preset):
        world.load_resource(preset.me)

        uri   = preset.as_string() or ""
        label = world.find_nodes(preset.me, ns_rdfs.label.me, None).get_first().as_string() or ""

        if not uri:
            errors.append("preset with label '%s' has no uri" % (label or "<unknown>"))
        if not label:
            errors.append("preset with uri '%s' has no label" % (uri or "<unknown>"))

        return (uri, label)

    presets = []

    presets_related = plugin.get_related(ns_pset.Preset)
    presets_data    = list(LILV_FOREACH(presets_related, get_preset_data))

    if len(presets_data) != 0:
        unsorted = dict(p for p in presets_data)
        uris     = list(unsorted.keys())
        uris.sort()
        presets  = list({ 'uri': p, 'label': unsorted[p] } for p in uris)
        del unsorted, uris

    del presets_related

    # --------------------------------------------------------------------------------------------------------
    # done

    return {
        'uri' : uri,
        'name': name,

        'binary' : binary,
        'brand'  : brand,
        'label'  : label,
        'license': license,
        'comment': comment,

        'category'    : get_category(plugin.get_value(ns_rdf.type_)),
        'microVersion': microVersion,
        'minorVersion': minorVersion,

        'version'  : version,
        'stability': stability,

        'author' : author,
        'bundles': bundles,
        'gui'    : gui,
        'ports'  : ports,
        'presets': presets,

        'errors'  : errors,
        'warnings': warnings,
    }

# ------------------------------------------------------------------------------------------------------------
# get_plugin_info_helper

# Get info from a simple URI, without the need of your own lilv world
# This is used by get_plugins_info in MOD-SDK
def get_plugin_info_helper(uri):
    world = lilv.World()
    world.load_all()
    plugins = world.get_all_plugins()
    return [get_plugin_info(world, p, False) for p in plugins]

# ------------------------------------------------------------------------------------------------------------
# get_plugins_info

# Get plugin-related info from a list of lv2 bundles
# @a bundles is a list of strings, consisting of directories in the filesystem (absolute pathnames).
def get_plugins_info(bundles):
    # if empty, do nothing
    if len(bundles) == 0:
        raise Exception('get_plugins_info() - no bundles provided')

    # Create our own unique lilv world
    # We'll load the selected bundles and get all plugins from it
    world = lilv.World()

    # this is needed when loading specific bundles instead of load_all
    # (these functions are not exposed via World yet)
    lilv.lilv_world_load_specifications(world.me)
    lilv.lilv_world_load_plugin_classes(world.me)

    # load all bundles
    for bundle in bundles:
        # lilv wants the last character as the separator
        bundle = os.path.abspath(bundle)
        if not bundle.endswith(os.sep):
            bundle += os.sep

        # convert bundle string into a lilv node
        bundlenode = lilv.lilv_new_file_uri(world.me, None, bundle)

        # load the bundle
        world.load_bundle(bundlenode)

        # free bundlenode, no longer needed
        lilv.lilv_node_free(bundlenode)

    # get all plugins available in the selected bundles
    plugins = world.get_all_plugins()

    # make sure the bundles include something
    if plugins.size() == 0:
        raise Exception('get_plugins_info() - selected bundles have no plugins')

    # return all the info
    return [get_plugin_info(world, p, False) for p in plugins]

# ------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    from sys import argv, exit
    from pprint import pprint
    #get_plugins_info(argv[1:])
    #for i in get_plugins_info(argv[1:]): pprint(i)
    #exit(0)
    for i in get_plugins_info(argv[1:]):
        warnings = i['warnings'].copy()

        if 'plugin brand is missing' in warnings:
            i['warnings'].remove('plugin brand is missing')

        if 'plugin label is missing' in warnings:
            i['warnings'].remove('plugin label is missing')

        if 'no modgui available' in warnings:
            i['warnings'].remove('no modgui available')

        for warn in warnings:
            if "has no short name" in warn:
                i['warnings'].remove(warn)

        pprint({
            'uri'     : i['uri'],
            'errors'  : i['errors'],
            'warnings': i['warnings']
        }, width=200)

# ------------------------------------------------------------------------------------------------------------
