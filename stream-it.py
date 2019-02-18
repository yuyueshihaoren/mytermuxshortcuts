#!/data/data/com.termux/files/usr/bin/env python
import subprocess as sp
import shlex
import json
import os

def termux_dialog_radio(title, choices):
    command_str = "termux-dialog radio -t \"" + title + "\" -v \"" + choices + "\""
    command_list = shlex.split(command_str)
    execution_object = sp.Popen(command_list, stdout=sp.PIPE)
    execution_output = execution_object.communicate()[0]
    result = json.loads(execution_output)['text']
    return result

def get_clipboard():
    clip = sp.Popen("termux-clipboard-get", stdout=sp.PIPE)
    clipp = clip.communicate()[0].decode('utf-8')
    return clipp

def youtube_stream_live(url):
    youtubedl_command_str = "youtube-dl -f 91 -o - \"{0}\"".format(url)
    youtube_dl_obj = sp.Popen(shlex.split(youtubedl_command_str), stdout=sp.PIPE)
    sp.call(["mpv", "-"], stdin=youtube_dl_obj.stdout)
    youtube_dl_obj.stdout.close()

def youtube_stream_normal(url):
    youtubedl_command_str = "youtube-dl -f 140 -o - \"{0}\"".format(url)
    #print(youtubedl_command_str)
    youtube_dl_obj = sp.Popen(shlex.split(youtubedl_command_str), stdout=sp.PIPE)
    sp.call(["mpv", "-"], stdin=youtube_dl_obj.stdout)
    youtube_dl_obj.stdout.close()

def youtube_stream_random(url):
    youtubedl_command_str = "youtube-dl -f 140 -o - \"{0}\" --playlist-random".format(url)
    youtube_dl_obj = sp.Popen(shlex.split(youtubedl_command_str), stdout=sp.PIPE)
    sp.call(["mpv", "-"], stdin=youtube_dl_obj.stdout)
    youtube_dl_obj.stdout.close()

def choose_and_play_bookmarks(bmj):
    title = ''
    for b in bmj:
        title += b['title'] + ','
    title = title[:-1]
    radio_command_str = "termux-dialog radio -t \"Choose one of the bookmarks\" -v \"" + title + "\""
    radio_command_obj = sp.Popen(shlex.split(radio_command_str), stdout=sp.PIPE)
    choice_json = radio_command_obj.communicate()[0]
    choice = json.loads(choice_json)['text']
    #print(choice)
    for b in bmj:
        if b['title'] == choice:
            #print("match")
            if b['live'] == 'yes':
                youtube_stream_live(b['url'])
            elif b['live'] == 'no':
                if b['playlist'] == 'no':
                    youtube_stream_normal(b['url'])
                elif b['playlist'] == 'yes':
                    youtube_stream_random(b['url'])


def main():
    cli_or_bm = termux_dialog_radio("From Clipboard or Bookmarks?", "Clipboard, Bookmarks")
    if cli_or_bm == "Clipboard":
        live_or_not = termux_dialog_radio("Is it live or not?", "Live, Not Live")
        if live_or_not == "Live":
            url = get_clipboard()
            youtube_stream_live(url)
        elif live_or_not == "Not Live":
            url = get_clipboard()
            youtube_stream_normal(url)
    elif cli_or_bm == "Bookmarks":
        bm = open(os.getenv("HOME") + '/.shortcuts/bookmarks.json', 'r')
        bmj = json.load(bm)
        choose_and_play_bookmarks(bmj)
        bm.close()

if __name__ == '__main__':
    main()
