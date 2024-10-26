#An add-on that improves object navigation and touch support in NVDA
#This add-on is licensed under the same licence as NVDA it self. To see the license, open the file named copying.txt
import addonHandler
addonHandler.initTranslation()
import api
import appModuleHandler
import braille
import ctypes
import config
import contextlib
import controlTypes
import copy
import cursorManager
import globalPluginHandler
import gui
import inputCore
import keyboardHandler
import locationHelper
import nvwave
import os
import random
import screenExplorer
import speech
import threading
import touchHandler
import ui
import UIAHandler
import winUser
import wx
from ctypes import *
from ctypes.wintypes import POINT, RECT
from controlTypes import Role
from globalCommands import *
from gui.settingsDialogs import SettingsDialog
from NVDAObjects import *
from scriptHandler import script, getLastScriptRepeatCount
from time import sleep
from UIAHandler import utils as UIAUtils
from .extraFunctions import NewDynamicNVDAObjectType, VirtualBase
translate = _
NVDAAudioFilesPath = os.path.join(globalVars.appDir, "waves")
startFile = os.path.join(os.path.dirname(__file__), "sounds", "start.wav")
element = UIAHandler.handler.clientObject
cacheRequest = UIAHandler.handler.baseCacheRequest
index = touchHandler.availableTouchModes.index('object')
touchHandler.availableTouchModes.append('navigation') # Insert the navigation mode on the index of the object mode to make it the new default
# Translators: A label for a touch mode
mode = _('Navigation mode')
touchHandler.touchModeLabels.update({'navigation': mode})
# Translators: The label for a script category
category = _('Enhanced Object Navigation')
confSpec = {
	'useByDefault': 'boolean(default=False)',
	'sortInTabOrder': 'boolean(default=False)',
	'scope': 'string(default="window")',
	'enhancedDetection': 'boolean(default=True)',
	'context': 'boolean(default=False)',
	'setFocus': 'boolean(default=False)',
	'activate': 'boolean(default=False)',
	'autoUpdate': 'boolean(default=True)',
	'altMode': 'boolean(default=True)',
	"useSounds": "boolean(default=True)",
	"advancedNavigation": "boolean(default=False)"
}
config.conf.spec['enhancedObjectNavigation'] = confSpec
internalScopeValues = ['window', 'desktop', 'container']
scopeValues = [
	# Translators: A choice in a combo box
	_('the window that the navigator object is in'),
	# Translators: A choice in a combo box
	_('all objects'),
	# Translators: A choice in a combo box
	_('the current control that the navigator object is in, e.g a list or a web page')
]
class EnhancedObjectNavigationSettingsPanel(gui.SettingsPanel):
	# Translators: the title of a settings panel
	title = _('Enhanced object navigation')
	def makeSettings(self, settingsSizer):
		settings = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: the label of a check box
		label = _('&Use navigation mode by default')
		self.navigationMode = settings.addItem(wx.CheckBox(self, label = label))
		self.navigationMode.SetValue(config.conf['enhancedObjectNavigation']['useByDefault'])
		# Translators: The label of a check box
		label = _('&When searching, sort the items in tab order instead of alphabetically')
		self.sortInTabOrder = settings.addItem(wx.CheckBox(self, label = label))
		self.sortInTabOrder.SetValue(config.conf['enhancedObjectNavigation']['sortInTabOrder'])
		# Translators: The label for a combo box
		label = _('&Search scope')
		self.scope = settings.addLabeledControl(label, wx.Choice, choices = scopeValues)
		self.scope.SetSelection(internalScopeValues.index(config.conf['enhancedObjectNavigation']['scope']))
		# Translators: the label for a check box
		label = _('Use &enhanced detection while searching for same item')
		self.enhancedDetection = settings.addItem(wx.CheckBox(self, label = label))
		self.enhancedDetection.SetValue(config.conf['enhancedObjectNavigation']['enhancedDetection'])
		# Translators: The label for a check box
		label = _('&Report object context while navigating in the search list')
		self.context = settings.addItem(wx.CheckBox(self, label = label))
		self.context.SetValue(config.conf['enhancedObjectNavigation']['context'])
		# Translators: The label for a check box
		label = _('Set focus to the item selected in the search list')
		self.setFocus = settings.addItem(wx.CheckBox(self, label = label))
		self.setFocus.SetValue(config.conf['enhancedObjectNavigation']['setFocus'])
		# Translators: The label for a check box
		label = _('Activate the item selected in the search list')
		self.activate = settings.addItem(wx.CheckBox(self, label = label))
		self.activate.SetValue(config.conf['enhancedObjectNavigation']['activate'])
		# Translators: The label for a check box
		label = _('When in navigation mode or in the search list, automatically update the braille display when the content of the shown object changes. Disable if you incounter problems using the add-on, such as lag.')
		self.autoUpdate = settings.addItem(wx.CheckBox(self, label = label))
		self.autoUpdate.SetValue(config.conf['enhancedObjectNavigation']['autoUpdate'])
		# Translators: The label for a check box
		label = _('When in the search list and holding down left alt, use first letter navigation')
		self.altMode = settings.addItem(wx.CheckBox(self, label = label))
		self.altMode.SetValue(config.conf['enhancedObjectNavigation']['altMode'])
		# Translators: The label for a check box
		label = _("Use sounds to indicate if navigation mode has been toggled")
		self.sounds = settings.addItem(wx.CheckBox(self, label = label))
		self.sounds.SetValue(config.conf["enhancedObjectNavigation"]["useSounds"])
	def onSave(self):
		config.conf['enhancedObjectNavigation']['useByDefault'] = self.navigationMode.GetValue()
		config.conf['enhancedObjectNavigation']['sortInTabOrder'] = self.sortInTabOrder.GetValue()
		config.conf['enhancedObjectNavigation']['scope'] = internalScopeValues[self.scope.GetSelection()]
		config.conf['enhancedObjectNavigation']['enhancedDetection'] = self.enhancedDetection.GetValue()
		config.conf['enhancedObjectNavigation']['context'] = self.context.GetValue()
		config.conf['enhancedObjectNavigation']['setFocus'] = self.setFocus.GetValue()
		config.conf['enhancedObjectNavigation']['activate'] = self.activate.GetValue()
		config.conf['enhancedObjectNavigation']['autoUpdate'] = self.autoUpdate.GetValue()
		config.conf['enhancedObjectNavigation']['altMode'] = self.altMode.GetValue()
		config.conf["enhancedObjectNavigation"]["useSounds"] = self.sounds.GetValue()
def sort(i):
	return(i[:-6].lower())
def send(name):
	gesture = keyboardHandler.KeyboardInputGesture.fromName(name)
	try:
		inputCore.manager.executeGesture(gesture)
	except:
		gesture.send()
def getNearestWindowHandle(element):
	if not element:
		return
	handle = None
	element = element.BuildUpdatedCache(UIAHandler.handler.baseCacheRequest)
	handle = UIAHandler.handler.getNearestWindowHandle(element)
	if handle:
		return(handle)
	obj = None
	unknown = element.GetCurrentPattern(UIAHandler.UIA_LegacyIAccessiblePatternId)
	if unknown:
		pattern = unknown.QueryInterface(UIAHandler.IUIAutomationLegacyIAccessiblePattern)
	if pattern:
		try:
			IA = pattern.GetIAccessible()
		except:
			IA = None
		if IA:
			try:
				obj = IAccessible.IAccessible(IAccessibleObject = IA, IAccessibleChildID = pattern.CurrentChildId)
			except:
				pass
		if obj:
			return(obj.windowHandle)
def setNavToNewUIA(argument):
	obj = api.getNavigatorObject()
	if isinstance(obj, NewUIA):
		pass
	else:
		obj = NVDAToUIA(obj)
		api.setNavigatorObject(obj)
	yield None

@contextlib.contextmanager(setNavToNewUIA)
def navigationScript():
	pass

