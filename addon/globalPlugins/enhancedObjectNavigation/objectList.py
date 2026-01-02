# Search dialogs for the enhanced object navigation add-on
# Copyright (C) 2024-2025, Emil-18
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html
# See the file COPYING for more details.
import api
import browseMode
import config
import controlTypes
import ctypes
import gui
import re
import threading
import time
import ui
import UIAHandler
import winUser
import watchdog
import wx
from gui import guiHelper
from logHandler import log
from NVDAObjects import IAccessible, window, UIA
from keyboardHandler import currentModifiers
from speech import speech



searching = False


def _recoverFromSearch():
	now = time.time()
	
	while searching:
		time.sleep(0.05)
		if ctypes.windll.user32.GetKeyState(winUser.VK_LCONTROL) > 1 and time.time()-now > 10: # The left control key is held down and we have searched for at least 10 seconds, to allow the user to release the control key first
			watchdog._recoverAttempt()


class ObjectList(gui.SettingsDialog):
	# Translators: The title of the search dialog
	title = _("Search")
	def _getListInformation(self, obj):
		from . import validateObject, getGlobalPluginInstance
		validation = self.getRotorOption()
		#now = time.time()
		global searching
		listInfo = []
		objectList = []
		searching = True
		#threading.Thread(target = _recoverFromSearch).start()
		
		for i in obj.recursiveDescendants:
			#if ctypes.windll.user32.GetKeyState(winUser.VK_LCONTROL) > 1 and time.time()-now > 10: # The left control key is held down and we have searched for at least 10 seconds, to allow the user to release the control key first
				#searching = False
				#return
			if i in objectList or not validateObject(i, validation = validation):
				continue
			objectList.append(i)
			role = i.roleText
			if not role:
				role = i.role.displayString
			name = i.name
			if name is None:
				name = ""
			listInfo.append((name, role, i))
		return(listInfo)
	def setAlive(self):
		while self.searching:
			watchdog.alive()
	def getRotorOption(self):
		from . import getGlobalPluginInstance
		plugin = getGlobalPluginInstance()
		key = self.key
		#key = "b"
		for i in plugin.rotor:
			if key and i.get("key") == key:
				return(i)
	def __init__(self,  *args, obj: "NVDAObject" = None, startObj: "NVDAObject" = None, key = None, wasInNavigationMode = False, **kwargs):
		global searching
		self.objectList = []
		self.startObj = startObj
		self.key = key
		self.wasInNavigationMode = wasInNavigationMode
		self.searching = True
		# If the getListInformation call takes too long, NVDA may think that the core is frozen, thus restoring it, canceling the call in the process
		# Do not use watchdog.Suspender, as it causes problems with fetching the name from sysListView32 controls within the NVDA process.
		# Instead, do the following
		threading.Thread(target = self.setAlive, daemon = True).start()
		try:
			self.objectList = self._getListInformation(obj)
		except Exception as ex:
			log.error(ex)
			self.searching = False
		self.searching = False
		if not config.conf["enhancedObjectNavigation"]["sortInTabOrder"]:
			def sort(key):
				return(key[0].lower())
			self.objectList.sort(key = sort)
		self.filteredObjectList = self.objectList.copy()
		self.displayNames = []
		for i in self.objectList:
			self.displayNames.append(self.listItemToDisplayName(i))
		super(ObjectList, self).__init__(*args, **kwargs)	
	def makeSettings(self, settingsSizer):
		
		startObj = self.startObj
		sizer = guiHelper.BoxSizerHelper(self, sizer = settingsSizer)
		# Translators: The label for an edit control in the object list dialog
		label = _("Filter by &control type")
		self.roleFilter = sizer.addLabeledControl(label, wx.TextCtrl)
		self.roleFilter.Bind(wx.EVT_TEXT, self.onTextChange)
		
		# Translators: The label for an edit control in the object list dialog
		label = _("Filter by n&ame")
		self.nameFilter = sizer.addLabeledControl(label, wx.TextCtrl)
		self.nameFilter.Bind(wx.EVT_TEXT, self.onTextChange)
		# Translators: the label for a list box in the object list dialog
		label = _("&Objects")
		self.list = sizer.addLabeledControl(label, wx.ListBox, choices=self.displayNames)
		self.list.Bind(wx.EVT_KEY_DOWN, self.onListChar)
		# Translators: The label for a button in the object list dialog
		label = _("Move &navigator object")
		self.moveNavigatorObjectBtn = sizer.addItem(wx.Button(self, label=label))
		self.moveNavigatorObjectBtn.Bind(wx.EVT_BUTTON, self.moveNavigatorObjectEvt)
		#self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		self.cachedRoleFilterText = ""
		self.cachedNameFilterText = ""
		focusIndex = 0
		if startObj and not isinstance(self, UIAObjectList):
			for i in enumerate(self.objectList):
				if i[1][2] == startObj:
					focusIndex = i[0]
		if self.objectList:
			self.list.SetSelection(focusIndex)
	def postInit(self):
		self.nameFilter.SetFocus()
	def onOk(self, evt):
		if not self.filteredObjectList:
			return
		if self.wasInNavigationMode:
			config.conf["enhancedObjectNavigation"]["useByDefault"] = True
		index = self.list.GetSelection()
		try:
			wx.CallLater(100, self.moveCursor, index)
		finally:
			super(ObjectList, self).onOk(evt)
	def onCancel(self, evt):
		if self.wasInNavigationMode:
			config.conf["enhancedObjectNavigation"]["useByDefault"] = True
		super(ObjectList, self).onOk(evt)

	def onTextChange(self, evt: wx.Event):
		nameText = self.nameFilter.GetValue()
		roleText = self.roleFilter.GetValue().lower()
		index = None
		obj = None
		if self.filteredObjectList:
			index = self.list.GetSelection()
			obj = self.filteredObjectList[index][2]
		self.filteredObjectList.clear()
		displayNames = []
		for data in self.objectList:
			displayName = self.listItemToDisplayName(data)
			name = data[0]
			role = data[1].lower()
			append = False
			if not nameText and not roleText:
				append = True
			try:
				foundName = nameText.lower() in name.lower() if not config.conf["enhancedObjectNavigation"]["regex"] else re.findall(nameText, name, re.IGNORECASE)
			except re.error:
				return
			if (nameText or roleText) and foundName and role.startswith(roleText):
				append = True
			if append:
				self.filteredObjectList.append(data)
				displayNames.append(self.listItemToDisplayName(data))
		self.list.SetItems(displayNames)
		speech.cancelSpeech()
		focusIndex = 0
		if displayNames:
			if len(roleText) < len(self.cachedRoleFilterText) or len(nameText) < len(self.cachedNameFilterText):
				for i in enumerate(self.filteredObjectList):
					if i[1][2] == obj:
						focusIndex = i[0]
		else:
			# Translators: The message reported when no items was found
			message = _("No items")
			ui.message(message)
			return
		text = displayNames[focusIndex]
		self.list.SetSelection(focusIndex)
		ui.message(text)
		self.cachedRoleFilterText = roleText
		self.cachedNameFilterText = nameText
	def onListChar(self, evt: wx.Event):
		if evt.GetKeyCode() == 32: # space
			self.moveNavigatorObject(self.list.GetSelection())
			return
		evt.Skip()



	def moveNavigatorObjectEvt(self, evt: wx.Event):
		if not self.filteredObjectList:
			return
		index = self.list.GetSelection()
		self.Destroy()
		wx.CallLater(100, self.moveNavigatorObject, index)


	def moveCursor(self, index):
		
		from . import handleMoveToUIA, handleMoveBrowseModeCursor, handleMoveFocusIfFailed, shouldUseUIAWhenNavigating
		speech.cancelSpeech()
		obj = self.filteredObjectList[index][2]
		if self.wasInNavigationMode:
			if shouldUseUIAWhenNavigating(obj):
				handleMoveToUIA(obj, shouldCreateUIAObject = True)
			else:
				api.setNavigatorObject(obj)
				#speech.cancelSpeech()
				speech.speakObject(obj, reason = controlTypes.OutputReason.FOCUS)
			return	
		if obj.treeInterceptor and isinstance(obj.treeInterceptor, browseMode.BrowseModeTreeInterceptor):
			handleMoveBrowseModeCursor(obj)
			return()
		obj.setFocus()
		wx.CallLater(500, handleMoveFocusIfFailed, obj)
	def moveNavigatorObject(self, index: int):
		obj = self.filteredObjectList[index][2]
		api.setNavigatorObject(obj)
		speech.cancelSpeech()
		speech.speakObject(obj, reason=controlTypes.OutputReason.FOCUS)

	@staticmethod
	def listItemToDisplayName(item: tuple) -> str:
		name, role = item[0], item[1]
		if name:
			displayName = f"{name}, {role}"
		else:
			displayName = role
		return(displayName)


