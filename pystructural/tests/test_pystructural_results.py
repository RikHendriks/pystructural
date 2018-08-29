import pystructural as ps
import numpy as np


######################
# BASIC RESULT TESTS #
######################

def test_basic_result_0():
    """Tests a structure with a simple point load in the middle of the frame.
    """
    # Create a structure instance
    structure = ps.core.Structure2D()
    # Add a frame element
    structure.add_frame_element([0.0, 0.0], [10.0, 0.0], 1.0, 1.0, 1.0, 1.0)
    # Add supports
    structure.add_support([0.0, 0.0], displacement_x=False, displacement_y=False)
    structure.add_support([10.0, 0.0], displacement_y=False)
    # Add a point load
    structure.add_point_load([5.0, 0.0], [0.0, -1.0, 0.0])
    # Solve the linear system
    structure.solve_linear_system()
    # Test the forces in the middle of the frame
    assert np.allclose(structure.get_line_force_vector([4.99, 0.0])[3:], np.array([0.0, -0.5, -2.5]))
    # Test the displacements in the middle of the frame
    assert np.allclose(structure.get_point_displacement_vector([5.0, 0.0]), np.array([0.0, -1000 / 48, 0.0]))


def test_basic_result_1():
    """Tests a structure with a simple q-load over the whole frame.
    """
    # Create a structure instance
    structure = ps.core.Structure2D(0.05)
    # Add a frame element
    frame_id = structure.add_frame_element([0.0, 0.0], [10.0, 0.0], 1.0, 1.0, 1.0, 1.0)
    # Add supports
    structure.add_support([0.0, 0.0], displacement_x=False, displacement_y=False)
    structure.add_support([10.0, 0.0], displacement_y=False)
    # Add a q-load
    structure.add_global_q_load(frame_id, -1.0)
    # Solve the linear system
    structure.solve_linear_system()
    # Test the forces in the middle of the frame
    assert np.allclose(structure.get_line_force_vector([4.99, 0.0])[3:], np.array([0.0, -0.05, -12.5]), atol=1.e-3)
    # Test the displacements in the middle of the frame
    assert np.allclose(structure.get_point_displacement_vector([5.0, 0.0]), np.array([0.0, -50000 / 384, 0.0]))


def test_basic_result_2():
    """Tests a structure with an imposed load over the whole frame.
    """
    # Create a structure instance
    structure = ps.core.Structure2D(0.05)
    # Add a frame element
    frame_id = structure.add_frame_element([0.0, 0.0], [10.0, 0.0], 1.0, 1.0, 1.0, 1.0)
    # Add supports
    structure.add_support([0.0, 0.0], displacement_x=False, displacement_y=False)
    structure.add_support([10.0, 0.0], displacement_y=False)
    # Add an imposed load
    structure.add_imposed_load(frame_id, [0.0, 100.0])
    # Solve the linear system
    structure.solve_linear_system()
    # Test the forces in the middle of the frame
    assert np.allclose(structure.get_line_force_vector([4.99, 0.0])[3:], np.array([0.0, 0.0, 0.0]), atol=1.e-7)
    # Test the displacements in the middle of the frame
    assert np.allclose(structure.get_point_displacement_vector([5.0, 0.0]), np.array([0.0, -1.25e3, 0.0]), atol=1.e-7)


def test_basic_result_3():
    """Tests a structure with vertical springs and a point load in the middle.
    """
    # Create a structure instance
    structure = ps.core.Structure2D()
    # Add a frame element
    structure.add_frame_element([0.0, 0.0], [10.0, 0.0], 1.0, 1.0, 1.0, 1.0)
    # Add supports
    structure.add_support([0.0, 0.0], displacement_x=False)
    # Add springs
    structure.add_spring([0.0, 0.0], spring_y=1)
    structure.add_spring([10.0, 0.0], spring_y=1)
    # Add a point load
    structure.add_point_load([5.0, 0.0], [0.0, -1.0, 0.0])
    # Solve the linear system
    structure.solve_linear_system()
    # Test the forces in the middle of the frame
    assert np.allclose(structure.get_line_force_vector([4.99, 0.0])[3:], np.array([0.0, -0.5, -2.5]))
    # Test the displacements in the middle of the frame
    assert np.allclose(structure.get_point_displacement_vector([5.0, 0.0]), np.array([0.0, -0.5 - 1000 / 48, 0.0]))


#################################
# LOAD COMBINATION RESULT TESTS #
#################################

