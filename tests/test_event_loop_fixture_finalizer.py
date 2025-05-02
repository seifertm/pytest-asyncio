from __future__ import annotations

from textwrap import dedent

from pytest import Pytester


def test_event_loop_fixture_finalizer_returns_fresh_loop_after_test(pytester: Pytester):
    pytester.makeini("[pytest]\nasyncio_default_fixture_loop_scope = function")
    pytester.makepyfile(
        dedent(
            """\
            import asyncio

            import pytest

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            @pytest.mark.asyncio
            async def test_1():
                # This async test runs in its own event loop
                global loop
                running_loop = asyncio.get_event_loop_policy().get_event_loop()
                # Make sure this test case received a different loop
                assert running_loop is not loop

            def test_2():
                # Code outside of pytest-asyncio should not receive a "used" event loop
                current_loop = asyncio.get_event_loop_policy().get_event_loop()
                assert not current_loop.is_running()
                assert not current_loop.is_closed()
            """
        )
    )
    result = pytester.runpytest("--asyncio-mode=strict")
    result.assert_outcomes(passed=2)


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
    result.assert_outcomes(passed=1, warnings=1)
    result.stdout.fnmatch_lines(
        '*is asynchronous and explicitly requests the "event_loop" fixture*'
    )
