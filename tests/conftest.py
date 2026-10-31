import copy

import pytest

from src import app as app_module


initial_activities = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = copy.deepcopy(initial_activities)
    yield
    app_module.activities = copy.deepcopy(initial_activities)
