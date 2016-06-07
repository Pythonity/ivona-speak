import os
import filecmp
import tempfile
from uuid import uuid4

import pytest
from flaky import flaky
from click.testing import CliRunner

from ivona_speak.command_line import cli


# Module fixtures
@pytest.fixture(scope='module')
def auth_keys():
    """Get working auth keys from environment variables"""
    access_key = os.environ["IVONA_ACCESS_KEY"]
    secret_key = os.environ["IVONA_SECRET_KEY"]
    assert access_key and secret_key

    return access_key, secret_key


# Tests
@pytest.mark.parametrize('subcommand,extra_args', [
    ('synthesize', ['-o', tempfile.NamedTemporaryFile().name, 'Hello world']),
    ('list-voices', []),
])
def test_auth_keys(subcommand, extra_args):
    """Test passing auth keys"""
    runner = CliRunner()

    # No keys provided
    args = [subcommand] + extra_args

    result = runner.invoke(cli, args)
    assert isinstance(result.exception, SystemExit)
    assert result.exit_code == 1

    # Wrong keys provided
    args = ([subcommand] +
            ['--access-key', str(uuid4()), '--secret-key', str(uuid4())] +
            extra_args)

    result = runner.invoke(cli, args)
    assert isinstance(result.exception, SystemExit)
    assert result.exit_code == 1

    # Incorrect auth file provided
    with tempfile.NamedTemporaryFile() as temp_file:
        args = ([subcommand] +
                ['--auth-file', temp_file.name] +
                extra_args)

        result = runner.invoke(cli, args)
        assert isinstance(result.exception, SystemExit)
        assert result.exit_code == 1


@flaky
@pytest.mark.parametrize('voice_name,voice_language,content,org_file', [
    ('Salli', 'en-US', 'Hello world', 'files/salli_hello_world.mp3'),
    ('Maja', 'pl-PL', 'Dzień dobry', 'files/maja_dzien_dobry.mp3'),
])
def test_synthesize(auth_keys, voice_name, voice_language, content, org_file):
    """Test 'synthesize' subcommand"""
    runner = CliRunner()

    with tempfile.NamedTemporaryFile() as temp_file:
        args = [
            'synthesize',
            '--access-key', auth_keys[0],
            '--secret-key', auth_keys[1],
            '--output-file', temp_file.name,
            '--voice-name', voice_name,
            '--voice-language', voice_language,
            content,
        ]
        result = runner.invoke(cli, args)
        assert result.exit_code == 0
        assert result.output

        assert filecmp.cmp(org_file, temp_file.name)


@flaky
def test_list_voices(auth_keys):
    """Test 'list-voice' subcommand"""
    runner = CliRunner()

    args = ['list-voices', '--access-key', auth_keys[0], '--secret-key',
            auth_keys[1]]

    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    assert result.output


@flaky
def test_list_voices_with_filter(auth_keys):
    """Test 'list-voice' subcommand with filter"""
    runner = CliRunner()

    # Correct filter
    args = [
        'list-voices',
        '--access-key', auth_keys[0],
        '--secret-key', auth_keys[1],
        '--voice-language', 'en-US',
    ]

    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    assert result.output

    # Incorrect filter
    args = [
        'list-voices',
        '--access-key', auth_keys[0],
        '--secret-key', auth_keys[1],
        '--voice-language', str(uuid4()),
    ]

    result = runner.invoke(cli, args)
    assert isinstance(result.exception, SystemExit)
    assert result.exit_code == 1
