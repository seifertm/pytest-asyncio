import pytest

pytest_plugins = "pytester"


@pytest.fixture(scope="session", name="factory_involving_factories")
def factory_involving_factories_fixture(unused_tcp_port_factory):
    def factory():
        return unused_tcp_port_factory()

    return factory
