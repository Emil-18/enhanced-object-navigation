# Enhanced Object Navigation.
* Author: Emil-18.
* NVDA compatibility: 2024.1 and beyond.
* Download: [Stable version](https://github.com/Emil-18/enhanced-object-navigation/releases/download/v0.2.1/enhancedObjectNavigation-0.2.1.nvda-addon).

This addon adds improvements to object navigation. Note that as of now, it doesn't work in java applications.

## Navigation mode.

To turn on navigation mode, press NVDA+shift+control+space.
Navigation mode can be turned on in any application.

Note:

All navigation commands described below will only navigate to objects in the same process that the navigator object is located in, unless stated otherwise.

They will also navigate to objects regardless of hierarchy, unless stated otherwise.


### Basic navigation mode commands.

* Left and right arrow: move the navigator object to the previous and next object.
* Up and down arrow: move the navigator object to the previous and next object depending on the rotor setting.
* Page up and down: move to the next/previous rotor setting.
* Space: interact with the control where the navigator object is located. This can include pressing a button, checking a check box, or setting focus to an edit field so you can start typing.
* Enter, applications key, shift+f10: set focus to the navigator object, and then send the pressed key through to the application.

### Advanced navigation.

To turn advanced navigation on, press NVDA+A while you are in navigation mode. NVDA will remember the state of the advanced navigation mode between sessions.

When advanced navigation is turned on, The arrow keys will move you around in the same way as normal object navigation, e.g Up arrow to move to the object containing the navigator object, left and right arrows move to the previous/next object, and down arrow moves to the first object inside the navigator object. The "Simple review mode" setting will affect what you can navigate to.
When using these commands, you  can navigate outside of the current process.
When advanced navigation is turned on, the rotor is not available, but all other commands works as normal, except for the arrow keys as described above.

### single letter navigation.

When navigation mode is turned on, you can use single letter navigation, like in browse mode, to jump to different types of objects.

The following single letter navigation keys are supported at this time.
Press the key on its own to jump to the next object, add shift to jump to the previous object, and add shift and control to list up all objects.

* b: button.
* c: combo box.
* d: document.
* e: edit controls.
* f: form field.
* g: graphic.
* h: heading (only supported in edge).
* i: list item.
* j: focusable control.
* k: link.
* l: list.
* m: menu, menu bar or menu item.
* n: landmark.
* o: tool bar.
* p: text.
* q: tab or tab item.
* r: radio button.
* s: same item.
* t: table.
* u: group.
* v: tree or tree item.
* w: control (areas that can be redefined with the [Enhanced control support add-on](https://github.com/emil-18/enhanced-control-support)).
* x: check box.
* y: focusable form field.
* z: status bar.

All of these are available in the rotor as well.
## The search list.

The search list is a virtual list that contains the objects you have listed up, for example by pressing control+shift+b while in navigation mode to list buttons.
To list objects regardless of role, press NVDA+control+enter. This command is available even when navigation mode is turned off. You can also press NVDA+shift+f7 anywhere, and then press a navigation key, e.g b for button, to only list up buttons.
Since the list is virtual, you can do things such as list all the objects in a menu, without the menu closing, because the system focus is not moved.

When you are in the list, you can start typing to filter the list. Hold down left alt and type a character to move to the next object starting with that character.

You can use the following commands while in the list.

* enter: move to the selected item and close the search list.
* backspace or delete: remove the search text and return all items to the list.
* up and down arrow: move to the next or previous item.
* left and right arrow: move to the next or previous item starting with a different character.
* Home and end: move to the beginning and end of the list.
* shift+backspace or shift+delete: reset the searchText. This will keep the list in its current state, but removes the search text, so you can start a new search. You could for example type "NV", press this command, and type "A" and items containing "NVDA" will show up.
* escape: exit  the search list and return the focus and the navigator object  to where they were before you opened the list.

## Enhanced touch support.

A new touch mode has been added, called navigation. This is not complete yet.
The gestures for this mode are as follows.
* 1 finger flick up/down: move to the next/previous object depending on the rotor setting.
* 2 finger flick write/left: move to the next/previous rotor setting.
* 3 finger flick right/left: press tab/shift+tab.
* 3 finger flick up/down: press f6/shift+f6.
* 2 finger flick up: press escape.
* 2 finger tripple tap: list all objects in the window where the navigator object is located.
## Settings.

* Use navigation mode by default.
This setting determines if navigation mode should be on by default, same as pressing NVDA+shift+control+space.
* When searching, sort the items in tab order instead of alphabetically.
When turned on, The search list will be sorted in tab order instead of alphabeticly.
* Search scope.
This is a combo box that allows you to choose the scope when searching for objects.
You can as of now choose between 3 options.
    * The foreground window.
    * All objects in the operating system.
    * The current browse mode document that the navigator object is in.
* Use enhanced detection while searching for same item.
When checked, the s single letter navigation key will include only objects that are programmaticly the same, instead of all objects with the same role.
* Report object context while navigating in the search list.
When checked, NVDA will report objects containing the object you landed in when navigating in the list if it differes from the previous object, like NVDA does normally when you move focus.
* When in navigation mode or in the search list, automatically update the braille display when the content of the shown object changes. Disable if you encounter problems using the add-on, such as lag. Self explanatory.
* When in the search list and holding down left alt, use first letter navigation.
When checked, You can hold down left alt while you are in the search list and press characters to move to the next item starting with that character.
* Use sounds to indicate if navigation mode has been toggled. Self explanatory.
* disable asynchronous navigation, useful if you encounter problems while navigating, such as NVDA becoming silent or playing error sounds. Self explanatory.

## Change log.


### v0.2
* Removed the concept of saving the navigation mode. Now, it will automaticly save when the gesture is pressed once.
* Navigation mode will no longer turn off automaticly when focus moves, except if focus lands in a browse mode document where browse mode is enabled. To enter forms mode, you need to press space on an editable control. once if the control has focus, and twice otherwize.
* When pressing enter on an item in the search list, the active cursor will be moved. If navigation mode is active, the navigator object will be moved. If the object represented by the current item is in a browse mode document and browse mode is turned on, the browse mode cursor will be moved.
else the focus is moved. If the focus can't be moved, the navigator object is moved instead.
* Fixed a bug where NVDA sometimes crashed when exiting or restarting.
* Made the searching for next and previous object in navigation mode asynchronous.
* Added a new quicknav key, y, that is for focusable form fields.
* Removed the "Set focus to the item selected in the search list" and the "Activate the item selected in the search list" settings

### v0.1.1

* The gestures in the search list should now work everywhere
* You should be able to use navigation mode in more situations

### v0.1.

Initial release.
