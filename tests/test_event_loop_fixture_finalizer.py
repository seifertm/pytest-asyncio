from __future__ import annotations

from textwrap import dedent

from pytest import Pytester


def test_event_loop_fixture_finalizer_handles_loop_set_to_none_sync(
    pytester: Pytester,
):
    pytester.makeini("[pytest]\nasyncio_default_fixture_loop_scope = function")
    pytester.makepyfile(
        dedent(
            """\
            import asyncio

            def test_sync(event_loop):
                asyncio.get_event_loop_policy().set_event_loop(None)
            """
        )
    )
    result = pytester.runpytest("--asyncio-mode=strict")
    result.assert_outcomes(passed=1)


def test_event_loop_fixture_finalizer_handles_loop_set_to_none_async_without_fixture(
    pytester: Pytester,
):
    pytester.makeini("[pytest]\nasyncio_default_fixture_loop_scope = function")
    pytester.makepyfile(
        dedent(
            """\
            import asyncio
            import pytest

            @pytest.mark.asyncio
            async def test_async_without_explicit_fixture_request():
                asyncio.get_event_loop_policy().set_event_loop(None)
            """
        )
    )
    result = pytester.runpytest("--asyncio-mode=strict")
    result.assert_outcomes(passed=1)


def test_event_loop_fixture_finalizer_handles_loop_set_to_none_async_with_fixture(
    pytester: Pytester,
):
    pytester.makeini("[pytest]\nasyncio_default_fixture_loop_scope = function")
    pytester.makepyfile(
        dedent(
            """\
            import asyncio
            import pytest

            @pytest.mark.asyncio
            async def test_async_with_explicit_fixture_request(event_loop):
                asyncio.get_event_loop_policy().set_event_loop(None)
            """
        )
    )
    result = pytester.runpytest_subprocess("--asyncio-mode=strict", "-W default")
    result.assert_outcomes(passed=1)