def createSimpleWalker():
	propertyCondition = UIAUtils.createUIAMultiPropertyCondition({UIAHandler.UIA_ControlTypePropertyId: [
		UIAHandler.UIA_GroupControlTypeId,
		UIAHandler.UIA_WindowControlTypeId,
		UIAHandler.UIA_TextControlTypeId
	], UIAHandler.UIA_NamePropertyId: [""]}, {UIAHandler.UIA_ControlTypePropertyId: [UIAHandler.UIA_PaneControlTypeId, UIAHandler.UIA_ScrollBarControlTypeId]}, {UIAHandler.UIA_IsControlElementPropertyId: [False]})
	condition = element.CreateNotCondition(propertyCondition)
	return(element.CreateTreeWalker(condition))
simpleWalker = createSimpleWalker()

def walkerWithProcessID(Element, walker):
	
	ID = Element.GetCachedPropertyValue(UIAHandler.UIA_ProcessIdPropertyId)
	c = element.CreatePropertyCondition(UIAHandler.UIA_ProcessIdPropertyId, ID)
	condition = element.CreateAndCondition(walker.Condition, c)
	return(element.CreateTreeWalker(condition))
def quickNavWalker(id = None):
	if isinstance(id, int):
		controlTypeCondition = element.CreatePropertyCondition(UIAHandler.UIA_ControlTypePropertyId, id)
	else:
		controlTypeCondition = id.condition
	condition = element.CreateAndCondition(simpleWalker.condition, controlTypeCondition)
	return(element.CreateTreeWalker(condition))
def createHeadingWalker():
	headingCondition = element.CreatePropertyCondition(UIAHandler.UIA_AriaRolePropertyId, "heading")
	condition = element.CreateAndCondition(headingCondition, simpleWalker.condition)
	return(element.CreateTreeWalker(condition))
def createMenuWalker():
	menuCondition = UIAUtils.createUIAMultiPropertyCondition({UIAHandler.UIA_ControlTypePropertyId: [
		UIAHandler.UIA_MenuControlTypeId,
		UIAHandler.UIA_MenuItemControlTypeId,
		UIAHandler.UIA_MenuBarControlTypeId
	]})
	condition = element.CreateAndCondition(menuCondition, simpleWalker.condition)
	return(element.CreateTreeWalker(condition))
def createTreeWalker():
	treeCondition = UIAUtils.createUIAMultiPropertyCondition({UIAHandler.UIA_ControlTypePropertyId: [
		UIAHandler.UIA_TreeControlTypeId,
		UIAHandler.UIA_TreeItemControlTypeId
	]})
	condition = element.CreateAndCondition(treeCondition, simpleWalker.condition)
	return(element.CreateTreeWalker(condition))
def createTabWalker():
	tabCondition = UIAUtils.createUIAMultiPropertyCondition({UIAHandler.UIA_ControlTypePropertyId: [
		UIAHandler.UIA_TabControlTypeId,
		UIAHandler.UIA_TabItemControlTypeId,
	]})
	condition = element.CreateAndCondition(tabCondition, simpleWalker.condition)
	return(element.CreateTreeWalker(condition))
def createFormFieldWalker():
	formFieldCondition = UIAUtils.createUIAMultiPropertyCondition({UIAHandler.UIA_ControlTypePropertyId: [
		UIAHandler.UIA_ButtonControlTypeId,
		UIAHandler.UIA_ComboBoxControlTypeId,
		UIAHandler.UIA_CheckBoxControlTypeId,
		UIAHandler.UIA_EditControlTypeId,
		UIAHandler.UIA_TabControlTypeId,
		UIAHandler.UIA_TabItemControlTypeId,
		UIAHandler.UIA_RadioButtonControlTypeId
	]})
	condition = element.CreateAndCondition(formFieldCondition, simpleWalker.condition)
	return(element.CreateTreeWalker(condition))
def createFocusableWalker():
	focusableCondition = element.CreatePropertyCondition(UIAHandler.UIA_IsKeyboardFocusablePropertyId, True)
	condition = element.CreateAndCondition(simpleWalker.condition, focusableCondition)
	return(element.CreateTreeWalker(condition))
def createLandmarkWalker():
	landmarkCondition = element.CreatePropertyCondition(UIAHandler.UIA_LandmarkTypePropertyId, 0)
	landmarkCondition = element.CreateNotCondition(landmarkCondition)
	condition = element.CreateAndCondition(landmarkCondition, simpleWalker.condition)
	return(element.CreateTreeWalker(condition))
def createSameItemWalker():
	obj = api.getNavigatorObject()
	controlType = obj.UIAElement.CurrentControlType
	sameItemCondition = element.CreatePropertyCondition(UIAHandler.UIA_ControlTypePropertyId, controlType)
	if config.conf["enhancedObjectNavigation"]["enhancedDetection"]:
		className = obj.UIAElement.CurrentClassName
		classNameCondition = element.CreatePropertyCondition(UIAHandler.UIA_ClassNamePropertyId, className)
		sameItemCondition = element.CreateAndCondition(sameItemCondition, classNameCondition)
	condition = element.CreateAndCondition(sameItemCondition, simpleWalker.condition)
	return(element.CreateTreeWalker(condition))
def getSearchableElement(conf = None):
	if not conf:
		conf = config.conf['enhancedObjectNavigation']['scope']
	handle = None
	obj = api.getNavigatorObject()
	desktop = ctypes.windll.user32.GetDesktopWindow()
	if conf == 'desktop':
		handle = desktop
	elif conf == 'container':
		handle = api.getNavigatorObject().windowHandle
	else:
		obj = window.Window(windowHandle = obj.windowHandle)
		parent = obj
		while parent.parent and not parent.parent.windowHandle == desktop:
			parent = parent.parent
		if parent:
			handle = parent.windowHandle
	e = element.ElementFromHandle(handle)
	return(e)

def createElementList(element, scope = UIAHandler.TreeScope_Descendants, condition = simpleWalker.condition):
	canUseFindAll = True
	try:
		UIAList = element.FindAllBuildCache(scope, condition, UIAHandler.handler.baseCacheRequest)
	except:
		canUseFindAll = False
	if not UIAList:
		canUseFindAll = False
	nameList = []
	elementDict = {}
	elementList = []
	if not canUseFindAll:
		obj = NewUIA(UIAElement = element.BuildUpdatedCache(cacheRequest))
		for i in obj.recursiveDescendants:
			if i.presentationType == i.presType_content:
				elementList.append(i.UIAElement)
	else:
		for i in range(UIAList.Length):
			elementList.append(UIAList.GetElement(i))
	for e in elementList:
		try:
			name = e.CurrentName
			if not isinstance(name, str):
				name = ''
		except:
			name = ''
		# Since dictionaries can't have duplicate keys, create a string of random numbers that always have the same length (so it can easily be discarded later) and add it to the name.
		randString = str(random.randint(111111, 999999))
		possibleName = name+randString
		while possibleName in nameList:
			possibleName = name + str(random.randint(111111, 999999))
		name = possibleName
		nameList.append(name)
		elementDict.update({name: e})
	return(nameList, elementDict)
def search(scope = UIAHandler.TreeScope_Descendants, walker = simpleWalker, gesture = None):
	conf = config.conf['enhancedObjectNavigation']['scope']
	if hasattr(walker, '__call__'):
		walker = walker()
	condition = walker.condition
	# Translators: The message reported when opening the item list
	message = _('Loading items, please wait...')
	ui.message(message)
	e = getSearchableElement()
	data = createElementList(e, scope = scope, condition = condition)
	if not data[1]:
		if conf == 'container': # The user probably tried to list all elements in a window that only has one element, such as a button window, so try to list in the foreground window instead
			e = getSearchableElement(conf = 'window')
		
		data = createElementList(e, scope = scope, condition = condition)
		if not data[1]:
			# Translators: the message reported when NVDA fails to create the search list
			message = _("No items found")
			ui.message(message)
			return(None)
	if not config.conf['enhancedObjectNavigation']['sortInTabOrder']:
		data[0].sort(key = sort)
	nameList = data[0]
	elementDict = data[1]
	searchInfo = SearchInfo(nameList, nameList, elementDict, '')
	searchObj = Search(searchInfo = searchInfo, index = 0)
	eventHandler.executeEvent('gainFocus', searchObj)
	if not isinstance(gesture, keyboardHandler.KeyboardInputGesture):
		return
	# NVDA may never release the modifiers, so do it manualy here
	for i in gesture.modifiers:
		keyboardHandler.internal_keyUpEvent(i[0], 0, False, False)
