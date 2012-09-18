#!/usr/bin/python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import os
import os.path
# import glob


def cycle_scheme(backward=False):
    schemes = []
    for dirpath, dirnames, filenames in os.walk(sublime.packages_path()):
        for filename in filenames:
            if os.path.splitext(filename)[1] == ".tmTheme":
                #the id to search and store in the preferences
                id = os.path.join(dirpath, filename)[len(sublime.packages_path()) - 8:]
                #the name without the extension
                name = os.path.splitext(filename)[0]
                schemes.append({'id': id, 'name': name})

    schemes = sorted(schemes, key=lambda x: x['name'])
    settings = sublime.load_settings('Preferences.sublime-settings')
    current_scheme = settings.get('color_scheme')
    for index, item in enumerate(schemes):
        if item['id'] == current_scheme:
            scheme_index = index
            break
    scheme_index += (backward and -1 or 1)

    if scheme_index == len(schemes):
        scheme_index = 0
    elif scheme_index == -1:
        scheme_index = len(schemes) - 1
    scheme = schemes[scheme_index]
    if not scheme:
        return
    settings.set('color_scheme', scheme['id'],)
    sublime.save_settings('Preferences.sublime-settings')

    sublime.status_message(
        u'Color Scheme: ' + scheme['name']
    )


class NextColorSchemeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        cycle_scheme()


class PreviousColorSchemeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        cycle_scheme(backward=True)