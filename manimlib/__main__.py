#!/usr/bin/env python
from manimlib import __version__
import manimlib.config
import manimlib.extract_scene
import manimlib.logger
import manimlib.utils.init_config

from manimlib.logger import log

def main():
    print(f"ManimGL \033[32mv{__version__}\033[0m")

    args = manimlib.config.parse_cli()
    if args.version and args.file is None:
        return
    if args.log_level:
        manimlib.logger.log.setLevel(args.log_level)

    if args.config:
        manimlib.utils.init_config.init_customization()
    else:
        config = manimlib.config.get_configuration(args)
        scenes = manimlib.extract_scene.main(config)

        log.info(f"\n===scenes: {scenes}\n")
        for scene in scenes:
            scene.run()
            log.info('\n===all is well')


if __name__ == "__main__":
    main()    