class NewScreenExplorer(screenExplorer.ScreenExplorer):
	updateReview = True
	def moveTo(self, x, y, *args, **kwargs):
		focus = api.getFocusObject()
		inSearchList = isinstance(focus, Search)
		if not inSearchList and not touchHandler.handler._curTouchMode == 'navigation':
			super(NewScreenExplorer, self).moveTo(x, y, *args, **kwargs)
			return
		point = POINT(x, y)
		e = element.ElementFromPointBuildCache(point, cacheRequest)
		if not inSearchList or e.CurrentClassName == 'CRootKey':
			obj = NewUIA(UIAElement = e)
			if obj == api.getNavigatorObject(): return
			api.setNavigatorObject(obj)
			speech.speech.cancelSpeech()
			speech.speech.speakObject(obj, reason = controlTypes.OutputReason.FOCUS)
			return
		desktop = windll.user32.GetDesktopWindow()
		rect = RECT()
		windll.user32.GetWindowRect(desktop, byref(rect))
		bottom = rect.bottom
		base = bottom//len(focus.searchInfo.modifiableNameList)
		anser = round(y//base)
		obj = Search(index = anser, searchInfo = focus.searchInfo)
		if obj and not obj == focus:
			speech.speech.cancelSpeech()
			eventHandler.executeEvent('gainFocus', obj)

if touchHandler.handler: touchHandler.handler.screenExplorer = NewScreenExplorer()
screenExplorer.ScreenExplorer = NewScreenExplorer
class NewUIA(UIA.UIA, metaclass = NewDynamicNVDAObjectType):
	def __init__(self, UIAElement = None, windowHandle = None,  fromTouch = False, wasNavigatedTo = True, *args, **kwargs):
		failed = False
		try:
			super(NewUIA, self).__init__(UIAElement = UIAElement, windowHandle = windowHandle, *args, **kwargs)
		except:
			failed = True
		if not UIAElement:
			raise InvalidNVDAObject
		if failed:
			obj = None
			pattern = self.UIALegacyIAccessiblePattern
			if pattern:
				try:
					IA = pattern.GetIAccessible()
				except:
					IA = None
				if IA:
					try:
						obj = IAccessible.IAccessible(IAccessibleObject = IA, IAccessibleChildID = pattern.CurrentChildId)
					except:
						pass
			if obj:
				super(NewUIA, self).__init__(UIAElement = UIAElement, windowHandle = obj.windowHandle, *args, **kwargs)
		self.wasNavigatedTo = wasNavigatedTo
		self.fromTouch = fromTouch
	def event_becomeNavigatorObject(self, isFocus):
		if isinstance(self, Search):
			return(		super(NewUIA, self).event_becomeNavigatorObject(isFocus = isFocus))

		if self.wasNavigatedTo:
			pattern = self._getUIAPattern(UIAHandler.UIA_ScrollItemPatternId, UIAHandler.IUIAutomationScrollItemPattern)
			if pattern:
				try:
					pattern.ScrollIntoView()
				except:
					pass
		super(NewUIA, self).event_becomeNavigatorObject(isFocus = isFocus)
	def _get_treeInterceptor(self):
		return(None)
	def _get_role(self):
		role = super(NewUIA, self).role
		if role != controlTypes.Role.HEADING and self.UIAElement.CurrentAriaRole == "heading":
			role = controlTypes.Role.HEADING
		return(role)
	def _get_roleText(self):
		roleText = super(NewUIA, self).roleText
		landmarkText = self.UIAElement.GetCurrentPropertyValue(UIAHandler.UIA_LocalizedLandmarkTypePropertyId)
		if not roleText and landmarkText:
			roleText = landmarkText
		if not roleText and self.role == controlTypes.Role.UNKNOWN:
			try:
				roleText = self._getUIACacheablePropertyValue(UIAHandler.UIA_LocalizedControlTypePropertyId)
			except:
				pass
		return(roleText)
	def _get_selectionContainer(self): # The normal implementation for this function sometimes creates errors when navigating in non native UIA elements.
		try:
			return(super(NewUIA, self)._get_selectionContainer())
		except:
			return(None)
	def _get_states(self):
		# Sometimes, _get_state raises an exception
		try:
			states = super(NewUIA, self)._get_states()
		except:
			states = set()
		return(states)
	def correctAPIForRelation(self, obj, relation = None):
		if obj:
			return(NewUIA(UIAElement = obj.UIAElement))
	def _get_previous(self):
		try:
			previousElement=UIAHandler.handler.baseTreeWalker.GetPreviousSiblingElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		except:
			return None
		if not previousElement:
			return None
		return(NewUIA(UIAElement = previousElement))

	def _get_next(self):
		try:
			nextElement=UIAHandler.handler.baseTreeWalker.GetNextSiblingElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		except:
			return None
		if not nextElement:
			return None
		return(NewUIA(UIAElement = nextElement))

	def _get_firstChild(self):
		try:
			firstChildElement=UIAHandler.handler.baseTreeWalker.GetFirstChildElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		except:
			return(None)
		if not firstChildElement:
			return None
		return(NewUIA(UIAElement = firstChildElement))

	def _get_parent(self):
		try:
			parentElement=UIAHandler.handler.baseTreeWalker.GetParentElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		except:
			parentElement=None
		if not parentElement:
			obj = super(NewUIA, self).parent
			if obj:
				return(NVDAToUIA(obj))
		return(NewUIA(UIAElement = parentElement))
	def _get_NVDAObject(self):
		if UIAHandler.handler.isUIAWindow(self.windowHandle):
			return(UIA.UIA(UIAElement = self.UIAElement))
		obj = None
		pattern = self.UIALegacyIAccessiblePattern
		if pattern:
			try:
				IA = pattern.GetIAccessible()
			except:
				IA = None
			if IA:
				try:
					obj = IAccessible.IAccessible(IAccessibleObject = IA, IAccessibleChildID = pattern.CurrentChildId)
				except:
					pass
		if not obj:
			location = self.location
			x, y = location.center.x, location.center.y
			objectFromPoint = api.getDesktopObject().objectFromPoint(x, y)
			while objectFromPoint and not objectFromPoint.location == self.location:
				objectFromPoint = objectFromPoint.parent
			if objectFromPoint:
				obj = objectFromPoint
		return(obj)
	def _get_UIATextPattern(self):
		return(None)

	def _get_value(self):
		value = super(NewUIA, self).value
		#limit the value to 100 characters because when the value is too large, it can make NVDA lag when the value is displayed on a braille display.
		if value and len(value) > 100 or value == self.name:
			value = ""
		return(value)
	def _get_presentationType(self):
		if UIAUtils.isUIAElementInWalker(self.UIAElement, simpleWalker):
			return(self.presType_content)
		return(self.presType_layout)
	def _get_TextInfo(self):
		return(NVDAObjectTextInfo)
	def findOverlayClasses(self, clsList):
		clsList.insert(0, self.APIClass)
		if self.windowHandle == winUser.getDesktopWindow():
			clsList.insert(0, Desktop)
		if not ctypes.windll.UIAutomationCore.UiaHasServerSideProvider(self.windowHandle):
			clsList.insert(0, MSAAProxy)

	def invoke(self, name = False, shouldSpeak = False):
		if shouldSpeak:
			return(True)
		pattern = None
		try:
			pattern = self.UIAInvokePattern
		except:
			pass
		if not pattern:
			return(False)
		if name:
			return translate('invoke')
		try:
			pattern.Invoke()
		except:
			return(False)
		return(True)
	def toggle(self, name = False, shouldSpeak = False):
		if shouldSpeak:
			return(True)
		pattern = None
		try:
			pattern = self.UIATogglePattern
		except:
			pass
		if not pattern:
			return(False)
		if name:
			if pattern.CurrentToggleState:
				# Translators: the message reported when doing an action
				message = _('uncheck')
			else:
				message = _('check')
			return(message)
		try:
			pattern.Toggle()
		except:
			return(False)
		return(True)
	def IAccessibleAction(self, name = False, shouldSpeak = False):
		if shouldSpeak:
			return(True)
		pattern = None
		try:
			pattern = self.UIALegacyIAccessiblePattern
		except:
			pass
		if not pattern:
			return(False)
		if name:
			try:
				message = pattern.CurrentDefaultAction
			except:
				message = False
			return(message)
		try:
			pattern.DoDefaultAction()
		except:
			return(False)
		return(True)
	def expandCollapse(self, name = False, shouldSpeak = False):
		if shouldSpeak:
			return(True)
		pattern = None
		try:
			pattern = self._getUIAPattern(UIAHandler.UIA_ExpandCollapsePatternId, UIAHandler.IUIAutomationExpandCollapsePattern)
		except:
			pass
		if not pattern:
			return(False)
		state = pattern.CurrentExpandCollapseState
		if name:
			if state:
				# Translators: the message reported when doing an action
				message = _('collapse')
			else:
				message = _('expand')
			return(message)
		if state:
			pattern.Collapse()
		else:
			pattern.Expand()
		return(True)
	def select(self, name = False, shouldSpeak = False):
		if shouldSpeak:
			return(True)
		pattern = None
		try:
			pattern = self.UIASelectionItemPattern
		except:
			pass
		if not pattern:
			return(False)
		selection = pattern.CurrentIsSelected
		if name:
			if not selection:
				# Translators: the message reported when doing an action
				name = _('select')
			else:
				name = _('remove selection')
			return(name)
		if selection:
			pattern.RemoveFromSelection()
		else:
			pattern.AddToSelection()
		return(True)
	def actionSetFocus(self, name = False, shouldSpeak = False):
		if shouldSpeak:
			return(True)
		if not (controlTypes.State.FOCUSABLE in self.states and not self.hasFocus):
			return(False)
		if name:
			# Translators: the message reported when setting focus to a control
			message = _('set focus')
			return(message)
		self.setFocus()
		return(True)
	def increaseValue(self, name = False, shouldSpeak = False):
		if shouldSpeak:
			return(False)
		pattern = self.UIARangeValuePattern
		if not pattern:
			return(False)
		value = pattern.CurrentValue
		newValue = pattern.CurrentSmallChange
		if name:
			# Translators: the message reported when doing an action
			message = _('Increase value')
			return(message)
		pattern.SetValue(value+newValue)
		return(True)
	def decreaseValue(self, name = False, shouldSpeak = False):
		if shouldSpeak:
			return(False)
		pattern = self.UIARangeValuePattern
		if not pattern:
			return(False)
		value = pattern.CurrentValue
		newValue = pattern.CurrentSmallChange
		if name:
			# Translators: the message reported when doing an action
			message = _('Decrease value')
			return(message)
			
		pattern.SetValue(value-newValue)
		return(True)
	def click(self, name = False, shouldSpeak = False):
		if shouldSpeak:
			return(True)
		if not (self.role in controlTypes.role.clickableRoles and self.role not in [controlTypes.Role.DOCUMENT, controlTypes.Role.SLIDER]):
			return(False)
		point = ctypes.wintypes.POINT(*self.location.center)
		newElement = element.ElementFromPoint(point)
		if not element.CompareElements(self.UIAElement, newElement):
			return(False)
		if name:
			# Translators: The message reported when doing an action
			message = _('Click')
			return(message)
		mousePosition = winUser.getCursorPos()
		winUser.setCursorPos(*self.location.center)
		mouseHandler.doPrimaryClick()
		winUser.setCursorPos(*mousePosition)
		return(True)
	def _get__possibleActions(self):
		actions = []
		actions.append(self.invoke)
		actions.append(self.toggle)
		actions.append(self.expandCollapse)
		actions.append(self.select)
		actions.append(self.increaseValue)
		actions.append(self.decreaseValue)
		actions.append(self.IAccessibleAction)
		actions.append((self.actionSetFocus))
		actions.append(self.click)
		return(actions)
	def _get_actionList(self):
		actions = []
		for i in self._possibleActions:
			name = i(name = True)
			if name:
				actions.append((i, name))
		return(actions)
	def getActionName(self, index = None):
		if not index:
			index = self.defaultActionIndex
		actionList = self.actionList
		if actionList:
			return(self.actionList[index][1])
		return(translate('No action'))
	def doDefaultAction(self):
		for i in self.actionList:
			try:
				i()
			except:
				continue
	def doAction(self, index = None):
		if not index:
			index = self.defaultActionIndex
		# sometimes, the UIAutomation implementation emulates key presses when the user is performing an action, so ignore injection here
		with keyboardHandler.ignoreInjection():
			try:
				self.actionList[index][0]()
			except:
				pass
	def simulateKeyPress(self, gesture):
		pattern = None
		try:
			pattern = self.UIASelectionItemPattern
		except:
			pass
		try:
			pattern.Select()
		except:
			pass
		self.actionSetFocus()
		gesture.send()

	def _get_UIAExpandCollapsePattern(self):
		return(self._getUIAPattern(UIAHandler.UIA_ExpandCollapsePatternId, UIAHandler.IUIAutomationExpandCollapsePattern))
	def setFocus(self):
		# Sometimes, trying to set focus raises an error
		try:
			super(NewUIA, self).setFocus()
		except:
			pass
class Desktop(window.Desktop, NewUIA):
	def _get_role(self):
		return(controlTypes.Role.WINDOW)
	def doAction(self, index = 0):
		raise NotImplementedError
	def _get_presentationType(self):
		return(self.presType_content)
class MSAAProxy(NewUIA):
	def _get_description(self):
		pattern = self.UIALegacyIAccessiblePattern
		if not pattern:
			return
		description = ''
		try:
			description = pattern.CurrentDescription
		except:
			pass
		return(description)
	def _get__possibleActions(self):
		actionList = []
		actionList.append(self.IAccessibleAction)
		actionList.append(self.click)
		actionList.append(self.expandCollapse)
		actionList.append(self.select)
		actionList.append(self.increaseValue)
		actionList.append(self.decreaseValue)
		actionList.append(self.actionSetFocus)
		actionList.append(self.invoke)
		actionList.append(self.toggle)
		return(actionList)
class SearchInfo():
	def __init__(self, nameList, modifiableNameList, elementDict, searchString):
		self.nameList = nameList
		self.modifiableNameList = modifiableNameList
		self.elementDict = elementDict
		self.searchString = searchString
class Ancestor(NewUIA):
	next =previous = firstChild = lastChild = None
	def _get_parent(self):
		try:
			parent = UIAHandler.handler.baseTreeWalker.GetParentElementBuildCache(self.UIAElement, UIAHandler.handler.baseCacheRequest)
		except:
			return(None)
		if not parent:
			return(None)
		return(Ancestor(UIAElement = parent))
class Search(NewUIA, VirtualBase):
	processID = 0
	appModule = appModuleHandler.getAppModuleFromProcessID(0)
	def __init__(self, searchInfo = None, index = None, *args, **kwargs):
		try:
			UIAElement = searchInfo.elementDict[searchInfo.modifiableNameList[index]]
		except:
			raise InvalidNVDAObject
		try:
			super(Search, self).__init__(UIAElement = UIAElement, *args, **kwargs)
		except:
			pass
		if not hasattr(self, "windowHandle"):
			super(Search, self).__init__(UIAElement = UIAElement, windowHandle = NVDAObject.objectWithFocus().windowHandle, *args, **kwargs)
		self.searchInfo = searchInfo
		self.index = index
	firstChild = lastChild = None
	def _get_name(self):
		try:
			name = self.searchInfo.modifiableNameList[self.index]
		except:
			name = ""
		return(name[:-6])
	def _get_parent(self):
		if not config.conf['enhancedObjectNavigation']['context']:
			return(None)
		try:
			parent = UIAHandler.handler.baseTreeWalker.GetParentElementBuildCache(self.UIAElement, UIAHandler.handler.baseCacheRequest)
		except:
			return(None)
		if not parent:
			return(None)
		return(Ancestor(UIAElement = parent))
	def _get_next(self):
		index = self.index+1
		l = self.searchInfo.modifiableNameList
		length = len(self.searchInfo.modifiableNameList)
		if index >= length:
			return(None)
		obj = Search(searchInfo = self.searchInfo, index = index)
		while not obj and index <= length:
			index += 1
			obj = Search(searchInfo = self.searchInfo, index = index)
		return(obj)
	def _get_previous(self):
		index = self.index-1
		l = self.searchInfo.modifiableNameList
		if index <0:
			return(None)
		obj = Search(searchInfo = self.searchInfo, index = index)
		while not obj:
			index -= 1
			obj = Search(searchInfo = self.searchInfo, index = index)
		return(obj)
	def searchForLetter(self, ch, index = None):
		indexList = []
		if not index:
			index = self.index
		nameList = self.searchInfo.modifiableNameList
		for i in range(len(nameList)):
			name = nameList[i][:-6].lower()
			if name.startswith(ch.lower()):
				indexList.append(i)
		if not indexList: return
		for i in indexList:
			if i > index:
				return(i)
		return(indexList[0])

	def event_typedCharacter(self, ch = None):
		super(Search, self).event_typedCharacter(ch = ch)
		searchInfo = self.searchInfo
		if config.conf['enhancedObjectNavigation']['altMode']:
			modifiers = keyboardHandler.currentModifiers
			if len(modifiers) == 1 and (winUser.VK_LMENU, False) in modifiers:
				index = self.searchForLetter(ch)
				if index == None: return
				obj = Search(searchInfo = self.searchInfo, index = index)
				while not obj:
					index = self.searchForLetter(ch)
					obj = Search(searchInfo = self.searchInfo, index = index)
				eventHandler.executeEvent('gainFocus', obj)
				return
		temporarySearchString = searchInfo.searchString
		temporarySearchString += ch
		l = []
		for i in searchInfo.modifiableNameList:
			if temporarySearchString.lower() in i[:-6].lower():
				l.append(i)
		if not l:
			# Translators: the message reported when no items is found
			message = _('No items')
			ui.message(message)
			return(None)
		searchInfo.modifiableNameList = copy.copy(l)
		searchInfo.searchString = temporarySearchString
		obj = Search(searchInfo = self.searchInfo, index = 0)
		index = 0
		while not obj:
			index += 1
			try:
				obj = Search(searchInfo = self.searchInfo, index = index)
			except:
				return
		eventHandler.executeEvent('gainFocus', obj)
	def _get_positionInfo(self):
		index = self.index+1
		d = {'indexInGroup': index, 'similarItemsInGroup': len(self.searchInfo.modifiableNameList)}
		return(d)
	def doAction(self, index = 0):
		eventHandler.executeEvent('gainFocus', self.focus)
		speech.speech.cancelSpeech()
		obj = NewUIA(UIAElement = self.UIAElement, windowHandle = self.windowHandle)
		api.setNavigatorObject(obj)
		speech.speech.speakObject(obj, reason = controlTypes.OutputReason.FOCUS)
		if config.conf['enhancedObjectNavigation']['setFocus']:
			obj.setFocus()
		if config.conf['enhancedObjectNavigation']['activate']:
			obj.doAction()
	@script(
		gestures = ('kb:downArrow', 'ts(navigation):flickDown')
	)
	def script_next(self, gesture):
		next = self.next
		if next:
			eventHandler.executeEvent('gainFocus', next)
	@script(
		gestures = ('kb:upArrow', 'ts(navigation):flickUp')
	)
	def script_previous(self, gesture):
		previous = self.previous
		if previous:
			eventHandler.executeEvent('gainFocus', previous)
	@script(
		gestures = ('kb:rightArrow', 'ts(navigation):flickRight')
	)
	def script_nextLetter(self, gesture):
		obj = self
		if not obj.name:
			while obj and not obj.name:
				obj = obj.next
			if obj:
				eventHandler.executeEvent('gainFocus', obj)
				return
		while obj and obj.name and obj.name[0].lower() == self.name[0].lower():
			obj = obj.next
		if obj:
			eventHandler.executeEvent('gainFocus', obj)
	@script(
		gestures = ('kb:leftArrow', 'ts(navigation):flickLeft')
	)
	def script_previousLetter(self, gesture):
		obj = self.previous
		if not obj: return
		name = True
		while not obj.name:
			name = False
			previous = obj.previous
			if not previous:
				break
			obj = previous
		if not name:
			eventHandler.executeEvent('gainFocus', obj)
			return
		letter = obj.name[0].lower()
		while obj.name and obj.name[0].lower() == letter:
			previous = obj.previous
			if previous:
				obj = previous
			else:
				break
		if previous:
			obj = obj.next
		if obj:
			eventHandler.executeEvent('gainFocus', obj)
	@script(
		gestures = ('kb:enter', 'kb:numpadEnter', 'ts(navigation):double_tap')
	)
	def script_enter(self, gesture):
		if isinstance(gesture, touchHandler.TouchInputGesture):
			obj = api.getNavigatorObject()
			if not isinstance(obj, Search) and isinstance(obj, UIA.UIA) and obj.UIAElement.CurrentClassName == 'CRootKey':
				obj.doAction()
				return
		self.doAction()
	@script(
		gestures = ('kb:backSpace', 'kb:delete', 'ts(navigation):2finger_flickLeft')
	)
	def script_backSpace(self, gesture):
		self.searchInfo.searchString = ''
		name = self.searchInfo.modifiableNameList[self.index]
		self.searchInfo.modifiableNameList = copy.copy(self.searchInfo.nameList)
		index = self.searchInfo.nameList.index(name)
		obj = Search(searchInfo = self.searchInfo, index = index)
		eventHandler.executeEvent('gainFocus', obj)
	@script(
		gestures = ('kb:shift+backspace', 'kb:shift+delete', 'ts(navigation):2finger_flickRight')
	)
	def script_shiftBackspace(self, gesture):
		self.searchInfo.searchString = ''
		# Translators: The message reported when resetting the search string
		message = _('Search reset')
		ui.message(message)
	@script(
		gesture = ("kb:home")
	)
	def script_home(self, gesture):
		obj = Search(searchInfo = self.searchInfo, index = 0)
		eventHandler.executeEvent("gainFocus", obj)
	@script(
		gesture = ("kb:end")
	)
	def script_end(self, gesture):
		index = len(self.searchInfo.modifiableNameList)-1
		obj = Search(searchInfo = self.searchInfo, index=index)
		eventHandler.executeEvent("gainFocus", obj)
def timerFunc(self): 
	if not config.conf['enhancedObjectNavigation']['autoUpdate']:
		return
	try:
		buffer = braille.handler.buffer
		if not buffer.regions:
			return
		lastRegion = buffer.regions[-1]
		if not buffer == braille.handler.mainBuffer or not isinstance(lastRegion, braille.NVDAObjectRegion) or not isinstance(lastRegion.obj, NewUIA):
			return
		braille.handler.handleUpdate(lastRegion.obj)
	except:
		pass
timer = wx.Timer(gui.mainFrame)
gui.mainFrame.Bind(wx.EVT_TIMER, handler = timerFunc, source = timer)
def NVDAToUIA(obj, useMSAA = False):
	if not isinstance(obj, window.Window):
		return(None)
	finalElement = None
	if isinstance(obj, UIA.UIA):
		return(NewUIA(UIAElement = obj.UIAElement, wasNavigatedTo= False))
	point = POINT(obj.location.center.x, obj.location.center.y)
	elementFromPoint = element.ElementFromPointBuildCache(point, UIAHandler.handler.baseCacheRequest)
	r = elementFromPoint.CurrentBoundingRectangle
	rect = locationHelper.RectLTRB(r.left, r.top, r.right, r.bottom)
	rect2 = rect.toLTWH()
	while elementFromPoint and rect2 != obj.location:
		elementFromPoint = element.RawViewWalker.GetParentElementBuildCache(elementFromPoint, UIAHandler.handler.baseCacheRequest)
		if elementFromPoint:
			r = elementFromPoint.CurrentBoundingRectangle
			rect = locationHelper.RectLTRB(r.left, r.top, r.right, r.bottom)
			rect2 = rect.toLTWH()
			if rect2 == obj.location and elementFromPoint.CurrentProcessId == obj.processID:
				break
		else:
			break
	if elementFromPoint:
		finalElement = elementFromPoint
	if not finalElement and isinstance(obj, IAccessible.IAccessible) and useMSAA:
		try:
			finalElement = element.ElementFromIAccessibleBuildCache(obj.IAccessibleObject, obj.IAccessibleChildID, UIAHandler.handler.baseCacheRequest)
		except:
			pass
	try:
		newObj = NewUIA(UIAElement = finalElement, wasNavigatedTo= False)
	except:
		newObj = None
	if newObj:
		return(newObj)
	finalElement = element.ElementFromHandleBuildCache(obj.windowHandle, UIAHandler.handler.baseCacheRequest)
	return(NewUIA(UIAElement = finalElement, wasNavigatedTo= False))
def nextElement(startElement, walker = simpleWalker):
	walker = walkerWithProcessID(startElement, walker)
	newElement = walker.GetFirstChildElement(startElement)
	if newElement and getNearestWindowHandle(newElement):
		return(newElement)
	newElement = walker.GetNextSiblingElement(startElement)
	if newElement and getNearestWindowHandle(newElement):
		return(newElement)
	newElement = startElement
	while newElement:
		newElement = walker.getParentElement(newElement)
		if newElement:
			siblingElement = walker.GetNextSiblingElement(newElement)
			if siblingElement and getNearestWindowHandle(siblingElement):
				return(siblingElement)
				
def previousElement(startElement, walker = simpleWalker):
	walker = walkerWithProcessID(startElement, walker)
	newElement = walker.GetPreviousSiblingElement(startElement)
	if not (newElement and getNearestWindowHandle(newElement)): # No valid previous sibling element
		newElement = walker.GetParentElement(startElement)
		return(newElement if newElement else None)
	while True:
		childElement = UIAUtils.getDeepestLastChildUIAElementInWalker(newElement, walker)
		if not childElement:
			break
		if childElement and getNearestWindowHandle(childElement):
			newElement = childElement
		else:
			break
	return(newElement)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = category
	__gestures = {}
	navigation = False
	forms = False
	wasInSearchList = False
	index = 0
	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(EnhancedObjectNavigationSettingsPanel)
		timer.Start(50)
		if touchHandler.handler: touchHandler.handler.setMode('navigation')
	def terminate(self, *args, **kwargs):
		super(GlobalPlugin, self).terminate(*args, **kwargs)
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(EnhancedObjectNavigationSettingsPanel)
		timer.Stop()
	def getScript(self, gesture):
		obj = api.getFocusObject()
		# Normaly, the GlobalPlugin scripts overwrites the NVDAObject scripts, but we don't want this when in the search list, as no of our GlobalPlugin scripts should be used in the search list,
		if isinstance(obj, Search):
			return
		return(super(GlobalPlugin, self).getScript(gesture))
	def nextAction(self, previous = False):
		obj = api.getNavigatorObject()
		if not obj.actionList:
			# Translators: the message reported when no actions are available
			message = _('No actions available')
			return(ui.message(message))
		actionList = obj.actionList
		index = obj.defaultActionIndex
		if not previous:
			index = obj.defaultActionIndex+1 if index < len(actionList)-1 else 0
		else:
			index = obj.defaultActionIndex-1 if index else len(actionList)-1
		obj.defaultActionIndex = index 
		ui.message(actionList[index][1])
	rotor = [
		{'displayName': Role.BUTTON.displayString, 'scriptName': 'Button', 'key': 'b', 'walker': quickNavWalker(UIAHandler.UIA_ButtonControlTypeId)},
		{'displayName': Role.LINK.displayString, 'scriptName': 'Link', 'key': 'k', 'walker': quickNavWalker(UIAHandler.UIA_HyperlinkControlTypeId)},
		# Translators: A rotor option:
		{'displayName': _("Actions"), 'function': nextAction, 'isSupported': lambda : isinstance(api.getNavigatorObject(), NewUIA) and api.getNavigatorObject().actionList},
		# Translators: A rotor option:
		{"displayName": _("control"), "scriptName": "control", "walker": quickNavWalker(UIAHandler.handler.windowTreeWalker), "key": "w"},
		{'displayName': Role.EDITABLETEXT.displayString, 'scriptName': 'Edit', 'key': 'e', 'walker': quickNavWalker(UIAHandler.UIA_EditControlTypeId)},
		{'displayName': Role.STATICTEXT.displayString, 'scriptName': 'Text', 'key': 'p', 'walker': quickNavWalker(UIAHandler.UIA_TextControlTypeId)},
		{'displayName': Role.DOCUMENT.displayString, 'scriptName': 'Document', 'key': 'd', 'walker': quickNavWalker(UIAHandler.UIA_DocumentControlTypeId)},
		{'displayName': Role.LIST.displayString, 'scriptName': 'List', 'key': 'l', 'walker': quickNavWalker(UIAHandler.UIA_ListControlTypeId)},
		{'displayName': Role.LISTITEM.displayString, 'scriptName': 'i', 'key': 'i', 'walker': quickNavWalker(UIAHandler.UIA_ListItemControlTypeId)},
		{'displayName': Role.TOOLBAR.displayString, 'scriptName': 'ToolBar', 'key': 'o', 'walker': quickNavWalker(UIAHandler.UIA_ToolBarControlTypeId)},
		{'displayName': Role.TABLE.displayString, 'scriptName': 'Table', 'key': 't', 'walker': quickNavWalker(UIAHandler.UIA_TableControlTypeId)},
		{'displayName': Role.COMBOBOX.displayString, 'scriptName': 'ComboBox', 'key': 'c', 'walker': quickNavWalker(UIAHandler.UIA_ComboBoxControlTypeId)},
		{'displayName': Role.HEADING.displayString, 'scriptName': 'Heading', 'key': 'h', 'walker': createHeadingWalker() },
		{'displayName': Role.CHECKBOX.displayString, 'scriptName': 'CheckBox', 'key': 'x', 'walker': quickNavWalker(UIAHandler.UIA_CheckBoxControlTypeId)},
		{'displayName': Role.RADIOBUTTON.displayString, 'scriptName': 'RadioButton', 'key': 'r', 'walker': quickNavWalker(UIAHandler.UIA_RadioButtonControlTypeId)},
		{'displayName': Role.GRAPHIC.displayString, 'scriptName': 'Graphic', 'key': 'g', 'walker': quickNavWalker(UIAHandler.UIA_ImageControlTypeId)},
		{'displayName': Role.STATUSBAR.displayString, 'scriptName': 'StatusBar', 'key': 'z', 'walker': quickNavWalker(UIAHandler.UIA_StatusBarControlTypeId)},
		{'displayName': Role.GROUPING.displayString, 'scriptName': 'Grouping', 'key': 'u', 'walker': quickNavWalker(UIAHandler.UIA_GroupControlTypeId)},
		{'displayName': _("menu, menu bar or menu item"), 'scriptName': 'Menu', 'key': 'm', 'walker': createMenuWalker()},
		{'displayName': _("tree or tree item"), 'scriptName': 'Tree', 'key': 'v', 'walker': createTreeWalker()},
		{'displayName': _("tab or tab item"), 'scriptName': 'Tab', 'key': 'q', 'walker': createTabWalker()},
		{'displayName': _("form field"), 'scriptName': 'FormField', 'key': 'f', 'walker': createFormFieldWalker()},
		{'displayName': _("focusable object"), 'scriptName': 'focusable', 'key': 'j', 'walker': createFocusableWalker()},
		{'displayName': _("Landmark").lower(), 'scriptName': 'Landmark', 'key': 'n', 'walker': createLandmarkWalker()},
		{'displayName': _("same item"), 'scriptName': 'SameItem', 'key': 's', 'walker': createSameItemWalker},
	]
	def nextRotor(self, previous = False, setIndex = True, index = None):
		if not index:
			index = self.index
		if not previous:
			index = index + 1 if index < len(self.rotor)-1 else 0
		else:
			index = index -1 if index else len(self.rotor)-1
		if not setIndex: return(index)
		supported = self.rotor[index].get('isSupported')
		while supported and not supported():
			index = self.nextRotor(previous = previous, setIndex = False, index = index)
			supported = self.rotor[index].get('isSupported')
		self.index = index
	def nextObject(self, obj, walker = simpleWalker):
		if hasattr(walker, '__call__'):
			walker = walker()
		element = nextElement(obj.UIAElement, walker)
		if not element:
			ui.message(translate('No next'))
			return(None)
		element = element.BuildUpdatedCache(cacheRequest)
		newObj = NewUIA(UIAElement = element)
		api.setNavigatorObject(newObj)
		speech.speech.speakObject(newObj, reason = controlTypes.OutputReason.FOCUS)
	def previousObject(self, obj, walker = simpleWalker):
		if not isinstance(obj, NewUIA):
			obj = NVDAToUIA(obj)
		if hasattr(walker, '__call__'):
			walker = walker()
		element = previousElement(obj.UIAElement, walker)
		if not element:
			ui.message(translate('No previous'))
			return(None)
		element = element.BuildUpdatedCache(cacheRequest)
		newObj = NewUIA(UIAElement = element)
		api.setNavigatorObject(newObj)
		speech.speech.speakObject(newObj, reason = controlTypes.OutputReason.FOCUS)
	def _report(self, on, forms = False):
		if not config.conf["enhancedObjectNavigation"]["useSounds"]:
			if on:
				# Translators: the message reported when navigation mode is turned on.
				message = _("Navigation mode")
			else:
				obj = api.getFocusObject()
				if obj.treeInterceptor and not obj.treeInterceptor.passThrough:
					message = translate("Focus mode")
				else:
					message = translate("Browse mode")
			ui.message(message)
			return
		if on:
			file = startFile
		else:
			obj = api.getFocusObject()
			if obj.treeInterceptor and not obj.treeInterceptor.passThrough:
				file = os.path.join(NVDAAudioFilesPath, "browseMode.wav")
			else:
				file = os.path.join(NVDAAudioFilesPath, "focusMode.wav")
		nvwave.playWaveFile(file)
	def turnOn(self):
		if self.navigation:
			return
		self.clearGestureBindings()
		self.bindGestures(self.__gestures)
		self.navigation = True
		self.forms = False
		self.bind()
		self._report(True)
	def turnOff(self, forms = False):
		if not self.navigation:
			return
		self.clearGestureBindings()
		self.bindGestures(self.__gestures)
		
		if forms:
			self.forms = True
			self.bindGesture('kb:escape', 'escapeForms')
			self._report(False, forms=True)
		if self.navigation:
			self.navigation = False
		if not forms:
			self._report(False)
	keyList = [
		('tab', 'ts(navigation):3finger_flickRight'),
		('shift+tab', 'ts(navigation):3finger_flickLeft'),
		('f6', 'ts(navigation):3finger_flickDown'),
		('shift+f6', 'ts(navigation):3finger_flickUp'),
		("escape", "ts(navigation):2finger_flickUp")
	]
	@classmethod
	def createScripts(cls):
		# Translators: A string that will be reported after a role in some input help messages, such as in 'moves to the next button in the same application'
		after = _('in the same application')

		for i in cls.rotor:
			key = i.get('key')
			walker = i.get('walker')
			if not key or not walker:
				continue
			scriptName = i.get('scriptName')
			# Translators: The message reported before a role name in input help, such as 'Moves the navigator object to the next' in 'Moves the navigator object to the next button in the same application'
			before = _('Moves the navigator object to the next')
			middle = f' {i.get("displayName")} '
			@navigationScript
			def next(self, gesture, key = key, walker = walker):
				self.nextObject(api.getNavigatorObject(), walker = walker)
			next.__doc__ = before+middle+after
			setattr(cls, 'script_next'+scriptName, next)
			# Translators: The message reported before a role name in input help, such as 'Moves the navigator object to the previous' in 'Moves the navigator object to the previous button in the same application'
			before = _('Moves the navigator object to the previous')
			middle = f' {i.get("displayName")} '
			@navigationScript
			def previous(self, gesture, key = key, walker = walker):
				self.previousObject(api.getNavigatorObject(), walker = walker)
			previous.__doc__ = before+middle+after
			setattr(cls, 'script_previous'+scriptName, previous)
			# Translators: The message reported before a role name in input help, such as 'lists every button' in the sentence 'Lists every button in the window'
			before = _('Lists every')
			middle = f' {i.get("displayName").lower()} '
			# Translators: the message reported after a role in input help, such as in the sentence 'Lists every button in the window'. Ignore this if not neaded for your language
			after2 = _('in the window or control where the navigator object is located, or  every object on the screen, depending on what you have selected in settings')
			@navigationScript
			def searchIndividualy(self, gesture, key = key, walker = walker):
				search(gesture = gesture, walker = walker)
			searchIndividualy.__doc__ = before+middle+after2
			setattr(cls, 'script_'+scriptName+'List', searchIndividualy)
		for i in cls.keyList:
			key = i[0]
			scriptName = key.replace('+', '_')
			def press(self, gesture, key = key):
				send(key)
			gesture = keyboardHandler.KeyboardInputGesture.fromName(key)
			# Translators: The start of a script description
			before = _('Emulates pressing')
			# Translators: The end of a script description
			after = _('on the system keyboard')
			press.__doc__ = before+f' {gesture.displayName} '+after
			setattr(cls, 'script_'+scriptName, press)
			cls.__gestures.update({i[1]: scriptName})
	def bind(self):
		if config.conf["enhancedObjectNavigation"]["advancedNavigation"]:
			self.bindGesture('kb:rightArrow', 'nextObject')
			self.bindGesture('kb:leftArrow', 'previousObject')
			self.bindGesture('kb:upArrow', 'previousRotorItem')
			self.bindGesture('kb:downArrow', 'nextRotorItem')
			self.bindGesture('kb:pageDown', 'nextRotor')
			self.bindGesture('kb:pageUp', 'previousRotor')
		else:
			self.bindGesture("kb:rightArrow", "nextSibling")
			self.bindGesture("kb:leftArrow", "previousSibling")
			self.bindGesture("kb:upArrow", "parent")
			self.bindGesture("kb:downArrow", "firstChild")
		self.bindGesture('kb:space', 'doAction')
		self.bindGesture("kb:shift+space", "secondaryAction")
		passThroughKeys = [
			"kb:enter",
			"kb:numbpadEnter",
			"kb:applications",
			"kb:shift+f10"
		]
		for i in passThroughKeys:
			self.bindGesture(i, "passThrough")
		self.bindGesture("kb:NVDA+a", "advancedNavigation")
		self.bindGesture("kb:home", "home")
		self.bindGesture("kb:end", "end")
		for i in self.rotor:
			scriptName = i.get('scriptName')
			if not scriptName:
				continue
			key = i.get('key')
			self.bindGesture('kb:'+key, 'next'+scriptName)
			self.bindGesture('kb:shift+'+key, 'previous'+scriptName)
			self.bindGesture('kb:shift+control+'+key, scriptName+'List')
	def event_gainFocus(self, obj, nextHandler):
		if not config.conf["enhancedObjectNavigation"]["useByDefault"] or not isinstance(obj, window.Window):
			self.turnOff()
			return(nextHandler())
		if isinstance(obj, cursorManager.CursorManager):
			self.turnOff()
			return(nextHandler())
		if obj.treeInterceptor and not obj.treeInterceptor.passThrough:
			self.turnOff()
			return(nextHandler())
		self.turnOn()
		nextHandler()
	@script(
		# Translators: the input help message for the UIANavigation script
		description = _("Turns on UIA navigation. This allows you to navigate through all UIAutomation elements with the object navigation commands. This is most useful for testing purposes."),
		category = SCRCAT_OBJECTNAVIGATION,
		gesture = ("kb:nvda+shift+f1")
	)
	def script_UIANavigation(self, gesture):
		obj = api.getNavigatorObject()
		if not obj:
			ui.message(translate("No navigator object"))
			return(None)
		obj = NVDAToUIA(obj)
		if not obj:
			# Translators: the message reported when the user can not turn on UIA navigation
			message = _('You can not turn on UIA navigation here')
			ui.message(message)
			return(None)
		api.setNavigatorObject(obj)
		# Translators: the message indicating that UIA navigation mode has been turned on.
		ui.message(_("UIA navigation on"))
		speech.speech.speakObject(api.getNavigatorObject())
	@script(
		# Translators: the input help message for the nextObject script
		description = _('Moves to the next object within the same application'),
		gesture = ('ts(navigation):flickRight')
	)
	@navigationScript
	def script_nextObject(self, gesture):
		obj = api.getNavigatorObject()
		self.nextObject(obj, simpleWalker)
	@script(
		# Translators: the description for the previousObject script
		description = _('Moves to the previous object within the same application'),
		gesture = ('ts(navigation):flickLeft')
	)
	@navigationScript
	def script_previousObject(self, gesture):
		obj = api.getNavigatorObject()
		self.previousObject(obj, simpleWalker)
	@script(
		# Translators: the input help message for the nextRotorItem script
		description = _('Moves to the next object depending on the rotor setting'),
		gesture = ('ts(navigation):flickDown')
	)
	@navigationScript
	def script_nextRotorItem(self, gesture):
		index = self.index
		supported = self.rotor[index].get('isSupported')
		if supported and not supported():
			self.nextRotor(previous = True)
		rotorItem = self.rotor[index]
		f = rotorItem.get('function')
		if not f:
			obj = NVDAToUIA(api.getNavigatorObject())
			self.nextObject(obj, rotorItem['walker'])
			return(None)
		f(self)
	@script(
		# Translators: the input help message for the previousRotorItem script
		description = _('Moves to the previous object depending on the rotor setting'),
		gesture = ('ts(navigation):flickUp')
	)
	@navigationScript
	def script_previousRotorItem(self, gesture):
		index = self.index
		supported = self.rotor[index].get('isSupported')
		if supported and not supported():
			self.nextRotor(previous = False)
		rotorItem = self.rotor[index]
		f = rotorItem.get('function')
		if not f:
			obj = NVDAToUIA(api.getNavigatorObject())
			self.previousObject(obj, rotorItem['walker'])
			return(None)
		f(self, previous = True)
	@script(
		# Translators: the input help message for the nextRotor script
		description = _('selects the next rotor setting'),
		gesture = ('ts(navigation):2finger_flickRight')
	)
	@navigationScript
	def script_nextRotor(self, gesture):
		self.nextRotor()
		rotorItem = self.rotor[self.index]
		ui.message(rotorItem['displayName'])
	@script(
		# Translators: the input help message for the previousRotor script
		description = _('selects the previous rotor setting'),
		gesture = ('ts(navigation):2finger_flickLeft')
	)
	@navigationScript
	def script_previousRotor(self, gesture):
		self.nextRotor(previous = True)
		rotorItem = self.rotor[self.index]
		ui.message(rotorItem['displayName'])
	@script(
		# Translators: the input help message for the navigationMode script
		description = _('Turns on or off navigation mode. If pressed twice, the state of the navigation mode is saved'),
		gesture = 'kb:nvda+shift+control+space'
	)
	def script_navigationMode(self, gesture):
		focus = api.getFocusObject()
		if focus.treeInterceptor and not focus.treeInterceptor.passThrough:
			# Translators: The message reported when the user is in browse mode and tries to turn on navigation mode
			ui.message(_("Please disable browse mode with NVDA + space before using navigation mode"))
			return
		if getLastScriptRepeatCount():
			# Translators: the message reported when saving the state of the navigation mode
			message = _('Saved')
			ui.message(message)
			config.conf['enhancedObjectNavigation']['useByDefault'] = self.navigation
			return
		obj = api.getNavigatorObject()
		if not self.navigation:
			self.turnOn()
			if not isinstance(obj, NewUIA):
				api.setNavigatorObject(NVDAToUIA(obj))
		else:
			self.turnOff()
			if isinstance(obj, NewUIA):
				api.setNavigatorObject(obj.NVDAObject)
	@script(
		# Translators: the input help message for the search script
		description = _('Lists every object in the current window, control or on the screen, depending on what you have selected in the settings.'),
		gestures = ('kb:NVDA+control+enter', 'ts(navigation):2finger_tripple_tap')
	)
	def script_search(self, gesture):
		search(gesture = gesture)
	@script(
		gesture = ('ts(navigation):double_tap'),
		description = commands.script_review_activate.__doc__
	)
	@navigationScript
	def script_doAction(self, gesture):
		obj = api.getNavigatorObject()
		focusElement = element.GetFocusedElement()
		if element.CompareElements(obj.UIAElement, focusElement) and not obj.actionList and super(NewUIA, obj).UIATextPattern:
			self.turnOff(forms = True)
			focusObj = api.getFocusObject()
			api.setNavigatorObject(focusObj)
			return
		index = obj.defaultActionIndex	
		if not obj.actionList:
			ui.message(translate('No action'))
			return
		if obj.actionList[index][0](shouldSpeak = True):
			commands.script_review_activate(gesture)
			return
		obj.doAction(index = obj.defaultActionIndex)
		if isinstance(gesture, touchHandler.TouchInputGesture):
			touchHandler.handler.notifyInteraction(obj)
	@script(
		gesture = ('ts(navigation):tripple_tap'),
		# Translators: The description for a script
		description = _('Selects, unselects, or decreases the value of the current navigator object depending on what the object supports')
	)
	@navigationScript
	def script_secondaryAction(self, gesture):
		obj = api.getNavigatorObject()
		obj = NVDAToUIA(obj)
		obj.select() or obj.decreaseValue()
	@navigationScript
	def script_escapeForms(self, gesture):
		self.turnOn()
	@script(
		description = commands.script_navigatorObject_next.__doc__
	)
	@navigationScript
	def script_nextSibling(self, gesture):
		commands.script_navigatorObject_next(gesture)
	@script(
		description = commands.script_navigatorObject_previous.__doc__
	)
	@navigationScript
	def script_previousSibling(self, gesture):
		commands.script_navigatorObject_previous(gesture)
	@script(
		description = commands.script_navigatorObject_firstChild.__doc__
	)
	@navigationScript
	def script_firstChild(self, gesture):
		commands.script_navigatorObject_firstChild(gesture)
	@script(
		description = commands.script_navigatorObject_parent.__doc__
	)
	@navigationScript
	def script_parent(self, gesture):
		commands.script_navigatorObject_parent(gesture)
	@script(
		# Translators: the description for a script
		description = _("Turns off or on advanced navigation")
	)
	def script_advancedNavigation(self, gesture):
		advancedNavigation = config.conf["enhancedObjectNavigation"]["advancedNavigation"]
		config.conf["enhancedObjectNavigation"]["advancedNavigation"] = not advancedNavigation
		self.clearGestureBindings()
		self.bindGestures(self.__gestures)
		self.bind()
		if advancedNavigation:
			# Translators: The message reported when toggeling advanced navigation
			message = _("Advanced navigation on")
		else:
			# Translators: The message reported when toggeling advanced navigation
			message = _("Advanced navigation off")
		ui.message(message)
	@script(
		# Translators: the description for a script
		description = _("Tryes to set focus to the current navigator object, and then passes the gesture through to the application")
	)
	@navigationScript
	def script_passThrough(self, gesture):
		api.getNavigatorObject().simulateKeyPress(gesture)
	@script(
		# Translators: the description for a script
		description = _("moves the navigator object to the first object in the current container")
	)
	@navigationScript
	def script_home(self, gesture):
		obj = api.getNavigatorObject()
		parent = obj.simpleParent
		if not parent:
			return
		api.setNavigatorObject(parent.simpleFirstChild)
		speech.speech.speakObject(api.getNavigatorObject(), reason = controlTypes.OutputReason.FOCUS)
	@script(
		# Translators: The description for a script
		description = _("Moves the navigator object to the last object in the current container")
	)
	@navigationScript
	def script_end(self, gesture):
		obj = api.getNavigatorObject()
		parent = obj.simpleParent
		if not parent:
			return
		api.setNavigatorObject(parent.simpleLastChild)
		speech.speech.speakObject(api.getNavigatorObject(), reason = controlTypes.OutputReason.FOCUS)
GlobalPlugin.createScripts()