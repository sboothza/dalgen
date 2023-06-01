import argparse
import os
from typing import List

from adaptors.adaptor_factory import AdaptorFactory
from database_objects import Table, KeyType, QueryType
from generators.generator_factory import GeneratorFactory
from naming import Naming
from utils import get_fullname


def import_db(db_connection: str, definition_file: str, dictionary_file: str, big_dictionary_file: str):
    naming = Naming(dictionary_file, big_dictionary_file)
    adaptor = AdaptorFactory.get_adaptor_for_connection_string(db_connection, naming)
    db = adaptor.import_schema(None)
    adaptor.generate_schema_definition(db, definition_file)


def generate_dal(definition_file: str, dictionary_file: str, big_dictionary_file: str, output_folder: str,
                 template_folder: str, language: str, db_type: str):
    naming = Naming(dictionary_file, big_dictionary_file)
    generator = GeneratorFactory.get_generator(language, naming)
    adaptor = AdaptorFactory.get_adaptor_for_dbtype(db_type, naming)
    database = generator.import_definition(definition_file, naming)
    # generator.copy_templates(template_folder, output_folder)
    generator.generate_entities(database, os.path.join(output_folder, "entities"), adaptor, naming)
    generator.generate_repositories(database, os.path.join(output_folder, "repositories"), adaptor, naming)


def generate_ddl(definition_file: str, dictionary_file: str, big_dictionary_file: str, db_type: str):
    naming = Naming(dictionary_file, big_dictionary_file)
    adaptor = AdaptorFactory.get_adaptor_for_dbtype(db_type, naming)
    database = adaptor.import_definition(definition_file, naming)

    # find references and push in front
    tables = adaptor.get_ordered_table_list(database)

    for table in tables:
        print(adaptor.generate_create_script(table))


def main():

    sql=f"select * from bob where id = '{QueryType.FetchAll}'"
    print(sql)

    parser = argparse.ArgumentParser(description="Generate DAL")
    parser.add_argument("operation",
                        help="Operation",
                        type=str.lower,
                        choices=["import-db", "generate-dal", "generate-ddl"])
    parser.add_argument("--db-connection",
                        help="DB Connection string",
                        dest="db_connection",
                        type=str,
                        default="not_set",
                        required=False)
    parser.add_argument("--definition-file",
                        help="Definition filename",
                        dest="definition_file",
                        type=str,
                        default="not_set",
                        required=False)
    parser.add_argument("--output-folder",
                        help="Output folder for generated files",
                        dest="output",
                        type=str,
                        default="not_set",
                        required=False)
    parser.add_argument("--template-folder",
                        help="Template folder for required files",
                        dest="template",
                        type=str,
                        default="not_set",
                        required=False)
    parser.add_argument("--dictionary",
                        help="Dictionary file",
                        dest="dictionary",
                        type=str,
                        default="not_set",
                        required=False)
    parser.add_argument("--big-dictionary",
                        help="Big Word Dictionary file",
                        dest="big_dictionary",
                        type=str,
                        default="not_set",
                        required=False)
    parser.add_argument("--language",
                        help="Language",
                        dest="language",
                        type=str,
                        default="not_set",
                        required=False)
    parser.add_argument("--db-type",
                        help="Db Type to generate",
                        dest="db_type",
                        type=str,
                        default="not_set",
                        required=False)

    args = parser.parse_args()
    if args.operation == "import-db":
        if args.db_connection == "not_set":
            print("Db connection is required")
            exit(1)

        if args.definition_file == "not_set":
            print("Definition filename is required")
            exit(1)

        if args.dictionary == "not_set":
            print("Dictionary filename is required")
            exit(1)

        if args.big_dictionary == "not_set":
            print("Big Word Dictionary filename is required")
            exit(1)

        import_db(args.db_connection, get_fullname(args.definition_file), get_fullname(args.dictionary),
                  get_fullname(args.big_dictionary))

    elif args.operation == "generate-dal":
        if args.definition_file == "not_set":
            print("Definition filename is required")
            exit(1)

        if args.dictionary == "not_set":
            print("Dictionary filename is required")
            exit(1)

        if args.big_dictionary == "not_set":
            print("Big Word Dictionary filename is required")
            exit(1)

        if args.output == "not_set":
            print("Output folder is required")
            exit(1)

        if args.template == "not_set":
            print("Template folder is required")
            exit(1)

        if args.language == "not_set":
            print("Language is required")
            exit(1)

        if args.db_type == "not_set":
            print("Db Type is required")
            exit(1)

        generate_dal(get_fullname(args.definition_file), get_fullname(args.dictionary),
                     get_fullname(args.big_dictionary), get_fullname(args.output),
                     get_fullname(args.template), args.language, args.db_type)

    elif args.operation == "generate-ddl":
        if args.definition_file == "not_set":
            print("Definition filename is required")
            exit(1)

        if args.dictionary == "not_set":
            print("Dictionary filename is required")
            exit(1)

        if args.big_dictionary == "not_set":
            print("Big Word Dictionary filename is required")
            exit(1)

        if args.db_type == "not_set":
            print("Db Type is required")
            exit(1)

        generate_ddl(get_fullname(args.definition_file), get_fullname(args.dictionary),
                     get_fullname(args.big_dictionary), args.db_type)


if __name__ == '__main__':
    main()
