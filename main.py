import logging
from mapper import MouseToJoystickMapper
from config import load_config, setup_logging

def main():
    """
    Main function to run the Joystickify.
    """
    config = load_config('config.yaml')

    setup_logging(
        enabled=config.get('logging_enabled', True),
        level=config.get('logging_level', 'INFO')
    )
    mapper = MouseToJoystickMapper(config)
    try:
        # Initialize mapper with configuration
        mapper.start()
    except KeyboardInterrupt:
        logging.info("Exiting...")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        mapper.stop()

if __name__ == "__main__":
    main()