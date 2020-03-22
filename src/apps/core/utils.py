import os

def get_env_variable(var_name):
    """
    Get the environment variable or return exception.

    Parameters
    ----------
    var_name : str
        Environment variable name.

    Raises
    ------
    ValueError : if the environment variable doesn't exist.

    Returns
    -------
    : str
        Value of the Environment variable name.
    """
    try:
        return os.environ[var_name]
    except KeyError:
        raise ValueError(f'Set the {var_name} environment variable.')