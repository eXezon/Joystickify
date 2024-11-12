import threading
import time
import logging
import pyvjoy
from pynput import mouse, keyboard


class MouseToJoystickMapper:
    """
    A class to map mouse movements to a virtual joystick using vJoy.
    """

    #joystick axis constants
    VJOY_AXIS_MIN = 1
    VJOY_AXIS_MAX = 32767 #(Max value, need to wchange later according to device)
    VJOY_AXIS_CENTER = (VJOY_AXIS_MAX + VJOY_AXIS_MIN) // 2

    def __init__(self, config):
        """
        Initialization.

        Args:
            config (dict): Configuration parameters.
        """
        self.config = config

        #initialize virutal (vJoy) device
        self.device_id = config.get('device_id', 1)
        self.joystick = pyvjoy.VJoyDevice(self.device_id)

        #axis values
        self.axis_x_value = self.VJOY_AXIS_CENTER
        self.axis_y_value = self.VJOY_AXIS_CENTER

        #paramters from config
        self.sensitivity = config.get('sensitivity', 0.5)
        self.dead_zone = config.get('dead_zone', 2000)
        self.movement_dead_zone = config.get('movement_dead_zone', 1)
        self.max_speed_enabled = config.get('max_speed_enabled', False)
        self.max_speed = config.get('max_speed', 1000)
        self.joystick_enabled = True  #start with emulation enabled
        self.smooth_reset_enabled = config.get('smooth_reset_enabled', True)
        self.smooth_reset_speed = config.get('smooth_reset_speed', 500)
        self.vertical_movement_enabled = config.get('vertical_movement_enabled', True)
        self.toggle_hotkey = config.get('toggle_hotkey', 'F8')

        #parse hotkey string to pynput key
        from config import get_hotkey
        self.toggle_hotkey = get_hotkey(self.toggle_hotkey)

        self._axis_lock = threading.Lock()
        self._last_mouse_x = None
        self._last_mouse_y = None
        self._last_time = None
        self._reset_thread = None

    def start(self):
        """
        mouse and keyboard listeners.
        """
        #mouse listener
        self.mouse_listener = mouse.Listener(on_move=self._on_mouse_move)
        self.mouse_listener.start()

        #keyboard listener
        self.keyboard_listener = keyboard.Listener(on_press=self._on_key_press)
        self.keyboard_listener.start()

        logging.info(f"Press {self.toggle_hotkey} to toggle joystick emulation.")

        self.mouse_listener.join()
        self.keyboard_listener.join()

    def _on_mouse_move(self, x, y):
        """
        Handle mouse movement events.
        """
        current_time = time.time()

        if self.joystick_enabled:
            with self._axis_lock:
                if (
                    self._last_mouse_x is not None
                    and self._last_mouse_y is not None
                    and self._last_time is not None
                ):
                    #delta between movements
                    dx = x - self._last_mouse_x
                    dy = y - self._last_mouse_y

                    #calculate time difference
                    dt = current_time - self._last_time or 1e-6  # Avoid division by zero

                    #max speed
                    if self.max_speed_enabled:
                        dx, dy = self._apply_max_speed(dx, dy, dt)

                    #movement dead zone
                    if abs(dx) >= self.movement_dead_zone:
                        self._update_axis('x', dx)

                    if self.vertical_movement_enabled and abs(dy) >= self.movement_dead_zone:
                        self._update_axis('y', dy)

                    # Send updated axis values to the virtual joystick
                    self._send_joystick_updates()

                #last positions and time
                self._last_mouse_x = x
                self._last_mouse_y = y
                self._last_time = current_time
        else:
            #smooth reset (WIP)
            if (
                self.smooth_reset_enabled
                and (self._reset_thread is None or not self._reset_thread.is_alive())
            ):
                self._reset_thread = threading.Thread(target=self._smooth_reset_axes)
                self._reset_thread.start()
            else:
                #instantly reset axes to center
                self._reset_axes_to_center()

            #reset last positions and time
            self._last_mouse_x = None
            self._last_mouse_y = None
            self._last_time = None

    def _on_key_press(self, key):
        """
        Handle key press events.
        """
        if key == self.toggle_hotkey:
            self.joystick_enabled = not self.joystick_enabled
            status = "Enabled" if self.joystick_enabled else "Disabled"
            logging.info(f"Joystick Emulation {status}")

    def _apply_max_speed(self, dx, dy, dt):
        """
        Cap the mouse movement speed to the maximum allowed speed.
        """
        # Calculate movement speeds
        speed_x = dx / dt
        speed_y = dy / dt

        # Cap the speeds if they exceed max_speed
        if abs(speed_x) > self.max_speed:
            dx = self.max_speed * dt * (1 if speed_x > 0 else -1)

        if self.vertical_movement_enabled and abs(speed_y) > self.max_speed:
            dy = self.max_speed * dt * (1 if speed_y > 0 else -1)

        return dx, dy

    def _update_axis(self, axis, delta):
        """
        Update the axis value based on the delta movement.
        """
        if axis == 'x':
            self.axis_x_value += int(delta * self.sensitivity * 100)
            # Clamp the axis value
            self.axis_x_value = max(self.VJOY_AXIS_MIN, min(self.VJOY_AXIS_MAX, self.axis_x_value))
        elif axis == 'y':
            self.axis_y_value += int(delta * self.sensitivity * 100)
            # Clamp the axis value
            self.axis_y_value = max(self.VJOY_AXIS_MIN, min(self.VJOY_AXIS_MAX, self.axis_y_value))

    def _send_joystick_updates(self):
        """
        Send the updated axis values to the virtual joystick, applying the dead zone.
        """
        # Apply dead zone for X-axis
        if abs(self.axis_x_value - self.VJOY_AXIS_CENTER) < self.dead_zone:
            axis_x_output = self.VJOY_AXIS_CENTER
        else:
            axis_x_output = self.axis_x_value

        # Apply dead zone for Y-axis
        if self.vertical_movement_enabled:
            if abs(self.axis_y_value - self.VJOY_AXIS_CENTER) < self.dead_zone:
                axis_y_output = self.VJOY_AXIS_CENTER
            else:
                axis_y_output = self.axis_y_value
        else:
            axis_y_output = self.VJOY_AXIS_CENTER

        # Send to virtual joystick
        self.joystick.set_axis(pyvjoy.HID_USAGE_X, axis_x_output)
        self.joystick.set_axis(pyvjoy.HID_USAGE_Y, axis_y_output)

    def _reset_axes_to_center(self):
        """
        Reset the joystick axes to the center position instantly.
        """
        with self._axis_lock:
            self.axis_x_value = self.VJOY_AXIS_CENTER
            self.axis_y_value = self.VJOY_AXIS_CENTER
            self._send_joystick_updates()

    def _smooth_reset_axes(self):
        """
        Smoothly reset the joystick axes to the center position.
        """
        while not self.joystick_enabled and (
            self.axis_x_value != self.VJOY_AXIS_CENTER or self.axis_y_value != self.VJOY_AXIS_CENTER
        ):
            with self._axis_lock:
                #calculate differences
                delta_x = self.VJOY_AXIS_CENTER - self.axis_x_value
                delta_y = self.VJOY_AXIS_CENTER - self.axis_y_value

                #calculate steps
                step_x = int(delta_x / self.smooth_reset_speed) or (1 if delta_x > 0 else -1)
                step_y = int(delta_y / self.smooth_reset_speed) or (1 if delta_y > 0 else -1)

                #update axis values
                self.axis_x_value += step_x
                self.axis_y_value += step_y

                #update joystick values
                self._send_joystick_updates()

            time.sleep(0.01)  # Adjust for smoothness

    def stop(self):
        """
        Stop the mouse and keyboard listeners.
        """
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        if self._reset_thread and self._reset_thread.is_alive():
            self._reset_thread.join()