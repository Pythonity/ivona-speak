from itertools import groupby

import yaml
import click
from click_default_group import DefaultGroup
from ivona_api.ivona_api import IvonaAPI, IvonaAPIException


@click.group(cls=DefaultGroup, default='synthesize', default_if_no_args=True,
             context_settings=dict(help_option_names=['-h', '--help']))
def cli():
    pass


@cli.command(name='synthesize')
@click.option('--access-key', type=str,
              help="IVONA Speech Cloud access key.")
@click.option('--secret-key', type=str,
              help="IVONA Speech Cloud secret key.")
@click.option('--auth-file', '-a', type=click.File(),
              help="Path to YAML file with 'access-key' and 'secret-key' set.")
@click.option('--output-file', '-o', required=True,
              type=click.Path(dir_okay=False, writable=True),
              help="Output audio file path.")
@click.option('--voice-name', '-n', type=str, default='Salli',
              help="Voice name (default: Salli).")
@click.option('--voice-language', '-l', type=str, default='en-US',
              help="Voice language (default: en-US).")
@click.option('--codec', '-c', type=click.Choice(IvonaAPI.ALLOWED_CODECS),
              default='mp3', help="Used codec (default: mp3).")
@click.argument('text', type=str)
def synthesize(access_key, secret_key, auth_file, output_file, voice_name,
               voice_language, codec, text):
    """Synthesize passed text and save it as an audio file"""
    access_key, secret_key = _get_config_keys(access_key, secret_key, auth_file)

    try:
        ivona_api = IvonaAPI(
            access_key, secret_key,
            voice_name=voice_name, language=voice_language, codec=codec,
        )
    except IvonaAPIException:
        raise click.ClickException("Given auth keys are incorrect.")

    with click.open_file(output_file, 'wb') as file:
        ivona_api.text_to_speech(text, file)

    click.secho(
        "File successfully saved as '{}'".format(output_file), fg='green'
    )


@cli.command(name='list-voices')
@click.option('--access-key', type=str,
              help="IVONA Speech Cloud access key.")
@click.option('--secret-key', type=str,
              help="IVONA Speech Cloud secret key.")
@click.option('--auth-file', '-a', type=click.File(),
              help="Path to YAML file with 'access-key' and 'secret-key' set.")
@click.option('--voice-language', '-l', type=str,
              help="Filter voice by language.")
def list_voices(access_key, secret_key, auth_file, voice_language):
    """List available Ivona voices"""
    access_key, secret_key = _get_config_keys(access_key, secret_key, auth_file)

    try:
        ivona_api = IvonaAPI(access_key, secret_key)
    except IvonaAPIException:
        raise click.ClickException("Given auth keys are incorrect.")

    click.echo("Listing available voices...")

    # Possibly filter voices by language
    if voice_language:
        try:
            voices_list = ivona_api.get_available_voices(voice_language)
        except ValueError:
            raise click.ClickException("Given filter language is incorrect.")
    else:
        voices_list = ivona_api.available_voices

    # Group voices by language
    voices_dict = dict()
    data = sorted(voices_list, key=lambda x: x['Language'])
    for k, g in groupby(data, key=lambda x: x['Language']):
        voices_dict[k] = list(g)

    for ln, voices in voices_dict.items():
        voice_names = [v['Name'] for v in voices]
        click.echo("{}: {}".format(ln, ', '.join(voice_names)))

    click.secho("All done", fg='green')


def _get_config_keys(access_key, secret_key, yaml_file):
    """
    Access and secret key must be either explicitly passed or be in YAML file
    """
    if yaml_file:
        config = yaml.safe_load(yaml_file)

        try:
            access_key = config['access-key']
            secret_key = config['secret-key']
        except (TypeError, KeyError):
            raise click.ClickException(
                "Passed YAML file doesn't have needed "
                "('access-key' and 'secret_key') values."
            )

    if not access_key or not secret_key:
        raise click.ClickException("Both access key and secret key are needed.")

    return access_key, secret_key

if __name__ == '__main__':
    cli()
