from pathlib import Path

OUTPUT_DATA_DIR = Path(__file__).parent

SCORES_FILE = OUTPUT_DATA_DIR.joinpath('scores.json')

A_OUTPUT = OUTPUT_DATA_DIR.joinpath('a_output')
B_OUTPUT = OUTPUT_DATA_DIR.joinpath('b_output')
C_OUTPUT = OUTPUT_DATA_DIR.joinpath('c_output')
D_OUTPUT = OUTPUT_DATA_DIR.joinpath('d_output')
E_OUTPUT = OUTPUT_DATA_DIR.joinpath('e_output')
