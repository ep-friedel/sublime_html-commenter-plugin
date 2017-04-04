import sublime
import sublime_plugin
import re

settings = sublime.load_settings('formatter.sublime_settings')
ParseOnSave = True if (settings.get('parseonsave') == 'yes') else False

class MyLine(object):
    text = ""
    classes = ""
    optag = False

    def __init__(self, text, classes, optag):
        self.text = text
        self.classes = classes
        self.optag = optag


class AddCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        collection = []
        parsedcollection = []
        stack = []
        allcontent = sublime.Region(0, self.view.size())
        alltext = self.view.substr(allcontent)
        collection = re.finditer('(<[^<>a-zA-Z]*div[^<>]*>(.|\s)*?)((?=<[^<>a-zA-Z]*div[^<>]*>)|(?!div)$)', alltext)
        remains = re.search('(.*?)<[^<>a-zA-Z]*div[^<>]*>', alltext, re.DOTALL)
        newtext = ""
        iterVar = 0

        for match in collection:
            iterVar = iterVar + 1
            optag = not bool(re.search('<[^<>]*\/[^<>]*div', match.group(0)))
            if optag:
                result = re.search('class=["\']([^"\']*)', re.sub('#IF.*#ENDIF', '', match.group(0)))
                classes = "" if result is None else result.group(1)

            else:
                classes = ""

            newMatch = MyLine(match.group(0), classes, optag)
            parsedcollection.append(newMatch)

        if (iterVar == 0):
            return

        iterVar = 0

        for match in parsedcollection:
            iterVar = iterVar + 1

            if match.optag:
                stack.append(match)
                newtext = newtext + match.text

            else:
                if len(stack) > 0:
                    if len(stack[-1].classes) > 0:
                        classlist = re.sub('#IF.*#ENDIF', '', stack[-1].classes).split(' ')
                        classlist = [cssclass for cssclass in classlist if bool(re.search('(col-|row|ep-(?!js))', cssclass))]
                        if (bool(re.search('.*\n.*', stack[-1].text)) and (len(classlist) > 0)):
                            classlist = ' .'.join(classlist)
                            match.text = re.sub('(<[^<>a-zA-Z]*div[^<>]*>)(( |#REM|)*<!--.*?-->( |#ENDREM)*|)((| )*)', '\g<1>#REM <!-- .' + classlist + ' --> #ENDREM\g<5>', match.text)

                    newtext = newtext + match.text
                    stack.pop()
                else:
                    sublime.error_message('Too many closing div-tags at tag nr: ' + str(iterVar))
                    return

        if len(stack) > 0:
            print(stack[-1].text)
            sublime.error_message('Too many opening div-tags. Couldnt match ' + str(len(stack)))
            return

        if remains is None:
            sublime.error_message('Could not find first div tag')
            return

        newtext = remains.group(1) + newtext

        self.view.replace(edit, allcontent, newtext)


class RunOnSaveCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global ParseOnSave

        ParseOnSave = not self.is_checked()
        settings.set('parseonsave', 'yes' if ParseOnSave else 'no')
        sublime.save_settings('formatter.sublime_settings')

    def is_checked(self):
        global ParseOnSave
        global settings
        if (settings.get('parseonsave') == None):
            settings = sublime.load_settings('formatter.sublime_settings')
            ParseOnSave = True if (settings.get('parseonsave') == 'yes') else False

        return ParseOnSave


class TranscryptEventListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        global ParseOnSave
        global settings
        if (settings.get('parseonsave') == None):
            settings = sublime.load_settings('formatter.sublime_settings')
            ParseOnSave = True if (settings.get('parseonsave') == 'yes') else False

        if bool(re.search('\.html', view.file_name())) and not bool(re.search('Data.Public', view.file_name())) and not bool(re.search('Data.javascript', view.file_name())) and ParseOnSave:
            view.run_command("add_comments")
