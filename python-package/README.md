# Decoder Ring

This simple package uses Drink More Water Ltd. standards to create names for IT purposes.

## Name Requirements

- Must be NetBios compatible
  - 15 ASCII characters max
  - Invalid characters: \/:*?"<>|
- Building ID
  - Must be zero padded
  - Official source of truth is a CSV in the company share
- Time Zone
  - The time zone, derived from the building address, must be included
- Entity
  - 3:7 characters are allowed
  - This is usually a device name
- Device function
  - Official functions: server, network, virtualized, app, or other
  - Must abbreviate function to the first letter
- Component
  - This can be whatever the user wants
  - Only allowed to use remaining characters to remain NetBios compatible

## Install

This package is installable via pip. Two simple ways to accomplish this are:

### Clone and install

```bash
git clone https://github.com/cdwlabs/ChiPy-Decoder-Ring.git
cd ChiPy-Decoder-Ring/python-package
~~ Create Python virtual environment as desired ~~
pip install .
```

### Pip install from GitHub

```bash
pip install 'dmw_decoder @ git+https://github.com/cdwlabs/ChiPy-Decoder-Ring/@main#subdirectory=python-package'
```

## Tests

We use pytest for this project. In order to run all tests, an API key for [geoapify](https://www.geoapify.com/) must be acquired and placed in to an .env file in the tests directory or setup as an environmental variable. There is an [example](./tests/example.env) file for reference.

Testing dependencies are listed in the pyproject.toml file and can be installed with the \[tests\] modifier. Installing locally might look something like the following.

```bash
pip install .[tests]
```

## Usage

This is an example package and likely has little real world use. Presently there are no cli or gui entrypoints so a user would treat this more like a library and utilize an import to access the code. Example:

```python
import dmw_decoder
decoder = dmw_decoder.Decoder(api_key)
name_result = decoder.create_netbios_compatible_name(building_id, device_function, entity, component)
```

©2023 CDW LLC
