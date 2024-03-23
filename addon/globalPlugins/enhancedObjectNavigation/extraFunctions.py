# A module witch contains classes and functions that I will be using in multiple of my addons
# Licensed under the same license as NVDA. To see the license, Open the NVDA menu, go to 'Help' and go to 'License'.
import api
import braille
import controlTypes
import copy
import ctypes
import cursorManager
import eventHandler
import globalPluginHandler
import keyboardHandler
import ui
import winInputHook
import winUser
from keyboardHandler import ignoreInjection
from logHandler import log
from NVDAObjects import DynamicNVDAObjectType, InvalidNVDAObject, NVDAObject
from NVDAObjects.window import Window
from textInfos import POSITION_FIRST
from textInfos.offsets import OffsetsTextInfo
from time import sleep
VK_NONE = 255
KEYEVENTF_KEYUP = 2
user32 = ctypes.windll.user32
translate = _
oldKeyDownCallback = winInputHook.keyDownCallback
def newKeyDownCallback(vkCode, scanCode, extended, injected):
	res = oldKeyDownCallback(vkCode, scanCode, extended, injected)
	obj = api.getFocusObject()
	if not res or vkCode in keyboardHandler.KeyboardInputGesture.TOGGLE_KEYS or not isinstance(obj, VirtualBase):
		return(res)
	modifiers = []
	for i in keyboardHandler.currentModifiers:
		modifier = keyboardHandler.KeyboardInputGesture.NORMAL_MODIFIER_KEYS.get(i[0])
		if isinstance(modifier, int):
			modifiers.append(modifier)
	states = (ctypes.c_byte*256)()
	for i in range(256):
		if i in modifiers:
			states[i] = -128 # we tell ToUnicodeEx that the key is down even when it isn't according to windows
		else:
			states[i] = ctypes.windll.user32.GetKeyState(i)
	buffer = ctypes.create_unicode_buffer(5)
	layout = ctypes.windll.user32.GetKeyboardLayout(obj.windowThreadID)
	res = ctypes.windll.user32.ToUnicodeEx(vkCode, scanCode, states, buffer, len(buffer), 0x0, layout)
	if res>0:
		for i in buffer[:res]:
			eventHandler.queueEvent("typedCharacter",obj, ch = i)
winInputHook.keyDownCallback = newKeyDownCallback
oldShouldUseToUnicodeEx = keyboardHandler.shouldUseToUnicodeEx
def newShouldUseToUnicodeEx(focus = None):
	res = oldShouldUseToUnicodeEx(focus = focus)
	if not focus:
		focus = api.getFocusObject()
	if not isinstance(focus, VirtualBase):
		return(res)
	return(False)
keyboardHandler.shouldUseToUnicodeEx = newShouldUseToUnicodeEx
class NewDynamicNVDAObjectType(DynamicNVDAObjectType):
	def __call__(self,chooseBestAPI=True,**kwargs):
		if chooseBestAPI:
			APIClass=self.findBestAPIClass(kwargs)
			if not APIClass: return None
		else:
			APIClass=self

		# Instantiate the requested class.
		try:
			obj=APIClass.__new__(APIClass,**kwargs)
			obj.APIClass=APIClass
			if isinstance(obj,self):
				obj.__init__(**kwargs)
		except InvalidNVDAObject as e:
			log.debugWarning("Invalid NVDAObject: %s" % e, exc_info=True)
			return None
		#return(obj)
		clsList = []
		if 'findOverlayClasses' in APIClass.__dict__:
			obj.findOverlayClasses(clsList)
		else:
			clsList.append(APIClass)
		# Skip app modules and global plugins, because they may contain classes that will create errors ore otherwise unexpected behavior.
		# After all other mutation has finished,
		# add LockScreenObject if Windows is locked.
		# LockScreenObject must become the first class to be resolved,
		# i.e. insertion order of 0.
		self._insertLockScreenObject(clsList)
		# Determine the bases for the new class.
		bases = []
		for i in range(len(clsList)):
			# A class doesn't need to be a base if it is already implicitly included by being a superclass of a previous base.
			if i==0 or not issubclass(clsList[i-1], clsList[i]):
				bases.append(clsList[i])
		if len(bases) == 1:
			# We only have one base, so there's no point in creating a dynamic type.
			newCls = clsList[0]
		else:
			bases = tuple(bases)
			newCls = self._dynamicClassCache.get(bases, None)
			if not newCls:
				name="Dynamic_%s"%"".join([x.__name__ for x in clsList])
				newCls=type(name,bases,{"__module__": __name__})
				self._dynamicClassCache[bases] = newCls
		oldMro = frozenset(obj.__class__.__mro__)
		# Mutate obj into the new class.
		obj.__class__ = newCls
		# Initialise the overlay classes.
		for cls in reversed(newCls.__mro__):
			if cls in oldMro:
				# This class was part of the initially constructed object, so its constructor would have been called.
				continue
			initFunc = cls.__dict__.get("initOverlayClass")
			if initFunc:
				try:
					initFunc(obj)
				except:
					log.exception(f"Exception in initOverlayClass for {cls}")
		return(obj)
