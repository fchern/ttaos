#!/home/$USER/anaconda3/bin/python3
import pandas as pd
import getpass
import os
import sys
import traceback
import argparse
import glob

__author__ = 'cchen'


def get_default(s):
    if s == 'int':
        return "=0"
    elif s == 'std::string':
        return ''
    elif s == 'int64_t':
        return '=0'
    elif s == 'short':
        return '=0'
    elif s == 'int32_t':
        return '=0'
    elif s == 'float':
        return '=0.0'
    elif s == 'double':
        return "=0.0"
    elif s == 'size_t':
        return "=0"
    elif s == 'bool':
        return "=true"
    elif 'Enum' in s:
        return "=static_cast<{}>(0)".format(s)
    else:
        return "=0"


def parse_header_file(struct_dict, header_file):
    create_header(header_file)

    print(struct_dict)
    for name, frame in struct_dict.items():
        print('------------------ creating class for {0} ------------------ '.format(name))
        create_vector_loader_class(frame, header_file, name)

        header_file.write("\n\n\n")

    header_file.write("}\n")

    header_file.write("#endif\n")


def create_vector_loader_class(column_notations, header_file, struct_name):
    header_file.write("class {} {{\n".format(struct_name))
    header_file.write("public:\n")
    for y, row in column_notations.iterrows():
        header_file.write(
            '{0} {1} {2};\n'.format(row['type_name'], row['member_name'], get_default(row['type_name'])))
    header_file.write(struct_name + "()	{;}\n")
    header_file.write(
        "{}(std::vector<std::string> columnNames, boost::tokenizer< boost::char_separator<char> > tokens){{\n".format(
            struct_name))
    header_file.write("	size_t i = 0;\n")
    header_file.write("	for (const std::string& t : tokens) {\n")
    for y, row in column_notations.iterrows():
        if row['type_name'] == 'std::string':
            temp_str = "if (columnNames[i] == std::string(\"{0}\")){{{0} = t;}}\n\n".format(
                row['member_name'])
            header_file.write(temp_str)
        elif row['type_name'] in set(['int', 'int64_t', 'double', 'bool', 'int32_t']):
            header_file.write(
                "if (columnNames[i] == std::string(\"{0}\")){{{0} = boost::lexical_cast<{1}>(t);}}\n\n".format(
                    row['member_name'], row['type_name']))
        elif 'Enum' in row['type_name']:
            header_file.write(
                "if (columnNames[i] == std::string(\"{0}\")){{{0} = EnumParser::fromString{1}(t);}}\n\n".format(
                    row['member_name'],
                    row['type_name']))
        else:
            raise ValueError('cannot parse typename {0}'.format(row['type_name']))

    header_file.write("++i;\n")
    header_file.write("}\n")

    # header_file.write("if(i != columnNames.size()){throw std::runtime_error(\"the column names and content does not match\");}\n")

    header_file.write("}\n")
    header_file.write("virtual ~{}(){{}};\n".format(struct_name))
    key_member = column_notations[column_notations['is_key'] == 1]['member_name'].iloc[0]
    key_type = column_notations[column_notations['is_key'] == 1]['type_name'].iloc[0]
    header_file.write(
        'bool operator < (const	' + struct_name + '& o) const	{	return o.' + key_member + ' < ' + key_member + ';}\n')
    header_file.write(key_type + ' getKey () const	{	return ' + key_member + ';}\n')
    header_file.write("};\n")


def create_header(header_file):
    header_file.write("#ifndef {}_H_\n".format('AUTO_GEN_CSV_LOADER'))
    header_file.write("#define {}_H_\n".format('AUTO_GEN_CSV_LOADER'))
    header_file.write("#include <boost/lexical_cast.hpp>\n")
    header_file.write("#include <boost/tokenizer.hpp>\n")
    header_file.write("#include \"../utilities/ProjectEnums.h\"\n")
    header_file.write("#include \"../utilities/ProjectTypes.h\"\n")
    header_file.write("#include <boost/foreach.hpp>\n")
    header_file.write("#include <vector>\n")
    header_file.write("namespace terran {\n")


def get_struct_name(x):
    return x.split('/')[-1].split('.')[0]


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--source", help="the target DIRECTORY that contains all the csv column definition file ",
                        required=False)
    parser.add_argument("-o", "--output", help="the output FILENAME where all the loaders are stored",
                        required=False)

    args = parser.parse_args()
    input_directory = args.source + '/*.type'

    print('we are generating csv loader from {}'.format(input_directory))

    column_files = glob.glob(input_directory)
    print(column_files)

    struct_names = [get_struct_name(x) for x in column_files ]

    print('these are all the structures we will be working on')
    print(struct_names)

    struct_dict = dict()

    for struct_name in struct_names:
        print('reading {}..., frame is:'.format(struct_name))
        type_frame = pd.read_csv('./type_files/{}.type'.format(struct_name))
        print(type_frame)
        struct_dict[struct_name] = type_frame

    print('writing loader to {}'.format(args.output))
    if os.path.isfile(args.output):
        print('\n... over-writing existing file : ' + args.output)

    with open(args.output, 'w') as header_file:
        parse_header_file(struct_dict, header_file)


if __name__ == "__main__":
    if getpass.getuser() != 'cchen':
        raise NameError('operational scripts can only be run by ubuntu')
    try:
        main()
    except Exception as e:
        print('\n')
        traceback.print_exc()
        print("\n")
        sys.exit(1)