def test_load_combination_result_0():
    """Tests a structure with two line q-loads which are combined in a load combination.
    """
    # Create a structure instance
    structure = ps.core.Structure2D()
    # Add a frame element
    frame_id_0 = structure.add_frame_element([0.0, 0.0], [5.0, 0.0], 1.0, 1.0, 1.0, 1.0)
    frame_id_1 = structure.add_frame_element([5.0, 0.0], [10.0, 0.0], 1.0, 1.0, 1.0, 1.0)
    # Add supports
    structure.add_support([0.0, 0.0], displacement_x=False, displacement_y=False)
    structure.add_support([10.0, 0.0], displacement_y=False)
    # Add the two q-load lines
    structure.add_global_q_load(frame_id_0, -1.0, '0')
    structure.add_global_q_load(frame_id_1, -1.0, '1')
    # Add the load combination
    structure.add_load_combination('lc', {'0': 1.0, '1': 1.0})
    # Solve the linear system
    structure.solve_linear_system('lc')
    # Test the forces in the middle of the frame
    assert np.allclose(structure.get_line_force_vector([4.99, 0.0], 'lc')[3:], np.array([0.0, -0.05, -12.5]),
                       rtol=1.e-4)
    # Test the displacements in the middle of the frame
    assert np.allclose(structure.get_point_displacement_vector([5.0, 0.0], 'lc'), np.array([0.0, -50000 / 384, 0.0]))


################################
# PHASED ANALYSIS RESULT TESTS #
################################

def test_phased_analysis_result_0():
    """Tests a structure that consists of one frame with two additive linear phases.
    """
    # Create the phased analysis
    phase_analysis = ps.solver.PhasedAnalysis()
    # Create the two phases
    phase_0 = phase_analysis.create_phase('phase_0')
    phase_1 = phase_analysis.create_phase('phase_1')
    # Add phase_0 as the previous phase to phase_1
    phase_analysis.add_previous_phase(phase_1, phase_0)
    # Create a structure instance
    structure = ps.core.Structure2D()
    structure.set_phase(phase_0, phase_1)
    # Add a frame element
    frame_id = structure.add_frame_element([0.0, 0.0], [10.0, 0.0], 1.0, 1.0, 1.0, 1.0)
    # Add supports
    structure.add_support([0.0, 0.0], displacement_x=False, displacement_y=False)
    structure.add_support([10.0, 0.0], displacement_y=False)
    # Add a q-load
    structure.set_phase(phase_0)
    structure.add_point_load([5.0, 0.0], [0.0, -1.0, 0.0])
    structure.set_phase(phase_1)
    structure.add_global_q_load(frame_id, -1.0)
    # Solve the linear system
    structure.solve_linear_phase_system(phase_analysis)
    # Test the forces in the middle of the frame
    assert np.allclose(structure.get_line_force_vector([4.99, 0.0])[3:], np.array([0.0, -0.55, -15.0]), atol=1.e-3)
    # Test the displacements in the middle of the frame
    assert np.allclose(structure.get_point_displacement_vector([5.0, 0.0]),
                       np.array([0.0, -1000 / 48 + -50000 / 384, 0.0]))


def test_phased_analysis_result_1():
    """Tests a structure that consists of two frame which are static undetermined with two additive linear phases.
    Tests specifically if adding and removing frames in phases doesn't break the code.
    """
    # Create the phased analysis
    phase_analysis = ps.solver.PhasedAnalysis()
    # Create the two phases
    phase_0 = phase_analysis.create_phase('phase_0')
    phase_1 = phase_analysis.create_phase('phase_1')
    phase_2 = phase_analysis.create_phase('phase_2')
    # Add phase_0 as the previous phase to phase_1
    phase_analysis.add_previous_phase(phase_2, phase_0, phase_1)
    # Create a structure instance
    structure = ps.core.Structure2D(0.05)

    # Add a frame element
    structure.set_phase(phase_0, phase_2)
    frame_id_0 = structure.add_frame_element([0.0, 0.0], [5.0, 0.0], 1.0, 1.0, 1.0, 1.0)
    structure.set_phase(phase_1, phase_2)
    frame_id_1 = structure.add_frame_element([5.0, 0.0], [10.0, 0.0], 1.0, 1.0, 1.0, 1.0)

    # Phase 0
    structure.set_phase(phase_0)
    # Add supports
    structure.add_support([0.0, 0.0], displacement_x=False, displacement_y=False)
    structure.add_support([5.0, 0.0], displacement_y=False)
    # Add a q-load
    structure.add_global_q_load(frame_id_0, -1.0)

    # Phase 1
    structure.set_phase(phase_1)
    # Add supports
    structure.add_support([5.0, 0.0], displacement_x=False, displacement_y=False)
    structure.add_support([10.0, 0.0], displacement_y=False)
    # Add a q-load
    structure.add_global_q_load(frame_id_1, -1.0)

    # Phase 2
    structure.set_phase(phase_2)
    # Add supports
    structure.add_support([0.0, 0.0], displacement_y=False)
    structure.add_support([5.0, 0.0], displacement_x=False, displacement_y=False)
    structure.add_support([10.0, 0.0], displacement_y=False)
    # Add a q-load
    structure.add_global_q_load(frame_id_0, -1.0)
    structure.add_global_q_load(frame_id_1, -1.0)

    # Solve the linear system
    structure.solve_linear_phase_system(phase_analysis)

    # Test the forces at the middle support in the frames
    assert np.allclose(structure.get_line_force_vector([4.99, 0.0])[3:], np.array([0.0, 5.525, 3.1233]), atol=1.e-5)
