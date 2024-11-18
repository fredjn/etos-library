from opentelemetry.sdk._logs import LogRecordProcessor, LogData


class ToStringProcessor(LogRecordProcessor):
    def emit(self, log_data: LogData) -> None:
        record = log_data.log_record
        if not isinstance(record.body, (str, bool, int, float)):
            record.body = str(record.body)

    def force_flush(self, timeout_millis: int) -> bool:
        return True

    def shutdown(self):
        pass