class nNewDynamicNVDAObjectType(DynamicNVDAObjectType):
	def __call__(self, chooseBestAPI = True, **kwargs):
#		return(super(NewDynamicNVDAObjectType, self).__call__(chooseBestAPI = chooseBestAPI, **kwargs))
		if chooseBestAPI:
			APIClass=self.findBestAPIClass(kwargs)
			if not APIClass: return None
		else:
			APIClass=self

		# Instantiate the requested class.
		try:
			obj=APIClass.__new__(APIClass,**kwargs)
			obj.APIClass=APIClass
			if isinstance(obj,self):
				obj.__init__(**kwargs)
		except InvalidNVDAObject as e:
			log.debugWarning("Invalid NVDAObject: %s" % e, exc_info=True)
			return None
		clsList = []
		obj.findOverlayClasses(clsList)
		obj.appModule.chooseNVDAObjectOverlayClasses(obj, clsList)
		return(obj)
	# Redefines _insertLockScreenObject, because it is the last function that modifies clsList in __call__. Because of this, we can remove any class from clsList that we don't want
#	def _insertLockScreenObject(self, clsList):
#		ui.message(str(clsList))
#		copyList = copy.copy(clsList)
#		for i in copyList:
#			if not issubclass(i, clsList[-1]): # This class is not a subclass of the API class, and therefor may cause unstable behavior
				#clsList.remove(i)
#				pass
#		ui.message(str(clsList))
#		return(super(NewDynamicNVDAObjectType, self)._insertLockScreenObject(clsList))
class VirtualDocumentTextInfo(cursorManager._ReviewCursorManagerTextInfo, OffsetsTextInfo):
	def _getStoryText(self):
		return(self.obj.value)
	def _getStoryLength(self):
		return(len(self._getStoryText()))
class VirtualBase(Window, metaclass = NewDynamicNVDAObjectType):
	def __init__(self, *args, **kwargs):
		super(VirtualBase, self).__init__(*args, **kwargs)
		focus = api.getFocusObject()
		nav = api.getNavigatorObject()
		review = api.getReviewPosition()
		if type(self) == type(focus):# The user navigated to an object that has the exact same type as this one, e.g another item in a virtual list, so fetch the properties from the previous item.
			nav =focus.nav
			review = focus.review

			focus = focus.focus
		self.focus = focus
		self.nav = nav
		self.review = review
	def script_escape(self, gesture):
		eventHandler.executeEvent('gainFocus', self.focus)
		api.setNavigatorObject(self.nav)
		api.setReviewPosition(self.review)
	__gestures ={
		'kb:escape': 'escape'
	}
class VirtualDocument(cursorManager.ReviewCursorManager, VirtualBase):

	def __init__(self, text = None, title = None):
		self.value = text
		if not title:
			title = translate('NVDA message')
		self.name = title
		super(VirtualDocument, self).__init__(windowHandle = -1)
	def initCursorManager(self):
		self._selection = self.makeTextInfo(POSITION_FIRST)
	TextInfo = VirtualDocumentTextInfo
	role = controlTypes.Role.DOCUMENT


