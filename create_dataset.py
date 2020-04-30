import argparse
import csv
import os
import time

import pandas as pd

from sklearn.model_selection import train_test_split

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

def make_args_parser():
    # create an ArgumentParser object
    parser = argparse.ArgumentParser()
    # fill parser with information about program arguments
    parser.add_argument('--dir', '-d', default='data',
                         help='Define the absolute path of the parent directory')
    parser.add_argument('--out', '-o', default='dataset.tsv',
                         help='Define the absolute path of the output file')

    # return an ArgumentParser object
    return parser.parse_args()

def print_args(args):
    print('---------------------- Constructing dataset ----------------------\n')
    print("Running with the following configuration")
    # get the __dict__ attribute of args using vars() function
    args_map = vars(args)
    for key in args_map:
        print('\t', key, '-->', args_map[key])
    # add one more empty line for better output
    print()

def construct_dataset(parent_dir, output_file):
    id = 0
    with open(output_file, mode='w') as dataset:
        dataset_writer = csv.writer(dataset, delimiter='\t',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
        dataset_writer.writerow(['Id', 'Title', 'Content', 'Category'])
        for root, _, files in os.walk(parent_dir, topdown=True):
            for file in files:
                if file.endswith('.txt'):
                    category = root.partition('/')[-1]
                    file_path = CURRENT_DIR + '/' + root + '/' + file
                    try:
                        # Open file in utf-8 encoding
                        file = open(file_path, 'r', encoding='utf-8')
                        # Read file and split content
                        file_lines = file.readlines()
                        title = file_lines[0]
                        content = ''.join(file_lines[1:])
                        # Write to csv
                        dataset_writer.writerow([id, title, content, category])
                        # Close file
                        file.close()
                        # Increase id number
                        id += 1
                    except:
                        print("\tAn error occured on reading file: {}".format(file_path))

def split_dataset(output_file):
    output_folder = output_file.partition('/')[0]
    df = pd.read_csv(output_file, sep='\t')
    df_train, df_test = train_test_split(df, test_size=0.2)
    # export to csv
    df_train.to_csv(output_folder + '/train_set.tsv', sep='\t', index=False)
    df_test.to_csv(output_folder + '/test_set.tsv', sep='\t', index=False)

def main():
    # parse and print arguments
    args = make_args_parser()
    print_args(args)
    # Check if dir exists
    if not os.path.exists(args.dir):
        print("Directory does not exists!")
    else:
        start = time.time()
        print("Creating datasets...")
        construct_dataset(args.dir, args.out)
        split_dataset(args.out)
        end = time.time()
        print("Datasets creating completed successfully. Time elapsed: {:.3f} seconds"
              .format(end - start))

if __name__ == "__main__":
    main()
