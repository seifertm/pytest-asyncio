import pytest


@pytest.mark.asyncio
async def test_factory_involving_factories(factory_involving_factories):
    factory_involving_factories()
