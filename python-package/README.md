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

©2023 CDW LLC