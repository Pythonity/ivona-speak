# -*- coding: utf-8 -*-
"""
Test 'ivona_speak.command_line' module
"""
from __future__ import absolute_import, unicode_literals

import os
import tempfile

import pytest
from click.testing import CliRunner
from ivona_api.ivona_api import IVONA_ACCESS_KEY_ENV, IVONA_SECRET_KEY_ENV

from ivona_speak.command_line import cli


# Module fixtures
@pytest.fixture(scope='module')
def runner():
    """Get CliRunner"""
    return CliRunner()


# Tests
@pytest.mark.parametrize('subcommand,extra_args', [
    ('synthesize', ['-o', tempfile.NamedTemporaryFile().name, 'Hello world']),
    ('list-voices', []),
])
def test_auth_keys(monkeypatch, runner, subcommand, extra_args):
    """Test passing auth keys"""
    monkeypatch.delenv(IVONA_ACCESS_KEY_ENV, raising=False)
    monkeypatch.delenv(IVONA_SECRET_KEY_ENV, raising=False)

    result = runner.invoke(
        cli, args=[subcommand] + extra_args
    )

    assert isinstance(result.exception, SystemExit)
    assert result.exit_code == 1


@pytest.mark.parametrize('voice_name,voice_language,content', [
    ('Salli', 'en-US', 'Hello world'),
    ('Maja', 'pl-PL', 'Dzień dobry'),
])
def test_synthesize(runner, voice_name, voice_language, content):
    """Test 'synthesize' subcommand"""
    temp_file = tempfile.NamedTemporaryFile(delete=False)

    args = [
        'synthesize',
        '--output-file', temp_file.name,
        '--voice-name', voice_name,
        '--voice-language', voice_language,
        content,
    ]
    result = runner.invoke(cli, args)

    assert result.exit_code == 0
    assert result.output

    assert os.path.getsize(temp_file.name) > 0


def test_list_voices(runner):
    """Test 'list-voice' subcommand"""
    result = runner.invoke(
        cli, args=['list-voices']
    )

    assert result.exit_code == 0
    assert result.output


def test_list_voices_with_filter(runner):
    """Test 'list-voice' subcommand with filter"""
    result = runner.invoke(
        cli, args=['list-voices', '--voice-language', 'en-US']
    )

    assert result.exit_code == 0
    assert result.output
