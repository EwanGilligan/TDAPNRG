import json
import sys
from randology.pnrg.binary import FromBinaryFile
from randology import *
import generators
import pprint
import os

USAGE = "usage: python run_test.py <config file name>"
HYPERCUBE = "hypercube"
MATRIX_RANK = "matrix rank"


def run_test():
    if len(sys.argv) != 2:
        print(USAGE)
        exit(1)
    config_file = sys.argv[1]
    # get the config dictionary
    data_dict = get_test_dict(config_file)
    # get the values needed to configure the test.
    test_dict = data_dict['test']
    generator_dict = data_dict['generators']
    runs = data_dict['runs']
    n_points = data_dict['n_points']
    homology_dimension = data_dict['homology_dimension']
    filtration_size = data_dict['filtration_size']
    verbose = data_dict['verbose'] if 'verbose' in data_dict else True
    store_data = data_dict['store_data'] if 'store_data' in data_dict else False
    gpu = data_dict['gpu'] if 'gpu' in data_dict else False
    recalculate_distribution = data_dict[
        'recalculate_distribution'] if 'recalculate_distribution' in data_dict else False
    reference_rng = generators.download_generator(data_dict['reference_rng'], "reference_rng",
                                                  n_points)  # FromBinaryFile(data_dict['reference_rng'], n_points)
    # get the generators.
    generators_list = list(get_generators(generator_dict))
    output_dict = None
    test = None
    # see which test is being done.
    if test_dict['name'] == HYPERCUBE:
        scales = test_dict['scales']
        dimension = test_dict['dimension']
        delayed_coordinates = test_dict['delayed_coordinates'] if 'delayed_coordinates' in test_dict else False
        failure_threshold = test_dict['failure_threshold'] if 'delayed_coordinates' in test_dict else 1
        test = HypercubeTest(reference_rng=reference_rng, number_of_points=n_points, runs=runs, dimension=dimension,
                             homology_dimension=homology_dimension, filtration_size=filtration_size,
                             recalculate_distribution=recalculate_distribution, delayed_coordinates=delayed_coordinates,
                             store_data=store_data, gpu=gpu)
        output_dict = test.test_generators_multiple_scales(generators_list, scales, failure_threshold, verbose)
    elif test_dict['name'] == MATRIX_RANK:
        matrix_size = test_dict['matrix_size']
        test = MatrixRankTest(reference_rng=reference_rng, number_of_points=n_points, runs=runs,
                              matrix_size=matrix_size,
                              homology_dimension=homology_dimension, recalculate_distribution=recalculate_distribution,
                              store_data=store_data)
        output_dict = test.test_generator_list(generators_list, verbose)
    else:
        raise ValueError("Test name not recognised.")
    output_file = os.environ['OUTPUTDIR'] + test.get_data_file_name() + "-summary.txt"
    with open(output_file, "w+") as f:
        f.write("[Test Configuration]\n")
        pprint.pprint(vars(test), stream=f, indent=4)
        f.write("\n[Test Output]\n")
        # Handles subdictionary formatting, which pprint doesn't
        json.dump(output_dict, f, indent=2)
        # pprint.pprint(output_dict, stream=f, indent=4)


def get_generators(generator_dict):
    salt = generator_dict['salt'] if 'salt' in generator_dict else None
    if 'group' in generator_dict:
        return generators.generator_group(generator_dict['group'], salt)(generator_dict['seeds'])
    elif 'list' in generator_dict:
        return generators.get_generator_list(generator_dict['list'], generator_dict['seeds'], salt)
    elif 'directory' in generator_dict:
        loop_file = generator_dict['loop_file'] if 'loop file' in generator_dict else True
        directory_url = generator_dict['directory']
        generators.download_directory(directory_url, os.environ['DATADIR'])
        return generators.get_generators_from_directory(os.environ['DATADIR'], 12000, loop_file)
    else:
        raise ValueError()


def get_test_dict(filename):
    with open(filename, "r") as json_file:
        data = json.load(json_file)
    return data


if __name__ == '__main__':
    run_test()
