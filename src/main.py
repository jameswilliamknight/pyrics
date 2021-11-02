#!/usr/bin/env python3

import argparse
from util.logger import Logger
import lyricsgenius as lg
import os

parser = argparse.ArgumentParser(
    usage="%(prog)s [OPTIONAL FLAGS] phrase",
    description="Converts all usages of xunit.assert nuget package to FluentAssertions.")

parser.add_argument("-v", "--verbose",
                    action="store_true",
                    help="Display verbose logging messages")

parser.add_argument("-t", "--token",
                    action="store",
                    type=str,
                    help="Client Access Token for Genius.com")

parser.add_argument("-a", "--artist",
                    action="store",
                    type=str,
                    help="Music artist")

args = parser.parse_args()
log = Logger(args)


genius = lg.Genius(
    args.token,
    skip_non_songs=True,
    excluded_terms=["(Remix)", "(Live)"],
    remove_section_headers=True)

home = os.path.expanduser("~")
lyrics_dir = f"{home}/lyrics"
# os.makedirs(lyrics_dir)

artist = "Tool"
album_name = "10,000 Days"

# TODO: slugify properly https://stackoverflow.com/a/295466/14568721
#  https://github.com/django/django/blob/master/django/utils/text.py
album_name_slug = album_name.replace(",","").replace(" ", "_")

filename_base = f"{artist}_{album_name_slug}"

lyrics_file = os.path.join(lyrics_dir, f"{filename_base}.temp.html")
lyrics_printout = os.path.join(lyrics_dir, f"{filename_base}.html")
# for f in open(lyrics_file, "w"):
#     pass

#songs = (genius.search_artist(args.artist, max_songs=1, sort='popularity')).songs

album = genius.search_album(album_name, artist)
#for song in songs:
#    remove = ["70EmbedShare URLCopyEmbedCopy"]
#    log.info(song.lyrics)

if not os.path.exists(lyrics_dir):
    os.makedirs(lyrics_dir)
else:
    if os.path.exists(lyrics_file):
        os.remove(lyrics_file)


with open(lyrics_file, 'w') as f:
    f.write(f"<h1>{artist}</h1>\n<h2>{album_name}</h2>\n<hr/>\n")
    for track in album.tracks:
        lyrics = track.song.lyrics.replace("EmbedShare", "").replace("URLCopyEmbedCopy", "").strip()
        lyrics_split = lyrics.split('\n\n')
        lyrics_paragraphed = ["<p>" + s + "</p>" for s in lyrics_split]
        lyrics = "\n".join(lyrics_paragraphed)
        if len(lyrics) < 1:
            continue
        track_no = str(track.number).zfill(2)
        title = track.song.title
        f.write(f"<div class=\"song\">\n<h3> {track_no}. {title}</h3>\n<span>{lyrics}</span>\n</div>\n<hr/>\n\n")


# TODO: take markdown file, and convert to HTML
this_script_path = os.path.dirname(os.path.realpath(__file__))

html: str = None
html_template_path = os.path.join(this_script_path, "res/template.html")
with open(html_template_path, 'r') as f:
    html = f.read()

with open(lyrics_file, 'r') as f:
    lyrics = f.read()
    html = html.replace("<content />", lyrics)

with open(lyrics_printout, 'w') as f:
    f.write(html)
