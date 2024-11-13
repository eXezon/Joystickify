# Joystickify - Mouse Input for Accessibility

**Note: This is an early-stage project and is **NOT** actively under development. It’s a project that has been gathering dust in my documents for some time, and I plan to work on it sporadically.**

## Overview

Joystickify is designed to bring joystick-like input to users who primarily rely on a mouse, enabling people with physical disabilities to play games that traditionally require controllers, joysticks, or steering wheels controls. By converting mouse input into joystick-style commands, this project aims to expand accessibility for a wider variety of games, especially for users who may face physical challenges that make traditional joystick use difficult.

## Features

- **Custom Sensitivity Adjustment**: Allows users to set mouse sensitivity levels for more precise control.
- **Deadzone Customization**: Users can define a "deadzone" range, where minimal mouse movement doesn’t translate to joystick input, helping reduce unintended movements.
- **Minimal Movement Deadzone**: Sets the minimum movement required for input to register, helpful for users who may experience minor, involuntary movements.
- **Maximum Speed Capping**: Limits the maximum speed of input, ensuring sudden or large movements are capped at a controlled speed. Useful for users who might experience spasms or rapid motions.
- **Separated Axis Support**: Currently optimized for horizontal axis input, with an option for vertical axis support.

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


### Planned Enhancements & Features

- **Anti-Cheat Compatibility**: Improve compatibility with anti-cheat systems, as some may falsely flag this input method. Possible solutions include building a Human Interface Device (HID) integration, such as using a RP2040 microcontroller.
- **Graphical Interface**: Develop a user-friendly graphical interface to make configuration simpler.
- **Performance Improvements**: Optimize code for smoother operation and lower latency.
- **Platform Rebuild**: Consider rebuilding the project in a more efficient programming language or framework for improved performance.
- **Custom Control Layouts**: Add support for fully customizable control layouts in future versions.

## Q&A and Tips

- **Why isn’t my game responding correctly?**\
  Some games might require to adjust in-game settings like deadzone and sensitivity to work well with Joystickify. This is not an issue with the software itselt but rather how certain games handle controller inputs and joystick sensitivity.\
E.g. For the best experience with *Trackmania* set ingame `Analog Sensitivity` to `1` and `Analog Dead Zone` to a low value, and then configure the settings in the `config.yaml` file.

- **How can I confirm Joystickify is working?**\
  Use the "Monitor vJoy" application that comes with vJoy. When Joystickify is running, you should see the virtual joystick axis "X" or "Y" move in response to mouse movements.
## Contributing

Feedback and contributions are welcome, especially from users who can offer insights on accessibility needs. Your input is essential for making this tool more inclusive and practical.

## License

This project is licensed under the AGPL-3.0 License.