class UIAObjectList(ObjectList):
	def _getListInformation(self, obj: "NVDAObject") -> list:
		from . import simpleWalker, getSearchableElement
		clientObject = UIAHandler.handler.clientObject
		#UIAElement = clientObject.ElementFromHandle(obj.windowHandle)
		UIAElement = getSearchableElement()
		
		condition = simpleWalker().Condition
		option = self.getRotorOption()
		if option:
			otherCondition = self.getRotorOption().get("walker")
			if hasattr(otherCondition, "__call__"):
				otherCondition = otherCondition()
			otherCondition = otherCondition.Condition
			condition = clientObject.CreateAndCondition(condition, otherCondition)
		
		elementList = UIAElement.FindAllBuildCache(
			UIAHandler.TreeScope_Descendants,
			condition,
			UIAHandler.handler.baseCacheRequest
		)
		listInfo = []
		for i in range(elementList.Length):
			element = elementList.GetElement(i)
			role = UIAHandler.UIAControlTypesToNVDARoles.get(element.CurrentControlType)
			if not role:
				role = controlTypes.Role.UNKNOWN
			roleText = role.displayString
			name = element.CurrentName
			if not name:
				name = ""
			listInfo.append((name, roleText, element))
		return(listInfo)

	def moveCursor(self, index):
		from . import handleMoveToUIA, NewUIA, shouldUseUIAWhenNavigating
		speech.cancelSpeech()
		element = self.filteredObjectList[index][2]
		element = element.BuildUpdatedCache(UIAHandler.handler.baseCacheRequest)
		obj = NewUIA(UIAElement = element)
		handleMoveToUIA(obj, shouldCreateUIAObject = shouldUseUIAWhenNavigating(obj))

	def moveNavigatorObject(self, index: int):
		clientObject = UIAHandler.handler.clientObject
		element = self.filteredObjectList[index][2]
		obj = None
		windowHandle = element.CurrentNativeWindowHandle
		IAccessibleObject = None
		if UIAHandler.handler.isNativeUIAElement(element):
			obj = UIA.UIA(UIAElement = element)
		elif windowHandle:
			obj = window.Window(windowHandle = windowHandle)
		if not obj:
			iUnknown = element.GetCurrentPattern(UIAHandler.UIA_LegacyIAccessiblePatternId)
			legacyIAccessiblePattern = iUnknown.QueryInterface(UIAHandler.IUIAutomationLegacyIAccessiblePattern)
			try:
				IAccessibleObject = legacyIAccessiblePattern.GetIAccessible()
			except:
				pass
			if IAccessibleObject:
				IAccessibleChildID = legacyIAccessiblePattern.CurrentChildId
				obj = IAccessible.IAccessible(IAccessibleObject=IAccessibleObject, IAccessibleChildID=IAccessibleChildID)
		if not obj:
			obj = UIA.UIA(UIAElement = element)
		api.setNavigatorObject(obj)
		speech.cancelSpeech()
		speech.speakObject(obj, reason=controlTypes.OutputReason.FOCUS)