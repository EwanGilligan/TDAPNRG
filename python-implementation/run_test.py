import json
import sys
from randology.pnrg.binary import FromBinaryFile
from randology import *
import generators

USAGE = "usage: python run_test.py <config file name>"
HYPERCUBE = "hypercube"
MATRIX_RANK = "matrix rank"


def run_test():
    if len(sys.argv) != 2:
        print(USAGE)
        exit(1)
    # get the config dictionary
    data_dict = get_test_dict(sys.argv[1])
    # get the values needed to configure the test.
    test_dict = data_dict['test']
    generator_dict = data_dict['generators']
    runs = data_dict['runs']
    n_points = data_dict['n_points']
    homology_dimension = data_dict['homology_dimension']
    filtration_size = data_dict['filtration_size']
    verbose = data_dict['verbose'] if 'verbose' in data_dict else True
    recalculate_distribution = data_dict[
        'recalculate_distribution'] if 'recalculate_distribution' in data_dict else False
    reference_rng = FromBinaryFile(data_dict['reference_rng'], n_points)
    # get the generators.
    generators = list(get_generators(generator_dict))
    print(generators)
    output_dict = None
    # see which test is being done.
    if test_dict['name'] == HYPERCUBE:
        scales = test_dict['scales']
        dimension = test_dict['dimension']
        delayed_coordinates = test_dict['delayed_coordinates'] if 'delayed_coordinates' in test_dict else False
        failure_threshold = test_dict['failure_threshold'] if 'delayed_coordinates' in test_dict else 1
        test = HypercubeTest(reference_rng=reference_rng, number_of_points=n_points, runs=runs, dimension=dimension,
                             homology_dimension=homology_dimension, filtration_size=filtration_size,
                             recalculate_distribution=recalculate_distribution, delayed_coordinates=delayed_coordinates)
        output_dict = test.test_generators_multiple_scales(generators, scales, failure_threshold, verbose)
    elif test_dict['name'] == MATRIX_RANK:
        pass
    else:
        raise ValueError("Test name not recognised.")
    print(output_dict)


def get_generators(generator_dict):
    salt = generator_dict['salt'] if 'salt' in generator_dict else None
    if 'group' in generator_dict:
        return generators.generator_group(generator_dict['group'], salt)(generator_dict['seeds'])
    elif 'list' in generator_dict:
        return generators.get_generator_list(generator_dict['list'], generator_dict['seeds'], salt)
    elif 'directory' in generator_dict:
        raise NotImplemented()
    else:
        raise ValueError()


def get_test_dict(filename):
    with open(filename, "r") as json_file:
        data = json.load(json_file)
    return data


if __name__ == '__main__':
    run_test()
