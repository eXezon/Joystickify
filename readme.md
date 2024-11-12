# Joystickify - Mouse Input for Accessibility

**Note: This project is in an early stage and is **NOT** actively under development.**

## Overview

This project is designed to bring joystick-like input to users who primarily rely on a mouse, enabling people with physical disabilities to play games that traditionally require joystick controls. By converting mouse input into joystick-style commands, this project aims to expand accessibility for a wider variety of games, especially for users who may face physical challenges that make traditional joystick use difficult.

## Features

- **Custom Sensitivity Adjustment**: Allows users to set mouse sensitivity levels for more precise control.
- **Deadzone Customization**: Users can define a "deadzone" range, where minimal mouse movement doesn’t translate to joystick input, helping reduce unintended movements.
- **Minimal Movement Deadzone**: Sets the minimum movement required for input to register, helpful for users who may experience minor, involuntary movements.
- **Maximum Speed Capping**: Limits the maximum speed of input, ensuring sudden or large movements are capped at a controlled speed. Useful for users who might experience spasms or rapid motions.
- **Axis Support**: Currently optimized for horizontal axis input, with an option for vertical axis support.

## Goals

Project's mission is to make gaming more accessible and inclusive by creating tools for people with physical disabilities. This project specifically aims to:

- Enable people to play joystick-dependent games using mouse input.
- Provide customizable settings tailored to individual needs.
- Collaborate with the accessibility community to continuously refine and improve the tool.

## How to Use

1. Install vJoy and pyvjoy:
   - Download and Install vJoy:
     - Go to the [vJoy Repo](https://github.com/jshafer817/vJoy) and follow the instructions.
     - Run the installer and follow the instructions to complete the installation.

2. Clone the repository:
   ```bash
   git clone https://github.com/eXezon/Joystickify/tree/main
   ```
3. Install the necessary requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the settings in the `config.yaml` file, adjusting sensitivity, deadzones, and speed caps to match personal preferences and needs.

## Roadmap

### Development Objectives

- **Initial Implementation**: Implement basic mouse-to-joystick mapping with customizable sensitivity, deadzones, and speed limits.
- **Project Restructuring**: Refactor the project to enhance its organization by implementing a modular structure with separate files, classes, and configuration files. This restructuring will lay the foundation for future improvements.


### Future Goals

- **Anti-Cheat Compatibility**: Improve compatibility with anti-cheat systems, as some may falsely flag this input method. Possible solutions include building a Human Interface Device (HID) integration, such as using an RP2040 microcontroller.
- **Graphical Interface**: Develop a user-friendly graphical interface to make configuration simpler.
- **Performance Improvements**: Optimize code for smoother operation and lower latency.
- **Platform Rebuild**: Consider rebuilding the project in a more efficient programming language or framework for improved performance.
- **Custom Control Layouts**: Add support for fully customizable control layouts in future versions.

## Contributing

Feedback and contributions are welcome, especially from users who can offer insights on accessibility needs. Your input is essential for making this tool more inclusive and practical.

## License

This project is licensed under the AGPL-3.0 License.
