# -*- coding: utf-8 -*-
"""
ivona_speak CLI related code
"""
from __future__ import absolute_import, unicode_literals

from itertools import groupby

import click
from click_default_group import DefaultGroup
from ivona_api import IvonaAPI
from ivona_api.exceptions import IvonaAPIException


click.disable_unicode_literals_warning = True


@click.group(cls=DefaultGroup, default='synthesize', default_if_no_args=True)
def cli():
    """
    Easily convert passed text to synthesized audio files, with help of
    Amazon's IVONA. All you need is a pair of auth keys.

    See https://github.com/Pythonity/ivona-speak for more info.
    """


@cli.command(name='synthesize')
@click.option('--access-key', type=str,
              help="IVONA Speech Cloud access key.")
@click.option('--secret-key', type=str,
              help="IVONA Speech Cloud secret key.")
@click.option('--output-file', '-o', required=True,
              type=click.Path(dir_okay=False, writable=True),
              help="Output audio file path.")
@click.option('--voice-name', '-n', type=str, default='Salli',
              help="Voice name (default: Salli).")
@click.option('--voice-language', '-l', type=str, default='en-US',
              help="Voice language (default: en-US).")
@click.option('--codec', '-c', type=click.Choice(['ogg', 'mp3', 'mp4']),
              default='mp3', help="Used codec (default: mp3).")
@click.argument('text', type=str)
def synthesize(access_key, secret_key, output_file, voice_name, voice_language,
               codec, text):
    """Synthesize passed text and save it as an audio file"""
    try:
        ivona_api = IvonaAPI(
            access_key, secret_key,
            voice_name=voice_name, language=voice_language, codec=codec,
        )
    except (ValueError, IvonaAPIException) as e:
        raise click.ClickException("Something went wrong: {}".format(repr(e)))

    with click.open_file(output_file, 'wb') as file:
        ivona_api.text_to_speech(text, file)

    click.secho(
        "File successfully saved as '{}'".format(output_file),
        fg='green',
    )


@cli.command(name='list-voices')
@click.option('--access-key', type=str,
              help="IVONA Speech Cloud access key.")
@click.option('--secret-key', type=str,
              help="IVONA Speech Cloud secret key.")
@click.option('--voice-language', '-l', type=str,
              help="Filter voice by language.")
@click.option('--voice-gender', '-g', type=str,
              help="Filter voice by gender.")
def list_voices(access_key, secret_key, voice_language, voice_gender):
    """List available Ivona voices"""
    try:
        ivona_api = IvonaAPI(access_key, secret_key)
    except (ValueError, IvonaAPIException) as e:
        raise click.ClickException("Something went wrong: {}".format(repr(e)))

    click.echo("Listing available voices...")

    voices_list = ivona_api.get_available_voices(
        language=voice_language,
        gender=voice_gender,
    )

    # Group voices by language
    voices_dict = dict()
    data = sorted(voices_list, key=lambda x: x['Language'])
    for k, g in groupby(data, key=lambda x: x['Language']):
        voices_dict[k] = list(g)

    for ln, voices in voices_dict.items():
        voice_names = [v['Name'] for v in voices]
        click.echo("{}: {}".format(ln, ', '.join(voice_names)))

    click.secho("All done", fg='green')


if __name__ == '__main__':
    cli()
