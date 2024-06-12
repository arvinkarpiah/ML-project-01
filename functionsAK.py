############## # Read SEG-Y header from file

import numpy as np

############## # Read .bin file

def read_bin(fileName, NZ, NX):
    # Open the binary file for reading
    with open(fileName, 'rb') as fid:
        # Read binary data as a 1D array of float32 values
        v = np.fromfile(fid, dtype=np.float32, count=NZ * NX)
    
    # Reshape the 1D array into a 2D array of shape (NZ, NX)
    vel = np.reshape(v, (NX, NZ))
    
    return vel 

############## Convert segy to su

import numpy as np

def sgy_to_sux(sgy_filename, su_filename):
    """
    Convert a SEG-Y file to SU format

    Args:
    sgy_filename (str): Path to the input SEG-Y file.
    su_filename (str): Path to the output SU file.
    """
    # Define SEG-Y binary header structure
    bin_header_format = np.dtype([
        ("job", "S40"),  # Job name
        ("line", ">i4"),  # Line number
        ("num_samples", ">i4"),  # Number of samples per trace
        # Add more fields as needed
    ])

    # Read SEG-Y binary header
    with open(sgy_filename, "rb") as sgy_file:
        binary_header = sgy_file.read(3200)
        bin_header = np.frombuffer(binary_header[:240], dtype=bin_header_format)[0]

    # Extract required header information
    job = bin_header["job"].decode("ascii").strip()
    line_number = bin_header["line"]
    num_samples = bin_header["num_samples"]

    # Read SEG-Y data
    with open(sgy_filename, "rb") as sgy_file:
        sgy_file.seek(3600)  # Skip text header and binary header
        sgy_data = np.fromfile(sgy_file, dtype=np.int32)

    # Reshape the data array
    sgy_data = sgy_data.reshape(-1, num_samples)

    # Write data to SU file
    with open(su_filename, "wb") as su_file:
        # Write SU header
        # (You may need to define a proper SU header format based on your requirements)
        su_header = f"C 1 {job} {line_number}".encode("ascii")
        su_file.write(su_header)
        
        # Write data to SU file
        sgy_data.T.tofile(su_file)

#################### read segyy using segyio        

import segyio

def read_segy_info(segy_filename):
    """
    Read information about a 2D SEG-Y file.

    Args:
    segy_filename (str): Path to the SEG-Y file.

    Returns:
    tuple: A tuple containing the number of samples per trace and the number of traces.
    """
    with segyio.open(segy_filename, "r") as segy_file:
        # Get number of samples per trace
        num_samples = segy_file.samples.size

        # Get number of traces
        num_traces = segy_file.tracecount

    return num_samples, num_traces














