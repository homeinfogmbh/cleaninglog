# ./cleaninglog/dom.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:f29217f8ca2b1effffed096df612b717ddf94ef0
# Generated 2022-10-28 10:29:04.308809 by PyXB version 1.2.7-DEV using Python 3.10.8.final.0
# Namespace http://xml.homeinfo.de/schema/cleaning

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:94f86e7e-569a-11ed-b52d-7427eaa9df7d')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.7-DEV'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://xml.homeinfo.de/schema/cleaning', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, fallback_namespace=None, location_base=None, default_namespace=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword fallback_namespace An absent L{pyxb.Namespace} instance
    to use for unqualified names when there is no default namespace in
    scope.  If unspecified or C{None}, the namespace of the module
    containing this function will be used, if it is an absent
    namespace.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.

    @keyword default_namespace An alias for @c fallback_namespace used
    in PyXB 1.1.4 through 1.2.6.  It behaved like a default namespace
    only for absent namespaces.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    if fallback_namespace is None:
        fallback_namespace = default_namespace
    if fallback_namespace is None:
        fallback_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=fallback_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, fallback_namespace=None, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if fallback_namespace is None:
        fallback_namespace = default_namespace
    if fallback_namespace is None:
        fallback_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, fallback_namespace)


# Complex type {http://xml.homeinfo.de/schema/cleaning}Cleanings with content type ELEMENT_ONLY
class Cleanings (pyxb.binding.basis.complexTypeDefinition):
    """
                Hauptobjekt für Reinigungsnachweise.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Cleanings')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 22, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element cleaning uses Python identifier cleaning
    __cleaning = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'cleaning'), 'cleaning', '__httpxml_homeinfo_deschemacleaning_Cleanings_cleaning', True, pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 29, 12), )

    
    cleaning = property(__cleaning.value, __cleaning.set, None, '\n                        Reinigungseinträge.\n                    ')

    _ElementMap.update({
        __cleaning.name() : __cleaning
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Cleanings = Cleanings
Namespace.addCategoryObject('typeBinding', 'Cleanings', Cleanings)


# Complex type {http://xml.homeinfo.de/schema/cleaning}Cleaning with content type ELEMENT_ONLY
class Cleaning (pyxb.binding.basis.complexTypeDefinition):
    """
                Ein Reinigungsnachweis.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Cleaning')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 40, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element timestamp uses Python identifier timestamp
    __timestamp = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'timestamp'), 'timestamp', '__httpxml_homeinfo_deschemacleaning_Cleaning_timestamp', False, pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 47, 12), )

    
    timestamp = property(__timestamp.value, __timestamp.set, None, '\n                        Datum und Uhrzeit der Reinigung.\n                    ')

    
    # Element user uses Python identifier user
    __user = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'user'), 'user', '__httpxml_homeinfo_deschemacleaning_Cleaning_user', False, pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 54, 12), )

    
    user = property(__user.value, __user.set, None, '\n                        Die Reinigungskraft oder das Reinigungsunternehmen.\n                    ')

    
    # Element annotation uses Python identifier annotation
    __annotation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'annotation'), 'annotation', '__httpxml_homeinfo_deschemacleaning_Cleaning_annotation', True, pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 61, 12), )

    
    annotation = property(__annotation.value, __annotation.set, None, '\n                        Anmerkungen zur Reinigung.\n                    ')

    _ElementMap.update({
        __timestamp.name() : __timestamp,
        __user.name() : __user,
        __annotation.name() : __annotation
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Cleaning = Cleaning
Namespace.addCategoryObject('typeBinding', 'Cleaning', Cleaning)


# Complex type {http://xml.homeinfo.de/schema/cleaning}User with content type SIMPLE
class User (pyxb.binding.basis.complexTypeDefinition):
    """
                Ein Reinigungsnachweis.
            """
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'User')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 72, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__httpxml_homeinfo_deschemacleaning_User_type', pyxb.binding.datatypes.string)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 80, 16)
    __type._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 80, 16)
    
    type = property(__type.value, __type.set, None, '\n                            Typ der Reinigung.\n                        ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __type.name() : __type
    })
_module_typeBindings.User = User
Namespace.addCategoryObject('typeBinding', 'User', User)


cleanings = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'cleanings'), Cleanings, documentation='\n                Wurzelelement.\n            ', location=pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 13, 4))
Namespace.addCategoryObject('elementBinding', cleanings.name().localName(), cleanings)



Cleanings._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'cleaning'), Cleaning, scope=Cleanings, documentation='\n                        Reinigungseinträge.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 29, 12)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 29, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Cleanings._UseForTag(pyxb.namespace.ExpandedName(None, 'cleaning')), pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 29, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Cleanings._Automaton = _BuildAutomaton()




Cleaning._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'timestamp'), pyxb.binding.datatypes.dateTime, scope=Cleaning, documentation='\n                        Datum und Uhrzeit der Reinigung.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 47, 12)))

Cleaning._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'user'), User, scope=Cleaning, documentation='\n                        Die Reinigungskraft oder das Reinigungsunternehmen.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 54, 12)))

Cleaning._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'annotation'), pyxb.binding.datatypes.string, scope=Cleaning, documentation='\n                        Anmerkungen zur Reinigung.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 61, 12)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 61, 12))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Cleaning._UseForTag(pyxb.namespace.ExpandedName(None, 'timestamp')), pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 47, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Cleaning._UseForTag(pyxb.namespace.ExpandedName(None, 'user')), pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 54, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Cleaning._UseForTag(pyxb.namespace.ExpandedName(None, 'annotation')), pyxb.utils.utility.Location('/home/neumann/Projekte/cleaninglog/cleaning.xsd', 61, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Cleaning._Automaton = _BuildAutomaton_()

