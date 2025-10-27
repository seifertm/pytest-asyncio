from textwrap import dedent

from pytest import Pytester


def test_uses_loop_factory_from_config(pytester: Pytester):
    pytester.makeini(
        dedent(
            """\
            [pytest]
            asyncio_default_fixture_loop_scope = function
            asyncio_loop_factory = mymodule.loop_factory
            """
        )
    )
    pytester.makepyfile(
        mymodule=dedent(
            """\
            import asyncio
            import pytest_asyncio
            import pytest

            class CustomEventLoop(asyncio.SelectorEventLoop):
                pass

            def loop_factory():
                return CustomEventLoop()
            """
        )
    )
    pytester.makepyfile(
        dedent(
            """\
            import asyncio
            import pytest_asyncio
            import pytest
            from mymodule import CustomEventLoop

            @pytest_asyncio.fixture(loop_scope="module")
            async def any_fixture():
                assert type(asyncio.get_running_loop()) == CustomEventLoop

            @pytest.mark.asyncio(loop_scope="module")
            async def test_set_loop_factory(any_fixture):
                assert type(asyncio.get_running_loop()) == CustomEventLoop
            """
        )
    )
    result = pytester.runpytest("--asyncio-mode=strict")
    result.assert_outcomes(passed=1)
