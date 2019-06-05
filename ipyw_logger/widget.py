import logging

from colorama import Fore, Style

import ipywidgets as ipyw

import traitlets as trt


__all__ = ("LoggerWidget",)


def get_active_loggers():
    return tuple(
        [("ROOT", logging.getLogger())] +
        list(sorted(logging.Logger.manager.loggerDict.items()))
    )


@ipyw.register
class LoggerWidget(ipyw.VBox):
    """Displays python logs in an IPython/Jupyter widget.

    Parameters
    ----------
    level: int
        the logging level to start the logger on

    height: str
        the layout height of the widget

    """

    level = trt.Instance(
        ipyw.Dropdown,
        kw=dict(
            options=tuple(getattr(logging, "_nameToLevel", {}).items()),
            layout=ipyw.Layout(width="100px"),
        )
    )
    selector = trt.Instance(
        ipyw.Dropdown,
        kw=dict(
            options=get_active_loggers(),
            layout=ipyw.Layout(width="300px"),
        )
    )
    refresh = trt.Instance(
        ipyw.Button,
        kw=dict(
            icon="refresh",
            tooltip="Refresh the list of available loggers",
            layout=ipyw.Layout(width="40px"),
        )
    )
    capture_warnings = trt.Instance(
        ipyw.Checkbox,
        kw=dict(description="Capture Warnings", value=True),
    )

    def __init__(self, *args,
                 height="100%",
                 level=40,
                 logger: (str, logging.Logger) = None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        if not isinstance(logger, logging.Logger):
            # logger can be a string with the name of the log or None for root
            logger = logging.getLogger(logger)
        self.logger = logger

        self.output = ipyw.Output(
            layout=ipyw.Layout(height="90%", border="solid"),
        )

        # For more information, refer to the Python 3 Logging Guide:
        # https://docs.python.org/3/library/logging.html#logrecord-attributes
        format_options = {
            "asctime": "Human-readable time when the LogRecord was created. "
                       "By default this is of the form ‘2003-07-08 "
                       "16:49:45,896’ (the numbers after the comma are "
                       "millisecond portion of the time).",
            "module": "Module (name portion of filename).",
            "filename": "Filename portion of pathname.",
            "name": "Name of the logger used to log the call.",
            "thread": "Thread ID (if available).",
            "threadName": "Thread name (if available).",
            "levelname": "Text logging level for the message ('DEBUG', "
                         "'INFO', 'WARNING', 'ERROR', 'CRITICAL')."
        }
        defaults = ("asctime", "name", "levelname")
        self.format_control = ipyw.HBox([
            ipyw.ToggleButton(False, description=name, tooltip=tooltip)
            for name, tooltip in format_options.items()
        ], layout=ipyw.Layout(height="100px"))
        for button in self.format_control.children:
            if button.description in defaults:
                button.value = True

        for button in self.format_control.children:
            button.observe(self.update_format, "value")

        self.handler = LogViewer(sink=self.output)
        self.logger.addHandler(self.handler)

        self.layout.height = height
        self.level.value = level or self.logger.level

        self.warnings = None

        logger_selector = ipyw.HBox(
            children=[
                ipyw.Label(
                    "Select Logger:",
                    layout=ipyw.Layout(width="100px"),
                ),
                self.selector,
                self.refresh,
            ],
            layout=ipyw.Layout(width="50%"),
        )
        level_selector = ipyw.HBox(
            children=[
                ipyw.Label(
                    "Set Log Level:",
                    layout=ipyw.Layout(width="100px"),
                ),
                self.level,
                self.capture_warnings,
            ],
            layout=ipyw.Layout(width="50%"),
        )
        clear_btn = ipyw.Button(
            icon="trash",
            layout=ipyw.Layout(width="40px"),
            tooltip="Clear Log",
        )
        clear_btn.on_click(self.clear_log)

        self.children = tuple([
            self.format_control,
            ipyw.HBox([
                logger_selector,
                ipyw.Label("", layout=ipyw.Layout(width="50px")),
                level_selector,
                clear_btn,
            ], layout=ipyw.Layout(height="100px")),
            self.output,
        ])
        self.update_warnings()
        self.update_options()
        # self.selector.label = self.logger.name
        self.update_logger()
        self.update_level()

        self.capture_warnings.observe(self.update_warnings, "value")
        self.level.observe(self.update_level, "value")
        self.refresh.on_click(self.update_options)
        self.selector.observe(self.update_logger, "value")

    def clear_log(self, change=None):
        _ = change  # denoting that the change input is intentionally ignored
        self.output.outputs = []

    def update_format(self, change=None):
        _ = change  # denoting that the change input is intentionally ignored
        record_format = " - ".join(
            [
                f"%({button.description})s"
                for button in self.format_control.children
                if button.value
            ] +
            ["%(message)s"]
        )
        self.handler.setFormatter(logging.Formatter(record_format))

    def update_level(self, change=None):
        _ = change  # denoting that the change input is intentionally ignored
        self.logger.setLevel(self.level.value)
        if self.warnings:
            self.warnings.setLevel(self.level.value)

    def update_logger(self, change=None):
        _ = change  # denoting that the change input is intentionally ignored
        self.logger = self.selector.value

    def update_options(self, change=None):
        _ = change  # denoting that the change input is intentionally ignored
        available_logs = get_active_loggers()
        value = self.selector.value
        self.selector.options = available_logs
        self.selector.value = value

    def update_warnings(self, change=None):
        _ = change  # denoting that the change input is intentionally ignored
        logging.captureWarnings(self.capture_warnings.value)
        if self.capture_warnings.value:
            self.logger.info("Capturing Warnings")
            self.warnings = logging.getLogger("py.warnings")
            self.warnings.addHandler(self.handler)
        else:
            self.logger.info("Disabling Capturing of Warnings")
            self.warnings = None


class LogViewer(logging.Handler):
    """ Class to redistribute python logging data """

    # have a class member to store the existing logger
    logger_instance = logging.getLogger("viewer")

    FORE_COLORS = {
        "CRITICAL": Fore.RED,
        "FATAL": Fore.RED,
        "ERROR": Fore.RED,
        "WARN": Fore.LIGHTRED_EX,
        "WARNING": Fore.LIGHTRED_EX,
        "INFO": Fore.BLUE,
        "DEBUG": Fore.GREEN,
        "NOTSET": Fore.BLACK,
    }

    def __init__(self, sink=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sink = sink

        # optional take format
        # setFormatter function is derived from logging.Handler
        for key, value in kwargs.items():
            if "{}".format(key) == "format":
                self.setFormatter(value)

        # make the logger send data to this class
        self.logger_instance.addHandler(self)

    # TODO make this more efficient (maybe implement throttling?)
    def emit(self, record):
        """ Overload of logging.Handler method. """
        if not self.sink:
            return

        ansi_style = Style.BRIGHT + self.FORE_COLORS[record.levelname]
        self.sink.outputs = (
            dict(
                name="stdout",
                output_type="stream",
                text=ansi_style + self.format(record) + "\n",
            ),
        ) + self.sink.outputs
