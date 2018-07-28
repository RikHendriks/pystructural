import pytest

from pystructural.solver.components.phased_analysis_components import *


@pytest.fixture
def phased_analysis():
    return PhasedAnalysis()


def test_create_phase(phased_analysis):
    assert phased_analysis.current_phase_id is 0

    phase_id = phased_analysis.create_phase('test')

    assert phase_id is 0
    assert phased_analysis.current_phase_id is 1
    assert phase_id in phased_analysis.phases
    assert 'test' in phased_analysis.phase_names


def test_phase_generator(phased_analysis):
    for i in range(5):
        phased_analysis.create_phase('phase_{0}'.format(i))

    i = 0
    for phase_id in phased_analysis.phase_generator():
        assert phase_id == i
        i += 1


def test_add_previous_phase(phased_analysis):
    phase_id_0 = phased_analysis.create_phase('phase_0')
    phase_id_1 = phased_analysis.create_phase('phase_1')
    phase_id_2 = phased_analysis.create_phase('phase_2')
    phase_id_3 = phased_analysis.create_phase('phase_3')

    phased_analysis.add_previous_phase(phase_id_0, phase_id_1, phase_id_2)
    phased_analysis.add_previous_phase(phase_id_2, phase_id_3)

    assert phased_analysis.previous_phases[phase_id_0] == [phase_id_1, phase_id_2]
    assert phased_analysis.previous_phases[phase_id_2] == [phase_id_3]
