"""Configuration file for managing environment variables."""
from dotenv import load_dotenv

import environ


@environ.config(prefix="")
class AppConfig:
    """Application configuration object used for managing environment variables."""

    @environ.config
    class Log:
        """App configuration object used for managing logging settings."""

        level = environ.var(default="INFO", help="The log level for the application.")

        @level.validator
        def _ensure_level_is_valid(self, var, level):
            valid_options = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if level not in valid_options:
                raise ValueError(
                    f"LOG_LEVEL is invalid.  Must be set to one of the following: {valid_options}"
                )

    log = environ.group(Log)

    @environ.config
    class App:
        """Web service app configurations."""

        port = environ.var(
            default=8080, help="The port number to start the web service."
        )

        host = environ.var(
            default="0.0.0.0",  # noqa: S104
            help="The host IP to start the web service.",
        )

    app = environ.group(App)

    @environ.config
    class MLModel:
        """Configuration for the ML Service."""

        file = environ.var(
            default="./models/iris_model.pkl",
            help="The file location of the ML Model.",
        )

    mlmodel = environ.group(MLModel)


# load environment and assign it to the environ config
load_dotenv()
app_cfg = environ.to_config(AppConfig)

if __name__ == "__main__":
    print(environ.generate_help(AppConfig, display_defaults=True))
