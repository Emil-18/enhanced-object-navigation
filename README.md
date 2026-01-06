# Enhanced Object Navigation.
* Author: Emil-18.
* NVDA compatibility: 2024.1 and beyond.
* Download: [Stable version](https://github.com/Emil-18/enhanced-object-navigation/releases/download/v0.3/enhancedObjectNavigation-0.3.nvda-addon).

This add-on adds improvements to object navigation. [Read this if you don't know what object navigation is or how to use it](https://afb.org/aw/fall2025/nvda-object-navigation-getting-started).
This add-on adds the following:

* A navigation mode, that allows you to use the arrow keys to move the navigator object between objects. You can also use quick navigation commands, (b for button, x for checkbox, etc), to move  the navigator object to the next/previous object of the specified type.
* the ability to list up objects, search for the object you want, and move directly to it.
* better touch support.

all of these features are affected by the "Simple review mode" setting, so when the setting is turned off, you will be able to find more objects that aren't necessarily relevant to the average user.

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

To turn advanced navigation on or off, press NVDA+A while you are in navigation mode. NVDA will remember the state of the advanced navigation mode between sessions.

When advanced navigation is turned on, The arrow keys will move you around in the same way as normal object navigation, e.g Up arrow to move to the object containing the navigator object, left and right arrows move to the previous/next object, and down arrow moves to the first object inside the navigator object.
When using these commands, you  can navigate outside of the current process.
When advanced navigation is turned on, the rotor is not available, but all other commands works as normal, except for the arrow keys as described above.

### single letter navigation.

When navigation mode is turned on, you can use single letter navigation, like in browse mode, to jump to different types of objects.

The following single letter navigation keys are supported at this time.
Press the key on its own to jump to the next object, add shift to jump to the previous object, and add shift and control to list up all objects.

* b: button.
* c: combo box.
* d: document.
* e: edit control.
* f: form field.
* g: graphic.
* h: heading.
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

### UIA vs none UIA navigation mode

By default, this add-on uses UI automation when you are navigating in navigation mode. This causes it to be faster, and  it will work in places where NVDA's normal object navigation has problems, however, this has some side effects.

* It will recognize some objects oddly, such as recognizing text in Mozilla applications as edit boxes, and not recognize headings in many situations.
* It won't recognize objects that NVDA  (either in core or via other add-ons) has customized. For example, if the object appears as a pane to screen readers normally, but NVDA is customized to treat it as an edit box, it will be treated as a pane to the navigation mode when it uses UI automation.

You can configure the add-on to not explicitly use UI automation in navigation mode. When you do this, the add-on navigates through objects as NVDA sees them normally, and you will not experience any of the side effects listed above.

## The search list.

The search list allows you to show objects in a list, search for the object you want, and move directly to it. You can choose to list up every object in the current window, every object in the current browse mode document, or all objects in the operating system.
independent of this, you can choose to list up all object types, or only the type assosiated with a spesific character, for example, you can press control+shift+b while in navigation mode to only list buttons.
To list objects regardless of role, press NVDA+control+enter. This command is available even when navigation mode is turned off. You can also press NVDA+shift+f7 anywhere, and then press a navigation key, e.g b for button, to only list up buttons.
### The virtual search list

By default, the add-on uses a virtual list to list up objects. This means that when you are opening the list and navigating around in it, nothing is displayed on the screen, and the system focus isn't moved. This has several advantages and disadvantages.
#### Advantages:

* Less loading time, and no loading time at all while you are typing in the list, as the system doesn't need to display the list items.
* The ability to be used in areas that disappear when focus is moved away from them.
* The reporting of the actual object, including optionally objects that it is inside of, while moving in the list.

#### Disadvantages:

* Doesn't work with Windows dictation.
* disappears when focus is moved away from it.
* Doesn't work well with touch.

When you are in the list, you can start typing to filter the list. Hold down left alt and type a character to move to the next object starting with that character.
You can use the following commands while in the list.

* enter: move to the selected item and close the search list.
* backspace or delete: remove the search text and return all items to the list.
* up and down arrow: move to the next or previous item.
* left and right arrow: move to the next or previous item starting with a different character.
* Home and end: move to the beginning or end of the list.
* shift+backspace or shift+delete: reset the searchText. This will keep the list in its current state, but removes the search text, so you can start a new search. You could for example type "NV", press this command, and type "A" and items containing "NVDA" will show up.
* escape: exit  the search list and return the focus and the navigator object  to where they were before you opened the list.

### the physical search list

The physical search list is always used in java applications, as the virtual search list isn't supported in them. You can also configure the add-on to use it everywhere.

#### Advantages:

* appears visually on the screen, and can be interacted with like any other application

#### Disadvantages:

* Takes longer to search or list up items.
* Can not be used in areas that disappear when focus is moved away from them.

#### Controls in the physical search list

* Filter by control type edit box: This edit box allows you to search for objects that has a control type that starts with your search. For example, if you search for "button", all buttons will be shown, and controls such as radio buttons, that contains but doesn't start with the word "button" will not be shown.
* Filter by name edit box: This edit box allows you to search for the objects in the list by their name.
* Objects list: This list contain the objects you have searched for. You can use first letter navigation to jump quickly to an item. If you press space while you are in the list, the navigator object will be moved to the object represented by the focused list item, but the search list will not be closed.
* Move navigator object button: This button closes the dialog, and moves the navigator object to the object represented by the selected list item, regardless of what mode you were in prior to opening the search list.
* OK button: This is the default button, activated by pressing enter. This will move the active cursor to the object represented by the selected list item, same as pressing enter in the virtual search list

### What happens when you press enter in the search list?

The list will close, and:

* If you were in navigation mode before opening the search list, the navigator object will be moved to the object represented by the current list item.
* If the object represented by the current list item is in a browse mode document, and if browse mode is turned on for that document, the browse mode cursor will be moved.
* Else focus will be moved. If the focus can't be moved, the navigator object will be moved instead.

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
* Use UI automation in navigation mode when available. See the "UIA vs none UIA navigation mode" section.
* disable asynchronous navigation, useful if you encounter problems while navigating, such as NVDA becoming silent or playing error sounds. When this is unchecked, and when you are searching for items such as buttons with the navigation mode, NVDA won't freeze while it is searching. Does only apply when the "Use UI automation in navigation mode when available" setting is turned on. If it isn't turned on, this will be treated as checked.
* Use a virtual list when listing up objects (does not work in Java applications). See the "Search list" section.
* Settings for the virtual search list:
    * Report object context while navigating in the search list.
    When checked, NVDA will report objects containing the object you landed in when navigating in the list if it differes from the previous object, like NVDA does normally when you move focus.
    * When in the search list and holding down left alt, use first letter navigation.
    When checked, You can hold down left alt while you are in the search list and press characters to move to the next item starting with that character.
* Settings for the physical search list:
    * Use UI automation when listing objects (same as in the virtual search list).
    * Use Regular expressions when searching.
    When checked, regular expressions can be used to search for the name of objects
* When in navigation mode or in the search list, automatically update the braille display when the content of the shown object changes. Disable if you encounter problems using the add-on, such as lag. Self explanatory.

* Use sounds to indicate if navigation mode has been toggled. Self explanatory.


## Change log.

### v0.3

* Added an optional physical search list.
* Added support for java applications.
* Added the possibility to not use UI automation when navigating in navigation mode.
* The add-on will now honour the "simple review mode" setting
* When pressing space on an edit field, the add-on will automatically go into forms mode. You no longer need to press space twice.

### v0.2.2
* Added compatibillity with NVDA 2025.1

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
