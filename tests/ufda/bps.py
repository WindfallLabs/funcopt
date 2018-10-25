# -*- coding: utf-8 -*-

def bp_model(db_in, file_out, name_opt="A", flag=False):
    """Building Permit Model.
    Args:
        db_in (str): File path to SQLite database
        file_out (str): File path to ...
        name_opt (str): A string
        flag (bool): a flag (default False)
    """
    print("('{0}', '{1}', '{2}', {3})".format(
        db_in, file_out, name_opt, flag))
    print("Analyzing...")
    return
