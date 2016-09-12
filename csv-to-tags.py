#!/usr/bin/env python

import boto3
import botocore
import argparse
import csv

# parse command line argumetns
def parse_args():
    parser = argparse.ArgumentParser(prog='csv-to-tags', description='Append tags to EC2 instances from a CSV file.')
    # required
    parser.add_argument('-i', '--in', required=True, action='store', dest='input_file', type=str, help='path to where the input file is located.')

    # optional
    parser.add_argument('-r', '--region',action='store', default='us-east-1', dest='aws_region', type=str, help='AWS region to use.')
    parser.add_argument('-v', '--version', action='version', version='0.1')

    args = parser.parse_args()
    return args

def tags_from_row(row, columns):
    tags = []
    for c in xrange(1, len(row)):
        tag = {}
        tag['Key'] = columns[c]
        tag['Value'] = row[c]
        tags.append(tag)
    return tags

def append_tags(instance_id, tags):
    if instance_id and tags:
        try:
            response = ec2.create_tags(
                Resources=[instance_id],
                Tags=tags
            )
        except botocore.exceptions.ClientError as e:
            print e.response['Error']['Message']

#
# Main
#
def main():
    global args
    global ec2

    args = parse_args()
    
    ec2 = boto3.client('ec2', region_name=args.aws_region)

    with open(args.input_file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        tag_names = []
        rows = list(reader)
        columns = rows[0]
        for r in xrange(1, len(rows)):
            instance_id = rows[r][0]
            tags = tags_from_row(rows[r], columns)
            append_tags(instance_id, tags)

if __name__ == "__main__":
    main()
